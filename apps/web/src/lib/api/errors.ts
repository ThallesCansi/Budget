import type { ApiErrorBody } from "@budget/api-client";

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly code: string,
    message: string,
    readonly details?: unknown,
  ) {
    super(message);
    this.name = "ApiError";
  }

  static fromBody(status: number, body: unknown): ApiError {
    const err = (body as Partial<ApiErrorBody> | undefined)?.error;
    return new ApiError(
      status,
      err?.code ?? "unknown",
      err?.message ?? "Algo deu errado. Tente novamente.",
      err?.details,
    );
  }
}

export function errorMessage(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  if (error instanceof TypeError) return "Sem conexão com o servidor.";
  return "Algo deu errado. Tente novamente.";
}
