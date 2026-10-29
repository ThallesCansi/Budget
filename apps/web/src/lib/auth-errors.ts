/** Supabase Auth returns English messages; translate the ones users actually see. */
const MESSAGES: [RegExp, string][] = [
  [/invalid login credentials/i, "E-mail ou senha incorretos."],
  [/email not confirmed/i, "Confirme seu e-mail antes de entrar — enviamos um link para você."],
  [/user already registered/i, "Já existe uma conta com este e-mail."],
  [/password should be at least/i, "A senha precisa ter pelo menos 8 caracteres."],
  [
    /rate limit|too many requests|security purposes/i,
    "Muitas tentativas. Aguarde um pouco e tente novamente.",
  ],
  [/same.*password/i, "A nova senha precisa ser diferente da atual."],
  [/weak|pwned|leaked/i, "Essa senha é fraca ou já vazou em outro site. Escolha outra."],
  [/network|fetch/i, "Sem conexão. Verifique sua internet."],
];

export function authErrorMessage(message: string | undefined): string {
  if (!message) return "Não foi possível concluir. Tente novamente.";
  return MESSAGES.find(([pattern]) => pattern.test(message))?.[1] ?? message;
}
