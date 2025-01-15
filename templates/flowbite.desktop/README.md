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

1. Run the Blazor Photinio App Server

   ```bash
   cd src/AppServer
   dotnet run
   ```

   Then a desktop windows will be visible with Flowbite contents.


## Deployment Setup

### Windows x64

The installer is created using [Inno Setup](https://jrsoftware.org/isinfo.php) and the [ISCC](https://jrsoftware.org/ishelp/index.php?topic=compilercmdline) command line tool.

To create the installer, run the following command from the project root directory:

```bash
.\build.ps1 -dist
```

This will create the installer in the `dist` directory.