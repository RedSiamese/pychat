import requests
import json
import unittest

BASE_URL = "http://localhost:3000"

class TestPyChatAPI(unittest.TestCase):
    def test_home_endpoint(self):
        response = requests.get(f"{BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Welcome to Calculator API")

    def test_info_endpoint(self):
        response = requests.get(f"{BASE_URL}/api")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("version", data)
        self.assertIn("name", data)
        self.assertIn("author", data)
        self.assertIn("description", data)
        self.assertIn("endpoints", data)

    def test_gpt_endpoint(self):
        url = f"{BASE_URL}/api/gpt"
        headers = {'Content-Type': 'application/json'}
        data = {
            'messages': [
                {'role': 'user', 'content': 'Hello, who are you?'}
            ]
        }
        response = requests.post(url, headers=headers, json=data, stream=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/event-stream')
        
        content = ""
        for line in response.iter_lines():
            if line:
                content += line.decode('utf-8')
        self.assertIn("data:", content)

    def test_deepseek_endpoint(self):
        url = f"{BASE_URL}/api/deepseek"
        headers = {'Content-Type': 'application/json'}
        data = {
            'messages': [
                {'role': 'user', 'content': 'Hello, what can you do?'}
            ]
        }
        response = requests.post(url, headers=headers, json=data, stream=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/event-stream')
        
        content = ""
        for line in response.iter_lines():
            if line:
                content += line.decode('utf-8')
        self.assertIn("data:", content)

    def test_invalid_endpoint(self):
        response = requests.get(f"{BASE_URL}/invalid")
        self.assertEqual(response.status_code, 404)

    def test_gpt_endpoint_invalid_data(self):
        url = f"{BASE_URL}/api/gpt"
        headers = {'Content-Type': 'application/json'}
        data = {}  # 空数据
        response = requests.post(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
