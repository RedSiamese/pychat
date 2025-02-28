import os
import re
import openai
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()  # 加载环境变量

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
GPT_PROXY_API_BASE = "https://www.riddler.icu"

def get_batch_embeddings(texts, model="text-embedding-3-small"):
    openai_client = openai.OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=GPT_PROXY_API_BASE
    )
    # 调用 OpenAI 的 Embedding API，批量输入
    response = openai_client.embeddings.create(
        input=texts,  # 输入是一个字符串列表
        model=model
    )
    # 返回所有字符串的嵌入向量
    return [item['embedding'] for item in response.to_dict()["data"]]


def load_func_info(lines: 'list[str]'):
    pattern = r'^\s*def\s+(\w+)\s*\(.*?\)\s*(->\s*.*?)?\s*:'
    function_doc = {}
    for i in range(len(lines)):
        line = lines[i]
        match = re.match(pattern, line.strip())
        if match and match.group(1) and '"""' in lines[i+1] and "async_" not in match.group(1):
            if match.group(1) not in function_doc:
                function_doc[match.group(1)] = ""
            for j in range(2, 100):
                if "```" in lines[i+j] or '"""' in lines[i+j] or "例如：" in lines[i+j] or "support asynchronous" in lines[i+j]:
                    break
                else:
                    function_doc[match.group(1)] += ' '.join(lines[i+j].split()) +"\n"
    return function_doc

def deal_with_rag():
    for a,b,_ in os.walk(os.path.dirname(__file__)+"/../info/pycluster2x/"):
        for name in b:
            if "__" in name or "example" in name:
                continue
            with open(f"{a}/{name}/{name}.pyi", encoding="utf-8") as f:
                lines = f.readlines()
                doc = load_func_info(lines)
                print(name,doc)
                emb = get_batch_embeddings(list(doc.values())[0:2])
                print(emb)
                break

if __name__ == "__main__":
    deal_with_rag()