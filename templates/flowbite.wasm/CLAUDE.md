# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flowbite Blazor WASM Admin Dashboard is a free and open-source UI admin dashboard template built with:
- **Blazor WebAssembly** (.NET 9.0)
- **Flowbite Blazor** component library (beta versions)
- **Tailwind CSS v4.1.8** for styling
- **BlazorWasmPreRendering.Build** for static prerendering
- **ApexCharts** for data visualization

## Build Commands

The project uses a Python build script (`build.py`) that automates all build tasks and dependency management.

### Prerequisites

The build script requires Python 3 and the `psutil` package:

```bash
# Install psutil (one-time setup)
pip install psutil
```

**IMPORTANT:** Always use `python` (not `python3`) to run build commands. The project assumes `python` is aliased to Python 3.

### Primary Commands

```bash
# Build the project (default)
python build.py
python build.py build

# Run the application (http://localhost:5269/)
python build.py run

# Development with hot reload
python build.py watch

# Create production build (outputs to ./dist)
python build.py publish
```

### Background Process Management

Run the application in the background while you work:

```bash
# Start WebApp in background (builds first, then runs on port 5269)
python build.py start

# Check if WebApp is running
python build.py status

# Stop background WebApp
python build.py stop
```

Background mode features:
- Automatically builds the solution before starting
- Runs Tailwind CSS compilation
- Logs all output to `webapp.log`
- Process ID stored in `.webapp.pid`
- Auto-stops running app before new builds to prevent file locks

### Log Management

View and search application logs from background runs:

```bash
# Show last 50 lines of log (default)
python build.py log

# Search log for specific pattern (case-insensitive regex)
python build.py log error
python build.py log "exception|error"

# Show last N lines
python build.py log --tail 100

# Filter by log level (error, warn, info, debug)
python build.py log --level error
python build.py log --level warn

# Combine filters
python build.py log --tail 200 --level info
```

### Test Commands

```bash
# Run unit tests (not yet configured)
python build.py test

# Run integration tests (not yet configured)
python build.py test-integration

# Test pre-rendering (catches binding errors before deployment)
python build.py test-publish

# Run all tests
python build.py test-all
```

**Note**: Unit and integration tests are not yet implemented. The `test-publish` command is useful for validating that all pages pre-render correctly without errors.

### Direct .NET CLI Commands

If you need to use .NET CLI directly:

```bash
# Build
dotnet build Flowbite.Wasm.csproj

# Run
dotnet run --project Flowbite.Wasm.csproj

# Watch (hot reload)
dotnet watch --project Flowbite.Wasm.csproj

# Publish
dotnet publish Flowbite.Wasm.csproj -c Release -o dist
```

### Serving Static Build Locally

```bash
# Install dotnet-serve (one-time setup)
dotnet tool install --global dotnet-serve

# Build and serve
python build.py publish
dotnet serve -d dist/wwwroot -p 8080
```

## Tailwind CSS Version Management

The project uses **Tailwind CSS v4.1.8** with the CSS-first configuration approach.

### Key Points

- Tailwind CSS executable stored at `tools/tailwindcss`
- Uses v4 syntax in `app.css`: `@import "tailwindcss"`, `@config`, `@source`
- Do not change Tailwind versions without explicit user request
- MSBuild target handles CSS compilation automatically
- Ensure `wwwroot/css/app.min.css` is committed when styles change

## Architecture

### Project Structure

```
Flowbite.Wasm/
├── Components/         # Reusable Razor components
├── Domain/            # Domain models and data types
├── Layout/            # Layout components (MainLayout, AppNavBar, AppSidebar, etc.)
│   ├── MainLayout.razor       # Sidebar layout (responsive)
│   ├── StackedLayout.razor    # Stacked navbar layout
│   ├── MarketingLayout.razor  # Marketing/landing page layout
│   └── LayoutBase.razor       # Base class with mobile menu state
├── Pages/             # Routable page components (@page directive)
├── Services/          # Service classes (ThemeService, SettingsService, etc.)
├── Charts/            # ApexCharts configuration and data
├── wwwroot/           # Static assets (CSS, JS, images, sample data)
├── tools/             # Tailwind CSS executable (DO NOT MODIFY)
├── Program.cs         # Application entry point
├── App.razor          # Root component
├── _Imports.razor     # Global using statements
├── tailwind.config.js # Tailwind CSS configuration
└── Flowbite.Wasm.csproj      # Project file with MSBuild targets
```

