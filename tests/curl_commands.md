# cURL 测试命令

## 获取系统信息
```bash
curl http://localhost:3000/api
```

## ChatGPT API 测试
```bash
curl -X POST http://localhost:3000/api/gpt \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello, who are you?"}]}'
```

## DeepSeek API 测试
```bash
curl -X POST http://localhost:3000/api/deepseek \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello, what can you do?"}]}'
```

## 测试无效端点
```bash
curl http://localhost:3000/invalid
```
