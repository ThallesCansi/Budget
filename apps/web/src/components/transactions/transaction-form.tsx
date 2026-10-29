"use client";

import type { Transaction, TransactionInput, TransactionKind } from "@budget/api-client";
import { subDays } from "date-fns";
import { ArrowRight, CalendarDays, ChevronDown, Trash2 } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useMemo, useState } from "react";
import { CategoryIcon } from "@/components/category-icon";
import { Chip } from "@/components/forms/chip";
import { applyKey, MoneyKeypad } from "@/components/forms/money-keypad";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { useMediaQuery } from "@/hooks/use-media-query";
import { useAccounts, useCategories, useMe } from "@/lib/api/queries";
import { formatMoney, toISODate } from "@/lib/format";
import { spring } from "@/lib/motion";
import { cn } from "@/lib/utils";

const KINDS: { value: TransactionKind; label: string; color: string }[] = [
  { value: "expense", label: "Despesa", color: "var(--expense)" },
  { value: "income", label: "Receita", color: "var(--income)" },
  { value: "transfer", label: "Transferência", color: "var(--transfer)" },
];

export interface TransactionFormProps {
  initial?: Transaction;
  initialKind?: TransactionKind;
  onSubmit: (body: TransactionInput) => void;
  onDelete?: () => void;
}

