import Link from "next/link";
import { Logo } from "@/components/brand/logo";
import { Features } from "@/components/marketing/features";
import { Hero } from "@/components/marketing/hero";
import { SiteHeader } from "@/components/marketing/site-header";
import { Team } from "@/components/marketing/team";

export default function HomePage() {
  return (
    <>
      <SiteHeader />
      <main>
        <Hero />
        <Features />
        <section className="mx-auto max-w-3xl px-6 pb-24 text-center">
          <h2 className="text-3xl font-bold md:text-4xl">Comece agora — é grátis</h2>
          <p className="text-muted-foreground mt-3 text-lg">
            Crie sua conta com e-mail ou Google em menos de um minuto.
          </p>
          <Link
            href="/cadastro"
            className="bg-brand-gradient shadow-glow mt-8 inline-block rounded-full px-8 py-4 text-lg font-semibold text-white transition-transform hover:scale-105"
          >
            Criar minha conta
          </Link>
        </section>
        <Team />
      </main>
      <footer className="bg-blue-accent-800 px-6 py-10 text-white/70">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 md:flex-row">
          <Logo className="h-9" light />
          <p className="text-sm">Budget · Feito com carinho no IFES.</p>
        </div>
      </footer>
    </>
  );
}
