import { createApiClient } from "@budget/api-client";
import { env } from "@/lib/env";
import { getSupabase } from "@/lib/supabase/client";
import { ApiError } from "./errors";

/** Free-tier API instances sleep; anything slower than this is treated as a cold start. */
const SLOW_REQUEST_MS = 3500;
export const API_SLOW_EVENT = "budget:api-slow";
export const API_READY_EVENT = "budget:api-ready";

let householdId: string | null = null;
export function setActiveHousehold(id: string | null) {
  householdId = id;
}

const slowTimers = new Map<Request, ReturnType<typeof setTimeout>>();

export const api = createApiClient({ baseUrl: env.apiUrl });

api.use({
  async onRequest({ request }) {
    const { data } = await getSupabase().auth.getSession();
    const token = data.session?.access_token;
    if (token) request.headers.set("Authorization", `Bearer ${token}`);
    if (householdId) request.headers.set("X-Household-Id", householdId);
    slowTimers.set(
      request,
      setTimeout(() => window.dispatchEvent(new Event(API_SLOW_EVENT)), SLOW_REQUEST_MS),
    );
    return request;
  },
  async onResponse({ request, response }) {
    clearTimeout(slowTimers.get(request));
    slowTimers.delete(request);
    window.dispatchEvent(new Event(API_READY_EVENT));
    if (!response.ok) {
      const body = await response
        .clone()
        .json()
        .catch(() => undefined);
      throw ApiError.fromBody(response.status, body);
    }
    return response;
  },
  onError({ request, error }) {
    clearTimeout(slowTimers.get(request));
    slowTimers.delete(request);
    throw error;
  },
});

/** Unwraps an openapi-fetch result, returning `data` (errors already throw in the middleware). */
export async function call<T>(promise: Promise<{ data?: T; error?: unknown; response: Response }>) {
  const { data, response } = await promise;
  if (response.status === 204) return undefined as T;
  return data as T;
}
