"use client";

import { LogOut } from "lucide-react";
import { motion } from "motion/react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Coin, Logo } from "@/components/brand/logo";
import { spring } from "@/lib/motion";
import { cn } from "@/lib/utils";
import { isActive, SIDEBAR_NAV } from "./nav";
import { SignOutDialog } from "./sign-out-dialog";

const itemClass =
  "relative flex h-12 items-center gap-3 rounded-xl px-3 font-semibold text-sidebar-foreground/85 transition-colors hover:text-sidebar-foreground md:justify-center lg:justify-start";

/** The blue sidebar of the original app: icons only on tablets, full labels on desktops. */
export function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="bg-sidebar text-sidebar-foreground fixed inset-y-0 left-0 z-30 hidden w-20 flex-col px-3 py-5 md:flex lg:w-64">
      <Link
        href="/inicio"
        className="mb-8 flex items-center justify-center px-2 lg:justify-start"
        aria-label="Início"
      >
        <Coin className="size-11 lg:hidden" />
        <Logo className="hidden h-10 lg:block" priority light />
      </Link>
      <nav className="flex flex-1 flex-col gap-1" aria-label="Principal">
        {SIDEBAR_NAV.map(({ href, label, icon: Icon }) => {
          const active = isActive(pathname, href);
          return (
            <Link
              key={href}
              href={href}
              aria-current={active ? "page" : undefined}
              className={cn(
                itemClass,
                active && "text-sidebar-accent-foreground hover:text-sidebar-accent-foreground",
              )}
              title={label}
            >
              {active && (
                <motion.span
                  layoutId="sidebar-active"
                  className="bg-sidebar-accent shadow-card absolute inset-0 rounded-xl"
                  transition={spring.snappy}
                />
              )}
              <Icon className="relative size-5 shrink-0" />
              {/* not-sr-only makes the label static; the wrapper keeps it above the active pill. */}
              <span className="relative">
                <span className="md:sr-only lg:not-sr-only">{label}</span>
              </span>
            </Link>
          );
        })}
      </nav>
      <SignOutDialog>
        <button type="button" className={cn(itemClass, "hover:bg-white/10")} title="Sair">
          <LogOut className="size-5 shrink-0" />
          <span className="md:sr-only lg:not-sr-only">Sair</span>
        </button>
      </SignOutDialog>
    </aside>
  );
}
