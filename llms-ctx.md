# Flowbite Blazor WASM .NET Template Documenation

## Overview

This .NET Template is based off of the .NET 8.0 Blazor WASM Standalonde template but has been
enhanced as follows:
- Use the tailwindcss-based Flowbite Blazor UI library for all of its Layout, Componets, and Icons
- Executes the tailwind standalone executable process the tailwind configuration
- When publishing, the BlazorWasmPreRendering.Build is used to generate the static HTML for the side to be

To quickly scaffold a new project using the using the CLI. The following project types include:


### Scaffold a Blazor WebAssembly Standalone App

- __For Window Platform:__

    ```powershell
    dotnet new install Flowbite.Blazor.Templates
    dotnet new flowbite-blazor-wasm -o {{PROJECT_NAME}};
    cd {{PROJECT_NAME}}
    mkdir .\tools -Force
    cd .\tools
    Invoke-WebRequest -Uri https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe -OutFile tailwindcss.exe -UseBasicParsing
    cd ..
    dotnet build
    ```

- __For Mac OSX Arm64:__

    ```zsh
    dotnet new install Flowbite.Blazor.Templates
    dotnet new flowbite-blazor-wasm -o {{PROJECT_NAME}};
    cd {{PROJECT_NAME}}
    mkdir ./tools
    cd ./tools
    curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64
    chmod +x tailwindcss-macos-arm64 
    mv tailwindcss-macos-arm64 tailwindcss
    cd ..
    dotnet build
    ```

## Project Structure

{{PROJECT_NAME}}
├── App.razor
├── Components
│   └── AppVersion.razor
├── Layout
│   ├── AppFooter.razor
│   ├── AppNavBar.razor
│   ├── AppSidebar.razor
│   └── MainLayout.razor
├── {{PROJECT_NAME}}.csproj
├── {{PROJECT_NAME}}.sln
├── Pages
│   ├── Counter.razor
│   ├── Home.razor
│   ├── Icons.razor
│   └── Weather.razor
├── Program.cs
├── Properties
│   └── launchSettings.json
├── README.md
├── _Imports.razor
├── postcss.config.js
├── tailwind.config.js
└── wwwroot
    ├── css
    │   ├── app.css
    │   └── app.min.css
    ├── favicon.png
    ├── index.html
    ├── js
    │   └── app.js
    └── sample-data
        └── weather.json

## Important File Contents

### {{PROJECT_NAME}}.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk.BlazorWebAssembly">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <InvariantGlobalization>true</InvariantGlobalization>
    <BlazorEnableTimeZoneSupport>false</BlazorEnableTimeZoneSupport>
    <PostCSSConfig>postcss.config.js</PostCSSConfig>
    <TailwindConfig>tailwind.config.js</TailwindConfig>
    <Version>0.0.1-alpha.1</Version>
  </PropertyGroup>

  <PropertyGroup>
    <BlazorWasmPrerenderingDeleteLoadingContents>true</BlazorWasmPrerenderingDeleteLoadingContents>
  </PropertyGroup>

  <ItemGroup>

    <PackageReference Include="Microsoft.AspNetCore.Components.WebAssembly" Version="8.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Components.WebAssembly.DevServer" Version="8.0.0" PrivateAssets="all" />
    <PackageReference Include="Flowbite" Version="0.0.*-*" />
    <PackageReference Include="BlazorWasmPreRendering.Build" Version="5.0.0" />
  </ItemGroup>

  <Target Name="Tailwind" BeforeTargets="Build" Condition="'$(OS)' == 'Windows_NT'">
    <Exec Command=".\tools\tailwindcss.exe -i ./wwwroot/css/app.css -o ./wwwroot/css/app.min.css" />
  </Target>

  <Target Name="DisableTailwindOnPublish" BeforeTargets="Publish">
    <PropertyGroup>
      <DisableTailwind>true</DisableTailwind>
    </PropertyGroup>
  </Target>

  <ItemGroup>
    <UpToDateCheckBuilt Include="wwwroot/css/app.css" Set="Css" />
    <UpToDateCheckBuilt Include="wwwroot/css/app.min.css" Set="Css" />
    <UpToDateCheckBuilt Include="tailwind.config.js" Set="Css" />
  </ItemGroup>


  <ItemGroup>
    <None Remove="wwwroot\css\app.css" />
    <None Remove="wwwroot\css\app.min.css" />
    <None Remove="tools\tailwindcss.exe" />
  </ItemGroup>

