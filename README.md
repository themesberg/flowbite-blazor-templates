# Flowbite Blazor Templates

Project templates for creating beautiful admin dashboards with Flowbite Blazor components. Includes both WebAssembly (WASM) and .NET MAUI Blazor Hybrid options.

## Features

- **Full Admin Dashboard** - Complete dashboard with charts, CRUD operations, settings, and more
- **Flowbite Blazor UI** - Beautiful, responsive components from the Flowbite design system
- **Tailwind CSS v4** - Modern styling with automatic CSS compilation
- **ApexCharts Integration** - Interactive data visualization
- **Dark Mode Support** - Built-in theme switching
- **Prerendering (WASM)** - Fast initial load with static prerendering

## Available Templates

| Template | Short Name | Description |
|----------|------------|-------------|
| **Flowbite Blazor WASM Admin Dashboard** | `flowbite-blazor-wasm` | Blazor WebAssembly app with prerendering (.NET 9) |
| **Flowbite Blazor MAUI Admin Dashboard** | `flowbite-blazor-maui` | .NET MAUI Blazor Hybrid desktop app (.NET 10) |

## Installation

Install the templates by running:

```sh
dotnet new install Flowbite.Blazor.Templates
```

## Usage

### WebAssembly Template

Create a new Blazor WASM admin dashboard:

```sh
dotnet new flowbite-blazor-wasm -o MyDashboard
cd MyDashboard

# Build and run (auto-downloads Tailwind CSS)
python build.py start

# Open http://localhost:5269
```

### MAUI Template

Create a new .NET MAUI Blazor Hybrid desktop app:

```sh
dotnet new flowbite-blazor-maui -o MyDesktopApp
cd MyDesktopApp

# Build and run (auto-downloads Tailwind CSS)
python build.py run
```

**Note:** MAUI template requires .NET 10 SDK and supports Windows and macOS.

## Build Commands

Both templates include a `build.py` script for common operations:

### WASM Commands

```sh
python build.py build      # Build the solution
python build.py run        # Run in foreground
python build.py start      # Build and run in background
python build.py stop       # Stop background process
python build.py status     # Check if running
python build.py watch      # Hot reload development
python build.py publish    # Create production build
python build.py test-publish  # Test prerendering
```

### MAUI Commands

```sh
python build.py build      # Build the application
python build.py run        # Build and run
python build.py publish    # Create release build
python build.py clean      # Clean build artifacts
```

## Prerequisites

- **Python 3** - For build scripts
- **.NET 9 SDK** - For WASM template
- **.NET 10 SDK** - For MAUI template
- **psutil** (optional) - For WASM background process management: `pip install psutil`

## Uninstalling

To uninstall the templates:

```sh
dotnet new uninstall Flowbite.Blazor.Templates
```

## Development

To install templates locally for development:

```sh
./publish-local.ps1
```

Then use the templates as normal with `dotnet new`.

## Support

The Flowbite Blazor library is an open source project maintained by PeakFlames and other contributors. Support is provided on a best effort basis through the GitHub repository.

## License

MIT
