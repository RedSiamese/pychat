

funcs = {
    "数据条目插入\保存":{"func":["emplace","write_down"], "doc":None},
    "列出\获取检索表":{"func":["get_table","get_tables"], "doc":None},
    "存储结构自省":{"func":["check_data", "check_data_keys","__len__"], "doc":"包含检查本地存储结构是否合法、列出所有字段等功能"},
    "数据条目遍历":{"func":["traversal","__iter__","__getitem__", "end"], "doc":None},
    "检索表重整":{"func":["reset_table"], "doc":None},

    "数据元素按上下界查找":{"func":["lower_bound", "upper_bound", "end"], "doc":None},
    "相同数据元素查找":{"func":["find","find_multi","find_eq", "end"], "doc":None},
    "数据表遍历":{"func":["begin", "end"], "doc":None},
    "数据表自省":{"func":["count", "check_tree", "unique_size"], "doc":None},

    "迭代器相关":{"func":["__bool__","__eq__","__ne__","__next__"], "doc":"所有的遍历和查找都会用到"}
}

import os,sys
import re, json, logging


def pyi_doc()->'str':
    pyi_doc = {}
    pyi_dir = os.path.dirname(__file__)
    for _, dirs, _ in os.walk(pyi_dir):
        for d in dirs:
            if d != "example" and "__" not in d:
                with open(f"{pyi_dir}/{d}/{d}.pyi", "r", encoding="utf-8") as f:
                    content = f.read()
                    # 使用正则匹配文件开头的docstring
                    doc_match = re.match(r'\s*"""(.*?)"""\s*', content, re.DOTALL)
                    if doc_match:
                        doc = doc_match.group(1).strip()
                        pyi_doc[d] = doc

    sysmsg = """
# 注解文件说明：
cork7包含的pyi注解文件包括：
"""
    for k in pyi_doc:
        sysmsg += f'\n - {k}: \n```\n{pyi_doc[k]}\n```\n'
    sysmsg += \
'''
当用户问cork7有关的问题时，用户大概率是在结合聚档项目，
在聚档项目中，每条数据是摄像头对一个人的一次抓拍，数据的检索表包括：
time            抓拍时间戳
partition       这张抓拍按照时空信息划分的分区号
p_recordid      抓拍中人体的单一记录id，即body record id
f_recordid      抓拍中人脸的单一记录id，即face record id

每条数据中除了上述字段外，还包含如
f_channelid             人脸相机id
f_captime               人脸时间戳
f_clarity               人脸清晰度
f_qescore               人脸qe分
f_confidence            人脸置信度
f_featuredata           人脸特征（可能是base64编码的连续内存的float数组 或者 numpy.ndarray特征向量）
p_channelid             人体相机id
p_captime               人体时间戳
p_qe_score              人体qe分
p_featuredata           人体特征（可能是base64编码的连续内存的float数组 或者 numpy.ndarray特征向量）
p_iqascore              人体iqa分
等等字段
'''
    return sysmsg

def func_doc(include_doc = False)->'str':
    sysmsg = \
'''
# api接口分类：
cork7是一个轻量化的类数据库的库，用于数据条目存储和检索\n\n它的api分为若干类，分别为:\n
'''
    for k in funcs:
        sysmsg += f' - "{k}": 其中包含的api接口有{funcs[k]["func"]}'
        if include_doc and "doc" in funcs[k] and funcs[k]["doc"]:
            sysmsg += f',{funcs[k]["doc"]}。'
        sysmsg += "\n"
    return sysmsg

