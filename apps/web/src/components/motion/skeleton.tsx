import { cn } from "@/lib/utils";

export function Shimmer({ className }: { className?: string }) {
  return <div aria-hidden className={cn("skeleton-shimmer rounded-lg", className)} />;
}
