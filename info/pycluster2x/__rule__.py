

funcs = {
    "dossier档案集聚档":{"func":["batch","simple_batch"], "doc":None},
    "dossier档案集合档/搜档":{"func":["oc","oc_separate","oc_separate_split","shadow","shadow_restore","search"], "doc":None},
    "dossier档案集离线合档":{"func":["check_multi"], "doc":None},
    "dossier档案集吸附/精准吸附":{"func":["adsorbed","adsorbed_recommend","precise_adsorbed","proxy_fuse"], "doc":None},
    "dossier档案集注册底库/分类等":{"func":["group","reg_gallery"], "doc":None},
    "dossier档案集设置和注册抓拍数据来源":{"func":["reg_database","set_cfg"], "doc":None},
    "dossier档案集参数配置/设置":{"func":["set_cfg","set_dim","__init__"], "doc":None},
    "dossier档案集自省":{"func":["cluster_num","person_num","get_alg","get_centriod_num","get_subnum_from_pid","is_person_exists","is_person_single","person_mdl","rid_unique_num"], "doc":"常用，包括如获取档案数、人数、算法句柄，判断人是否存在、人的有效模态等功能"},
    "dossier档案集人的抓拍信息获取":{"func":["get_person_info","get_person_info_include_scrap"], "doc":"常用，通常可以用于通过档案集dossier中的人，构造抓拍集pypic.pic_info"},
    "dossier档案集中提取/构建单人档案集":{"func":["get_person_from_pid","get_person_from_rid"], "doc":None},
    "dossier档案集检索":{"func":["__contains__","__getitem__"], "doc":None},
    "dossier档案集创建":{"func":["copy","create_empty","split","__init__"], "doc":None},
    "dossier档案集增删改":{"func":["__add__","__iadd__","__iadd__","add","add_person_from_pic","emplace_from_other","remove_person","remove_single","replace_from_other"], "doc":None},
    "dossier档案集整理":{"func":["recreate","recreate_coarse","reduce_person_dossier","tidy_up"], "doc":None},
    "dossier档案集质心特征查询":{"func":["get_feature","get_feature_as_view","is_feature_effective"], "doc":None},
    "dossier档案集rid/mid/pid转换":{"func":["get_mid_from_pid","get_mid_from_rid","get_pid_from_mid","get_pid_from_rid","get_rid_from_mid","get_rid_from_pid","get_r2p_map","get_rid2mid","get_rid2pid"], "doc":None},
    "dossier档案集uuid转换":{"func":["get_pid_from_uuid","get_uuid_from_pid","get_uuids_from_pid"], "doc":None},
    "dossier档案集io":{"func":["save","save_big","save_small","load","load_big","load_small","unser","ser"], "doc":None},
    "dossier档案集其他功能":{"func":["use_mmap","data2div","release_div","dos_adsorbed_impl","simple_info"], "doc":"不常用"},
    "dossier档案集数据结构规范性检查":{"func":["check_person_dos", "check_record", "check_rid_matching"], "doc":"不常用"},
    
    "cache数据缓存数据库中的抓拍数据查询/存储/修改操作":{"func":["__init__","contains_partition","big_partition_list","contains","db_data_num","db_write_down","from_rid","from_rids","get","get_partition","get_time_it","keys","partition_list","size","small_partition_list","not_end"], "doc":None},
    
    "pic_info抓拍集自省": {"func":["__getitem__","get_rids","get_rids_level","get_space_info","include","person_num","person_num_mdl","channel_code","gps","time"], "doc":None},
    "pic_info抓拍集算法功能/分级": {"func":["filter_from_level","get_level","get_rids_level"], "doc":None},
    "pic_info抓拍集构造/序列化成python基本类型/io": {"func":["__init__","copy","dump","feature_set_enhancement","ser","split","pb_input_csv","unser"], "doc":None},
    "pic_info抓拍集整理/增删改":{"func":["__add__","__iadd__","add","exclude","filter_from_level","get_level","include"], "doc":None},
    "pic_info抓拍集特征":{"func":["get_feature","get_feature_as_view","get_ftr"], "doc":None},
    "pic_info抓拍集合并":{"func":["__iadd__","__add__","add"], "doc":None},
    
    "cluster聚档基础功能":{"func":["c_threadid","__init__","default_cfg","this_platform"], "doc":None},
    "cluster版本管理":{"func":["demo_version","lib_version","sdk_version","doc"], "doc":None},
}

