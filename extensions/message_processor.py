import re
import requests
import os
import importlib.util
import sys

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import extensions.ai as ai

def process_local_info(messages):
    """处理本地info目录下的文件，支持多个@指令和自定义规则"""
    if not messages:
        return messages

    content = ""
    for msg in messages:
        if msg["role"] == "user":
            content += msg["content"]+"\n"

    local_info_matches = re.finditer(r'@(\w+)\s', content)
    
    system_messages = []
    matches = set()
    for match in local_info_matches:
        matches.add(match.group(1))
    for info_dir in matches:
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'info', info_dir)
        
        if not os.path.exists(base_path):
            continue

        # 检查是否存在自定义规则文件
        rule_path = os.path.join(base_path, '__rule__.py')
        if os.path.exists(rule_path):
            try:
                # 动态导入规则模块
                spec = importlib.util.spec_from_file_location(f"{info_dir}_rule", rule_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[f"{info_dir}_rule"] = module
                    spec.loader.exec_module(module)
                    
                    # 调用规则函数
                    if hasattr(module, 'rule'):
                        context = module.rule(messages, ai.tencent)
                        if context:
                            system_messages.append(f"参考文档[{info_dir}]:\n\n{context}\n\n")
                    continue
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Error loading rule from {rule_path}: {e}")

        # 如果没有规则文件或规则加载失败，使用默认处理方式
        all_content = []
        for filename in os.listdir(base_path):
            file_path = os.path.join(base_path, filename)
            if os.path.isfile(file_path) and filename not in ['__rule__.py']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    all_content.append(f"File: {filename}\n\n{file_content}\n\n")
        
        if all_content:
            system_message = f"Content from info/{info_dir}/:\n\n{''.join(all_content)}\n\n"
            system_messages.append(system_message)
    
    if system_messages:
        messages[-1]['content'] = ''.join(system_messages) + messages[-1]['content']

    return messages


def process_url(messages):
    if not messages:
        return messages
    """处理消息，包括GitHub链接"""
    
    # 然后处理GitHub链接
    last_message = messages[-1]
    if last_message['role'] == 'user':
        content = last_message['content']
        github_url_match = re.search(r'@(https://github\.com/[^\s]+)', content)
        
        if github_url_match:
            github_url = github_url_match.group(1)
            raw_url = github_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
            
            try:
                response = requests.get(raw_url)
                response.raise_for_status()
                file_content = response.text
                
                # 创建新的系统消息，包含文件内容和URL
                system_message = f"参考资料: {github_url}:\n\n{file_content}\n\n"
                
                # 将新的系统消息插入到倒数第二个位置
                messages[-1]['content'] = system_message + messages[-1]['content']
                
            except requests.RequestException as e:
                print(f"Error fetching GitHub file: {e}")
    
    return messages



def process_order(messages):
    new_messages = []
    for msg in messages:
        if len(new_messages) == 0 or new_messages[-1]["role"] != msg["role"]:
            new_messages.append(msg)
        else:
            new_messages[-1]["content"] += f"\n\n{msg['content']}"
        
    return new_messages




def process_system(messages):
    """处理消息截断，当遇到只包含连续破折号的消息时截断历史"""
    if not messages:
        return messages

    return [{"role": "system", "content": "用中文思考和回答，尽可能根据用户提供的文档和信息回答问题，尽可能不要擅自发挥和猜测，如果文档和已知信息不足以解决问题，请像用户提问或索要更多文档。"}] + messages

def process_messages(messages):
    if not messages:
        return messages

    messages = process_system(messages)
    messages = process_local_info(messages)
    messages = process_url(messages)
    messages = process_order(messages)
    
    return messages


