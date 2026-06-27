// src/utils/formatStats.ts

export function formatCount(n: number): string {
  if (n >= 1_000_000) {
    return parseFloat((n / 1_000_000).toFixed(1)) + "M";
  }
  if (n >= 1_000) {
    return parseFloat((n / 1_000).toFixed(1)) + "k";
  }
  return n.toString();
}

export function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return `${date.getUTCFullYear()}-${date.getUTCMonth() + 1}-${date.getUTCDate()}`;
}
