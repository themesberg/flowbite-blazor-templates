# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains .NET templates for creating Flowbite Blazor admin dashboard applications. It is a template package project that bundles two distinct project templates:
- **flowbite-blazor-wasm**: Blazor WebAssembly Admin Dashboard with Tailwind CSS, Flowbite UI, and ApexCharts (.NET 9)
- **flowbite-blazor-maui**: .NET MAUI Blazor Hybrid Desktop Admin Dashboard with Tailwind CSS, Flowbite UI, and ApexCharts (.NET 10)

The repository itself is NOT a runnable application - it's a template package that generates NuGet packages for `dotnet new` template installation.

## Architecture

### Template Package Structure

```
Flowbite.Blazor.Templates.csproj (Root package project - v0.2.0)
├── templates/
│   ├── flowbite.wasm/           (WebAssembly Admin Dashboard template)
│   │   ├── .template.config/    (Template configuration)
│   │   ├── build.py             (Build automation script)
│   │   ├── CLAUDE.md            (Template-specific Claude guidance)
│   │   ├── Pages/               (14 dashboard pages)
│   │   ├── Components/          (24+ reusable components)
│   │   ├── Layout/              (MainLayout, StackedLayout, etc.)
│   │   ├── Services/            (ThemeService, SettingsService, PricingService)
│   │   ├── Domain/              (Data models)
│   │   ├── Charts/              (ApexCharts configuration)
│   │   └── wwwroot/             (Static assets, CSS, JS)
│   └── flowbite.maui/           (MAUI Blazor Hybrid template)
│       ├── .template.config/    (Template configuration)
│       ├── build.py             (Build automation script)
│       ├── CLAUDE.md            (Template-specific Claude guidance)
│       ├── Platforms/           (MacCatalyst, Windows)
│       ├── Resources/           (App icons, splash, styles)
│       ├── Components/          (Blazor components including Routes.razor)
│       ├── Pages/               (Same pages as WASM)
│       ├── Layout/              (Same layouts as WASM)
│       ├── Services/            (Same services as WASM)
│       ├── Domain/              (Same models as WASM)
│       ├── Charts/              (Same charts as WASM)
│       └── wwwroot/             (Static assets for MAUI)
```

### Key Concepts

**Template Configuration**: Each template has a `.template.config/template.json` file defining:
- Short name for CLI usage (`flowbite-blazor-wasm`, `flowbite-blazor-maui`)
- Template identity and group
- Source exclusions and file renames
- Classification tags

**Template Package**: The root `.csproj` uses `PackageType=Template` and includes all template files in `ContentTargetFolders`. This is not a standard .NET project - it cannot be built or run, only packed into a NuGet package.

**Build Automation**: Both templates include a `build.py` script that:
- Auto-downloads Tailwind CSS executable for the target OS
- Checks for required .NET SDK version
- Provides commands for build, run, publish, etc.

**Tailwind Integration**: Both templates use the standalone Tailwind CSS v4.1.8 executable (not npm/node). Templates include custom MSBuild targets that run the Tailwind CLI before build to generate `app.min.css` from `app.css`.

## Common Commands

### Template Development

Install templates locally for testing:
```bash
./publish-local.ps1
```
This script:
1. Deletes `./artifacts` directory
2. Runs `dotnet pack` to create NuGet package
3. Uninstalls existing template with `dotnet new uninstall Flowbite.Blazor.Templates`
4. Installs from `./artifacts/*.nupkg` with `dotnet new install`

Publish to NuGet.org (requires `NUGET_API_KEY` environment variable and `main` branch):
```bash
./publish-to-nuget.ps1
```

### Template Usage (After Installation)

Create a new WebAssembly project:
```bash
dotnet new flowbite-blazor-wasm -o MyDashboard
cd MyDashboard
python build.py start    # Auto-downloads Tailwind, builds, and runs
# Open http://localhost:5269
```

Create a new MAUI Desktop project:
```bash
dotnet new flowbite-blazor-maui -o MyDesktopApp
cd MyDesktopApp
python build.py run      # Auto-downloads Tailwind, builds, and runs
```

### Testing Template Changes

After modifying template files, you must reinstall the template locally to test changes:
```bash
./publish-local.ps1
# Then create a test project using the template
dotnet new flowbite-blazor-wasm -o test-wasm
dotnet new flowbite-blazor-maui -o test-maui
```

