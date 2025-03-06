# 导入必要的库
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS  # 导入 CORS 库 用于处理跨域请求
import os
import sys
import json
import logging

# 引入注解类型
from flask import Request
from typing import Callable,List,Dict,Generator


logging.basicConfig(level=logging.INFO)

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import extensions.message_processor as message_processor
import extensions.message_history as message_history
import extensions.ai as ai

CHAT_DICT = {
    # "deepseek-v3": lambda x:ai.deepseek(x, "deepseek-chat"), 
    # "deepseek-r1": lambda x:ai.deepseek(x, "deepseek-reasoner"), 
    "gpt": ai.gpt,
    "gpt-4o-mini": ai.gpt,
    "siliconflow-v3": lambda x:ai.siliconflow(x, "deepseek-ai/DeepSeek-V3"),
    "siliconflow-r1": lambda x:ai.siliconflow(x, "deepseek-ai/DeepSeek-R1"),
    # "siliconflow-r1-32B": lambda x:ai.siliconflow(x, "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"),
    "tencent-v3": lambda x:ai.tencent(x, "deepseek-v3"), 
    "tencent-r1": lambda x:ai.tencent(x, "deepseek-r1"), 
    "openrouter-4o-mini": lambda x:ai.openrouter(x, "gpt-4o-mini"), 
}

# 定义系统信息常量
SYSTEM_INFO = {
    "version": "1.0.0",
    "name": "AI Chat API",
    "author": "wxy",
    "description": "Multi-model AI chat API service",
    "endpoints": {
        "unified_chat": "/api/ai/v1/chat/completions",
        "openrouter": "/api/openrouter/v1/chat/completions"
    },
    "supported_models": {
        "unified_chat": list(CHAT_DICT.keys()),
    },
}

DEFAULT_INFO = """```
pycluster2x聚档python扩展包api、代码生成相关的问题请添加“@pycluster2x ”，例如：@pycluster2x 怎么获取档案集中一个人的所有rid？
聚档测试、运行，项目流程信息相关的问题请添加“@cluster ”，例如：@cluster 安徽多卡测试怎么跑？ 
（@xxx 后面要带空格）
聊天记录保存在服务器中，上下文默认大小为20，修改本地上下文大小无效。
为规避10KB数据上传限制，本地上下文大小默认设置为2，用于和服务器聊天记录同步，和实际对话上下文无关。
超过10KB的单条大对话，可以分段上传，每段结尾添加"#continue"，最后一段不添加。
暂不支持上传文件和网页链接。
```
"""


# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域资源共享

# 系统信息路由
@app.route('/api', methods=['GET']) 
def get_info():
    return jsonify(SYSTEM_INFO)



@app.route('/chatbox-set')
def download_json():
    # 创建一个示例 JSON 数据
    chatbox_set = {
        "settings": {
            "aiProvider": "custom",
            "temperature": 0.32,
            "topP": 1,
            "openaiMaxContextMessageCount": 2,
            "customProviders": [
                {
                    "id": "custom-provider-1740037025384",
                    "name": "cluster",
                    "api": "openai",
                    "host": "https://riddler.mynatapp.cc/api/ai/v1",
                    "path": "/chat/completions",
                    "key": "",
                    "model": "gpt-4o-mini",
                    "useProxy": False,
                    "modelOptions": list(CHAT_DICT.keys())
                }
            ],
            "language": "zh-Hans",
            "showWordCount": False,
            "showTokenCount": True,
            "showTokenUsed": True,
            "showModelName": True,
            "showMessageTimestamp": True,
            "showFirstTokenLatency": True,
            "selectedCustomProviderId": "custom-provider-1740037025384",
            "defaultPrompt":"",
            "injectDefaultMetadata": False,
            "pasteLongTextAsAFile": False,
        }
    }
    # 将数据转换为 JSON 格式
    json_data = jsonify(chatbox_set)
    # 创建一个响应对象
    response = Response(
        json_data.data,
        mimetype='application/json'
    )
    # 设置下载的文件名
    response.headers.set('Content-Disposition', 'attachment', filename='chatbox-set.json')
    return response


def chat_template(request:Request, ai_obj:Callable[[List[Dict[str,str]], str], Generator]) -> Generator:
    """
    除了接收请求外，接受一个ai组
    ai组接受message和model
    ai组通过model区分具体处理方法，处理输入message得到输出
    """
    def generate_error(error_message:str):
        def generate():
            yield f'data: {{"error" : {error_message}}}\n\n'
            yield "data: [DONE]\n\n"

    api_key = request.headers.get('Authorization')
    if not api_key:
        return generate_error("Invalid API key")
    if api_key.startswith('Bearer '):
        api_key = api_key[7:]

    data = request.get_json()
    if not data or 'messages' not in data:
        return generate_error("Invalid request data")

    if 'model' not in data:
        return generate_error("Invalid request model")
    
    model:str = data['model']
    messages:list[dict[str,str|int|None]] = data['messages']
    
    snippet = False
    if "Based on the chat history, give this conversation a name." in messages[-1]['content']:
        processed_messages = messages
    else:
        if messages[-1]['content'].endswith("#continue"):
            # 去除#continue
            messages[-1]['content'] = messages[-1]['content'][:-9]
            snippet = True
        
        message_db = message_history.ChatDatabase("./.db/message_db/")
        # 保存消息到数据库
        message_db.save_conversation(messages)
        # 从数据库中获取消息
        messages = message_db.get_conversation_branch(messages[-1]["id"])
        # 处理消息
        processed_messages = message_processor.process_messages(messages, lambda msgs: ai_obj(msgs, model))

    def generate():
        try:
            if len(messages)<3:
                yield f'data: {json.dumps(ai.create_message(reasoning_content = DEFAULT_INFO))}\n\n'
            if snippet:
                yield f'data: {json.dumps(ai.create_message(content ="OK"))}\n\n'
                yield f'data: {json.dumps(ai.create_message(stop="stop"))}\n\n'
            else:
                if "Based on the chat history, give this conversation a name." in messages[-1]['content']:
                    # chatbox 起名这种事情，交给gpt来做，速度快
                    for msg in CHAT_DICT["gpt"](processed_messages):
                        yield f"data: {msg}\n\n"
                else:
                    # 使用处理后的消息调用OpenAI API
                    for msg in ai_obj(processed_messages, model):
                        yield f"data: {msg}\n\n"
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            yield "data: [DONE]\n\n"
    
    return generate


# OpenRouter API路由
@app.route('/api/openrouter/v1/chat/completions', methods=['POST'])
def openrouter_chat():
    try:
        return Response(
            stream_with_context(chat_template(request, ai.openrouter)()),
            content_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache, no-transform',
                'X-Accel-Buffering': 'no'
            }
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ChatGPT API路由
@app.route('/api/ai/v1/chat/completions', methods=['POST']) 
def ai_chat():
    try:
        # 返回流式响应
        return Response(
            stream_with_context(chat_template(request, lambda message, model: CHAT_DICT[model](message))()),
            content_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache, no-transform',
                'X-Accel-Buffering': 'no',  # 禁用nginx缓冲
            }
        )
    
    except Exception as e:
        # 处理整体异常
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500



# 主页路由
@app.route('/')
def home():
    return 'Welcome to Calculator API'

# 应用程序入口点
if __name__ == '__main__':
    # 根据环境变量设置调试模式
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug='development', port=5000, host='0.0.0.0')
