#!/usr/bin/env node
// Full local stack without Docker or a Supabase project:
//   embedded Postgres (pgserver) + migrations, mock Supabase Auth, FastAPI and Next.js.
// Usage: pnpm dev:local          (next dev, hot reload)
//        pnpm dev:local --prod   (production build: service worker / PWA install enabled)
// Any e-mail + password signs in (the mock auth accepts everything). Ctrl+C stops everything.
import { execFileSync, spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("..", import.meta.url));
const api = `${root}apps/api`;
const web = `${root}apps/web`;
const prod = process.argv.includes("--prod");

const AUTH_URL = "http://127.0.0.1:54399";
const API_URL = "http://localhost:8000";
const WEB_URL = "http://localhost:3000";

const colors = { db: 90, auth: 35, api: 36, web: 32 };
const children = [];

function log(name, text) {
  for (const line of text.toString().split("\n")) {
    if (line.trim()) process.stdout.write(`\x1b[${colors[name]}m[${name}]\x1b[0m ${line}\n`);
  }
}

function start(name, cmd, args, opts) {
  const child = spawn(cmd, args, { ...opts, env: { ...process.env, ...opts.env } });
  child.stdout.on("data", (d) => log(name, d));
  child.stderr.on("data", (d) => log(name, d));
  child.on("exit", (code) => {
    log(name, `saiu (código ${code})`);
    shutdown(code ?? 1);
  });
  children.push(child);
}

let stopping = false;
function shutdown(code = 0) {
  if (stopping) return;
  stopping = true;
  for (const child of children) child.kill("SIGINT");
  setTimeout(() => process.exit(code), 500);
}
process.on("SIGINT", () => shutdown(0));
process.on("SIGTERM", () => shutdown(0));

log("db", "iniciando Postgres embutido…");
const databaseUrl = execFileSync("uv", ["run", "python", "scripts/devdb.py"], { cwd: api })
  .toString()
  .trim();
execFileSync("uv", ["run", "alembic", "upgrade", "head"], {
  cwd: api,
  env: { ...process.env, DATABASE_URL: databaseUrl },
  stdio: "ignore",
});
log("db", "migrations aplicadas");

const webEnv = {
  NEXT_PUBLIC_SUPABASE_URL: AUTH_URL,
  NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY: "mock-key",
  NEXT_PUBLIC_API_URL: API_URL,
  NEXT_PUBLIC_SITE_URL: WEB_URL,
  NEXT_TELEMETRY_DISABLED: "1",
};

start("auth", "node", ["e2e/mock-auth.mjs", "54399"], { cwd: web });
start(
  "api",
  "uv",
  ["run", "uvicorn", "app.main:app", "--port", "8000", ...(prod ? [] : ["--reload"])],
  {
    cwd: api,
    env: {
      DATABASE_URL: databaseUrl,
      SUPABASE_URL: AUTH_URL,
      CORS_ORIGINS: WEB_URL,
      ENVIRONMENT: "development",
    },
  },
);

if (prod) {
  log("web", "gerando build de produção…");
  execFileSync("pnpm", ["build"], {
    cwd: web,
    env: { ...process.env, ...webEnv },
    stdio: "ignore",
  });
  start("web", "pnpm", ["start", "--port", "3000"], { cwd: web, env: webEnv });
} else {
  start("web", "pnpm", ["dev"], { cwd: web, env: webEnv });
}

log("web", `abra ${WEB_URL} — entre com qualquer e-mail e senha (login simulado)`);
