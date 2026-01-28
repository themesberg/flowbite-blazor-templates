using System.Collections.Generic;

namespace Flowbite.Wasm.Domain.Dashboard;

public sealed record ChartSeriesDefinition<TPoint>(string Name, IReadOnlyList<TPoint> Points, string? Color = null)
  where TPoint : class;
