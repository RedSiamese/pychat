import numpy as np
import pickle

def save_embeddings(data, name:str):
    values_file=f'{name}.npy'
    keys_file=f'{name}.pkl'

    np.save(values_file, data[1])
    with open(keys_file, 'wb') as f:
        pickle.dump(data[0], f)



def load_embeddings(name:str) -> 'tuple[list[str], np.ndarray]':
    values_file=f'{name}.npy'
    keys_file=f'{name}.pkl'

    values = np.load(values_file)
    with open(keys_file, 'rb') as f:
        keys = pickle.load(f)

    return keys, values

def cosine_similarity(a, b):
    """计算两个向量的余弦相似度"""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0  # 防止除以零
    return dot_product / (norm_a * norm_b)

def top_n_similarities(input_features, reference_features, top_n=3, thd = 0.70):
    """
    计算输入特征矩阵与参考特征矩阵之间的余弦相似度，并返回每个输入特征的最近的 top N 特征。

    参数:
    - input_features: 输入特征矩阵 (shape: [m, n])
    - reference_features: 参考特征矩阵 (shape: [k, n])
    - top_n: 返回最近的 top N 特征

    返回:
    - result: 每个输入特征的最近 top N 特征的索引
    """
    result = []
    
    for input_vector in input_features:
        similarities = []
        
        for idx, reference_vector in enumerate(reference_features):
            sim = cosine_similarity(input_vector, reference_vector)
            similarities.append((sim, idx))  # 保存相似度和索引
        
        # 按相似度排序并取 top N
        similarities = filter(lambda x: x[0] > thd, similarities)
        top_n_similarities = sorted(similarities, key=lambda x: x[0], reverse=True)[:top_n]
        result.append(top_n_similarities)

    return result

def get_top_n_elements(top_n_indices, reference_list) -> 'set[str]':
    """
    根据 top N 特征的索引从参考列表中获取对应的元素。

    参数:
    - top_n_indices: top N 特征的索引列表，格式为 [[(sim1, idx1), (sim2, idx2), ...], ...]
    - reference_list: 与参考特征矩阵同样长度的列表

    返回:
    - result: 每个输入特征对应的 top N 元素的列表
    """
    result = set()
    
    for indices in top_n_indices:
        for _, idx in indices:
            result.add(reference_list[idx])

    return result

import os
import re
import openai
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()  # 加载环境变量

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
GPT_PROXY_API_BASE = "https://www.riddler.icu"

def get_batch_embeddings(texts, model="text-embedding-3-small") -> np.ndarray:
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
    embeddings = [item['embedding'] for item in response.to_dict()["data"]]
    return np.array(embeddings)


def get_func_info(lines: 'list[str]'):
    pattern = r'^\s*def\s+(\w+)\s*\(.*?\)\s*(->\s*.*?)?\s*:'
    function_doc = []
    for i in range(len(lines)):
        line = lines[i]
        match = re.match(pattern, line.strip())
        if match and match.group(1) and '"""' in lines[i+1] and "async_" not in match.group(1):
            for j in range(2, 100):
                if "```" in lines[i+j] or '"""' in lines[i+j] or "例如：" in lines[i+j] or "support asynchronous" in lines[i+j]:
                    break
                else:
                    info = ' '.join(lines[i+j].split())
                    if info != '':
                        function_doc += [(match.group(1), info)]
    return function_doc

def deal_with_rag():
    for a,b,_ in os.walk(os.path.dirname(__file__)+"/../info/pycluster2x/"):
        for name in b:
            if "__" in name or "example" in name:
                continue
            with open(f"{a}/{name}/{name}.pyi", encoding="utf-8") as f:
                lines = f.readlines()
                doc = get_func_info(lines)
                emb = get_batch_embeddings(list(map(lambda x:x[1], doc)))
                save_embeddings((list(map(lambda x:x[0], doc)), emb), f"{a}/{name}/{name}")
                # a,b = load_embeddings(f"{a}/{name}/{name}")
                # print(a,b)
                # res = top_n_similarities(emb, emb)
                # print(res)
                # save_embeddings(emb, f"{a}/{name}/{name}")
                # break



if __name__ == "__main__":
    deal_with_rag()