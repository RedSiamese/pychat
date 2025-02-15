from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS  # 添加这行
from dotenv import load_dotenv
import os
import openai

load_dotenv()  # 加载环境变量

# 配置API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"  # DeepSeek API基础URL

# 添加系统信息常量
SYSTEM_INFO = {
    "version": "1.0.0",
    "name": "Calculator API",
    "author": "wxy",
    "description": "A simple calculator API service",
    "endpoints": [
        {"path": "/", "method": "GET", "description": "Welcome page"},
        {"path": "/api", "method": "GET", "description": "Get system information"},
        {"path": "/api/gpt", "method": "POST", "description": "Chat with GPT"},
        {"path": "/api/deepseek", "method": "POST", "description": "Chat with DeepSeek"}
    ]
}

app = Flask(__name__)
CORS(app)  # 添加这行

@app.route('/api', methods=['GET'])  # 修改这里
def get_info():
    return jsonify(SYSTEM_INFO)

@app.route('/api/gpt', methods=['POST'])  # 修改路由
def gpt_chat():
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        
        # 在函数内创建OpenAI客户端实例
        openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        def generate():
            # 使用OpenAI客户端实例调用API
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True  # 启用流式输出
            )
            
            # 逐块返回响应
            for chunk in response:
                # 更新处理逻辑以适应新的API结构
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    # 使用SSE格式发送数据
                    yield f"data: {content}\n\n"
                    
        return Response(
            stream_with_context(generate()),
            content_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',  # 禁用nginx缓冲
                'Connection': 'keep-alive'
            }
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/deepseek', methods=['POST'])
def deepseek_chat():
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        
        # 创建一个新的OpenAI客户端实例，专门用于DeepSeek
        deepseek_client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_API_BASE
        )
        
        def generate():
            # 使用OpenAI库调用DeepSeek API
            response = deepseek_client.chat.completions.create(
                model="deepseek-chat",  # 替换为实际的模型名称
                messages=messages,
                stream=True
            )
            
            # 处理流式响应
            for chunk in response:
                # 更新处理逻辑以适应新的API结构
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    yield f"data: {content}\n\n"
                    
        return Response(
            stream_with_context(generate()),
            content_type='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Connection': 'keep-alive'
            }
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/')
def home():
    return 'Welcome to Calculator API'

# 注释掉或删除本地运行代码
if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, port=3000)
