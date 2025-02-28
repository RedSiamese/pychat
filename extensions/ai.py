import requests
import openai
import os
import json

from dotenv import load_dotenv
# 加载环境变量
load_dotenv()  # 加载环境变量

# 配置API密钥和基础URL
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
SILICONFLOW_API_KEY = os.getenv('SILICONFLOW_API_KEY', '')  # 添加硅基流动API密钥
TENCENT_API_KEY = os.getenv('TENCENT_API_KEY', '')

DEEPSEEK_API_BASE = "https://api.deepseek.com"
SILICONFLOW_API_BASE = "https://api.siliconflow.com/v1/chat/completions"  # 修改硅基流动API基础URL
TENCENT_API_BASE = "https://api.lkeap.cloud.tencent.com/v1"
GPT_PROXY_API_BASE = "https://www.riddler.icu"

def deepseek(messages:'list[dict[str, str]]', model:str = "deepseek-chat"):
    deepseek_client = openai.OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_API_BASE
    )
    
    # 定义流式响应生成器
    def generate(messages):
        try:
            # 使用处理后的消息调用OpenAI API
            response = deepseek_client.chat.completions.create(
                # model="deepseek-reasoner",
                model=model,
                messages=messages,
                stream=True,  # 启用流式输出
                temperature=0.36
            )
            
            for chunk in response:
                yield chunk.to_json()

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield "error: " + str(e)
        
    yield from generate(messages)


def gpt(messages:'list[dict[str, str]]',model:str="gpt-4o-mini"):

    openai_client = openai.OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=GPT_PROXY_API_BASE
    )
    
    # 定义流式响应生成器
    def generate(messages):
        try:
            # 使用处理后的消息调用OpenAI API
            response = openai_client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,  # 启用流式输出
                temperature=0.36
            )
            
            for chunk in response:
                yield chunk.to_json()

        except Exception as e:
            import traceback
            traceback.print_exc()
            print("error", str(e))
            yield f"data: error:{str(e)}"
        
    yield from generate(messages)



def tencent(messages:'list[dict[str, str]]', model:str = "deepseek-v3"):
    deepseek_client = openai.OpenAI(
        api_key=TENCENT_API_KEY,
        base_url=TENCENT_API_BASE
    )
    
    # 定义流式响应生成器
    def generate(messages):
        try:
            # 使用处理后的消息调用OpenAI API
            response = deepseek_client.chat.completions.create(
                # model="deepseek-reasoner",
                model=model,
                messages=messages,
                stream=True,  # 启用流式输出
                temperature=0.36
            )
            
            for chunk in response:
                yield chunk.to_json()

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield "error: " + str(e)
        
    yield from generate(messages)



def siliconflow(messages:'list[dict[str, str]]',model:str = "deepseek-ai/DeepSeek-V3"):
    """使用硅基流动API处理对话"""
    
    headers = {
        "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    def generate(messages):
        try:
            data = {
                "model": model,
                "messages": messages,
                "stream": True,
                "temperature": 0.36
            }
            
            # 使用requests发送流式请求
            response = requests.post(
                SILICONFLOW_API_BASE,
                headers=headers,
                json=data,
                stream=True
            )
            
            def deal_response_to_json(resp:requests.Response):
                for line in resp.iter_lines():
                    if line:
                        # 删除 "data: " 前缀并解析 JSON
                        line:str = line.decode('utf-8')
                        if line.startswith("data: "):
                            try:
                                yield line[6:]
                            except json.JSONDecodeError:
                                continue
            
            # 处理流式响应
            for chunk in deal_response_to_json(response):
                yield chunk

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield "error: " + str(e)
        
    yield from generate(messages)
    