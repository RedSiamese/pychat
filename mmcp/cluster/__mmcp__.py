import logging, os

docs = {
    "常用脚本":"包含cluster聚档项目常用的脚本运行方法，例如运行单卡、多卡的流程测试、上传下载数据集脚本等等",
    "快速入门":"包含如何使用聚档项目pycluster2x python扩展包的安装部署等",
    "历史版本":"包含聚档项目pycluster2x python扩展包的历史版本，以及版本更新内容",
    "资源列表":"包含cluster聚档项目常用数据集的地址，如安徽数据集，龙泉驿数据集",
}

def ask_ai(message:'list[dict[str,str]]', ai_client)->'list[str]':
    sysmsg = """
# 背景：
聚档项目相关信息包含几个文档文件：
"""

    for i, (k,v) in enumerate(docs.items()):
        sysmsg += f" {i}. '{k}': {v}\n\n"
    
    askmsg = message[-1]['content']
    askmsg = \
f"""
# 问题：
用户的问题是"{askmsg}"，那么解决用户的问题可能需要哪些文档文件？

# 说明：
你的回答将有一行：
回答解决上述问题可能需要的文档名称，用','隔开，如果不需要该库的功能，返回"none"

# 示例：
例如：
 - 问题：龙泉驿单卡任务怎么测试
 - 分析：当用户在问某个地区的数据怎么跑的时候，需要查找指定数据集的访问方法，并且你需要了解运行单卡测试脚本的方法。结果中所有文档名用逗号隔开。
 - 回答：快速入门,常用脚本,资源列表

请务必按照这个回答格式。NO COMMENTS. NO ACKNOWLEDGEMENTS.
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
    return answer


def call(message:'list[dict[str,str]]', ai_client = None):
    maybe_use = ask_ai(message, ai_client).split(",")
    maybe_use = list(map(lambda x: x+".md", maybe_use))
    base_path = os.path.dirname(__file__)
    all_content:'list[str]' = []
    for filename in os.listdir(base_path):
        if filename in maybe_use:
            file_path = os.path.join(base_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    all_content.append(f"<{filename}>:\n{file_content}\n")
    # logging.info(all_content)
    return "\n\n".join(all_content)


