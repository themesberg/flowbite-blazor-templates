using System.Collections.Generic;

namespace Flowbite.Maui.Domain.Dashboard;

public sealed record ChartSeriesDefinition<TPoint>(string Name, IReadOnlyList<TPoint> Points, string? Color = null)
  where TPoint : class;
