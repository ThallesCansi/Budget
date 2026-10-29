"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { spring } from "@/lib/motion";
import { cn } from "@/lib/utils";
import { FabMenu } from "./fab-menu";
import { isActive, type NavItem, TAB_NAV } from "./nav";

function Tab({ item, active }: { item: NavItem; active: boolean }) {
  const Icon = item.icon;
  return (
    <Link
      href={item.href}
      aria-current={active ? "page" : undefined}
      className={cn(
        "relative flex flex-1 flex-col items-center gap-0.5 pt-2 pb-1 text-[11px] font-medium transition-colors",
        active ? "text-primary dark:text-foreground" : "text-muted-foreground",
      )}
    >
      {active && (
        <motion.span
          layoutId="tab-indicator"
          className="bg-primary dark:bg-secondary absolute top-0 h-1 w-8 rounded-b-full"
          transition={spring.snappy}
        />
      )}
      <motion.span
        animate={{ y: active ? -1 : 0, scale: active ? 1.08 : 1 }}
        transition={spring.snappy}
      >
        <Icon className="size-6" strokeWidth={active ? 2.4 : 2} />
      </motion.span>
      {item.label}
    </Link>
  );
}

/** Phone navigation: four tabs with the raised "+" in the middle. */
export function BottomNav() {
  const pathname = usePathname();
  const [first, second, third, fourth] = TAB_NAV as [NavItem, NavItem, NavItem, NavItem];
  return (
    <nav
      aria-label="Principal"
      className="bg-card/90 pb-safe fixed inset-x-0 bottom-0 z-30 border-t backdrop-blur-lg md:hidden"
    >
      <div className="mx-auto flex max-w-md items-start">
        <Tab item={first} active={isActive(pathname, first.href)} />
        <Tab item={second} active={isActive(pathname, second.href)} />
        <div className="flex flex-1 justify-center">
          <FabMenu variant="tab" />
        </div>
        <Tab item={third} active={isActive(pathname, third.href)} />
        <Tab item={fourth} active={isActive(pathname, fourth.href)} />
      </div>
    </nav>
  );
}
