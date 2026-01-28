# Flowbite Blazor MAUI Admin Dashboard

A beautiful, modern desktop admin dashboard built with .NET MAUI Blazor Hybrid, Flowbite Blazor components, Tailwind CSS, and ApexCharts.

## Features

- Full admin dashboard with 14+ pages
- Dark mode support
- Native desktop application (Windows, macOS)
- ApexCharts integration for data visualization
- CRUD operations examples
- Settings and profile pages

## Supported Platforms

- **Windows** 10 (version 17763.0 or higher)
- **macOS** (Mac Catalyst 15.0 or higher)

## Quick Start

```bash
# Build and run (auto-downloads Tailwind CSS)
python build.py run
```

## Build Commands

The project includes a `build.py` script for all common operations:

```bash
python build.py build      # Build the application
python build.py run        # Build and run
python build.py publish    # Create release build
python build.py clean      # Clean build artifacts
```

### Prerequisites

- Python 3
- .NET 10 SDK

## Project Structure

```
Flowbite.Maui/
├── Components/     # Blazor components (Routes, _Imports, Dashboard/, etc.)
├── Pages/          # Dashboard pages (14+ pages)
├── Layout/         # Layout components (MainLayout, StackedLayout)
├── Services/       # Application services
├── Domain/         # Data models
├── Charts/         # ApexCharts configuration
├── Platforms/      # Platform-specific code
│   ├── MacCatalyst/
│   └── Windows/
├── Resources/      # App icons, splash screen, fonts
├── wwwroot/        # Static assets (CSS, JS, images)
├── build.py        # Build automation script
└── CLAUDE.md       # Claude Code guidance
```

## Development Workflow

### Build and Run

```bash
# Build for current platform
python build.py build

# Build and run
python build.py run
```

### Release Build

Create an optimized release build:

```bash
python build.py publish
```

The output will be in `dist/`.

## Direct .NET CLI Usage

If you prefer using the .NET CLI directly:

```bash
# Build for macOS
dotnet build Flowbite.Maui.csproj -f net10.0-maccatalyst

# Build for Windows
dotnet build Flowbite.Maui.csproj -f net10.0-windows10.0.19041.0

# Run (macOS)
dotnet run --project Flowbite.Maui.csproj -f net10.0-maccatalyst

# Run (Windows)
dotnet run --project Flowbite.Maui.csproj -f net10.0-windows10.0.19041.0
```

**Note:** Direct CLI usage requires manually downloading Tailwind CSS first. Use `build.py` for automatic setup.

## Tailwind CSS

The project uses Tailwind CSS v4.1.8 with the CSS-first configuration approach. The `build.py` script automatically downloads the Tailwind executable on first run.

CSS files:
- Input: `wwwroot/css/app.css`
- Output: `wwwroot/css/app.min.css`

## Technologies

- .NET 10 / MAUI Blazor Hybrid
- Flowbite Blazor components
- Tailwind CSS v4.1.8
- ApexCharts (Blazor-ApexCharts)

## Window Configuration

The default window size is configured in `App.xaml.cs`:
- Default: 1280x800
- Minimum: 800x600

You can modify these values in the `CreateWindow` method.

## License

MIT
