> **IMPORTANT!!**
> Just as with the standard Blazor Web App template, Blazor will use SSR by default. If you want to have interactive components, make sure you add a rendermode to the app, page or component!

## Installation

Install the templates by running the command:

~~~sh
dotnet new install Flowbite.Blazor.Templates
~~~

## Usage

After installing the templates you can create new a project from either the CLI or by creating a new project in Visual Studio Code or VS2022.

- For creating a Flowbite Blazor WebAssembly Standalone App project from the CLI:

    ~~~sh
    dotnet new flowbite-blazor-wasm -o {your project name}
    # Open the project README.md to complete the setup and run the app
    ~~~

- For creating a Flowbite Blazor WebAssembly Standalone App project from the CLI:

    ~~~sh
    dotnet new flowbite-blazor-desktop -o {your project name}
    # Open the project README.md to complete the setup and run the app
    ~~~

## Uninstalling the templates

If you want to uninstall the templates, both from the CLI and Visual Studio 2022,  run the following command:

~~~sh
dotnet new uninstall Flowbite.Blazor.Templates
~~~

## Support

The Flowbite Blazor library is an open source project. It is built and maintained by PeakFlames maintainers (**and** other contributors)
and offers support, like most other open source projects, on a best effort base through the GitHub repository **only**.


## Development

To insall the templates locally, run the following command:

~~~sh
./publish-local.ps1
~~~

Then use the tempaltes as you would normally.
