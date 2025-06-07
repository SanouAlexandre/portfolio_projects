# PowerShell script to execute Docker commands

# Local directory
Write-Host "local repository..."
docker context use default

# Build a Docker image from the current directory (Dockerfile must be present)
Write-Host "Building the Docker image from the current directory..."
docker build --platform linux/amd64 -t chatbotui-nextjs-frontend .

# Wait for 10 seconds before proceeding
Write-Host "Waiting for 10 seconds..."
Start-Sleep -Seconds 10

docker run -p 3000:3000 --env-file .env.local chatbotui-nextjs-frontend

# run this command
# .\run_docker_commands_terralabour_web.ps1