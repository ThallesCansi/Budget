// Minimal Supabase Auth stand-in for local/CI end-to-end runs (no Docker needed).
// Implements password/refresh grants, sign-up, user and a real ES256 JWKS, so both the Next.js
// proxy (getClaims) and the API (PyJWT + JWKS) verify tokens exactly as in production.
//   node e2e/mock-auth.mjs [port]   ->  NEXT_PUBLIC_SUPABASE_URL / SUPABASE_URL = http://127.0.0.1:<port>
import { createHash, generateKeyPairSync, randomUUID, sign } from "node:crypto";
import { createServer } from "node:http";

const PORT = Number(process.argv[2] ?? 54399);
const BASE = `http://127.0.0.1:${PORT}`;
const KID = "mock-key-1";
const { privateKey, publicKey } = generateKeyPairSync("ec", { namedCurve: "P-256" });
const jwk = { ...publicKey.export({ format: "jwk" }), kid: KID, alg: "ES256", use: "sig" };

const users = new Map(); // email -> user
const refreshTokens = new Map(); // token -> email

const b64url = (input) => Buffer.from(input).toString("base64url");

function userFor(email, fullName) {
  if (!users.has(email)) {
    const hash = createHash("sha256").update(email).digest("hex");
    const id = `${hash.slice(0, 8)}-${hash.slice(8, 12)}-4${hash.slice(13, 16)}-a${hash.slice(17, 20)}-${hash.slice(20, 32)}`;
    users.set(email, {
      id,
      aud: "authenticated",
      role: "authenticated",
      email,
      email_confirmed_at: new Date().toISOString(),
      app_metadata: { provider: "email", providers: ["email"] },
      user_metadata: { full_name: fullName ?? email.split("@")[0] },
      identities: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  }
  return users.get(email);
}

function session(user) {
  const now = Math.floor(Date.now() / 1000);
  const header = b64url(JSON.stringify({ alg: "ES256", typ: "JWT", kid: KID }));
  const payload = b64url(
    JSON.stringify({
      iss: `${BASE}/auth/v1`,
      sub: user.id,
      aud: "authenticated",
      role: "authenticated",
      email: user.email,
      user_metadata: user.user_metadata,
      app_metadata: user.app_metadata,
      aal: "aal1",
      session_id: randomUUID(),
      iat: now,
      exp: now + 3600,
    }),
  );
  const signature = sign("sha256", Buffer.from(`${header}.${payload}`), {
    key: privateKey,
    dsaEncoding: "ieee-p1363",
  });
  const refresh = randomUUID();
  refreshTokens.set(refresh, user.email);
  return {
    access_token: `${header}.${payload}.${b64url(signature)}`,
    token_type: "bearer",
    expires_in: 3600,
    expires_at: now + 3600,
    refresh_token: refresh,
    user,
  };
}

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "apikey, authorization, content-type, x-client-info, x-supabase-api-version",
  "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
};

function send(res, status, body) {
  res.writeHead(status, { "Content-Type": "application/json", ...CORS });
  res.end(body === undefined ? "" : JSON.stringify(body));
}

function userFromAuthHeader(req) {
  const token = req.headers.authorization?.replace(/^Bearer /, "");
  if (!token) return null;
  try {
    const { email } = JSON.parse(Buffer.from(token.split(".")[1], "base64url").toString());
    return users.get(email) ?? null;
  } catch {
    return null;
  }
}

createServer(async (req, res) => {
  if (req.method === "OPTIONS") return send(res, 204);
  const url = new URL(req.url, BASE);
  let body = {};
  if (req.method === "POST" || req.method === "PUT") {
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    body = chunks.length ? JSON.parse(Buffer.concat(chunks).toString() || "{}") : {};
  }

  switch (url.pathname) {
    case "/auth/v1/.well-known/jwks.json":
      return send(res, 200, { keys: [jwk] });
    case "/auth/v1/token": {
      const grant = url.searchParams.get("grant_type");
      if (grant === "password") {
        if (!body.email || !body.password)
          return send(res, 400, {
            error_code: "invalid_credentials",
            msg: "Invalid login credentials",
          });
        return send(res, 200, session(userFor(body.email)));
      }
      if (grant === "refresh_token") {
        const email = refreshTokens.get(body.refresh_token);
        if (!email)
          return send(res, 400, {
            error_code: "refresh_token_not_found",
            msg: "Invalid Refresh Token",
          });
        return send(res, 200, session(users.get(email)));
      }
      return send(res, 400, { msg: "unsupported grant" });
    }
    case "/auth/v1/signup":
      return send(res, 200, session(userFor(body.email, body.data?.full_name)));
    case "/auth/v1/user": {
      const user = userFromAuthHeader(req);
      if (!user) return send(res, 401, { msg: "invalid JWT" });
      if (req.method === "PUT" && body.data) Object.assign(user.user_metadata, body.data);
      return send(res, 200, user);
    }
    case "/auth/v1/logout":
      return send(res, 204);
    default:
      return send(res, 404, { msg: `mock-auth: ${url.pathname} not implemented` });
  }
}).listen(PORT, "127.0.0.1", () => console.log(`mock auth on ${BASE}`));
