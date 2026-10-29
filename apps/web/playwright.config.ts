import { defineConfig, devices } from "@playwright/test";

/**
 * E2E against a production build. Expects the API on :8000 (pointed at the mock auth server);
 * starts the mock auth (:54399) and `next start` (:3000) itself. See .github/workflows/e2e.yml.
 */
export default defineConfig({
  testDir: "e2e",
  timeout: 60_000,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["github"], ["html", { open: "never" }]] : "list",
  use: {
    baseURL: "http://localhost:3000",
    locale: "pt-BR",
    timezoneId: "America/Sao_Paulo",
    trace: "retain-on-failure",
  },
  projects: [
    { name: "iphone", use: { ...devices["iPhone 14"], browserName: "chromium" } },
    { name: "desktop", use: { viewport: { width: 1440, height: 900 } } },
  ],
  webServer: [
    {
      command: "node e2e/mock-auth.mjs 54399",
      url: "http://127.0.0.1:54399/auth/v1/.well-known/jwks.json",
      reuseExistingServer: true,
    },
    {
      command: "pnpm start --port 3000",
      url: "http://localhost:3000",
      reuseExistingServer: true,
      timeout: 120_000,
    },
  ],
});
