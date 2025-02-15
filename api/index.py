# 导入必要的库
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS  # 添加这行
from dotenv import load_dotenv
import os
import openai
import httpx

# 加载环境变量
load_dotenv()  # 加载环境变量

# 配置API密钥和基础URL
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_BASE = "https://api.deepseek.com"  # DeepSeek API基础URL

# 定义系统信息常量
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

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域资源共享

# 系统信息路由
@app.route('/api', methods=['GET']) 
def get_info():
    return jsonify(SYSTEM_INFO)

# ChatGPT API路由
@app.route('/api/gpt', methods=['POST']) 
def gpt_chat():
    try:
        # 获取并验证请求数据
        data = request.get_json()
        if not data or 'messages' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        messages = data['messages']

        # 修改这里：正确设置代理
        # proxy = "http://127.0.0.1:7078"
        # http_client = httpx.Client(proxies={"http://": proxy, "https://": proxy})

        openai_client = openai.OpenAI(
            api_key=OPENAI_API_KEY,
            # http_client=http_client
        )
        
        # 定义流式响应生成器
        def generate():
            try:
                # 调用OpenAI API并处理流式响应
                response = openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    stream=True  # 启用流式输出
                )
                
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        yield f"data: {content}\n\n"
                        
            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"
        
        # 返回流式响应
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
        # 处理整体异常
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# DeepSeek API路由
@app.route('/api/deepseek', methods=['POST'])
def deepseek_chat():
    try:
        # 获取并验证请求数据
        data = request.get_json()
        if not data or 'messages' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        messages = data['messages']
        
        # 创建DeepSeek客户端实例
        deepseek_client = openai.OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_API_BASE
        )
        
        # 定义流式响应生成器
        def generate():
            # 调用DeepSeek API并处理流式响应
            response = deepseek_client.chat.completions.create(
                model="deepseek-chat",  # 替换为实际的模型名称
                messages=messages,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    yield f"data: {content}\n\n"
                    
        # 返回流式响应
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
        # 处理整体异常
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 400

# 主页路由
@app.route('/')
def home():
    return 'Welcome to Calculator API'

# 应用程序入口点
if __name__ == '__main__':
    # 根据环境变量设置调试模式
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, port=3000, host='0.0.0.0')
