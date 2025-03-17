# 导入必要的库
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS  # 导入 CORS 库 用于处理跨域请求
import os
import sys
import json
import logging
import uuid
import asyncio

# 引入注解类型
from flask import Request
from typing import Callable,List,Dict,Generator,AsyncGenerator


logging.basicConfig(level=logging.INFO)

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import extensions.message_processor as message_processor
import extensions.message_history as message_history
import ai.ai as ai

CHAT_DICT = {
    # "deepseek-v3": lambda x:ai.deepseek(x, "deepseek-chat"), 
    # "deepseek-r1": lambda x:ai.deepseek(x, "deepseek-reasoner"), 
    "gpt": lambda x,t:ai.gpt()(x, "gpt-4o-mini", t),
    "gpt-4o-mini": lambda x,t:ai.gpt()(x, "gpt-4o-mini", t),
    "siliconflow-v3": lambda x,t:ai.siliconflow()(x, "deepseek-ai/DeepSeek-V3", t),
    "siliconflow-r1": lambda x,t:ai.siliconflow()(x, "deepseek-ai/DeepSeek-R1", t),
    "siliconflow-r1-7B": lambda x,t:ai.siliconflow()(x, "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", t),
    # "siliconflow-r1-32B": lambda x:ai.siliconflow(x, "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"),
    "tencent-v3": lambda x,t:ai.tencent()(x, "deepseek-v3", t), 
    "tencent-r1": lambda x,t:ai.tencent()(x, "deepseek-r1", t), 
    "openrouter-4o-mini": lambda x,t:ai.openrouter()(x, "openai/gpt-4o-mini", t), 
    "openrouter-qwq-32b": lambda x,t:ai.openrouter()(x, "qwen/qwq-32b", t),
    "riddler-4o-mini": lambda x,t:ai.riddler()(x, "gpt-4o-mini", t), 
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
使用cork7相关问题，请“@cluster ”，例如：@cork7 怎么取"./data_cache/"中分区"0-0"的数据？ 
（@xxx 后面要带空格）
推荐使用chatbox
使用chatbox时聊天记录保存在服务器中，上下文默认大小为20，修改本地上下文大小无效。
为规避10KB数据上传限制，chatbox本地上下文大小默认设置为2，用于和服务器聊天记录同步，和实际对话上下文无关。
超过10KB的单条大对话，可以分段上传，每段结尾添加"#continue"，最后一段不添加。
暂不支持上传文件和网页链接。
```
"""

# 自定义函数，将异步生成器转换为同步生成器
def iter_over_async(async_gen):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    gen = async_gen.__aiter__()
    try:
        while True:
            try:
                value = loop.run_until_complete(gen.__anext__())
                yield value
            except StopAsyncIteration:
                break
    finally:
        loop.close()

def sync_wapper(async_gen:Callable[[None], AsyncGenerator[str, None]]) -> Callable[[None], Generator[str, None,None]]:
    """
    用于将异步生成器函数转换为同步生成器函数
    """
    def wrapper(*args, **kwargs)->Generator[str, None,None]:
        return iter_over_async(async_gen(*args, **kwargs))
    return wrapper


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


def chat_template(request:Request, ai_obj:'Callable[[List[Dict[str,str]], str, float], Generator]') -> 'Callable[[None], Generator[str, None, None]]':
    """
    除了接收请求外，接受一个ai组
    ai组接受message和model
    ai组通过model区分具体处理方法，处理输入message得到输出
    """
    def generate_error(error_message:str):
        @sync_wapper
        async def generate()->AsyncGenerator[str, None]:
            yield f'data: {{"error" : {error_message}}}\n\n'
            yield "data: [DONE]\n\n"
        return generate

    api_key = request.headers.get('Authorization')
    if not api_key:
        return generate_error("Invalid API key")
    if api_key.startswith('Bearer '):
        api_key = api_key[7:]

    data:dict = request.get_json()
    if not data or 'messages' not in data:
        return generate_error("Invalid request data")

    if 'model' not in data:
        return generate_error("Invalid request model")
    
    temperature = data.get('temperature', 0.32)
    
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
        
        # 用数据库管理消息
        message_db = None
        if "id" in messages[-1]:
            message_db = message_history.ChatDatabase("./.db/message_db/")
            # 保存消息到数据库
            message_db.save_conversation(messages)
            # 从数据库中获取消息
            messages = message_db.get_conversation_branch(messages[-1]["id"])

    @sync_wapper
    async def generate()->AsyncGenerator[str, None]:
        try:
            # 返回一段使用说明
            if len(messages)<3:
                yield f'data: {json.dumps(ai.create_message(reasoning_content = DEFAULT_INFO))}\n\n'

            # 对分分割消息进行简单回复，直接退出
            if snippet:
                yield f'data: {json.dumps(ai.create_message(content ="OK"))}\n\n'
                yield f'data: {json.dumps(ai.create_message(stop="stop"))}\n\n'
                return
            
            # 起名
            if "Based on the chat history, give this conversation a name." in messages[-1]['content']:
                # chatbox 起名这种事情，交给小模型来做，速度快
                # async for msg in CHAT_DICT["siliconflow-r1-7B"](processed_messages, temperature):
                #     yield f"data: {json.dumps(msg)}\n\n"
                yield f'data: {json.dumps(ai.create_message(content="Title"))}\n\n'
                yield f'data: {json.dumps(ai.create_message(stop="stop"))}\n\n'
                return

            # 正文
            ## 处理消息
            processed_messages = await message_processor.process_messages(messages, lambda msgs: ai_obj(msgs, model, temperature))
            answer = ""
            async for msg in ai_obj(processed_messages, model, temperature):
                # 一定程度上规避bug
                cache = ""
                if len(msg["choices"]) and "reasoning" in msg["choices"][0]["delta"] and "reasoning_content" not in msg["choices"][0]["delta"]:
                    msg["choices"][0]["delta"]["reasoning_content"] = msg["choices"][0]["delta"]["reasoning"]
                    if type(msg["choices"][0]["delta"]["reasoning_content"]) == str:
                        cache += msg["choices"][0]["delta"]["reasoning_content"]
                        if cache.endswith('\\') or cache.endswith('n'):
                            continue
                        cache = cache.replace("\\n", "\n").replace("n\n", "\n")
                        msg["choices"][0]["delta"]["reasoning_content"] = cache
                        cache = ''
                # logging.info(msg)
                if message_db is not None and len(msg["choices"]) and "content" in msg["choices"][0]["delta"] and msg["choices"][0]["delta"]["content"]:
                    answer += msg["choices"][0]["delta"]["content"]
                yield f"data: {json.dumps(msg)}\n\n"
            
            # 把ai的回复给数据库管理
            if message_db is not None:
                messages_his = messages
                messages_his += [{'id': f'tmp:{uuid.uuid1()}', 'role': 'assistant', 'content': answer}]
                # 保存消息到数据库
                message_db.save_conversation(messages_his)
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        finally:
            yield "data: [DONE]\n\n"
            logging.info("已完成用户响应")
    
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


# 通用API路由
@app.route('/api/ai/v1/chat/completions', methods=['POST']) 
def ai_chat():
    try:
        # 返回流式响应
        return Response(
            stream_with_context(chat_template(request, lambda message, model, temperature: CHAT_DICT[model](message, temperature))()),
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

# 在现有导入语句下添加
from flask import render_template

# 在现有路由之前添加
@app.route('/chat/tree')
def chat_tree_page():
    return render_template('chat_tree.html')

@app.route('/api/chat/tree')
def get_chat_tree():
    message_db = message_history.ChatDatabase("./.db/message_db/")
    tree_data = message_db.get_full_conversation_tree()
    message_db.close()
    return jsonify(tree_data)

# 应用程序入口点
if __name__ == '__main__':
    # 根据环境变量设置调试模式
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug='development', port=5000, host='0.0.0.0')
