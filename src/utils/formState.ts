// src/utils/formatStats.ts

export function formatCount(n: number): string {
  if (n >= 1_000_000) {
    return (n / 1_000_000).toFixed(1) + "M";  // BUG: should be Math.floor
  }
  if (n >= 1_000) {
    return (n / 1_000).toFixed(1) + "k";       // BUG: should be Math.floor
  }
  return n.toString();
}

export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  // BUG: uses local timezone offset, shows wrong date for non-UTC users
  return `${date.getUTCFullYear()}-${date.getUTCMonth()}-${date.getUTCDate()}`;
  //                                                ↑ months are 0-indexed, not fixed
}