import requests,json,os
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()  # 加载环境变量

# 配置API密钥和基础URL
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
SILICONFLOW_API_KEY = os.getenv('SILICONFLOW_API_KEY', '')  # 添加硅基流动API密钥
DEEPSEEK_API_BASE = "https://api.deepseek.com"
SILICONFLOW_API_BASE = "https://api.siliconflow.com/v1/chat/completions"  # 修改硅基流动API基础URL

def siliconflow(messages:'list[dict[str, str]]'):
    """使用硅基流动API处理对话"""
    
    headers = {
        "Authorization": f"Bearer {SILICONFLOW_API_KEY}",
        "Content-Type": "application/json"
    }
    
    def generate(messages):
        try:
            data = {
                "model": "deepseek-ai/DeepSeek-V3",
                "messages": messages,
                "stream": True,
                "temperature": 0.2
            }
            
            # 使用requests发送流式请求
            response = requests.post(
                SILICONFLOW_API_BASE,
                headers=headers,
                json=data,
                stream=True
            )
            
            content = ""
            reasoning_content = ""

            def deal_response(resp:requests.Response):
                for line in resp.iter_lines():
                    if line:
                        # 删除 "data: " 前缀并解析 JSON
                        line:str = line.decode('utf-8')
                        if line.startswith("data: "):
                            try:
                                yield json.loads(line[6:])
                            except json.JSONDecodeError:
                                continue
                        else:
                            print("error line:", line)
                            continue
            
            # 处理流式响应
            for chunk in deal_response(response):
                if chunk["choices"][0]["delta"].get("reasoning_content"):
                    reasoning_content += chunk["choices"][0]["delta"]["reasoning_content"]
                    if reasoning_content and len(reasoning_content) > 200 and reasoning_content.endswith("。"):
                        reasoning_content = reasoning_content.replace("\n","\n> ")
                        yield f"Reason: (思考)\n> \n{reasoning_content}\n\n"
                        reasoning_content = ""
                elif chunk["choices"][0]["delta"].get("content"):
                    if reasoning_content:
                        reasoning_content = reasoning_content.replace("\n","\n> ")
                        yield f"Reason: (思考)\n> \n{reasoning_content}\n\n"
                        reasoning_content = ""
                    content += chunk["choices"][0]["delta"]["content"]


            if content:
                yield content
                    
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield "error: " + str(e)
        
    yield from generate(messages)

import re

def ask_ai(message:'list[dict[str,str]]')->'list[str]':
    pyi_doc = {}
    pyi_dir = os.path.dirname(__file__)
    for root, dirs, _ in os.walk(pyi_dir):
        for d in dirs:
            if d != "example" and "__" not in d:
                with open(f"{pyi_dir}/{d}/{d}.pyi", "r", encoding="utf-8") as f:
                    content = f.read()
                    # 使用正则匹配文件开头的docstring
                    doc_match = re.match(r'\s*"""(.*?)"""\s*', content, re.DOTALL)
                    if doc_match:
                        doc = doc_match.group(1).strip()
                        pyi_doc[d] = doc

    sysmsg = "\n\npycluster2x是一个用于把抓拍特征进行聚类分析的python库\n"
    for k in pyi_doc:
        sysmsg += f'\n{pyi_doc[k]}\n'

    sysmsg += "\npycluster2x的api分为若干类，分别为:\n"
    for k in funcs:
        sysmsg += f'"{k}",包含的api接口有{funcs[k]["func"]}'
        if "doc" in funcs[k] and funcs[k]["doc"]:
            sysmsg += f',{funcs[k]["doc"]}'
        sysmsg += "\n"

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
    
    sysmsg += "\n\n下面是使用pycluster2x python api写的一些代码示例的功能介绍:\n"
    for i, k in enumerate(examples):
        doc, _ = examples[k]
        sysmsg += f'{i}. "{k}":```\n{doc}\n```\n\n'

    sysmsg += \
