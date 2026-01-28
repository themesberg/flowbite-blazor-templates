namespace Flowbite.Maui.Domain.Dashboard;

public sealed record ProductStatistic(
  string Name,
  string ImageUrl,
  decimal Revenue,
  decimal ChangePercent);
