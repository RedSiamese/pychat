import re
import requests
import os
import importlib.util
import sys, logging

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def force_run_mmcp(messages,ai_client):
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
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mmcp', info_dir)
        if not os.path.exists(base_path):
            continue

        # 检查是否存在自定义规则文件
        mmcp_path = os.path.join(base_path, '__mmcp__.py')
        if os.path.exists(mmcp_path):
            try:
                # 动态导入规则模块
                spec = importlib.util.spec_from_file_location(f"{info_dir}_mmcp", mmcp_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[f"{info_dir}_mmcp"] = module
                    spec.loader.exec_module(module)
                    # 调用规则函数
                    if hasattr(module, 'call'):
                        context = module.call(messages, ai_client)
                        if context:
                            system_messages.append(f"参考文档[{info_dir}]:\n\n{context}\n\n")
                    continue
            except Exception as e:
                import traceback
                traceback.print_exc()
                logging.error(f"Error loading mmcp from {mmcp_path}: {e}")

    
    if system_messages:
        messages = process_system(messages)
        messages = [{'role': 'system', 'content': ''.join(system_messages)}] + messages

    return messages



def process_system(messages):
    if not messages:
        return messages

    return [{"role": "system", "content": "用中文思考和回答，根据用户提供的文档和信息回答问题，不要擅自发挥和猜测，如果文档和已知信息不足以解决问题，请向用户提问或索要更多文档。"}] + messages



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
                logging.error(f"Error fetching GitHub file: {e}")
    
    return messages



def process_order(messages):
    new_messages = []
    for msg in messages:
        if len(new_messages) == 0 or new_messages[-1]["role"] != msg["role"]:
            new_messages.append(msg)
        else:
            new_messages[-1]["content"] += f"\n\n{msg['content']}"
        
    return new_messages





def process_messages(messages, ai_client):
    if not messages:
        return messages
    messages = force_run_mmcp(messages, ai_client)
    return messages


