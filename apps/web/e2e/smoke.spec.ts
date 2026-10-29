import { expect, type Page, test } from "@playwright/test";

async function signIn(page: Page, email: string) {
  await page.goto("/inicio");
  await expect(page).toHaveURL(/\/entrar/);
  await page.getByLabel("E-mail").fill(email);
  await page.getByLabel("Senha", { exact: true }).fill("segredo123");
  await page.getByRole("button", { name: "Entrar", exact: true }).click();
  await expect(page).toHaveURL(/\/inicio/);
  await expect(page.getByText("saldo atual")).toBeVisible();
}

async function addTransaction(
  page: Page,
  kind: "Despesa" | "Receita",
  keys: string[],
  category: string,
  description?: string,
) {
  await page.getByRole("button", { name: "Novo lançamento" }).last().click();
  await page.getByRole("button", { name: kind, exact: true }).click();
  const amount = page.getByRole("button", { name: /^Valor:/ });
  await amount.focus();
  for (const key of keys) await page.keyboard.press(key);
  if (description) await page.getByLabel("Descrição").fill(description);
  await page.getByRole("button", { name: category, exact: true }).click();
  await page.getByRole("button", { name: "Adicionar", exact: true }).click();
}

test("landing page presents the product", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Organize suas finanças");
  await expect(page.getByRole("link", { name: "Criar conta grátis" })).toBeVisible();
});

test("sign in, record income and expense, see exact totals", async ({ page }, info) => {
  await signIn(page, `e2e-${info.project.name}-${Date.now()}@example.com`);

  await addTransaction(page, "Receita", ["5", "0", "0", "0", "0", "0"], "Salário");
  await addTransaction(page, "Despesa", ["4", "5", "9", "0"], "Mercado", "Mercado do mês");

  await expect(page.getByText("Mercado do mês").first()).toBeVisible();
  // Animated numbers must settle on the exact amounts.
  await expect(page.getByText("R$ 5.000,00").first()).toBeVisible();
  await expect(page.getByText("R$ 4.954,10").first()).toBeVisible();

  await page.goto("/transacoes");
  await expect(page.getByRole("heading", { name: "Transações" })).toBeVisible();
  await expect(page.getByText("Mercado do mês")).toBeVisible();
});

test("privacy mode blurs amounts", async ({ page }, info) => {
  await signIn(page, `privacy-${info.project.name}-${Date.now()}@example.com`);
  await page.getByRole("button", { name: "Esconder valores" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-privacy", "on");
});

test("offline: expense is kept on the device and synced when back online", async ({
  page,
  context,
}, info) => {
  await signIn(page, `offline-${info.project.name}-${Date.now()}@example.com`);

  await context.setOffline(true);
  await expect(page.getByText("Você está offline")).toBeVisible();
  await addTransaction(page, "Despesa", ["1", "2", "5", "0"], "Restaurantes", "Almoço sem sinal");
  await expect(page.getByText("Almoço sem sinal").first()).toBeVisible();
  await expect(page.getByLabel("Aguardando sincronização").first()).toBeVisible();

  await context.setOffline(false);
  await expect(page.getByLabel("Aguardando sincronização")).toHaveCount(0, { timeout: 15_000 });

  // A full reload proves the server has it (not just the local cache).
  await page.reload();
  await page.goto("/transacoes");
  await expect(page.getByText("Almoço sem sinal")).toBeVisible();
});
