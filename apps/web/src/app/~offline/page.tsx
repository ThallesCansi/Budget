import { WifiOff } from "lucide-react";
import Link from "next/link";

export const metadata = { title: "Sem conexão" };

export default function OfflinePage() {
  return (
    <main className="bg-brand-gradient-vertical grid min-h-dvh place-items-center p-6 text-center text-white">
      <div className="max-w-sm space-y-4">
        <WifiOff className="mx-auto size-12 opacity-90" aria-hidden />
        <h1 className="text-2xl font-semibold">Você está offline</h1>
        <p className="text-white/80">
          Esta página ainda não foi salva no aparelho. As telas que você já abriu continuam
          funcionando, e os lançamentos feitos agora serão enviados quando a conexão voltar.
        </p>
        <Link
          href="/inicio"
          className="text-primary inline-block rounded-full bg-white px-5 py-2.5 font-medium"
        >
          Voltar ao início
        </Link>
      </div>
    </main>
  );
}
