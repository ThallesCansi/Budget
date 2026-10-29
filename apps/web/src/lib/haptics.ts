/** Light haptic feedback where supported (Android). iOS Safari ignores the Vibration API. */
export function haptic(pattern: "tap" | "success" | "warning" = "tap") {
  if (typeof navigator === "undefined" || !("vibrate" in navigator)) return;
  const patterns: Record<typeof pattern, VibratePattern> = {
    tap: 8,
    success: [10, 40, 18],
    warning: [30, 50, 30],
  };
  navigator.vibrate(patterns[pattern]);
}
