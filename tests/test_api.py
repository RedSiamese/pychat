import requests
import json
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:3000"

def test_api(endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        if data:
            response = requests.post(url, headers=headers, json=data, stream=True)
        else:
            response = requests.get(url)
        
        response.raise_for_status()
        logger.info(f"API Test ({endpoint}) - Status Code: {response.status_code}")
        
        if response.headers.get('Content-Type') == 'text/event-stream':
            print(f"{endpoint} Test (Streaming):")
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    print(decoded_line)
                    logger.debug(f"Received: {decoded_line}")
        else:
            print(f"{endpoint} Test:")
            print(json.dumps(response.json(), indent=2))
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        logger.error(f"Request failed: {e}", exc_info=True)

if __name__ == '__main__':
    test_api("/api")
    test_api("/api/gpt", {"messages": [{"role": "user", "content": "Hello, who are you?"}]})
    test_api("/api/deepseek", {"messages": [{"role": "user", "content": "Hello, what can you do?"}]})
    test_api("/invalid")  # 测试无效端点
