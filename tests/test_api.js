const fetch = require('node-fetch');

const BASE_URL = 'http://localhost:3000';

async function testAPI(endpoint, data = null) {
    const url = `${BASE_URL}${endpoint}`;
    const options = {
        method: data ? 'POST' : 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        console.log(`API Test (${endpoint}) - Status Code: ${response.status}`);

        if (response.headers.get('Content-Type') === 'text/event-stream') {
            console.log(`${endpoint} Test (Streaming):`);
            const reader = response.body.getReader();
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                console.log(new TextDecoder().decode(value));
            }
        } else {
            const json = await response.json();
            console.log(`${endpoint} Test:`);
            console.log(JSON.stringify(json, null, 2));
        }
    } catch (error) {
        console.error(`Request failed: ${error.message}`);
    }
}

(async () => {
    await testAPI('/api');
    await testAPI('/api/gpt', { messages: [{ role: 'user', content: 'Hello, who are you?' }] });
    await testAPI('/api/deepseek', { messages: [{ role: 'user', content: 'Hello, what can you do?' }] });
    await testAPI('/invalid');  // 测试无效端点
})();
