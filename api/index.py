# 导入必要的库
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS  # 添加这行
import os
import sys
import json

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions.message_processor import process_messages
import extensions.ai as ai

CHAT_DICT = {
    "deepseek-v3": lambda x:ai.deepseek(x, "deepseek-chat"), 
    "deepseek-r1": lambda x:ai.deepseek(x, "deepseek-reasoner"), 
    "gpt": ai.gpt,
    "siliconflow-v3": lambda x:ai.siliconflow(x, "deepseek-ai/DeepSeek-V3"),
    "siliconflow-r1": lambda x:ai.siliconflow(x, "deepseek-ai/DeepSeek-R1"),
    "tencent-v3": lambda x:ai.tencent(x, "deepseek-v3"), 
    "tencent-r1": lambda x:ai.tencent(x, "deepseek-r1"), 
}

# 定义系统信息常量
SYSTEM_INFO = {
    "version": "1.0.0",
    "name": "AI Chat API",
    "author": "wxy",
    "description": "Multi-model AI chat API service",
    "supported_models": {
        "unified_chat": list(CHAT_DICT.keys()),
        "gpt": [],
        "deepseek": [],
        "siliconflow": [],
        "tencent": []
    },
    "endpoints": {
        "info": "/api",
        "unified_chat": "/api/ai/v1/chat/completions",
        "gpt": "/api/gpt/v1/chat/completions",
        "deepseek": "/api/deepseek/v1/chat/completions",
        "siliconflow-v3": "/api/siliconflow/v1/chat/completions",
        "tencent": "/api/tencent/v1/chat/completions"
    }
}

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域资源共享

# 系统信息路由
@app.route('/api', methods=['GET']) 
def get_info():
    return jsonify(SYSTEM_INFO)


# ChatGPT API路由
@app.route('/api/ai/v1/chat/completions', methods=['POST']) 
def ai_chat():
    try:
        # 获取 API Key
        api_key = request.headers.get('Authorization')
        if not api_key:
            return jsonify({'error': 'Missing API Key'}), 401
            
        # 如果 API Key 格式为 "Bearer xxx"，提取实际的 key
        if api_key.startswith('Bearer '):
            api_key = api_key[7:]

        # 获取并验证请求数据
        data = request.get_json()
        if not data or 'messages' not in data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        model = data['model']
        messages = data['messages']

        print("model",model)
        # 处理消息
        processed_messages = process_messages(messages)
        # print(messages)
        print("processed_messages end")
        
        # 定义流式响应生成器
        def generate():
            try:
                # 使用处理后的消息调用OpenAI API
                for msg in CHAT_DICT[model](processed_messages):
                    yield f"data: {msg}\n\n"
                
                # 在响应结束时发送 [DONE] 标记
                yield "data: [DONE]\n\n"
                print("已完成用户回复")
                        
            except Exception as e:
                import traceback
                traceback.print_exc()
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                yield "data: [DONE]\n\n"
        
        # 返回流式响应
        return Response(
            stream_with_context(generate()),
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


# # siliconflow API路由
# @app.route('/api/gpt/v1/chat/completions', methods=['POST']) 
# def siliconflow_chat():
#     try:
#         # 获取并验证请求数据
#         data = request.get_json()

#         # print(data)
#         if not data:
#             return jsonify({'error': 'Invalid request data'}), 400

#         print(data)
        
        
#         # 定义流式响应生成器
#         def generate():
#             # 在响应结束时发送 [DONE] 标记
#             yield "data: [DONE]\n\n"
                    
#         # 返回流式响应
#         return Response(
#             stream_with_context(generate()),
#             content_type='text/event-stream',
#             headers={
#                 'Cache-Control': 'no-cache, no-transform',
#                 'X-Accel-Buffering': 'no',
#             }
#         )
    
#     except Exception as e:
#         # 处理整体异常
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': str(e)}), 400



# 主页路由
@app.route('/')
def home():
    return 'Welcome to Calculator API'

# 应用程序入口点
if __name__ == '__main__':
    # 根据环境变量设置调试模式
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug='development', port=5000, host='0.0.0.0')
