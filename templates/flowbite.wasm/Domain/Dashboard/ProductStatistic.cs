namespace Flowbite.Wasm.Domain.Dashboard;

public sealed record ProductStatistic(
  string Name,
  string ImageUrl,
  decimal Revenue,
  decimal ChangePercent);
