import requests

def test_gpt_stream():
    url = 'http://localhost:3000/api/gpt'
    headers = {'Content-Type': 'application/json'}
    data = {
        'messages': [
            {'role': 'user', 'content': 'Hello, who are you?'}
        ]
    }
    
    # 发送请求并获取流式响应
    response = requests.post(url, json=data, headers=headers, stream=True)
    
    # 处理响应
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                content = line[6:]  # 移除 'data: ' 前缀
                print(content, end='', flush=True)

if __name__ == '__main__':
    test_gpt_stream()