</Project>
```

### Program.cs

```csharp
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using PROJECT_NAME;
using Flowbite.Services;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

// Required for prerendering (BlazorWasmPreRendering.Build)
ConfigureServices(builder.Services, builder.HostEnvironment.BaseAddress);

await builder.Build().RunAsync();

// Required for prerendering (BlazorWasmPreRendering.Build)
// extract the service-registration process to the static local function.
static void ConfigureServices(IServiceCollection services, string baseAddress)
{
  services.AddScoped(sp => new HttpClient { BaseAddress = new Uri(baseAddress) });
  services.AddFlowbite();
}
```

### wwwroot/index.html

```html
<!DOCTYPE html>
<html lang="en" class="dark">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>PROJECT_NAME</title>
    <base href="/" />
    <link rel="stylesheet" href="css/app.min.css" />
    <link rel="stylesheet" href="_content/Flowbite/flowbite.min.css" />
    <link rel="icon" type="image/png" sizes="32x32" href="favicon.png">

    <script>

        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark')
        }

    </script>

</head>

<body class="dark:bg-gray-900 antialiased">

    <div id="app">
        <svg class="loading-progress">
            <circle r="40%" cx="50%" cy="50%" />
            <circle r="40%" cx="50%" cy="50%" />
        </svg>
        <div class="loading-progress-text">Loading...</div>
    </div>

    <div id="blazor-error-ui">
        An unhandled error has occurred.
        <a href="." class="reload">Reload</a>
        <span class="dismiss">🗙</span>
    </div>
    <script src="_framework/blazor.webassembly.js"></script>
    <script src="/js/app.js"></script>
    <script src="_content/Flowbite/flowbite.js"></script>
    <script src="_content/Flowbite/prism.js"></script>
</body>

</html>
```

### App.razor

```razor
<Router AppAssembly="@typeof(App).Assembly">
    <Found Context="routeData">
        <RouteView RouteData="@routeData" DefaultLayout="@typeof(MainLayout)" />
    </Found>
    <NotFound>
        <PageTitle>Not found</PageTitle>
        <LayoutView Layout="@typeof(MainLayout)">
            <p role="alert" class="p-4 border rounded-lg bg-red-300 text-red-900 dark:bg-red-700 dark:text-red-100">Sorry, there's nothing at this address. This page is likely yet to be implemented</p>
        </LayoutView>
    </NotFound>
</Router>
```

### _Imports.razor

```razor
@using System.Net.Http
@using System.Net.Http.Json
@using Microsoft.AspNetCore.Components.Forms
@using Microsoft.AspNetCore.Components.Routing
@using Microsoft.AspNetCore.Components.Sections
@using Microsoft.AspNetCore.Components.Web
@using Microsoft.AspNetCore.Components.Web.Virtualization
@using Microsoft.AspNetCore.Components.WebAssembly.Http
@using Microsoft.JSInterop
@using Flowbite.Base
@using Flowbite.Components
@using Flowbite.Components.Tabs
@using Flowbite.Components.Table
@using Flowbite.Icons
@using Flowbite.Services
@using static Flowbite.Components.Button
@using static Flowbite.Components.Tooltip
@using static Flowbite.Components.Avatar
@using static Flowbite.Components.Sidebar
@using static Flowbite.Components.SidebarCTA
@using static Flowbite.Components.Dropdown
@using PROJECT_NAME
@using PROJECT_NAME.Layout
@using PROJECT_NAME.Components
```

### tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "App.razor",
        "./wwwroot/**/*.{razor,html,cshtml,cs}",
        "./Layout/**/*.{razor,html,cshtml,cs}",
        "./Pages/**/*.{razor,html,cshtml,cs}",
        "./Components/**/*.{razor,html,cshtml,cs}"
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: { "50": "#eff6ff", "100": "#dbeafe", "200": "#bfdbfe", "300": "#93c5fd", "400": "#60a5fa", "500": "#3b82f6", "600": "#2563eb", "700": "#1d4ed8", "800": "#1e40af", "900": "#1e3a8a", "950": "#172554" }
            },
            maxHeight: {
                'table-xl': '60rem',
            }
        },
        fontFamily: {
            'body': [
                ... font names ...
            ],
            'sans': [
                ... font names ...
            ],
            'mono': [
                ... font names ...
            ]
        }
    }
}
```

### Layout/AppNavBar.razor

