using System;
using System.Net.Http;
using Microsoft.Extensions.DependencyInjection;
using Photino.Blazor;
using Flowbite.Desktop;

class Program
{
    [STAThread]
    static void Main(string[] args)
    {
        var appBuilder = PhotinoBlazorAppBuilder.CreateDefault(args);

        appBuilder.Services.AddLogging();

        // register root component and selector
        appBuilder.RootComponents.Add<Flowbite.Desktop.App>("app");

        var app = appBuilder.Build();

        // customize window
        app.MainWindow
            .SetIconFile("favicon.ico")
            .SetHeight(1080)
            .SetWidth(1920)
            .SetTitle("Flowbite Blazor Desktop");

        AppDomain.CurrentDomain.UnhandledException += (sender, error) =>
        {
            app.MainWindow.ShowMessage("Fatal exception", error.ExceptionObject.ToString());
        };

        app.Run();
    }
}
