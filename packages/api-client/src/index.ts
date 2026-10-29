import createClient, { type ClientOptions } from "openapi-fetch";
import type { components, paths } from "./schema";

export type { components, paths };
export type Schemas = components["schemas"];

export type Me = Schemas["MeOut"];
export type Household = Schemas["HouseholdOut"];
export type Member = Schemas["MemberOut"];
export type Account = Schemas["AccountOut"];
export type AccountInput = Schemas["AccountIn"];
export type Category = Schemas["CategoryOut"];
export type CategoryInput = Schemas["CategoryIn"];
export type Transaction = Schemas["TransactionOut"];
export type TransactionInput = Schemas["TransactionIn"];
export type TransactionPage = Schemas["TransactionPage"];
export type MonthSummary = Schemas["MonthSummary"];
export type AccountKind = Account["kind"];
export type TransactionKind = Transaction["kind"];

/** Error body returned by the API: `{ error: { code, message, details } }`. */
export interface ApiErrorBody {
  error: { code: string; message: string; details?: unknown };
}

export function createApiClient(options: ClientOptions) {
  return createClient<paths>(options);
}

export type ApiClient = ReturnType<typeof createApiClient>;
