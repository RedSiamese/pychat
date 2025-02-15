# PyChat API

一个基于 Flask 的 ChatGPT 代理 API 服务，支持流式输出。

## 功能特点

- 支持 ChatGPT API 的流式输出
- 提供系统信息查询接口
- 部署简单，支持 Vercel 自动部署
- 使用 TypeScript 类型注解提供更好的代码提示

## 快速开始

### 环境要求

- Python 3.7+
- OpenAI API Key

### 安装步骤

1. 克隆项目
```bash
git clone <your-repository-url>
cd pychat
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
复制 `.env.local` 到 `.env` 并填入你的 OpenAI API Key：
```
OPENAI_API_KEY=your_api_key_here
```

### 环境变量设置

1. 复制环境变量示例文件：
```bash
cp .env.local .env
```

2. 编辑 .env 文件，填入你的 API Keys：
```properties
OPENAI_API_KEY=your_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

注意：永远不要提交 .env 文件到版本控制系统。

4. 启动服务
```bash
python api/index.py
```

服务将在 http://localhost:3000 启动

## API 文档

### 获取系统信息
- 方法: `GET`
- 路径: `/api`
- 响应示例:
```json
{
    "version": "1.0.0",
    "name": "Calculator API",
    "author": "wxy",
    "description": "A simple calculator API service",
    "endpoints": [
        {"path": "/", "method": "GET", "description": "Welcome page"},
        {"path": "/api/info", "method": "GET", "description": "Get system information"},
        {"path": "/api/gpt", "method": "POST", "description": "Chat with GPT"},
        {"path": "/api/deepseek", "method": "POST", "description": "Chat with DeepSeek"}
    ]
}
```

### ChatGPT 对话
- 方法: `POST`
- 路径: `/api/gpt`
- 请求体示例:
```json
{
    "messages": [
        {"role": "user", "content": "Hello!"}
    ]
}
```

### DeepSeek 对话
- 方法: `POST`
- 路径: `/api/deepseek`
- 请求体示例: 与 GPT API 相同

### 前端集成示例

```javascript
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
            console.log(content);
        }
    });
}
```

## 部署

### Vercel 部署
1. Fork 此项目
2. 在 Vercel 中导入项目
3. 设置环境变量 `OPENAI_API_KEY`
4. 完成部署

## 许可证

MIT License

## 作者

wxy

## 文档

详细的 API 文档请参考 [API文档](docs/api.md)
