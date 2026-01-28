using System;
using System.Threading.Tasks;
using Microsoft.JSInterop;

namespace Flowbite.Maui.Services;

public sealed class ThemeService : IAsyncDisposable
{
  private readonly IJSRuntime _jsRuntime;
  private IJSObjectReference? _module;
  private DotNetObjectReference<ThemeService>? _dotNetRef;
  private bool _isInitialized;
  private bool _isDarkMode = true; // Default to dark mode

  public ThemeService(IJSRuntime jsRuntime)
  {
    ArgumentNullException.ThrowIfNull(jsRuntime);
    _jsRuntime = jsRuntime;
  }

  public event Action<bool>? ThemeChanged;

  public bool IsDarkMode => _isDarkMode;

  public async Task<bool> InitializeAsync()
  {
    if (_isInitialized)
    {
      return _isDarkMode;
    }

    try
    {
      // Add delay for MAUI WebView initialization
      await Task.Delay(200);

      _module = await _jsRuntime.InvokeAsync<IJSObjectReference>("import", "./js/themeObserver.js");
      _dotNetRef ??= DotNetObjectReference.Create(this);
      _isDarkMode = await _module.InvokeAsync<bool>("start", _dotNetRef);
      _isInitialized = true;
    }
    catch (InvalidOperationException)
    {
      // WebView context not ready - use default dark mode
      _isDarkMode = true;
      _isInitialized = true;
    }
    catch (JSException)
    {
      // JS error - use default dark mode
      _isDarkMode = true;
      _isInitialized = true;
    }

    return _isDarkMode;
  }

  [JSInvokable(nameof(NotifyThemeChanged))]
  public Task NotifyThemeChanged(bool isDark)
  {
    if (_isDarkMode == isDark)
    {
      return Task.CompletedTask;
    }

    _isDarkMode = isDark;
    ThemeChanged?.Invoke(isDark);
    return Task.CompletedTask;
  }

  public async ValueTask DisposeAsync()
  {
    if (_isInitialized && _module is not null)
    {
      try
      {
        await _module.InvokeVoidAsync("stop");
      }
      catch
      {
        // ignored - shutdown
      }
    }

    _dotNetRef?.Dispose();
    _dotNetRef = null;
    _module = null;
    _isInitialized = false;
  }
}
