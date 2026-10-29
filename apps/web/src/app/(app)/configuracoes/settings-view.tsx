"use client";

import type { Category } from "@budget/api-client";
import { ChevronRight, LogOut, Plus, UserRound } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { toast } from "sonner";
import { CategoryIcon } from "@/components/category-icon";
import { PageHeader } from "@/components/layout/page-header";
import { SignOutDialog } from "@/components/layout/sign-out-dialog";
import { usePrivacy } from "@/components/providers/privacy-provider";
import { ResponsiveModal } from "@/components/responsive-modal";
import { SettingsSection } from "@/components/settings-section";
import { ThemeToggle } from "@/components/theme-toggle";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  useCategories,
  useCreateCategory,
  useDeleteCategory,
  useUpdateCategory,
} from "@/lib/api/queries";
import { CategoryForm } from "./category-form";

type Editing = { kind: Category["kind"]; category?: Category } | null;

export function SettingsView() {
  const { hidden, toggle } = usePrivacy();
  const { data: categories = [] } = useCategories();
  const create = useCreateCategory();
  const update = useUpdateCategory();
  const remove = useDeleteCategory();
  const [editing, setEditing] = useState<Editing>(null);
  const close = () => setEditing(null);
  const closeWith = (message: string) => () => {
    close();
    toast.success(message);
  };

  const list = (kind: Category["kind"]) => (
    <ul className="divide-y">
      {categories
        .filter((c) => c.kind === kind && !c.archived)
        .map((c) => (
          <li key={c.id}>
            <button
              type="button"
              onClick={() => setEditing({ kind, category: c })}
              className="flex w-full items-center gap-3 py-2.5 text-left hover:opacity-80"
            >
              <CategoryIcon icon={c.icon} color={c.color} size="sm" />
              <span className="flex-1 text-sm font-medium">{c.name}</span>
              <ChevronRight className="text-muted-foreground size-4" />
            </button>
          </li>
        ))}
      <li>
        <button
          type="button"
          onClick={() => setEditing({ kind })}
          className="text-primary dark:text-secondary flex w-full items-center gap-3 py-2.5 text-sm font-medium"
        >
          <span className="grid size-8 place-items-center rounded-xl border-2 border-dashed border-current">
            <Plus className="size-4" />
          </span>
          Nova categoria
        </button>
      </li>
    </ul>
  );

  return (
    <div className="space-y-8">
      <PageHeader title="Configurações" />

      <div className="grid gap-8 lg:grid-cols-2">
        <div className="space-y-8">
          <SettingsSection title="Aparência">
            <ThemeToggle />
          </SettingsSection>

          <SettingsSection title="Privacidade">
            <div className="flex items-center justify-between gap-4">
              <Label htmlFor="privacy" className="block">
                <span className="font-medium">Esconder valores</span>
                <span className="text-muted-foreground block text-sm font-normal">
                  Borra todos os valores — útil para usar o app em público. Também no ícone de olho.
                </span>
              </Label>
              <Switch id="privacy" checked={hidden} onCheckedChange={toggle} />
            </div>
          </SettingsSection>

          <SettingsSection title="Conta">
            <div className="divide-y">
              <Link href="/perfil" className="flex items-center gap-3 py-2.5 text-sm font-medium">
                <UserRound className="text-muted-foreground size-5" />{" "}
                <span className="flex-1">Perfil</span>
                <ChevronRight className="text-muted-foreground size-4" />
              </Link>
              <SignOutDialog>
                <button
                  type="button"
                  className="text-destructive flex w-full items-center gap-3 py-2.5 text-sm font-medium"
                >
                  <LogOut className="size-5" /> Sair
                </button>
              </SignOutDialog>
            </div>
          </SettingsSection>
        </div>

        <SettingsSection title="Categorias" description="Organize seus lançamentos do seu jeito.">
          <Tabs defaultValue="expense">
            <TabsList className="w-full">
              <TabsTrigger value="expense">Despesas</TabsTrigger>
              <TabsTrigger value="income">Receitas</TabsTrigger>
            </TabsList>
            <TabsContent value="expense">{list("expense")}</TabsContent>
            <TabsContent value="income">{list("income")}</TabsContent>
          </Tabs>
        </SettingsSection>
      </div>

      <ResponsiveModal
        open={editing !== null}
        onOpenChange={(open) => !open && close()}
        title={editing?.category ? "Editar categoria" : "Nova categoria"}
      >
        {editing && (
          <CategoryForm
            key={editing.category?.id ?? `new-${editing.kind}`}
            kind={editing.kind}
            initial={editing.category}
            pending={create.isPending || update.isPending}
            onSubmit={(body) => {
              const done = closeWith("Categoria salva");
              if (editing.category) {
                const { kind: _kind, ...changes } = body;
                update.mutate({ id: editing.category.id, body: changes }, { onSuccess: done });
              } else create.mutate(body, { onSuccess: done });
            }}
            onRemove={
              editing.category
                ? () =>
                    remove.mutate(editing.category!.id, {
                      onSuccess: closeWith("Categoria removida"),
                    })
                : undefined
            }
          />
        )}
      </ResponsiveModal>
    </div>
  );
}
