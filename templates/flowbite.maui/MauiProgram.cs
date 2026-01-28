using ApexCharts;
using Microsoft.Extensions.Logging;
using Flowbite.Maui.Charts;
using Flowbite.Maui.Services;
using Flowbite.Services;

namespace Flowbite.Maui;

public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        builder
            .UseMauiApp<App>()
            .ConfigureFonts(fonts =>
            {
                fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
            });

        builder.Services.AddMauiBlazorWebView();

#if DEBUG
        builder.Services.AddBlazorWebViewDeveloperTools();
#endif

        // Add Flowbite services
        builder.Services.AddFlowbite();

        // Add ApexCharts
        builder.Services.AddApexCharts(options =>
        {
            options.GlobalOptions = DashboardChartOptions.CreateGlobalDefaults(false);
        });

        // Add application services
        builder.Services.AddSingleton<ThemeService>();
        builder.Services.AddSingleton<SettingsService>();
        builder.Services.AddSingleton<PricingService>();

        return builder.Build();
    }
}
