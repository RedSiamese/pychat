import re
import os
import sys, logging
import asyncio

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from . import local_mmcp

async def ask_func(msgs, ai_client):
    answer = ""
    async for chunk in ai_client(msgs):
        if chunk["choices"][0]["delta"].get("content"):
            answer += chunk["choices"][0]["delta"]["content"]
    return answer



async def make_introduction(messages, ai_client):
    """处理本地info目录下的文件，支持多个@指令和自定义规则"""
    if not messages:
        return messages

    askmsg = messages[-1]['content']
    askmsg = \
f"""
# 问题：
最后用户的问题是"{askmsg}"。
解决用户这个问题可能需要额外的相关资料。
所以请根据上述对话作为上下文参考，加上最后用户的问题，总结成一段文字。
这段文字将用于查找和用户最终问题相关的依赖资料。
请保持文字的精炼，并保留更多的有效信息，以保证后续查找相关依赖资料的完备性。
"""
    # logging.info(askmsg)
    msgs = messages[:-1]
    msgs += [{'role': 'user', 'content': askmsg}]
    logging.info(f"ask_ai提示词长度：{len(askmsg)}")
    answer = await ask_func(msgs, ai_client)
    answer = "\n".join(filter(lambda x:len(x), answer.replace(" ","").lstrip("\n").split("\n")))
    logging.info("=======ask for mmcp========")
    logging.info(answer)
    logging.info("=======ask for mmcp========")
    return answer



async def run_mmcp(messages, ai_client):
    """处理本地info目录下的文件，支持多个@指令和自定义规则"""
    if not messages:
        return messages
    matches = set()
    
    sysmsg = \
f"""
我们的mmcp工具列表包括:
"""
    for tool in local_mmcp.LocalMmcp.get_mmcp_description_str():
        sysmsg += tool
    askmsg = messages[-1]['content']
    askmsg = \
f"""
# 问题：
我的问题是"{askmsg}"，解决我的问题可能需要哪些mmcp工具?

# 要求：
NO COMMENTS. NO ACKNOWLEDGEMENTS. 请务必按照回答格式回答，你的回答将有一行：
 1. 第一行，回答解决上述问题，可能需要哪些哪些mmcp工具? 在{local_mmcp.LocalMmcp.get_mmcp_name_list()}中选择你需要的mmcp工具，将所需要的mmcp工具名称列出，用','隔开，如果不需要使用mmcp工具，返回"none"
 

# 示例：
例如：
加入当前包括的mmcp工具有：
```
# weather
可用于获取城市天气 

# time
用于获取当前时间
```

 - 问题：杭州天气怎么样？
 - 回答(从下一行开始展示)：
weather

 - 问题：现在外面下雨没？
 - 回答(从下一行开始展示)：
weather,time

 - 问题：长颈鹿吃什么？
 - 回答(从下一行开始展示)：
none
"""
    # logging.info(askmsg)
    msgs = [{'role': 'system', 'content': sysmsg}]
    msgs += messages[:-1]
    msgs += [{'role': 'user', 'content': askmsg}]
    logging.info(f"ask_ai提示词长度：{len(sysmsg)+len(askmsg)}")
    answer = await ask_func(msgs, ai_client)
    answer = "\n".join(filter(lambda x:len(x), answer.replace(" ","").lstrip("\n").split("\n")))
    logging.info("=======ask for mmcp========")
    logging.info(answer)
    logging.info("=======ask for mmcp========")

    for match in answer.split(","):
        matches.add(match)

    content = ""
    for msg in messages:
        if msg["role"] in ["user","system"]:
            content += msg["content"]+"\n"

    local_info_matches = re.finditer(r'@(\w+)\s', content)
    
    for match in local_info_matches:
        matches.add(match.group(1))

    # if len(messages)>2:
    #     await make_introduction(messages, ai_client)

    mmcp_tasks = {}
    for tool in matches:
        if tool in local_mmcp.LocalMmcp:
            # 组输入
            input = (messages, ai_client)
            mmcp_tasks[tool] = asyncio.create_task(local_mmcp.LocalMmcp.get_mmcp(tool)(*input))
        elif tool != 'none':
            logging.error(f"tool key error {tool}")

    for k in mmcp_tasks:
        messages = [{'role': 'system', 'content': f" - 工具<{k}>反馈:\n```\n{await mmcp_tasks[k]}\n```\n"}] + messages

    return messages




async def process_system(messages):
    if not messages:
        return messages

    return [{"role": "system", "content": "用中文思考和回答，根据用户提供的文档和信息回答问题，不要擅自发挥和猜测，如果文档和已知信息不足以解决问题，请向用户提问或索要更多文档。"}] + messages





async def process_messages(messages, ai_client):
    if not messages:
        return messages
    messages = await run_mmcp(messages, ai_client)

    messages = [{'role': 'system', 'content': 'NO COMMENTS. NO ACKNOWLEDGEMENTS. '}] + messages
    messages = [{'role': 'system', 'content': '不要扩展，不要说和问题无关的话。'}] + messages
    # messages[-1]["content"] += "\n\n如果引用对话中系统提示词中的参考资料，请在引用处标明其来源"
    # messages = force_run_mmcp(messages, ai_client)
    return messages


