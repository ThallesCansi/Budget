import { describe, expect, it } from "vitest";
import { applyKey } from "./money-keypad";

describe("applyKey", () => {
  it("types cents right-to-left like banking apps", () => {
    const typed = ["1", "2", "3", "4"].reduce(applyKey, 0);
    expect(typed).toBe(1234); // R$ 12,34
  });
  it("supports 00 and backspace", () => {
    expect(applyKey(5, "00")).toBe(500);
    expect(applyKey(1234, "back")).toBe(123);
    expect(applyKey(0, "back")).toBe(0);
  });
  it("ignores input beyond the maximum", () => {
    expect(applyKey(99_999_999_99, "9")).toBe(99_999_999_99);
  });
});
