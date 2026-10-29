"use client";

import type { Account } from "@budget/api-client";
import { Plus, Wallet } from "lucide-react";
import { motion } from "motion/react";
import { useState } from "react";
import { toast } from "sonner";
import { AccountForm, kindLabel } from "@/components/accounts/account-form";
import { CategoryIcon } from "@/components/category-icon";
import { EmptyState } from "@/components/empty-state";
import { PageHeader } from "@/components/layout/page-header";
import { Money } from "@/components/money";
import { ProgressBar } from "@/components/motion/progress-bar";
import { Shimmer } from "@/components/motion/skeleton";
import { ResponsiveModal } from "@/components/responsive-modal";
import { Button } from "@/components/ui/button";
import {
  useAccounts,
  useCreateAccount,
  useDeleteAccount,
  useUpdateAccount,
} from "@/lib/api/queries";
import { fadeUp, stagger } from "@/lib/motion";

function AccountCard({ account, onClick }: { account: Account; onClick: () => void }) {
  const isCard = account.kind === "credit_card";
  const used = isCard ? Math.max(0, -account.balance_cents) : 0;
  const limit = account.credit_limit_cents ?? 0;
  return (
    <motion.button
      type="button"
      variants={fadeUp}
      whileHover={{ y: -3 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className="bg-card shadow-card relative flex flex-col gap-4 overflow-hidden rounded-2xl border p-5 text-left"
    >
      <span className="absolute inset-x-0 top-0 h-1.5" style={{ backgroundColor: account.color }} />
      <div className="flex items-center gap-3">
        <CategoryIcon icon={account.icon} color={account.color} />
        <div className="min-w-0">
          <p className="truncate font-semibold">{account.name}</p>
          <p className="text-muted-foreground text-xs">{kindLabel(account.kind)}</p>
        </div>
      </div>
      {isCard ? (
        <div className="space-y-2">
          <p className="text-muted-foreground text-xs">Fatura em aberto</p>
          <Money cents={used} tone="expense" animate className="text-2xl font-bold" />
          {limit > 0 && (
            <>
              <ProgressBar value={used / limit} thresholds />
              <p className="text-muted-foreground text-xs">
                Disponível <Money cents={Math.max(0, limit - used)} /> de <Money cents={limit} />
              </p>
            </>
          )}
        </div>
      ) : (
        <div>
          <p className="text-muted-foreground text-xs">Saldo</p>
          <Money
            cents={account.balance_cents}
            tone={account.balance_cents < 0 ? "expense" : "default"}
            animate
            className="text-2xl font-bold"
          />
          {account.projected_balance_cents !== account.balance_cents && (
            <p className="text-muted-foreground text-xs">
              Previsto: <Money cents={account.projected_balance_cents} />
            </p>
          )}
        </div>
      )}
    </motion.button>
  );
}

export function AccountsView() {
  const { data: accounts, isPending } = useAccounts();
  const create = useCreateAccount();
  const update = useUpdateAccount();
  const remove = useDeleteAccount();
  const [editing, setEditing] = useState<Account | "new" | null>(null);

  const active = (accounts ?? []).filter((a) => !a.archived);
  const archived = (accounts ?? []).filter((a) => a.archived);
  const total = active.reduce((sum, a) => sum + a.balance_cents, 0);
  const close = () => setEditing(null);
  const closeWith = (message: string, description?: string) => () => {
    close();
    toast.success(message, { description });
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Carteiras"
        subtitle={
          <>
            Patrimônio: <Money cents={total} className="text-foreground font-semibold" />
          </>
        }
        actions={
          <Button
            onClick={() => setEditing("new")}
            className="bg-brand-gradient hidden text-white sm:inline-flex"
          >
            <Plus /> Nova conta
          </Button>
        }
      />

      {isPending && !accounts ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[0, 1, 2].map((i) => (
            <Shimmer key={i} className="h-40" />
          ))}
        </div>
      ) : active.length === 0 ? (
        <EmptyState
          icon={Wallet}
          title="Nenhuma conta ativa"
          description="Crie contas para separar dinheiro, banco e cartões."
        />
      ) : (
        <motion.div
          initial="hidden"
          animate="show"
          variants={stagger()}
          className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
        >
          {active.map((a) => (
            <AccountCard key={a.id} account={a} onClick={() => setEditing(a)} />
          ))}
          <motion.button
            type="button"
            variants={fadeUp}
            onClick={() => setEditing("new")}
            className="text-muted-foreground hover:border-primary hover:text-primary flex min-h-40 flex-col items-center justify-center gap-2 rounded-2xl border-2 border-dashed transition-colors"
          >
            <Plus className="size-6" />
            Adicionar conta ou cartão
          </motion.button>
        </motion.div>
      )}

      {archived.length > 0 && (
        <details className="bg-card rounded-2xl border p-4">
          <summary className="text-muted-foreground cursor-pointer text-sm font-medium">
            Arquivadas ({archived.length})
          </summary>
          <ul className="mt-3 divide-y">
            {archived.map((a) => (
              <li key={a.id} className="flex items-center justify-between gap-3 py-2">
                <span className="flex items-center gap-2 text-sm">
                  <CategoryIcon icon={a.icon} color={a.color} size="sm" /> {a.name}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => update.mutate({ id: a.id, body: { archived: false } })}
                >
                  Restaurar
                </Button>
              </li>
            ))}
          </ul>
        </details>
      )}

      <ResponsiveModal
        open={editing !== null}
        onOpenChange={(open) => !open && close()}
        title={editing === "new" ? "Nova conta" : "Editar conta"}
      >
        {editing !== null && (
          <AccountForm
            key={editing === "new" ? "new" : editing.id}
            initial={editing === "new" ? undefined : editing}
            pending={create.isPending || update.isPending}
            onSubmit={(body) => {
              if (editing === "new") {
                create.mutate(body, { onSuccess: closeWith("Conta criada") });
              } else {
                const { kind: _kind, ...changes } = body;
                update.mutate(
                  { id: editing.id, body: changes },
                  { onSuccess: closeWith("Conta atualizada") },
                );
              }
            }}
            onArchive={
              editing === "new"
                ? undefined
                : () =>
                    remove.mutate(editing.id, {
                      onSuccess: closeWith(
                        "Conta removida",
                        "Contas com lançamentos ficam em Arquivadas.",
                      ),
                    })
            }
          />
        )}
      </ResponsiveModal>
    </div>
  );
}
