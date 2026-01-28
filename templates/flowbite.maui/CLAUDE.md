# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flowbite Blazor MAUI Admin Dashboard is a free and open-source desktop admin dashboard template built with:
- **.NET MAUI Blazor Hybrid** (.NET 10.0)
- **Flowbite Blazor** component library (beta versions)
- **Tailwind CSS v4.1.8** for styling
- **ApexCharts** for data visualization

Supported Platforms:
- **Windows** (Windows 10 version 17763.0 or higher)
- **macOS** (Mac Catalyst 15.0 or higher)

## Build Commands

The project uses a Python build script (`build.py`) that automates all build tasks and dependency management.

### Prerequisites

- Python 3
- .NET 10 SDK

### Primary Commands

```bash
# Build the project (default)
python build.py
python build.py build

# Run the application
python build.py run

# Create production build (outputs to ./dist)
python build.py publish

# Clean build artifacts
python build.py clean
```

### Direct .NET CLI Commands

If you need to use .NET CLI directly:

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

## Tailwind CSS

The project uses **Tailwind CSS v4.1.8** with the CSS-first configuration approach.

### Key Points

- Tailwind CSS executable stored at `tools/tailwindcss`
- Uses v4 syntax in `app.css`: `@import "tailwindcss"`, `@config`, `@source`
- MSBuild target handles CSS compilation automatically
- Ensure `wwwroot/css/app.min.css` is committed when styles change

## Architecture

### Project Structure

```
Flowbite.Maui/
├── Components/         # Blazor components (Routes.razor, _Imports.razor, Dashboard/, etc.)
├── Domain/            # Domain models and data types
├── Layout/            # Layout components (MainLayout, AppNavBar, AppSidebar, etc.)
├── Pages/             # Routable page components (@page directive)
├── Services/          # Service classes (ThemeService, SettingsService, etc.)
├── Charts/            # ApexCharts configuration and data
├── Platforms/         # Platform-specific code
│   ├── MacCatalyst/   # macOS-specific files
│   └── Windows/       # Windows-specific files
├── Resources/         # App resources (icons, splash, fonts)
├── wwwroot/           # Static assets (CSS, JS, images, sample data)
├── tools/             # Tailwind CSS executable (DO NOT MODIFY)
├── App.xaml           # MAUI Application definition
├── App.xaml.cs        # MAUI Application code-behind
├── MainPage.xaml      # BlazorWebView host page
├── MainPage.xaml.cs   # MainPage code-behind
├── MauiProgram.cs     # Application entry point and DI configuration
├── tailwind.config.js # Tailwind CSS configuration
└── Flowbite.Maui.csproj # Project file
```

### Key Architecture Patterns

**.NET MAUI Blazor Hybrid Application**:
- Desktop application hosting Blazor components in a native WebView
- Uses BlazorWebView to render Blazor content
- Full access to device capabilities through MAUI APIs
- No server required - all code runs locally

**Entry Point**:
- `MauiProgram.cs` configures the MAUI app and services
- Services registered as Singletons (not Scoped like WASM)
- BlazorWebView added via `AddMauiBlazorWebView()`

**Layout System**:
- Multiple layout options: `MainLayout.razor` (sidebar), `StackedLayout.razor` (stacked navbar)
- Responsive design adapts to window size
- Dark mode support with `dark:` prefix

**Dependency Injection**:
- Services registered in `MauiProgram.cs`
- Flowbite services added via `AddFlowbite()` extension method
- ApexCharts configured via `AddApexCharts()` with global options
- Use `AddSingleton<T>()` for services (not Scoped)

**Component Library Integration**:
- Uses Flowbite Blazor components (beta)
- Flowbite.ExtendedIcons for icon library (alpha)
- Blazor-ApexCharts for charts (v6.0.2)
- Import structure defined in `Components/_Imports.razor`

### Routing and Pages

- Standard Blazor routing via `@page` directives
- Routes defined in `Components/Routes.razor`
- Pages located in `Pages/`
- Navigation structure defined in `Layout/AppSidebar.razor`

### Static Asset Management

- Assets served from `wwwroot/`
- CSS files compiled to `wwwroot/css/app.min.css`
- Host page at `wwwroot/index.html`

