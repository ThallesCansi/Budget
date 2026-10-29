"use client";

import { Eye, EyeOff } from "lucide-react";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type FieldProps = React.ComponentProps<typeof Input> & { label: string; id: string };

export function Field({ label, id, ...props }: FieldProps) {
  return (
    <div className="space-y-1.5">
      <Label htmlFor={id}>{label}</Label>
      <Input id={id} className="h-12 text-base" {...props} />
    </div>
  );
}

export function PasswordField({ label, id, ...props }: FieldProps) {
  const [visible, setVisible] = useState(false);
  return (
    <div className="space-y-1.5">
      <Label htmlFor={id}>{label}</Label>
      <div className="relative">
        <Input
          id={id}
          type={visible ? "text" : "password"}
          className="h-12 pr-12 text-base"
          {...props}
        />
        <button
          type="button"
          onClick={() => setVisible((v) => !v)}
          aria-label={visible ? "Esconder senha" : "Mostrar senha"}
          className="text-muted-foreground hover:text-foreground absolute inset-y-0 right-0 grid w-12 place-items-center"
        >
          {visible ? <EyeOff className="size-5" /> : <Eye className="size-5" />}
        </button>
      </div>
    </div>
  );
}
