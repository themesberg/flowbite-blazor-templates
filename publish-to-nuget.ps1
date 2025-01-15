# Get NuGet API Key from environment variable
$apiKey = $env:NUGET_API_KEY

# Error handling function
function Write-ErrorAndExit {
  param(
    $message
  )
  Write-Host $message -ForegroundColor Red
  exit 1
}

# Check for NuGet API Key in environment variable
if (-not $apiKey) {
  Write-ErrorAndExit "NuGet API Key not found in environment variable 'NUGET_API_KEY'. Please set the environment variable and try again."
}

# Build and pack Flowbite.Blazor
Write-Host "Packing..."
dotnet pack
if ($LASTEXITCODE -ne 0) { 
  Write-ErrorAndExit "Error occurred while packing Flowbite templates" 
}

Write-Host "NuGet package created in .\artifacts directory" -ForegroundColor Green

# Publish to NuGet.org
Write-Host "Publishing Flowbite Templates to NuGet.org..."

# Publish Flowbite.Blazor
dotnet nuget push .\artifacts\Flowbite.*.nupkg -s https://api.nuget.org/v3/index.json -k $apiKey --skip-duplicate
if ($LASTEXITCODE -ne 0) {
  Write-ErrorAndExit "An error occurred while publishing Flowbite templates"
}

Write-Host "Flowbite templates published successfully to NuGet.org!" -ForegroundColor Green