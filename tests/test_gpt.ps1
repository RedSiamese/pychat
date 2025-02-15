$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    messages = @(
        @{
            role = "user"
            content = "Hello, who are you?"
        }
    )
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/api/gpt" -Method Post -Headers $headers -Body $body
    Write-Host $response.Content
} catch {
    Write-Host "Error: $_"
}