```razor
@inherits FlowbiteComponentBase

<!-- Header (begin) -->
<header class="z-40 w-full mx-auto bg-gray-50 border-b border-gray-200 dark:border-gray-600 dark:bg-gray-800">
    <div class="px-2 py-2.5 flex flex-wrap justify-between items-center" >

        <!-- Left-Side Component Group -->
        <div class="flex justify-start items-center">

            @if (ResponsiveMenuEnabled)
            {
                <button id="responsive-menu-toggle"
                    @onclick="OnResponsiveMenuToggle"
                    class="p-2 text-gray-600 rounded-lg cursor-pointer lg:hidden hover:text-gray-900 hover:bg-gray-100 focus:bg-gray-100 dark:focus:bg-gray-700 focus:ring-2 focus:ring-gray-100 dark:focus:ring-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">

                    @* Hamburger Icon *@
                    <svg id="hamburger-icon" aria-hidden="true" class="w-6 h-6 @(IsOpen ? "hidden" : "")" fill="currentColor" viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd"
                            d="M3 5a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM3 10a1 1 0 011-1h6a1 1 0 110 2H4a1 1 0 01-1-1zM3 15a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z"
                            clip-rule="evenodd"></path>
                    </svg>

                    @* Close Icon *@
                    <svg id="close-icon" aria-hidden="true" class="w-6 h-6 @(IsOpen ? "" : "hidden")" fill="currentColor" viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd"
                            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                            clip-rule="evenodd"></path>
                    </svg>
                    <span class="sr-only">Toggle sidebar</span>
                </button>
            }

            <NavbarBrand Href="/">
                <img src="/favicon.png" class="mr-3 h-6 sm:h-9" alt="PROJECT_NAME Logo" />
                <span class="self-center text-xl font-semibold whitespace-nowrap dark:text-white">PROJECT_NAME</span>
            </NavbarBrand>

        </div>

        <DarkMode/>

    </div>
</header>


@code
{
    /// <summary>
    /// Boolean parameter to determine if the header shows the collapsible menu
    /// </summary>
    [Parameter]
    public bool ResponsiveMenuEnabled { get; set; } = true;

    /// <summary>
    /// Event callback that fires when the responsive menu toggle button is clicked
    /// </summary>
    [Parameter]
    public EventCallback OnResponsiveMenuToggle { get; set; }

    /// <summary>
    /// Boolean parameter to determine if the responsive menu is open
    /// </summary>
    [Parameter]
    public bool IsOpen { get; set; }
}
```

### Layout/AppSidebar.razor

```razor
@using Microsoft.AspNetCore.Components.Routing

<div id="da-sidebar-outlet" class="h-full">
    <Sidebar class="h-full">

        <SidebarItem
            Href="/"
            Icon="@(new HomeIcon())">
            Home
        </SidebarItem>
        <SidebarItem
            Href="/counter"
            Icon="@(new PlusIcon())">
            Counter
        </SidebarItem>
        <SidebarItem
            Href="/weather"
            Icon="@(new InfoCircleIcon())">
            Weather
        </SidebarItem>
        <SidebarItem
            Href="/icons"
            Icon="@(new StarIcon())">
            Icons
        </SidebarItem>
    </Sidebar>
</div>
```

### Layout/MainLayout.razor

```razor
@inherits LayoutComponentBase
@inject IJSRuntime JSRuntime

<div class="antialiased h-screen flex flex-col bg-gray-50 dark:bg-gray-900">

    <AppNavBar ResponsiveMenuEnabled=@true OnResponsiveMenuToggle="HandleMenuToggle" IsOpen="_isSidebarOpen" />

    <div class="flex flex-col justify-between flex-auto overflow-y-auto">

        <section class="flex-auto flex overflow-y-auto">

            <aside id="fb-sidebar"
                   class="z-40 h-full min-w-max fixed lg:relative overflow-auto transition-transform left-0 @(_isSidebarOpen ? "" : "-translate-x-full") bg-white border-r border-gray-300 lg:translate-x-0 dark:bg-gray-800 dark:border-gray-700"
                   aria-label="sidenav" >

                <AppSidebar />

            </aside>

            <main class="p-4  overflow-auto w-full">
                @Body
            </main>

        </section>

        <AppFooter/>

    </div>

</div>

<div id="blazor-error-ui">
    An unhandled error has occurred.
    <a href="" class="reload">Reload</a>
    <a class="dismiss">🗙</a>
</div>

@code {
    private bool _isSidebarOpen = false;

    private void HandleMenuToggle()
    {
        _isSidebarOpen = !_isSidebarOpen;
    }
}

```

### Layout/AppFooter.razor

```razor
```
