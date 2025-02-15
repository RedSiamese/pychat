import re
import requests

def process_messages(messages):
    if not messages:
        return messages

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
                system_message = {
                    'role': 'user',
                    'content': f"File content from {github_url}:\n\n{file_content}"
                }
                
                # 将新的系统消息插入到倒数第二个位置
                messages.insert(-1, system_message)
                
            except requests.RequestException as e:
                print(f"Error fetching GitHub file: {e}")
    
    return messages