## Important Build Details

**Automatic Dependency Management**:
- `build.py` checks for .NET SDK 10.0+
- Tailwind CSS executable (v4.1.8) downloaded automatically for the target OS
- Cross-platform support: Windows, macOS

**Target Frameworks**:
- macOS: `net10.0-maccatalyst`
- Windows: `net10.0-windows10.0.19041.0`

**Project Configuration**:
- Uses MAUI SingleProject structure
- UseMaui enabled
- Nullable reference types enabled
- Implicit usings enabled

## Dependencies

Core packages (defined in `Flowbite.Maui.csproj`):
- `Microsoft.Maui.Controls`
- `Microsoft.AspNetCore.Components.WebView.Maui`
- `Flowbite` [0.2.0-beta,)
- `Flowbite.ExtendedIcons` [0.0.6-alpha,)
- `Blazor-ApexCharts` 6.0.2

Tailwind CSS v4.1.8 (standalone executable, not npm)

## Common Patterns

**Adding a New Page**:
1. Create `.razor` file in `Pages/`
2. Add `@page "/route"` directive
3. Optionally specify layout: `@layout MainLayout` (sidebar) or `@layout StackedLayout`
4. Update `Layout/AppSidebar.razor` if navigation link needed
5. Ensure Tailwind classes are used for styling

**Adding a New Service**:
1. Create service class in `Services/`
2. Register in `MauiProgram.cs`:
   ```csharp
   builder.Services.AddSingleton<YourService>();
   ```
3. Inject into components via `@inject` directive:
   ```razor
   @inject YourService Service
   ```

**Working with Tailwind**:
- Run `python build.py build` to compile CSS
- Add new content paths to `tailwind.config.js` if needed
- Use safelist for dynamic classes that Tailwind might not detect
- Prefer Tailwind utility classes over custom CSS
- Commit `app.min.css` when styles change

**Dark Mode Support**:
- Use `dark:` prefix for dark mode variants (e.g., `dark:bg-gray-900`)
- Dark mode toggled via `class` on root element (managed by ThemeService)
- Layout already configured for dark mode styling

## Development Conventions

**Code Style**:
- 4-space indentation for C#, 2-space for Razor
- Use PascalCase for public APIs, `_camelCase` for private fields
- Keep C# logic in `.razor.cs` files via partial classes
- Parameters are public properties with `[Parameter]` attribute

**Component Patterns**:
- Use `[CaptureUnmatchedValues]` for additional HTML attributes
- Use `RenderFragment? ChildContent` for slots
- Always apply `@key` when looping components with `@foreach`
- Use Tailwind utility classes exclusively
- Ensure dark mode coverage with `dark:` variants
- Only use icons from `Flowbite.Icons` or `Flowbite.ExtendedIcons`

**Library Discipline (CRITICAL)**:
- **YOU MUST USE Flowbite Blazor components** when they exist
- **Do not** build custom components from scratch if the library provides them
- **Do not** pollute the codebase with redundant custom CSS

## CSS Commits

**CRITICAL:** When Tailwind classes change, the generated CSS MUST be committed:

```bash
git add wwwroot/css/app.min.css
git commit -m "style: update Tailwind CSS output"
```

## Design Guidelines

**It is ULTRA IMPORTANT to adhere to the Flowbite Design Style System as it is Mobile first and good looking.**

When implementing components:
- Follow Flowbite's mobile-first responsive design patterns
- Use Flowbite Blazor components when available
- Ensure proper responsive behavior across window sizes

## MAUI-Specific Notes

**Service Lifetime**:
- Use `AddSingleton<T>()` for services in MAUI (not `AddScoped<T>()`)
- MAUI apps have a single instance, so Singleton is appropriate

**Window Configuration**:
- Window size configured in `App.xaml.cs` via `CreateWindow()`
- Default size: 1280x800, Minimum: 800x600

**Platform-Specific Code**:
- MacCatalyst code in `Platforms/MacCatalyst/`
- Windows code in `Platforms/Windows/`
- Use `#if MACCATALYST` or `#if WINDOWS` for conditional compilation
