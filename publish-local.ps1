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


# Build and pack Flowbite.Blazor
Write-Host "Packing..."

# Delete the .\artifacts directory before running pack
if (Test-Path ".\artifacts") {
  rm -r -force .\artifacts
}


dotnet pack
if ($LASTEXITCODE -ne 0) { 
  Write-ErrorAndExit "Error occurred while packing Flowbite templates" 
}

Write-Host "NuGet package created in .\artifacts directory" -ForegroundColor Green

# Test if the nuget package exists
$nugetPackage = Get-ChildItem -Path .\artifacts -Filter "*.nupkg" -Recurse
if (-not $nugetPackage) {
  Write-ErrorAndExit "NuGet package not found in .\artifacts directory"
}

# Publish to NuGet.org
Write-Host "Installing the nuget package locally..."

# Get the file name of the package by searching the directory for the .nupkg file
$nugetPackageFileName = Get-ChildItem -Path .\artifacts -Filter "*.nupkg" -Recurse | Select-Object -ExpandProperty Name -First 1


# Install the nuget package locally
dotnet new uninstall Flowbite.Blazor.Templates
dotnet new install ./artifacts/$nugetPackageFileName
if ($LASTEXITCODE -ne 0) {
  Write-ErrorAndExit "An error occurred while publishing Flowbite templates"
}

Write-Host "Flowbite templates published locally!" -ForegroundColor Green
