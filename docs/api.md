# PyChat API 文档

## 基础信息

- 基础URL: `http://localhost:3000` (本地开发)
- 内容类型: `application/json`
- 编码方式: UTF-8

## 接口列表

### 1. 首页 API

获取服务欢迎信息。

- **URL**: `/`
- **方法**: `GET`
- **响应示例**:
```
Welcome to Calculator API
```

### 2. 系统信息 API

获取系统版本和可用接口信息。

- **URL**: `/api`
- **方法**: `GET`
- **响应示例**:
```json
{
    "version": "1.0.0",
    "name": "Calculator API",
    "author": "wxy",
    "description": "A simple calculator API service",
    "endpoints": [
        {"path": "/", "method": "GET", "description": "Welcome page"},
        {"path": "/api", "method": "GET", "description": "Get system information"},
        {"path": "/api/gpt", "method": "POST", "description": "Chat with GPT"},
        {"path": "/api/deepseek", "method": "POST", "description": "Chat with DeepSeek"}
    ]
}
```

### 3. ChatGPT 对话 API

与 ChatGPT 进行对话，支持流式输出。

- **URL**: `/api/gpt`
- **方法**: `POST`
- **请求头**:
```
Content-Type: application/json
```
- **请求体**:
```json
{
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"}
    ]
}
```

- **请求参数说明**:
  - `messages`: 对话消息数组
    - `role`: 消息角色，可选值：
      - `system`: 系统提示
      - `user`: 用户输入
      - `assistant`: AI 助手回复
    - `content`: 消息内容

- **响应**:
  - 内容类型: `text/event-stream`
  - 格式: Server-Sent Events (SSE)
  - 每个事件以 `data: ` 开头，后跟实际内容

- **示例代码**:

```javascript
// 发送请求
async function chatWithGPT() {
    const response = await fetch('http://localhost:3000/api/gpt', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            messages: [
                {"role": "user", "content": "Hello!"}
            ]
        })
    });

    // 处理流式响应
    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const {value, done} = await reader.read();
        if (done) break;
        
        const text = decoder.decode(value);
        const lines = text.split('\n');
        
        lines.forEach(line => {
            if (line.startsWith('data: ')) {
                const content = line.slice(6);
                console.log(content); // 处理收到的内容
            }
        });
    }
}
```

### Python 客户端示例

```python
import requests
import json

def chat_with_gpt():
    url = 'http://localhost:3000/api/gpt'
    headers = {'Content-Type': 'application/json'}
    data = {
        'messages': [
            {'role': 'user', 'content': 'Hello!'}
        ]
    }
    
    # 使用 stream=True 获取流式响应
    response = requests.post(url, headers=headers, json=data, stream=True)
    
    for line in response.iter_lines():
        if line:
            # 解析 SSE 格式数据
            line = line.decode('utf-8')
            if line.startswith('data: '):
                content = line[6:]  # 移除 'data: ' 前缀
                print(content, end='', flush=True)

```

### 4. DeepSeek 对话 API

与 DeepSeek 进行对话，支持流式输出。

- **URL**: `/api/deepseek`
- **方法**: `POST`
- **请求头**:
```
Content-Type: application/json
```
- **请求体**:
```json
{
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"}
    ]
}
```

- **请求参数说明**: 同 ChatGPT API
- **响应格式**: 同 ChatGPT API
- **示例代码**:

```javascript
async function chatWithDeepSeek() {
    const response = await fetch('http://localhost:3000/api/deepseek', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            messages: [
                {"role": "user", "content": "Hello!"}
            ]
        })
    });
    // 处理响应的代码与 GPT API 相同
}
```

### 错误处理

当发生错误时，API 将返回 HTTP 状态码和错误信息：

```json
{
    "error": "错误信息描述"
}
```

常见状态码：
- 200: 请求成功
- 400: 请求参数错误
- 500: 服务器内部错误

## 部署说明

### Vercel 环境变量

在 Vercel 部署时需要设置以下环境变量：

1. `OPENAI_API_KEY`: OpenAI API 密钥
2. `DEEPSEEK_API_KEY`: DeepSeek API 密钥

### CORS 支持

所有 API 端点都支持跨域请求（CORS），可以直接从浏览器调用。

## 注意事项

1. 使用流式响应时需要正确处理 SSE 格式数据
2. 建议在生产环境中添加适当的错误处理和重试机制
3. 请确保提供的 OpenAI API Key 有足够的使用额度
4. 建议在前端实现打字机效果来展示流式响应
