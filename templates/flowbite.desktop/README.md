# Flowbite.Desktop

## Development Setup

1. Install standalone Tailwind CSS CLI executable:

   Mac/Linux:

   ```bash
   mkdir ./tools && cd ./tools && curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64  && chmod +x tailwindcss-macos-arm64 && mv tailwindcss-macos-arm64 tailwindcss
   ```

   Windows:

   ```pwsh
   mkdir ./tools -Force; `
   cd ./tools; `
   Invoke-WebRequest -Uri "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe" `
      -OutFile "tailwindcss.exe" `
      -UseBasicParsing ; `
   cd ..

   ```

1. Build the solution

   ```bash
   dotnet build
   ```

1. Run the Blazor Photino App Server

   ```bash
   cd src/AppServer
   dotnet run
   ```

   Then a desktop windows will be visible with Flowbite contents.

## Distribution

### Building the Installer (Windows x64)

#### Prerequisites

1. [Inno Setup 6](https://jrsoftware.org/isinfo.php) - Required for creating the Windows installer
2. Windows 10 version 1809 or later
3. .NET 8.0 SDK

#### Creating the Installer

The build script provides options for creating the installer:

```powershell
# Show all available options
.\build.ps1 -Help

# Build and create installer with default version (1.0.0)
.\build.ps1 -dist

# Build and create installer with specific version
.\build.ps1 -dist -version 1.2.3
```

The installer will be created in `dist/win-x64` with the naming format: `Flowbite.Desktop-{version}-Setup.exe`

### Installation Details

The application installs with the following characteristics:

- **Installation Directory**: `C:\Program Files\ACME\Flowbite.Desktop`
- **Start Menu**: Programs > ACME > Flowbite.Desktop
- **Desktop Shortcut**: Optional during installation
- **System Requirements**:
  - Windows 10 version 1809 or later
  - 64-bit processor
  - Standard user installation supported

### Installer Features

- Self-contained deployment (includes .NET runtime)
- Single-file application with compression
- Clean uninstallation with proper cleanup
- Proper version management
- Support for silent installation
- Automatic updates of existing installations

### Silent Installation

For automated deployment, the installer supports silent installation:

```powershell
# Silent installation
Flowbite.Desktop-1.0.0-Setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART

# Silent uninstallation
"C:\Program Files\ACME\Flowbite.Desktop\unins000.exe" /VERYSILENT
```
