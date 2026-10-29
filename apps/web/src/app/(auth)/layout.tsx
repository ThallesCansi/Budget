import Image from "next/image";
import Link from "next/link";
import { FloatingIllustration } from "@/components/auth/floating-illustration";
import { Logo } from "@/components/brand/logo";

export default function AuthLayout({ children }: LayoutProps<"/">) {
  return (
    <div className="grid min-h-dvh md:grid-cols-2">
      <aside className="bg-brand-gradient-vertical relative hidden overflow-hidden p-10 text-white md:flex md:flex-col">
        <Link href="/" aria-label="Página inicial">
          <Logo className="h-11" priority light />
        </Link>
        <div className="flex flex-1 items-center justify-center">
          <FloatingIllustration>
            <Image
              src="/illustrations/header.svg"
              alt=""
              width={520}
              height={420}
              priority
              className="h-auto w-full max-w-md drop-shadow-2xl"
            />
          </FloatingIllustration>
        </div>
        <p className="max-w-md text-2xl leading-snug font-semibold">
          Organize suas finanças de forma <u>fácil</u>, <u>prática</u> e <u>segura</u>.
        </p>
        <div className="pointer-events-none absolute -right-24 -bottom-24 size-96 rounded-full bg-white/10 blur-3xl" />
      </aside>

      <main className="bg-brand-gradient-vertical md:bg-background flex min-h-dvh flex-col md:bg-none">
        <div className="pt-safe flex items-center justify-center px-6 md:hidden">
          <Link href="/" aria-label="Página inicial" className="py-8">
            <Logo className="h-11" priority light />
          </Link>
        </div>
        <div className="bg-background pb-safe flex flex-1 items-start justify-center rounded-t-[2rem] px-6 pt-8 md:items-center md:rounded-none md:pt-0">
          <div className="w-full max-w-sm py-6">{children}</div>
        </div>
      </main>
    </div>
  );
}
