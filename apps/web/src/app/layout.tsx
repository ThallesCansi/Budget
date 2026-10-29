import { SerwistProvider } from "@serwist/turbopack/react";
import type { Metadata, Viewport } from "next";
import { DM_Sans } from "next/font/google";
import { Providers } from "@/components/providers/providers";
import { env } from "@/lib/env";
import "./globals.css";

const dmSans = DM_Sans({ subsets: ["latin"], variable: "--font-dm-sans", display: "swap" });

export const metadata: Metadata = {
  metadataBase: new URL(env.siteUrl),
  title: { default: "Budget — suas finanças no controle", template: "%s · Budget" },
  description:
    "Controle financeiro pessoal e familiar: contas, cartões, metas e orçamentos — no celular ou no computador.",
  applicationName: "Budget",
  appleWebApp: { capable: true, title: "Budget", statusBarStyle: "default" },
  formatDetection: { telephone: false },
  icons: {
    icon: [
      { url: "/favicon.ico" },
      { url: "/icons/icon-192.png", type: "image/png", sizes: "192x192" },
    ],
    apple: "/icons/apple-touch-icon.png",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#2b478b" },
    { media: "(prefers-color-scheme: dark)", color: "#0c1529" },
  ],
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="pt-BR" className={dmSans.variable} suppressHydrationWarning>
      <body className="min-h-dvh">
        <SerwistProvider swUrl="/serwist/sw.js" disable={process.env.NODE_ENV === "development"}>
          <Providers>{children}</Providers>
        </SerwistProvider>
      </body>
    </html>
  );
}
