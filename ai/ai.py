
import openai
import os
import json
import logging

from dotenv import load_dotenv
# 加载环境变量
load_dotenv()  # 加载环境变量

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


def proxy():
    import httpx
    proxy = "http://127.0.0.1:7078"
    return httpx.Client(proxies={"http://": proxy, "https://": proxy})


class ai_chat_service:
    def __init__(self, key:str = None, url:str = None, http_client = None, extra_headers:'dict[str, str]|None' = None, extra_body:'dict[str, str|int|float|None|bool]|None' = None):
        self.client = openai.OpenAI(
            api_key=key,
            base_url=url,
            http_client=http_client
        )
        self.extra_headers = extra_headers
        self.extra_body = extra_body
        
    # 定义流式响应生成器
    def __call__(self, messages, model, temperature = 0.32):
        try:
            count = sum(map(lambda msg:len(msg["content"]), messages))
            logging.info(f"上下文长度：{count}")

            # 使用处理后的消息调用OpenAI API
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,  # 启用流式输出
                temperature=temperature, 
                extra_headers=self.extra_headers,
                extra_body=self.extra_body
            )
            
            for chunk in response:
                yield chunk.to_dict()

        except Exception as e:
            import traceback
            traceback.print_exc()
            print("error", str(e))
            yield {"error":str(e)}
        



def gpt() -> ai_chat_service:
    return ai_chat_service(*AI_SERVER["openai"], http_client = proxy())

def tencent() -> ai_chat_service:
    return ai_chat_service(*AI_SERVER["tencent"], http_client = proxy())

def openrouter() -> ai_chat_service:
    return ai_chat_service(*AI_SERVER["openrouter"], http_client = proxy())

def siliconflow() -> ai_chat_service:
    return ai_chat_service(*AI_SERVER["siliconflow"], http_client = proxy())

def riddler() -> ai_chat_service:
    return ai_chat_service(*AI_SERVER["riddler"], http_client = proxy())



