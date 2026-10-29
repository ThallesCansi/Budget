"use client";

import type { Account, AccountInput, AccountKind } from "@budget/api-client";
import { Archive } from "lucide-react";
import { useState } from "react";
import { CategoryIcon } from "@/components/category-icon";
import { Chip } from "@/components/forms/chip";
import { ColorPicker, IconPicker, MoneyInput } from "@/components/forms/pickers";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export const ACCOUNT_KINDS: { value: AccountKind; label: string; icon: string }[] = [
  { value: "cash", label: "Dinheiro", icon: "wallet" },
  { value: "checking", label: "Conta corrente", icon: "landmark" },
  { value: "savings", label: "Poupança", icon: "piggy-bank" },
  { value: "investment", label: "Investimento", icon: "trending-up" },
  { value: "credit_card", label: "Cartão de crédito", icon: "credit-card" },
];

export const kindLabel = (kind: AccountKind) =>
  ACCOUNT_KINDS.find((k) => k.value === kind)?.label ?? kind;

interface AccountFormProps {
  initial?: Account;
  pending?: boolean;
  onSubmit: (body: AccountInput) => void;
  onArchive?: () => void;
}

export function AccountForm({ initial, pending, onSubmit, onArchive }: AccountFormProps) {
  const [name, setName] = useState(initial?.name ?? "");
  const [kind, setKind] = useState<AccountKind>(initial?.kind ?? "checking");
  const [color, setColor] = useState(initial?.color ?? "#2b478b");
  const [icon, setIcon] = useState(initial?.icon ?? "landmark");
  const [initialBalance, setInitialBalance] = useState(initial?.initial_balance_cents ?? 0);
  const [limit, setLimit] = useState(initial?.credit_limit_cents ?? 0);
  const [closingDay, setClosingDay] = useState(String(initial?.closing_day ?? ""));
  const [dueDay, setDueDay] = useState(String(initial?.due_day ?? ""));
  const isCard = kind === "credit_card";

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      name: name.trim(),
      kind,
      color,
      icon,
      initial_balance_cents: isCard ? 0 : initialBalance,
      credit_limit_cents: isCard && limit > 0 ? limit : null,
      closing_day: isCard ? Number(closingDay) : null,
      due_day: isCard ? Number(dueDay) : null,
    });
  };

  return (
    <form onSubmit={submit} className="space-y-5 pt-2 pb-4">
      <div className="flex items-center gap-3">
        <CategoryIcon icon={icon} color={color} size="lg" />
        <div className="flex-1 space-y-1.5">
          <Label htmlFor="acc-name">Nome</Label>
          <Input
            id="acc-name"
            required
            maxLength={60}
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Ex.: Nubank, Carteira"
            className="h-11 text-base"
          />
        </div>
      </div>

      {!initial && (
        <fieldset>
          <legend className="mb-2 text-sm font-medium">Tipo</legend>
          <div className="flex flex-wrap gap-2">
            {ACCOUNT_KINDS.map((k) => (
              <Chip
                key={k.value}
                selected={kind === k.value}
                onClick={() => {
                  setKind(k.value);
                  setIcon(k.icon);
                }}
              >
                {k.label}
              </Chip>
            ))}
          </div>
        </fieldset>
      )}

      {isCard ? (
        <div className="grid grid-cols-3 gap-3">
          <div className="col-span-3 space-y-1.5">
            <Label htmlFor="acc-limit">Limite</Label>
            <MoneyInput id="acc-limit" value={limit} onChange={setLimit} />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="acc-closing">Fecha dia</Label>
            <Input
              id="acc-closing"
              required
              type="number"
              min={1}
              max={31}
              inputMode="numeric"
              value={closingDay}
              onChange={(e) => setClosingDay(e.target.value)}
              className="h-11 text-base"
            />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="acc-due">Vence dia</Label>
            <Input
              id="acc-due"
              required
              type="number"
              min={1}
              max={31}
              inputMode="numeric"
              value={dueDay}
              onChange={(e) => setDueDay(e.target.value)}
              className="h-11 text-base"
            />
          </div>
        </div>
      ) : (
        <div className="space-y-1.5">
          <Label htmlFor="acc-balance">Saldo inicial</Label>
          <MoneyInput
            id="acc-balance"
            value={initialBalance}
            onChange={setInitialBalance}
            allowNegative
          />
          <p className="text-muted-foreground text-xs">
            Quanto havia na conta antes do primeiro lançamento.
          </p>
        </div>
      )}

      <div className="space-y-2">
        <Label>Cor</Label>
        <ColorPicker value={color} onChange={setColor} />
      </div>
      <div className="space-y-2">
        <Label>Ícone</Label>
        <IconPicker value={icon} color={color} onChange={setIcon} />
      </div>

      <div className="flex gap-2">
        {onArchive && (
          <Button
            type="button"
            variant="destructive"
            size="lg"
            className="h-12"
            onClick={onArchive}
          >
            <Archive /> Remover
          </Button>
        )}
        <Button
          type="submit"
          size="lg"
          disabled={pending}
          className="bg-brand-gradient h-12 flex-1 font-semibold text-white"
        >
          {initial ? "Salvar" : "Criar conta"}
        </Button>
      </div>
    </form>
  );
}