"""
解决上述问题可能需要哪些类型的api？这些代码示例中，有哪些有助于解决上述问题，可以用于上述问题中作为代码生成的参考？
你的回答将有两行：
第一行，回答解决上述问题可能需要哪些类型的api，将所需要的api类型输出，用','隔开，如果不需要该库的功能，返回"none"，如：
dossier档案集rid/mid/pid转换,dossier档案集io,cluster聚档基础功能
第二行，回答这些代码示例中，有哪些有助于解决上述问题，可以用于上述问题中作为代码生成的参考，将可以用于参考的代码示例文件名输出，用','隔开。
如果上述描述的问题不是代码生成问题，或者问题和pycluster2x库无关，或者没有哪个代码示例可以用于参考，则返回"none"。
例如，当a.py和b.py可以作为参考时，输出：
a.py,b.py
当前面的提问不为代码生成问题时，输出：
none
当没有任何一个代码示例有助于前面的提问的代码生成时，输出：
none
"""
    print(sysmsg)
    msg = message[-1]["content"]
    message[-1]["content"] += sysmsg

    answer = ""
    for res in siliconflow(message):
        answer = res
    message[-1]["content"] = msg
    print("=======ask ai========")
    print(answer)
    print("=======ask ai========")
    if "\n" not in answer:
        return "none","none"
    answer = answer.split("\n")
    return answer[0], answer[1]





def maybe_use_func(answer:str) -> 'dict[str,set[str]]':
    res = {"dos":set(),"pic":set(),"clu":set(),"cac":set()}
    if answer == "none":
        return res
    keys = answer.split(",")
    for k in keys:
        if k not in funcs:
            print("error key", k)
            continue
        for func in funcs[k]["func"]:
            res[k[0:3]].add(func)
    return res


def extract_function_def_names(lines: 'list[str]', maybe_use:'set[str]') -> 'list[str]':
    if maybe_use == set():
        return ""
    all_funcs = set(sum(map(lambda x: x["func"], funcs.values()), []))
    pattern = r'^\s*def\s+(\w+)\s*\(.*?\)\s*(->\s*.*?)?\s*:'
    function_names = []
    jump = 0
    for i in range(len(lines)):
        line = lines[i]
        match = re.match(pattern, line.strip())
        if match and match.group(1) not in maybe_use and '"""' in lines[i+1] and match.group(1) in all_funcs or match and "async_" in match.group(1):
            if "@typing.overload" in function_names[-1]:
                function_names.pop()
            jump += 2
        else:
            # if match and match.group(1) not in all_funcs and "__" not in match.group(1):
            #     print("miss", match.group(1))
            if jump != 0:
                if '"""' in lines[i]:
                    jump -= 1
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
    res = ""
    for k in keys:
        if k not in examples:
            print("error key", k)
            continue
        res += f"参考示例\"{k}\":\n```python\n{examples[k][1]}\n```\n\n"
    return res



def rule(message:'list[dict[str,str]]'):
    func, example = ask_ai(message)
    maybe_use = maybe_use_func(func)
    res = ""
    for a,b,_ in os.walk(os.path.dirname(__file__)):
        for name in b:
            if "__" in name or "example" in name:
                continue
            with open(f"{a}/{name}/{name}.pyi", encoding="utf-8") as f:
                lines = f.readlines()
                # print(maybe_use)
                use_funcs = extract_function_def_names(lines, maybe_use[name[2:5]])
                if use_funcs:
                    res += f"api文档[pycluster2x/{name}.pyi]:```\n{use_funcs}```\n\n"
    res += maybe_use_example(example)
    # print(res)
    return res

# if __name__ == "__main__":
#     rule()