export function TransactionForm({
  initial,
  initialKind = "expense",
  onSubmit,
  onDelete,
}: TransactionFormProps) {
  const { data: accounts = [] } = useAccounts();
  const { data: categories = [] } = useCategories();
  const { data: me } = useMe();
  const touch = useMediaQuery("(pointer: coarse)", true);

  const activeAccounts = accounts.filter((a) => !a.archived || a.id === initial?.account_id);
  const [kind, setKind] = useState<TransactionKind>(initial?.kind ?? initialKind);
  const [amount, setAmount] = useState(initial?.amount_cents ?? 0);
  const [keypadOpen, setKeypadOpen] = useState(!initial && touch);
  const [description, setDescription] = useState(initial?.description ?? "");
  const [categoryId, setCategoryId] = useState<string | null>(initial?.category_id ?? null);
  const [accountId, setAccountId] = useState(initial?.account_id ?? activeAccounts[0]?.id ?? "");
  const [toAccountId, setToAccountId] = useState(initial?.to_account_id ?? "");
  const [memberId, setMemberId] = useState<string | null>(initial?.member_id ?? null);
  const [date, setDate] = useState(initial?.date ?? toISODate(new Date()));
  const [paid, setPaid] = useState(initial?.paid ?? true);
  const [notes, setNotes] = useState(initial?.notes ?? "");
  const [showNotes, setShowNotes] = useState(Boolean(initial?.notes));
  const [error, setError] = useState<string | null>(null);

  const kindColor = KINDS.find((k) => k.value === kind)!.color;
  const kindCategories = useMemo(
    () => categories.filter((c) => c.kind === kind && (!c.archived || c.id === categoryId)),
    [categories, kind, categoryId],
  );
  const members = me?.household.members ?? [];
  const today = toISODate(new Date());
  const yesterday = toISODate(subDays(new Date(), 1));

  const changeKind = (next: TransactionKind) => {
    setKind(next);
    setCategoryId(null);
    setError(null);
  };

  const submit = (event: React.FormEvent) => {
    event.preventDefault();
    const category = categories.find((c) => c.id === categoryId);
    const finalDescription =
      description.trim() || category?.name || KINDS.find((k) => k.value === kind)!.label;
    if (amount <= 0) return setError("Informe um valor maior que zero.");
    if (!accountId) return setError("Escolha uma conta.");
    if (kind === "transfer" && (!toAccountId || toAccountId === accountId))
      return setError("Escolha uma conta de destino diferente da origem.");
    onSubmit({
      kind,
      amount_cents: amount,
      description: finalDescription,
      account_id: accountId,
      to_account_id: kind === "transfer" ? toAccountId : null,
      category_id: kind === "transfer" ? null : categoryId,
      member_id: memberId,
      date,
      paid,
      notes: notes.trim() || null,
    });
  };

  return (
    <form onSubmit={submit} className="space-y-5 pt-2 pb-4">
      {/* Kind selector with sliding pill */}
      <div
        className="bg-muted grid grid-cols-3 rounded-full p-1"
        role="tablist"
        aria-label="Tipo de lançamento"
      >
        {KINDS.map((k) => (
          <button
            key={k.value}
            type="button"
            role="tab"
            aria-selected={kind === k.value}
            onClick={() => changeKind(k.value)}
            className={cn(
              "relative rounded-full py-2 text-sm font-medium transition-colors",
              kind === k.value ? "text-white" : "text-muted-foreground",
            )}
          >
            {kind === k.value && (
              <motion.span
                layoutId="kind-pill"
                className="absolute inset-0 rounded-full"
                style={{ backgroundColor: k.color }}
                transition={spring.snappy}
              />
            )}
            <span className="relative">{k.label}</span>
          </button>
        ))}
      </div>

      {/* Amount */}
      <div className="text-center">
        <button
          type="button"
          onClick={() => setKeypadOpen((v) => !v)}
          onKeyDown={(e) => {
            if (/^\d$/.test(e.key)) setAmount((v) => applyKey(v, e.key));
            else if (e.key === "Backspace") setAmount((v) => applyKey(v, "back"));
            else return;
            e.preventDefault();
          }}
          className="focus-visible:ring-ring/50 mx-auto block rounded-2xl px-4 py-1 outline-none focus-visible:ring-3"
          aria-label={`Valor: ${formatMoney(amount)}. Digite os números ou toque para abrir o teclado.`}
        >
          <motion.span
            key={kind}
            initial={{ scale: 0.96, opacity: 0.6 }}
            animate={{ scale: 1, opacity: 1 }}
            className="block text-4xl font-bold tracking-tight tabular-nums"
            style={{ color: kindColor }}
          >
            {formatMoney(amount)}
          </motion.span>
          <span className="text-muted-foreground text-xs">
            {touch ? "Toque para digitar o valor" : "Digite o valor com o teclado"}
          </span>
        </button>
        <AnimatePresence initial={false}>
          {keypadOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={spring.gentle}
              className="overflow-hidden"
            >
              <div className="pt-3">
                <MoneyKeypad value={amount} onChange={setAmount} />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <div className="space-y-1.5">
        <Label htmlFor="tx-description">Descrição</Label>
        <Input
          id="tx-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          onFocus={() => setKeypadOpen(false)}
          placeholder={
            kind === "expense"
              ? "Ex.: Mercado do mês"
              : kind === "income"
                ? "Ex.: Salário"
                : "Ex.: Reserva"
          }
          maxLength={140}
          autoComplete="off"
          className="h-11 text-base"
        />
      </div>

      {kind !== "transfer" && (
        <fieldset className="space-y-2">
          <legend className="mb-2 text-sm font-medium">Categoria</legend>
          <div className="-mx-1 grid max-h-52 grid-cols-4 gap-1 overflow-y-auto px-1 sm:grid-cols-5">
            {kindCategories.map((c) => (
              <motion.button
                key={c.id}
                type="button"
                whileTap={{ scale: 0.94 }}
                onClick={() => setCategoryId((current) => (current === c.id ? null : c.id))}
                aria-pressed={categoryId === c.id}
                className={cn(
                  "flex flex-col items-center gap-1 rounded-xl border-2 p-1.5 text-center text-[11px] leading-tight transition-colors",
                  categoryId === c.id
                    ? "bg-muted border-current"
                    : "hover:bg-muted border-transparent",
                )}
                style={categoryId === c.id ? { color: c.color } : undefined}
              >
                <CategoryIcon icon={c.icon} color={c.color} size="sm" />
                <span className="text-foreground line-clamp-2">{c.name}</span>
              </motion.button>
            ))}
          </div>
        </fieldset>
      )}

      <fieldset className="space-y-2">
        <legend className="mb-2 text-sm font-medium">{kind === "transfer" ? "De" : "Conta"}</legend>
        <div className="-mx-4 flex gap-2 overflow-x-auto px-4 pb-1">
          {activeAccounts.map((a) => (
            <Chip
              key={a.id}
              selected={accountId === a.id}
              color={a.color}
              onClick={() => setAccountId(a.id)}
            >
              {a.name}
            </Chip>
          ))}
        </div>
        {kind === "transfer" && (
          <>
            <div className="flex items-center gap-2 pt-1 text-sm font-medium">
              <ArrowRight className="text-muted-foreground size-4" /> Para
            </div>
            <div className="-mx-4 flex gap-2 overflow-x-auto px-4 pb-1">
              {activeAccounts
                .filter((a) => a.id !== accountId)
                .map((a) => (
                  <Chip
                    key={a.id}
                    selected={toAccountId === a.id}
                    color={a.color}
                    onClick={() => setToAccountId(a.id)}
                  >
                    {a.name}
                  </Chip>
                ))}
            </div>
          </>
        )}
      </fieldset>

      <fieldset className="space-y-2">
        <legend className="mb-2 text-sm font-medium">Data</legend>
        <div className="flex flex-wrap items-center gap-2">
          <Chip selected={date === today} onClick={() => setDate(today)}>
            Hoje
          </Chip>
          <Chip selected={date === yesterday} onClick={() => setDate(yesterday)}>
            Ontem
          </Chip>
          <label
            className={cn(
              "relative inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-medium",
              date !== today && date !== yesterday
                ? "border-primary bg-primary text-primary-foreground"
                : "bg-card",
            )}
          >
            <CalendarDays className="size-4" />
            {date !== today && date !== yesterday ? date.split("-").reverse().join("/") : "Outra"}
            <input
              type="date"
              value={date}
              onChange={(e) => e.target.value && setDate(e.target.value)}
              className="absolute inset-0 cursor-pointer opacity-0"
              aria-label="Escolher data"
            />
          </label>
        </div>
      </fieldset>

      {members.length > 1 && (
        <fieldset className="space-y-2">
          <legend className="mb-2 text-sm font-medium">Quem?</legend>
          <div className="flex flex-wrap gap-2">
            {members.map((m) => (
              <Chip
                key={m.id}
                selected={memberId === m.id}
                onClick={() => setMemberId(memberId === m.id ? null : m.id)}
              >
                {m.display_name}
              </Chip>
            ))}
          </div>
        </fieldset>
      )}

      <div className="bg-muted/60 flex items-center justify-between rounded-xl px-4 py-3">
        <Label htmlFor="tx-paid" className="font-medium">
          {kind === "income" ? "Já recebido" : kind === "transfer" ? "Já realizada" : "Já pago"}
          <span className="text-muted-foreground block text-xs font-normal">
            Desmarque para deixar como previsto
          </span>
        </Label>
        <Switch id="tx-paid" checked={paid} onCheckedChange={setPaid} />
      </div>

      {showNotes ? (
        <div className="space-y-1.5">
          <Label htmlFor="tx-notes">Observação</Label>
          <Textarea
            id="tx-notes"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            maxLength={2000}
            rows={3}
          />
        </div>
      ) : (
        <button
          type="button"
          onClick={() => setShowNotes(true)}
          className="text-muted-foreground hover:text-foreground flex items-center gap-1 text-sm"
        >
          <ChevronDown className="size-4" /> Adicionar observação
        </button>
      )}

      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            role="alert"
            className="bg-destructive/10 text-destructive rounded-lg px-3 py-2 text-sm"
          >
            {error}
          </motion.p>
        )}
      </AnimatePresence>

      <div className="flex gap-2">
        {onDelete && (
          <Button
            type="button"
            variant="destructive"
            size="lg"
            className="h-12 px-4"
            onClick={onDelete}
            aria-label="Excluir"
          >
            <Trash2 />
          </Button>
        )}
        <Button
          type="submit"
          size="lg"
          className="bg-brand-gradient shadow-glow h-12 flex-1 text-base font-semibold text-white"
        >
          {initial ? "Salvar alterações" : "Adicionar"}
        </Button>
      </div>
    </form>
  );
}
