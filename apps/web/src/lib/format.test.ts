import { describe, expect, it } from "vitest";
import { formatMoney, parseMoney } from "./format";

const nbsp = (s: string) => s.replace(/ /g, " ");

describe("parseMoney", () => {
  it.each([
    ["45,90", 4590],
    ["45.90", 4590],
    ["1.234,56", 123456],
    ["1,234.56", 123456],
    ["R$ 10", 1000],
    ["10", 1000],
    ["0,5", 50],
    ["1.000", 100000],
  ])("%s -> %i", (input, cents) => {
    expect(parseMoney(input)).toBe(cents);
  });

  it("returns null for non-numbers", () => {
    expect(parseMoney("abc")).toBeNull();
    expect(parseMoney("")).toBeNull();
  });
});

describe("formatMoney", () => {
  it("formats BRL", () => {
    expect(nbsp(formatMoney(123456))).toBe("R$ 1.234,56");
  });
  it("uses a real minus sign for negatives and optional plus", () => {
    expect(nbsp(formatMoney(-500))).toBe("−R$ 5,00");
    expect(nbsp(formatMoney(500, { sign: true }))).toBe("+R$ 5,00");
  });
});
