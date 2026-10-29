"use client";

import type { Transaction, TransactionInput, TransactionKind } from "@budget/api-client";
import { onlineManager } from "@tanstack/react-query";
import { createContext, type ReactNode, useCallback, useContext, useMemo, useState } from "react";
import { toast } from "sonner";
import { ResponsiveModal } from "@/components/responsive-modal";
import { useDeleteTransaction, useSaveTransaction } from "@/lib/api/queries";
import { haptic } from "@/lib/haptics";
import { newId } from "@/lib/uuid";
import { TransactionForm } from "./transaction-form";

interface SheetState {
  open: boolean;
  kind: TransactionKind;
  editing?: Transaction;
  key: number;
}

interface TransactionSheetApi {
  create: (kind?: TransactionKind) => void;
  edit: (transaction: Transaction) => void;
  remove: (transaction: Transaction) => void;
}

const SheetContext = createContext<TransactionSheetApi | null>(null);

const LABELS: Record<TransactionKind, string> = {
  expense: "Despesa",
  income: "Receita",
  transfer: "Transferência",
};

export function toInput(t: Transaction): TransactionInput {
  return {
    kind: t.kind,
    account_id: t.account_id,
    to_account_id: t.to_account_id,
    category_id: t.category_id,
    member_id: t.member_id,
    amount_cents: t.amount_cents,
    date: t.date,
    description: t.description,
    notes: t.notes,
    paid: t.paid,
    invoice_month: t.invoice_month,
  };
}

export function TransactionSheetProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<SheetState>({ open: false, kind: "expense", key: 0 });
  const save = useSaveTransaction();
  const del = useDeleteTransaction();

  const create = useCallback(
    (kind: TransactionKind = "expense") => setState((s) => ({ open: true, kind, key: s.key + 1 })),
    [],
  );
  const edit = useCallback(
    (editing: Transaction) =>
      setState((s) => ({ open: true, kind: editing.kind, editing, key: s.key + 1 })),
    [],
  );

  const remove = useCallback(
    (transaction: Transaction) => {
      del.mutate({ id: transaction.id });
      haptic("warning");
      toast(`${LABELS[transaction.kind]} excluída`, {
        description: transaction.description,
        action: {
          label: "Desfazer",
          // Same id + idempotent PUT = the exact transaction comes back.
          onClick: () => save.mutate({ id: transaction.id, body: toInput(transaction) }),
        },
      });
    },
    [del, save],
  );

  const submit = (body: TransactionInput) => {
    const id = state.editing?.id ?? newId();
    save.mutate({ id, body });
    haptic("success");
    setState((s) => ({ ...s, open: false }));
    const label = LABELS[body.kind];
    if (!onlineManager.isOnline()) {
      toast.info(`${label} salva no aparelho`, {
        description: "Será enviada quando a conexão voltar.",
      });
    } else {
      toast.success(state.editing ? `${label} atualizada` : `${label} adicionada`);
    }
  };

  const api = useMemo(() => ({ create, edit, remove }), [create, edit, remove]);
  const editing = state.editing;

  return (
    <SheetContext value={api}>
      {children}
      <ResponsiveModal
        open={state.open}
        onOpenChange={(open) => setState((s) => ({ ...s, open }))}
        title={editing ? `Editar ${LABELS[editing.kind].toLowerCase()}` : "Novo lançamento"}
      >
        <TransactionForm
          key={state.key}
          initial={editing}
          initialKind={state.kind}
          onSubmit={submit}
          onDelete={
            editing
              ? () => {
                  setState((s) => ({ ...s, open: false }));
                  remove(editing);
                }
              : undefined
          }
        />
      </ResponsiveModal>
    </SheetContext>
  );
}

export function useTransactionSheet() {
  const ctx = useContext(SheetContext);
  if (!ctx) throw new Error("useTransactionSheet must be used within TransactionSheetProvider");
  return ctx;
}
