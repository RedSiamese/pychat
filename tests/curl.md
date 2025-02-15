```curl -X POST https://pychat-iota.vercel.app/api/gpt -H "Content-Type: application/json" -d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"```

```curl -X POST http://localhost:3000/api/deepseek -H "Content-Type: application/json" -d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"```

# Curl 测试命令

## GPT API 测试

### 本地测试
```bash
curl -X POST http://localhost:3000/api/gpt \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello, who are you?"}]}'
```

### Vercel 部署测试
```bash
curl -X POST https://pychat-iota.vercel.app/api/gpt \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello, who are you?"}]}'
```

## DeepSeek API 测试

### 本地测试
```bash
curl -X POST http://localhost:3000/api/deepseek \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello, what can you do?"}]}'
```

### Vercel 部署测试
```bash
curl -X POST https://pychat-iota.vercel.app/api/deepseek \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello, what can you do?"}]}'
```

## 系统信息 API 测试

### 本地测试
```bash
curl http://localhost:3000/api
```

### Vercel 部署测试
```bash
curl https://pychat-iota.vercel.app/api
```

### 使用 HTTP 代理
```bash
# Windows CMD
curl --proxy http://127.0.0.1:7078 -X POST https://pychat-iota.vercel.app/api/gpt -H "Content-Type: application/json" d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"

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

### Windows CMD 测试命令
```bash
# 本地测试
curl -x http://127.0.0.1:7078 -X POST http://localhost:3000/api/gpt ^
-H "Content-Type: application/json" ^
-d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"

# Vercel 部署测试
curl -x http://127.0.0.1:7078 -X POST https://pychat-iota.vercel.app/api/gpt ^
-H "Content-Type: application/json" ^
-d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}]}"
```

### Git Bash 测试命令
```bash
# 本地测试
curl -x http://127.0.0.1:7078 -X POST http://localhost:3000/api/gpt \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello"}]}'

# Vercel 部署测试
curl -x http://127.0.0.1:7078 -X POST https://pychat-iota.vercel.app/api/gpt \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### PowerShell 测试命令
```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    messages = @(
        @{
            role = "user"
            content = "Hello"
        }
    )
} | ConvertTo-Json

# 本地测试
$proxy = "http://127.0.0.1:7078"
$response = Invoke-WebRequest -Uri "http://localhost:3000/api/gpt" -Method Post -Headers $headers -Body $body -Proxy $proxy
$response.Content

# Vercel 部署测试
$proxy = "http://127.0.0.1:7078"
$response = Invoke-WebRequest -Uri "https://pychat-iota.vercel.app/api/gpt" -Method Post -Headers $headers -Body $body -Proxy $proxy
$response.Content
```

### 注意事项
1. Windows CMD 中使用 `^` 换行
2. Git Bash 中使用 `\` 换行
3. Windows CMD 中需要对引号转义 `\"`
4. Git Bash 可以使用单引号，不需要转义
5. 确保在命令中添加 `-d` 参数前的横杠