# PyChat API 文档

## 基础信息

- 基础URL: `https://pychat-iota.vercel.app` (生产环境)
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

### 4. DeepSeek 对话 API

与 DeepSeek 进行对话，支持流式输出。

- **URL**: `/api/deepseek`
- **方法**: `POST`
- **请求头**:
```
Content-Type: application/json
```
- **请求体**: 同 ChatGPT API
- **响应**: 同 ChatGPT API

## 错误处理

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

## 注意事项

1. 使用流式响应时需要正确处理 SSE 格式数据
2. 建议在生产环境中添加适当的错误处理和重试机制
3. 请确保提供的 API Key 有足够的使用额度
4. 建议在前端实现打字机效果来展示流式响应
