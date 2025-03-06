import requests
import openai
import os
import json

from dotenv import load_dotenv
# 加载环境变量
load_dotenv()  # 加载环境变量

# 配置API密钥和基础URL
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
SILICONFLOW_API_KEY = os.getenv('SILICONFLOW_API_KEY', '')
TENCENT_API_KEY = os.getenv('TENCENT_API_KEY', '')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')

SILICONFLOW_API_BASE = "https://api.siliconflow.com/v1"
TENCENT_API_BASE = "https://api.lkeap.cloud.tencent.com/v1"
GPT_PROXY_API_BASE = "https://www.riddler.icu"
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"

AI_SERVER = {
    "openai":(os.getenv('OPENAI_API_KEY', ''), None),
    "siliconflow":(os.getenv('SILICONFLOW_API_KEY', ''), "https://api.siliconflow.com/v1"),
    "tencent":(os.getenv('TENCENT_API_KEY', ''), "https://api.lkeap.cloud.tencent.com/v1"),
    "openrouter":(os.getenv('OPENROUTER_API_KEY', ''), "https://openrouter.ai/api/v1"),
    "riddler":(os.getenv('OPENAI_API_KEY', ''), "https://www.riddler.icu"),
}

def create_message(role = "assistant", content = None, reasoning_content = None, stop = None): 
    return {
    "id": "riddler-admin",
    "choices": [
        {
            "delta": {
                "content":content,
                "reasoning_content": reasoning_content,
                "role": role,
                "refusal": None
            },
            "finish_reason": stop,
            "index": 0,
            "logprobs": None
        }
    ],
    "created": 1740036135,
    "model": "unknown",
    "object": "chat.completion.chunk",
    "service_tier": "default",
    "system_fingerprint": "unknown"
}


def error(*args, **kargs):
    yield "error: model select error"


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
                yield json.dumps(chunk.to_dict())

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield "error: " + str(e)
        
    yield from generate(messages)


def gpt(messages:'list[dict[str, str]]',model:str="gpt-4o-mini"):
    import httpx
    proxy = "http://127.0.0.1:7078"
    http_client = httpx.Client(proxies={"http://": proxy, "https://": proxy})

    openai_client = openai.OpenAI(
        api_key=OPENAI_API_KEY,
        http_client=http_client
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
                yield json.dumps(chunk.to_dict())

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
                yield json.dumps(chunk.to_dict())

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield "error: " + str(e)
        
    yield from generate(messages)


def openrouter(messages:'list[dict[str, str]]', model:str = "gpt-4o-mini"):
    import httpx
    proxy = "http://127.0.0.1:7078"
    http_client = httpx.Client(proxies={"http://": proxy, "https://": proxy})

    openrouter_client = openai.OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_API_BASE,
        http_client=http_client
    )
    
    # 定义流式响应生成器
    def generate(messages):
        try:
            # 使用处理后的消息调用OpenAI API
            response = openrouter_client.chat.completions.create(
                # model="deepseek-reasoner",
                model=model,
                messages=messages,
                stream=True,  # 启用流式输出
                temperature=0.36,
                extra_body={'provider': {
                        'order': [
                            'OpenAI'
                        ],'allow_fallbacks': False}} if model in ["openai/gpt-4o-mini", "gpt-4o-mini"] else {}
            )
            
            for chunk in response:
                yield json.dumps(chunk.to_dict())

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield "error: " + str(e)
        
    yield from generate(messages)

    
def siliconflow(messages:'list[dict[str, str]]', model:str = "deepseek-ai/DeepSeek-V3"):
    deepseek_client = openai.OpenAI(
        api_key=SILICONFLOW_API_KEY,
        base_url=SILICONFLOW_API_BASE
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
                yield json.dumps(chunk.to_dict())

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield "error: " + str(e)
        
    yield from generate(messages)


