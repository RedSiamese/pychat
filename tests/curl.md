```curl -X POST https://pychat-iota.vercel.app/api/gpt -H "Content-Type: application/json" -d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"```

```curl -X POST http://localhost:3000/api/deepseek -H "Content-Type: application/json" -d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"```

### 使用 HTTP 代理
```bash
# Windows CMD
curl -x http://127.0.0.1:7078 -X POST https://pychat-iota.vercel.app/api/gpt -H "Content-Type: application/json" d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"

# Git Bash 或 Linux
curl -x http://127.0.0.1:7078 -X POST https://pychat-iota.vercel.app/api/gpt \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### 使用 HTTPS 代理
```bash
# Windows CMD
curl -x https://127.0.0.1:7078 -X POST https://pychat-iota.vercel.app/api/gpt ^
-H "Content-Type: application/json" ^
-d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"

# Git Bash 或 Linux
curl -x https://127.0.0.1:7078 -X POST https://pychat-iota.vercel.app/api/gpt \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### 使用 SOCKS5 代理
```bash
# Windows CMD
curl --socks5 127.0.0.1:7078 -X POST https://pychat-iota.vercel.app/api/gpt ^
-H "Content-Type: application/json" ^
-d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"

# Git Bash 或 Linux
curl --socks5 127.0.0.1:7078 -X POST https://pychat-iota.vercel.app/api/gpt \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### 本地测试命令
```bash
# Windows CMD
curl -x http://127.0.0.1:7078 -X POST http://localhost:3000/api/gpt ^
-H "Content-Type: application/json" ^
-d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"

# Git Bash 或 Linux
curl -x http://127.0.0.1:7078 -X POST http://localhost:3000/api/gpt \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello"}]}'
```