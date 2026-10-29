import {
  ArrowLeftRight,
  Ellipsis,
  LayoutDashboard,
  type LucideIcon,
  Settings,
  Target,
  Wallet,
} from "lucide-react";

export interface NavItem {
  href: string;
  label: string;
  icon: LucideIcon;
}

export const SIDEBAR_NAV: NavItem[] = [
  { href: "/inicio", label: "Início", icon: LayoutDashboard },
  { href: "/transacoes", label: "Transações", icon: ArrowLeftRight },
  { href: "/carteiras", label: "Carteiras", icon: Wallet },
  { href: "/planejamento", label: "Planejamento", icon: Target },
  { href: "/configuracoes", label: "Configurações", icon: Settings },
];

/** Bottom tab bar (phones). The "+" button sits in the middle, between items 2 and 3. */
export const TAB_NAV: NavItem[] = [
  { href: "/inicio", label: "Início", icon: LayoutDashboard },
  { href: "/transacoes", label: "Transações", icon: ArrowLeftRight },
  { href: "/planejamento", label: "Planejar", icon: Target },
  { href: "/mais", label: "Mais", icon: Ellipsis },
];

export const isActive = (pathname: string, href: string) =>
  pathname === href || pathname.startsWith(`${href}/`);
