"use client";

import { Check } from "lucide-react";
import { motion } from "motion/react";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { formatMoney, parseMoney } from "@/lib/format";
import { ICONS, PALETTE } from "@/lib/icons";
import { spring } from "@/lib/motion";
import { cn } from "@/lib/utils";

export function ColorPicker({
  value,
  onChange,
}: {
  value: string;
  onChange: (color: string) => void;
}) {
  return (
    <fieldset className="flex min-w-0 flex-wrap gap-2">
      <legend className="sr-only">Cor</legend>
      {PALETTE.map((color) => (
        <motion.button
          key={color}
          type="button"
          aria-pressed={value.toLowerCase() === color}
          aria-label={color}
          whileTap={{ scale: 0.85 }}
          onClick={() => onChange(color)}
          className="ring-offset-background aria-pressed:ring-foreground/40 grid size-8 place-items-center rounded-full ring-offset-2 aria-pressed:ring-2"
          style={{ backgroundColor: color }}
        >
          {value.toLowerCase() === color && (
            <motion.span initial={{ scale: 0 }} animate={{ scale: 1 }} transition={spring.bouncy}>
              <Check className="size-4 text-white" strokeWidth={3} />
            </motion.span>
          )}
        </motion.button>
      ))}
    </fieldset>
  );
}

export function IconPicker({
  value,
  color,
  onChange,
}: {
  value: string;
  color: string;
  onChange: (icon: string) => void;
}) {
  return (
    <fieldset className="grid max-h-40 min-w-0 grid-cols-8 gap-1 overflow-y-auto">
      <legend className="sr-only">Ícone</legend>
      {Object.entries(ICONS).map(([name, Icon]) => (
        <button
          key={name}
          type="button"
          aria-pressed={value === name}
          aria-label={name}
          onClick={() => onChange(name)}
          className={cn(
            "hover:bg-muted grid aspect-square place-items-center rounded-lg transition-colors",
            value === name && "bg-muted",
          )}
          style={value === name ? { color } : undefined}
        >
          <Icon className="size-5" />
        </button>
      ))}
    </fieldset>
  );
}

/** Free-typed BRL amount ("1.234,56"), normalized on blur. */
export function MoneyInput({
  value,
  onChange,
  id,
  allowNegative,
}: {
  value: number;
  onChange: (cents: number) => void;
  id?: string;
  allowNegative?: boolean;
}) {
  const [text, setText] = useState(value ? formatMoney(value).replace(/^R\$\s?/, "") : "");
  return (
    <Input
      id={id}
      inputMode="decimal"
      value={text}
      placeholder="0,00"
      onChange={(e) => {
        setText(e.target.value);
        const cents = parseMoney(e.target.value);
        if (cents !== null)
          onChange(allowNegative && e.target.value.trim().startsWith("-") ? -cents : cents);
        else if (!e.target.value.trim()) onChange(0);
      }}
      onBlur={() =>
        setText(
          value
            ? formatMoney(value)
                .replace(/^R\$\s?/, "")
                .replace("−", "-")
            : "",
        )
      }
      className="h-11 text-base"
    />
  );
}