## Template-Specific Details

### WebAssembly Template (flowbite-blazor-wasm)

**Key Technologies**:
- `Microsoft.NET.Sdk.BlazorWebAssembly` (.NET 9)
- `BlazorWasmPreRendering.Build` v6.0.0 for static HTML generation
- `Flowbite` [0.2.0-beta,) and `Flowbite.ExtendedIcons` [0.0.6-alpha,)
- `Blazor-ApexCharts` v6.0.2 for data visualization
- Tailwind CSS v4.1.8 via standalone executable

**Build Commands**:
```bash
python build.py build      # Build the solution
python build.py run        # Run in foreground
python build.py start      # Build and run in background
python build.py stop       # Stop background process
python build.py status     # Check if running
python build.py watch      # Hot reload development
python build.py publish    # Create production build
python build.py test-publish  # Test prerendering
```

**Build Process**:
1. `build.py` downloads Tailwind CSS if not present
2. MSBuild target runs Tailwind CLI to generate CSS
3. Blazor WASM compilation
4. Prerendering for static HTML (on publish)

**Important Files**:
- `Program.cs`: Must use `ConfigureServices` static method for prerendering support
- `wwwroot/index.html`: Includes dark mode detection script in `<head>`
- `tailwind.config.js`: Configured for Tailwind v4 CSS-first approach
- `build.py`: Handles Tailwind download and all build commands

### MAUI Template (flowbite-blazor-maui)

**Key Technologies**:
- `Microsoft.NET.Sdk.Razor` with MAUI (.NET 10)
- `Microsoft.AspNetCore.Components.WebView.Maui` for Blazor Hybrid
- `Flowbite` [0.2.0-beta,) and `Flowbite.ExtendedIcons` [0.0.6-alpha,)
- `Blazor-ApexCharts` v6.0.2 for data visualization
- Tailwind CSS v4.1.8 via standalone executable

**Supported Platforms**:
- Windows 10 (version 17763.0 or higher)
- macOS (Mac Catalyst 15.0 or higher)

**Build Commands**:
```bash
python build.py build      # Build the application
python build.py run        # Build and run
python build.py publish    # Create release build
python build.py clean      # Clean build artifacts
```

**Build Process**:
1. `build.py` downloads Tailwind CSS if not present
2. MSBuild target runs Tailwind CLI to generate CSS
3. MAUI Blazor Hybrid compilation for target platform

**Important Files**:
- `MauiProgram.cs`: Application entry point and DI configuration
- `MainPage.xaml`: BlazorWebView host page
- `wwwroot/index.html`: Blazor host page (uses `blazor.webview.js`)
- `App.xaml.cs`: Window configuration (size, title)
- `build.py`: Handles Tailwind download and all build commands

## Important Notes

### Modifying Templates

When editing template files:
- Changes in `templates/*/` directories affect generated projects, not this repository
- Template files use token replacement: `Flowbite.Wasm` → project name, `Flowbite.Maui` → project name
- `.template.config/template.json` controls file exclusions and renames
- Both templates share the same Pages, Components, Layout, Services, Domain, and Charts code

### Package References

Template `.csproj` files use floating version ranges for Flowbite packages:
- `Flowbite` → `[0.2.0-beta,)` (minimum version with no upper bound)
- `Flowbite.ExtendedIcons` → `[0.0.6-alpha,)`

### Tailwind CSS Setup

Both templates automatically download Tailwind CSS via `build.py`. Manual download is no longer required.

The `build.py` script:
1. Detects the operating system
2. Downloads the appropriate Tailwind v4.1.8 executable
3. Places it in `tools/tailwindcss` (or `tools/tailwindcss.exe` on Windows)
4. Makes it executable on Unix-like systems

### Shared Content Between Templates

The WASM and MAUI templates share the same:
- Pages (14 dashboard pages)
- Components (Dashboard, CRUD, Settings, etc.)
- Layout (MainLayout, StackedLayout, etc.)
- Services (ThemeService, SettingsService, PricingService)
- Domain models
- Charts configuration
- Most wwwroot assets

The key differences are:
- WASM uses `blazor.webassembly.js` and prerendering
- MAUI uses `blazor.webview.js` and BlazorWebView
- WASM services are registered as Scoped
- MAUI services are registered as Singleton
