# Flowbite Blazor WASM Admin Dashboard

A beautiful, modern admin dashboard built with Blazor WebAssembly, Flowbite Blazor components, Tailwind CSS, and ApexCharts.

## Features

- Full admin dashboard with 14+ pages
- Dark mode support
- Responsive design
- ApexCharts integration for data visualization
- CRUD operations examples
- Settings and profile pages
- Prerendering support for fast initial load

## Quick Start

```bash
# Build and run in background (auto-downloads Tailwind CSS)
python build.py start

# Open http://localhost:5269
```

## Build Commands

The project includes a `build.py` script for all common operations:

```bash
python build.py build        # Build the solution
python build.py run          # Run in foreground
python build.py start        # Build and run in background
python build.py stop         # Stop background process
python build.py status       # Check if running
python build.py watch        # Hot reload development
python build.py publish      # Create production build
python build.py test-publish # Test prerendering
python build.py log          # View application logs
```

### Prerequisites

- Python 3
- .NET 9 SDK
- psutil (optional, for background process management): `pip install psutil`

## Project Structure

```
Flowbite.Wasm/
├── Pages/          # Dashboard pages (14+ pages)
├── Components/     # Reusable Razor components
├── Layout/         # Layout components (MainLayout, StackedLayout)
├── Services/       # Application services
├── Domain/         # Data models
├── Charts/         # ApexCharts configuration
├── wwwroot/        # Static assets (CSS, JS, images)
├── build.py        # Build automation script
└── CLAUDE.md       # Claude Code guidance
```

## Development Workflow

### Background Development

For development, use background mode to keep the app running while you work:

```bash
# Start in background
python build.py start

# Check status
python build.py status

# View logs
python build.py log

# Stop when done
python build.py stop
```

### Hot Reload Development

For immediate feedback on changes:

```bash
python build.py watch
```

### Production Build

Create an optimized production build with prerendering:

```bash
python build.py publish
```

The output will be in `dist/wwwroot/`. To serve locally:

```bash
dotnet tool install -g dotnet-serve
cd dist/wwwroot && dotnet serve -p 8080
```

## Direct .NET CLI Usage

If you prefer using the .NET CLI directly:

```bash
# Build
dotnet build Flowbite.Wasm.csproj

# Run
dotnet run --project Flowbite.Wasm.csproj

# Watch
dotnet watch --project Flowbite.Wasm.csproj

# Publish
dotnet publish Flowbite.Wasm.csproj -c Release -o dist
```

**Note:** Direct CLI usage requires manually downloading Tailwind CSS first. Use `build.py` for automatic setup.

## Tailwind CSS

The project uses Tailwind CSS v4.1.8 with the CSS-first configuration approach. The `build.py` script automatically downloads the Tailwind executable on first run.

CSS files:
- Input: `wwwroot/css/app.css`
- Output: `wwwroot/css/app.min.css`

## Technologies

- .NET 9 / Blazor WebAssembly
- Flowbite Blazor components
- Tailwind CSS v4.1.8
- ApexCharts (Blazor-ApexCharts)
- BlazorWasmPreRendering.Build

## License

MIT
