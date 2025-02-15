$BASE_URL = "http://localhost:3000"

function Test-API {
    param (
        [string]$Endpoint,
        $Data = $null
    )

    $url = "${BASE_URL}${Endpoint}"
    $headers = @{
        "Content-Type" = "application/json"
    }

    try {
        if ($Data) {
            $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body ($Data | ConvertTo-Json) -ContentType "application/json"
        } else {
            $response = Invoke-RestMethod -Uri $url -Method Get
        }

        Write-Host "API Test ($Endpoint) - Status: Success"
        $response | ConvertTo-Json -Depth 5
    }
    catch {
        Write-Host "API Test ($Endpoint) - Status: Failed"
        Write-Host "Error: $_"
    }
}

# 测试系统信息 API
Test-API -Endpoint "/api"

# 测试 ChatGPT API
$gptData = @{
    messages = @(
        @{
            role = "user"
            content = "Hello, who are you?"
        }
    )
}
Test-API -Endpoint "/api/gpt" -Data $gptData

# 测试 DeepSeek API
$deepseekData = @{
    messages = @(
        @{
            role = "user"
            content = "Hello, what can you do?"
        }
    )
}
Test-API -Endpoint "/api/deepseek" -Data $deepseekData

# 测试无效端点
Test-API -Endpoint "/invalid"
