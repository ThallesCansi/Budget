"use client";

import type { Category, CategoryInput } from "@budget/api-client";
import { Archive } from "lucide-react";
import { useState } from "react";
import { CategoryIcon } from "@/components/category-icon";
import { ColorPicker, IconPicker } from "@/components/forms/pickers";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface CategoryFormProps {
  initial?: Category;
  kind: Category["kind"];
  pending?: boolean;
  onSubmit: (body: CategoryInput) => void;
  onRemove?: () => void;
}

export function CategoryForm({ initial, kind, pending, onSubmit, onRemove }: CategoryFormProps) {
  const [name, setName] = useState(initial?.name ?? "");
  const [color, setColor] = useState(initial?.color ?? "#56ab91");
  const [icon, setIcon] = useState(initial?.icon ?? "tag");

  return (
    <form
      className="space-y-5 pt-2 pb-4"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit({ name: name.trim(), kind, color, icon });
      }}
    >
      <div className="flex items-center gap-3">
        <CategoryIcon icon={icon} color={color} size="lg" />
        <div className="flex-1 space-y-1.5">
          <Label htmlFor="cat-name">Nome</Label>
          <Input
            id="cat-name"
            required
            maxLength={60}
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="h-11 text-base"
          />
        </div>
      </div>
      <div className="space-y-2">
        <Label>Cor</Label>
        <ColorPicker value={color} onChange={setColor} />
      </div>
      <div className="space-y-2">
        <Label>Ícone</Label>
        <IconPicker value={icon} color={color} onChange={setIcon} />
      </div>
      <div className="flex gap-2">
        {onRemove && (
          <Button type="button" variant="destructive" size="lg" className="h-12" onClick={onRemove}>
            <Archive /> Remover
          </Button>
        )}
        <Button
          type="submit"
          size="lg"
          disabled={pending}
          className="bg-brand-gradient h-12 flex-1 font-semibold text-white"
        >
          {initial ? "Salvar" : "Criar categoria"}
        </Button>
      </div>
    </form>
  );
}