### Key Architecture Patterns

**Blazor WebAssembly Application**:
- Single-page application running entirely in the browser
- Uses prerendering for improved initial load performance (BlazorWasmPreRendering.Build v6.0.0)
- No backend server required after initial load

**Layout System**:
- Multiple layout options: `MainLayout.razor` (sidebar), `StackedLayout.razor` (stacked navbar), `MarketingLayout.razor`
- All layouts inherit from `LayoutBase.razor` which manages mobile menu state
- Sidebar toggle controlled via `IsMobileMenuOpen` state in LayoutBase
- Responsive sidebar implementation:
  - Mobile: Slides in/out with backdrop overlay (`-translate-x-full` when closed)
  - Desktop: Always visible at `lg:` breakpoint (`lg:translate-x-0`, `lg:relative`)
- Three main layout components: `AppNavBar`, `AppSidebar`, `AppFooter`
- Layout uses Tailwind utility classes with dark mode support (`dark:` prefix)

**Dependency Injection**:
- Services registered in `Program.cs` via static `ConfigureServices()` function
- Static function required for BlazorWasmPreRendering compatibility
- Flowbite services added via `AddFlowbite()` extension method
- ApexCharts configured via `AddApexCharts()` with global options
- HTTP client configured with base address for API calls
- Example services: `ThemeService`, `SettingsService`, `PricingService`

**Component Library Integration**:
- Uses Flowbite Blazor components (beta)
- Flowbite.ExtendedIcons for icon library (alpha)
- QuickGrid for table/grid functionality
- Blazor-ApexCharts for charts (v6.0.2)
- Import structure defined in `_Imports.razor`

### Tailwind CSS Integration

**Build Process**:
- Tailwind CSS executable stored in `tools/`
- Automatically downloaded by `build.py` for the target OS
- MSBuild target `TailwindBuild` runs before each build
- Input: `wwwroot/css/app.css` → Output: `wwwroot/css/app.min.css`
- Tailwind disabled during publish to avoid conflicts (`DisableTailwindOnPublish` target)
- CSS output file (`app.min.css`) should be committed to git when it changes

**Configuration**:
- Content paths scan all Razor, HTML, and C# files in Components, Layout, and Pages
- Dark mode enabled via `class` strategy (toggled on root element)
- Safelist includes responsive classes that Tailwind might miss (`md:*`, carousel heights, etc.)
- Responsive breakpoints heavily utilized (especially `md:` and `lg:` prefixes)

### Routing and Pages

- Standard Blazor routing via `@page` directives
- Pages located in `Pages/`
- Example pages: Dashboard, Settings, Pricing, Grid, Icons, Playground (Sidebar/Stacked)
- Navigation structure defined in `AppSidebar.razor`
- Layout selection via `@layout` directive on pages

### Static Asset Management

- Assets served from `wwwroot/`
- CSS files compiled to `wwwroot/css/app.min.css`
- JavaScript interop files in `wwwroot/js/`
- Sample data in `wwwroot/sample-data/`

## Important Build Details

**Automatic Dependency Management**:
- `build.py` checks for .NET SDK 9.0+ and installs locally if missing
- Tailwind CSS executable (v4.1.8) downloaded automatically for the target OS
- Cross-platform support: Windows, Linux, macOS

**Project Configuration**:
- Uses InvariantGlobalization for smaller bundle size
- BlazorEnableTimeZoneSupport disabled for reduced size
- Nullable reference types enabled
- Implicit usings enabled

**Prerendering**:
- BlazorWasmPreRendering.Build v6.0.0 enables static prerendering
- `ConfigureServices()` must be static for prerendering compatibility
- `BlazorWasmPrerenderingDeleteLoadingContents` removes loading UI after render

