[CmdletBinding()]
param(
    [switch]$dist,
    [switch]$Help
)

function Show-Usage {
    Write-Host "Usage: .\build.ps1 [-dist] [-Help]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -dist          Create the installer after building"
    Write-Host "  -Help               Display this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\build.ps1                 # Build the project"
    Write-Host "  .\build.ps1 -dist       # Build and create installer"
    Write-Host "  .\build.ps1 -Help           # Display this help message"
}

function Publish-Project {
    if ($dist) {
        Write-Host "Publishing project..."
        Remove-Item -Recurse -Force src/AppServer/publish -ErrorAction SilentlyContinue
        dotnet publish src/AppServer/AppServer.csproj -c Release -r win-x64 --self-contained
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to publish project."
            exit 1
        }
        Write-Host "Project published successfully."
    } else {
        Write-Host "Building project..."
        dotnet build --project src/AppServer/AppServer.csproj
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to build project."
            exit 1
        }
         Write-Host "Project built successfully."
    }
}

function Create-Installer {
    Write-Host "Creating installer..."
    $innoSetupCompiler = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if (-not (Test-Path $innoSetupCompiler)) {
        Write-Error "Inno Setup Compiler not found. Please make sure Inno Setup is installed."
        exit 1
    }
    
    & $innoSetupCompiler "AppServerSetup.iss"
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create installer."
        exit 1
    }
    Write-Host "Installer created successfully."
}

# Main script execution
if ($Help) {
    Show-Usage
    exit 0
}

Publish-Project

if ($dist) {
    Create-Installer
}

Write-Host "All operations completed successfully."