def examples_doc()->'str':
    examples = {}
    example_dir = os.path.join(os.path.dirname(__file__), "example")
    
    if not os.path.exists(example_dir):
        return ""
        
    for root, _, files in os.walk(example_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # 使用正则匹配文件开头的docstring
                    doc_match = re.match(r'\s*"""(.*?)"""\s*', content, re.DOTALL)
                    if doc_match:
                        doc = doc_match.group(1).strip()
                        examples[file] = (doc,content)
    
    sysmsg = """
# 代码示例：
下面是使用cork7 python api写的一些代码示例的功能介绍:\n
"""
    for i, k in enumerate(examples):
        doc, _ = examples[k]
        sysmsg += f'{i}. "{k}":\n```\n{doc}\n```\n\n'
    return sysmsg

def ask_ai_2(message:'list[dict[str,str]]', ai_client)->'list[str]':
    sysmsg = func_doc()
    sysmsg += \
'''
# 问题：
接下来用户会提一个陈述或者问题，在用户的陈述或者问题中，用户指定或者推荐了使用的接口或函数名或函数功能类型吗？

# 要求：
NO COMMENTS. NO ACKNOWLEDGEMENTS. 请务必按照回答格式回答，你的回答将只有一行：
如果用户的上述问题中指定或者推荐了使用的接口或函数名，则列出用户推荐使用的接口名所在的api分类，用","隔开，如果用户问题中没有推荐使用接口或方法，则返回"none".

# 示例：
 - 问题：我可以用find_eq做到这些功能吗?
 - 回答：数据元素相同查找

 - 问题：数据条目查找怎么做?
 - 回答：数据元素相同查找,数据元素按上下界查找

 - 问题：为啥不用find_eq和count做到这些功能?
 - 回答：数据元素相同查找,数据表自省

 - 问题：怎么没用lower_bound
 - 回答：数据元素按上下界查找

 - 问题：我如何通过一个人pid获得档案集中这个人所有的rid
 - 回答：none

'''
    logging.info(f"ask_ai_2提示词长度：{len(sysmsg)}")
    msgs = [{'role': 'system', 'content': sysmsg}]
    msgs += [message[-1]]
    answer = ""
    # logging.info(msgs)
    for chunk in ai_client(msgs):
        if chunk["choices"][0]["delta"].get("content"):
            answer += chunk["choices"][0]["delta"]["content"]
    answer = "\n".join(filter(lambda x:len(x), answer.replace(" ","").lstrip("\n").split("\n")))
    logging.info("=======ask ai 2========")
    logging.info(answer)
    logging.info("=======ask ai 2========")
    return answer


def ask_ai(message:'list[dict[str,str]]', ai_client)->'list[str]':
    sysmsg = pyi_doc() + "\n\n"
    sysmsg += func_doc(include_doc=True) + "\n\n"

    sysmsg += examples_doc() + "\n\n"

    askmsg = message[-1]['content']
    askmsg = \
f"""
# 问题：
用户的问题是"{askmsg}"，解决用户的问题可能需要cork7中哪些类型的api？cork7中这些代码示例中，有哪些有助于解决上述问题，可以用于上述问题中作为代码生成的参考？

# 要求：
NO COMMENTS. NO ACKNOWLEDGEMENTS. 请务必按照回答格式回答，你的回答将有两行：
 1. 第一行，回答解决上述问题可能需要哪些类型的api，将所需要的api类型输出，用','隔开，如果不需要该库的功能，返回"none"，如：
 2. 第二行，回答这些代码示例中，有哪些有助于解决上述问题，可以用于上述问题中作为代码生成的参考，将可以用于参考的代码示例文件名输出，用','隔开。
如果上述描述的问题不是代码生成问题，或者问题和cork7库无关，或者没有哪个代码示例可以用于参考，则返回"none"。
（如果不是代码生成问题，例如介绍接口、代码解释等，尽可能减少代码示例的参考而选用api文档参考。）

# 示例：
例如：
 - 问题：对于已有的数据缓存"./data_cache", 如何找到其中"f_recordid"为"123456"的数据条目？
 - 分析："相同数据元素查找"这个分类的函数可以完成用户的需求，同时假如没有文件可以作为参考,你的回答将有两行
 - 回答(从下一行开始展示)：
相同数据元素查找
none

 - 问题：对于已有的数据缓存"./data_cache", 如何找到其中"f_recordid"为"123456"的数据条目？如何找到时间戳大于1629929715的数据条目？
 - 分析："相同数据元素查找"这个分类的函数可以完成用户的需求，同时假如a.py和b.py可以作为参考,你的回答将有两行
 - 回答(从下一行开始展示)：
相同数据元素查找,数据元素按上下界查找
a.py,b.py

"""
    # logging.info(sysmsg)
    msgs = [{'role': 'system', 'content': sysmsg}]
    msgs += message[:-1]
    msgs += [{'role': 'user', 'content': askmsg}]
    logging.info(f"ask_ai提示词长度：{len(sysmsg)+len(askmsg)}")

    answer = ""
    # logging.info(msgs)
    for chunk in ai_client(msgs):
        if chunk["choices"][0]["delta"].get("content"):
            answer += chunk["choices"][0]["delta"]["content"]
    answer = "\n".join(filter(lambda x:len(x), answer.replace(" ","").lstrip("\n").split("\n")))
    logging.info("=======ask ai========")
    logging.info(answer)
    logging.info("=======ask ai========")
    if "\n" not in answer:
        return "none","none"
    answer = answer.split("\n")
    if answer[0] != "none":
        include = ask_ai_2(message,ai_client)
        if include != "none":
            answer[0] += "," + include
    return answer[0], answer[1]





def maybe_use_func(answer:str) -> 'set[str]':
    res = set()
    if answer == "none":
        return res
    keys = ''.join(answer.split()).split(",")
    for k in keys:
        if k not in funcs:
            logging.error(f"error key {k}")
            continue
        for func in funcs[k]["func"]:
            res.add(func)
    return res


def extract_function_def_names(lines: 'list[str]', maybe_use:'set[str]') -> 'list[str]':
    if maybe_use == set():
        return ""
    all_funcs = set(sum(map(lambda x: x["func"], funcs.values()), []))
    pattern = r'^\s*def\s+(\w+)\s*\(.*?\)\s*(->\s*.*?)?\s*:'
    function_names = []
    jump = 0
    space_jump = 0   # 匹配所有注解中开头的空格，全部去掉，减少字数
    for i in range(len(lines)):
        match = re.match(pattern, lines[i].strip())
        if '"""' in lines[i]:
            if space_jump == 0:
                space_jump = 1
            else:
                space_jump -= 1
        if match and match.group(1) not in maybe_use and '"""' in lines[i+1] and match.group(1) in all_funcs or match and "async_" in match.group(1):
            if "@typing.overload" in function_names[-1]:
                function_names.pop()
            jump += 2
        else:
            # if match and match.group(1) not in all_funcs and "__" not in match.group(1):
            #     logging.error("miss", match.group(1))
            if jump != 0:
                if '"""' in lines[i]:
                    jump -= 1
            else:
                if space_jump and '"""' not in lines[i]:
                    function_names.append(lines[i].lstrip())
                else:
                    function_names.append(lines[i])
    return "".join(function_names)


def maybe_use_example(answer:'str')->'str':
    examples = {}
    example_dir = os.path.join(os.path.dirname(__file__), "example")
    
    if not os.path.exists(example_dir):
        return ""
        
    for root, _, files in os.walk(example_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # 使用正则匹配文件开头的docstring
                    doc_match = re.match(r'\s*"""(.*?)"""\s*', content, re.DOTALL)
                    if doc_match:
                        doc = doc_match.group(1).strip()
                        examples[file] = (doc,content)
                    else:
                        doc_match = re.match(r'\s*\'\'\'(.*?)\'\'\'\s*', content, re.DOTALL)
                        if doc_match:
                            doc = doc_match.group(1).strip()
                            examples[file] = (doc,content)
    
    if answer == "none":
        return ""
    keys = answer.split(",")
    res = """
# 参考示例代码：
"""
    for i,k in enumerate(keys):
        if k not in examples:
            logging.error(f"error key {k}")
            continue
        res += f"## {k}:\n```python\n{examples[k][1]}\n```\n\n"
    return res



# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import extra.embedding as embedding

# def rag_get_funcs(texts:'list[str]', name:str) -> 'set[str]':
#     """
#     message : 按步骤分段，每步一行，'\n'分割
#     """
#     logging.info(texts)
#     in_emb = embedding.get_batch_embeddings(texts)
#     funcs, base_emb = embedding.load_embeddings(name)
#     indexs = embedding.top_n_similarities(in_emb, base_emb)
#     logging.info(indexs)
#     maybe_use_funcs  = embedding.get_top_n_elements(indexs, funcs)
#     return maybe_use_funcs





def call(message:'list[dict[str,str]]', ai_client = None):
    func, example = ask_ai(message, ai_client)
    maybe_use = maybe_use_func(func)
    res = pyi_doc() + "\n\n"
    res += "# api文档：\n"
    for a,b,_ in os.walk(os.path.dirname(__file__)):
        for name in b:
            if "__" in name or "example" in name:
                continue
            with open(f"{a}/{name}/{name}.pyi", encoding="utf-8") as f:
                lines = f.readlines()
                if '"""' in lines[0]:
                    jump = 2
                    for i in range(len(lines)):
                        if '"""' in lines[0]:
                            jump -= 1
                        lines.pop(0)
                        if jump == 0:
                            break
                use_funcs = extract_function_def_names(lines, maybe_use)
                if use_funcs:
                    res += f"## api文档[cork7/{name}.pyi]:\n```\n{use_funcs}```\n\n"
    res += maybe_use_example(example)
    # logging.info(res)
    logging.info(f"上下文提示词总字数：{len(res)}")
    return res


