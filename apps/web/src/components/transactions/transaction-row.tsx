"use client";

import type { Account, Category, Transaction } from "@budget/api-client";
import { ArrowLeftRight, CloudUpload } from "lucide-react";
import { CategoryIcon } from "@/components/category-icon";
import { Money } from "@/components/money";
import { cn } from "@/lib/utils";

interface TransactionRowProps {
  transaction: Transaction;
  category?: Category;
  account?: Account;
  toAccount?: Account;
  pending?: boolean;
  onClick?: () => void;
}

export function TransactionRow({
  transaction: t,
  category,
  account,
  toAccount,
  pending,
  onClick,
}: TransactionRowProps) {
  const isTransfer = t.kind === "transfer";
  const subtitle = isTransfer
    ? `${account?.name ?? "?"} → ${toAccount?.name ?? "?"}`
    : [category?.name ?? "Sem categoria", account?.name].filter(Boolean).join(" · ");

  return (
    <button
      type="button"
      onClick={onClick}
      className="hover:bg-muted/60 focus-visible:bg-muted/60 flex w-full items-center gap-3 px-3 py-3 text-left transition-colors focus-visible:outline-none"
    >
      {isTransfer ? (
        <span className="bg-transfer/15 text-transfer grid size-10 shrink-0 place-items-center rounded-xl">
          <ArrowLeftRight className="size-5" />
        </span>
      ) : (
        <CategoryIcon icon={category?.icon} color={category?.color} />
      )}
      <span className="min-w-0 flex-1">
        <span className="flex items-center gap-1.5">
          <span className="truncate font-medium">{t.description}</span>
          {pending && (
            <CloudUpload
              className="text-muted-foreground size-3.5 shrink-0"
              aria-label="Aguardando sincronização"
            />
          )}
        </span>
        <span className="text-muted-foreground block truncate text-xs">{subtitle}</span>
      </span>
      <span className="flex flex-col items-end">
        <Money
          cents={t.kind === "expense" ? -t.amount_cents : t.amount_cents}
          tone={t.kind === "income" ? "income" : t.kind === "expense" ? "expense" : "muted"}
          sign={t.kind === "income"}
          className={cn("font-semibold", !t.paid && "opacity-60")}
        />
        {!t.paid && (
          <span className="bg-warning/20 dark:text-warning rounded-full px-1.5 text-[10px] font-medium tracking-wide text-amber-700 uppercase">
            previsto
          </span>
        )}
      </span>
    </button>
  );
}
