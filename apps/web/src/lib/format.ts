import { format, isToday, isYesterday, parseISO } from "date-fns";
import { ptBR } from "date-fns/locale";

const brl = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
const brlCompact = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
  notation: "compact",
  maximumFractionDigits: 1,
});

export function formatMoney(cents: number, opts: { compact?: boolean; sign?: boolean } = {}) {
  const value = (opts.compact ? brlCompact : brl).format(Math.abs(cents) / 100);
  if (cents < 0) return `−${value}`;
  return opts.sign && cents > 0 ? `+${value}` : value;
}

/** "45,90" | "45.90" | "1.234,56" | "R$ 10" -> cents. Returns null when not a number. */
export function parseMoney(input: string): number | null {
  const cleaned = input.replace(/[^\d,.-]/g, "");
  if (!cleaned) return null;
  const lastSep = Math.max(cleaned.lastIndexOf(","), cleaned.lastIndexOf("."));
  const hasDecimals = lastSep >= 0 && cleaned.length - lastSep - 1 <= 2;
  const integer = hasDecimals ? cleaned.slice(0, lastSep) : cleaned;
  const decimals = hasDecimals ? cleaned.slice(lastSep + 1) : "";
  const digits = integer.replace(/[^\d]/g, "") + decimals.padEnd(2, "0");
  const cents = Number.parseInt(digits, 10);
  return Number.isFinite(cents) ? cents : null;
}

export const toISODate = (date: Date) => format(date, "yyyy-MM-dd");
export const monthKey = (date: Date) => format(date, "yyyy-MM");
export const fromISODate = (iso: string) => parseISO(iso);

export function formatMonth(date: Date) {
  const label = format(date, "MMMM 'de' yyyy", { locale: ptBR });
  return label.charAt(0).toUpperCase() + label.slice(1);
}

export function formatDayHeading(iso: string) {
  const date = parseISO(iso);
  if (isToday(date)) return "Hoje";
  if (isYesterday(date)) return "Ontem";
  const label = format(date, "EEEE, d 'de' MMMM", { locale: ptBR });
  return label.charAt(0).toUpperCase() + label.slice(1);
}

export function formatShortDate(iso: string) {
  return format(parseISO(iso), "dd/MM", { locale: ptBR });
}

export function greeting(now = new Date()) {
  const hour = now.getHours();
  if (hour >= 5 && hour < 12) return "Bom dia";
  if (hour >= 12 && hour < 18) return "Boa tarde";
  return "Boa noite";
}
