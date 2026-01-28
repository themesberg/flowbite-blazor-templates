namespace Flowbite.Maui;

public partial class App : Application
{
    public App()
    {
        InitializeComponent();
    }

    protected override Window CreateWindow(IActivationState? activationState)
    {
        return new Window(new MainPage())
        {
            Title = "Flowbite Dashboard",
            Width = 1280,
            Height = 800,
            MinimumWidth = 800,
            MinimumHeight = 600
        };
    }
}