## Dependencies

Core packages (defined in `Flowbite.Wasm.csproj`):
- `Microsoft.AspNetCore.Components.WebAssembly` 9.0.0
- `Microsoft.AspNetCore.Components.QuickGrid` 9.0.0
- `Flowbite` [0.2.0-beta,)
- `BlazorWasmPreRendering.Build` 6.0.0
- `Blazor-ApexCharts` 6.0.2

Tailwind CSS v4.1.8 (standalone executable, not npm)

## Common Patterns

**Adding a New Page**:
1. Create `.razor` file in `Pages/`
2. Add `@page "/route"` directive
3. Optionally specify layout: `@layout MainLayout` (sidebar) or `@layout StackedLayout` (stacked navbar)
4. Update `AppSidebar.razor` if navigation link needed
5. Ensure Tailwind classes are used for styling

**Adding a New Service**:
1. Create service class in `Services/`
2. Register in `Program.cs` ConfigureServices function:
   ```csharp
   services.AddScoped<YourService>();
   ```
3. Inject into components via `@inject` directive:
   ```razor
   @inject YourService Service
   ```

**Working with Tailwind**:
- Run `python build.py watch` for automatic CSS rebuilding
- Add new content paths to `tailwind.config.js` if needed
- Use safelist for dynamic classes that Tailwind might not detect
- Prefer Tailwind utility classes over custom CSS
- Commit `app.min.css` when styles change

**Dark Mode Support**:
- Use `dark:` prefix for dark mode variants (e.g., `dark:bg-gray-900`)
- Dark mode toggled via `class` on root element (managed by ThemeService)
- Layout already configured for dark mode styling

**Component Composition**:
- Use `[Parameter]` attribute for component props
- Use `RenderFragment` for child content slots:
  ```csharp
  [Parameter]
  public RenderFragment? ChildContent { get; set; }
  ```
- Use `EventCallback` for component events:
  ```csharp
  [Parameter]
  public EventCallback<bool> OnToggle { get; set; }
  ```

## Development Conventions

**Code Style**:
- Follow `.editorconfig`: 4-space indentation for C#, 2-space for Razor, file-scoped namespaces
- Use PascalCase for public APIs, `_camelCase` for private fields
- Keep C# logic in `.razor.cs` files via partial classes
- Parameters are public properties with `[Parameter]` attribute
- Document all public APIs with XML comments

**Component Patterns**:
- Use `[CaptureUnmatchedValues]` for additional HTML attributes
- Use `RenderFragment? ChildContent` for slots
- Prefer enums for style variations
- Always apply `@key` when looping components with `@foreach`
- Use Tailwind utility classes exclusively
- Ensure dark mode coverage with `dark:` variants
- Accept a `Class` parameter for custom styling
- Only use icons from `Flowbite.Icons` or `Flowbite.ExtendedIcons`

**Library Discipline (CRITICAL)**:
- **YOU MUST USE Flowbite Blazor components** when they exist
- **Do not** build custom components (modals, dropdowns, buttons) from scratch if the library provides them
- **Do not** pollute the codebase with redundant custom CSS
- Exception: You may wrap or style library components, but the underlying primitive must come from the library

## CSS Commits

**CRITICAL:** When Tailwind classes change, the generated CSS MUST be committed:

```bash
git add wwwroot/css/app.min.css
git commit -m "style: update Tailwind CSS output"
```

**Why this matters:**
- `app.min.css` is generated by `tailwindcss.exe` during build
- When you add new Tailwind classes, this file changes
- Failing to commit it means styles won't work in production
- The file MUST be committed for deployment to work correctly

## Design Guidelines

**It is ULTRA IMPORTANT to adhere to the Flowbite Design Style System as it is Mobile first and good looking.**

When implementing components:
- Follow Flowbite's mobile-first responsive design patterns
- Use Flowbite Blazor components when available
- Ensure proper responsive behavior across breakpoints (mobile → tablet → desktop)
