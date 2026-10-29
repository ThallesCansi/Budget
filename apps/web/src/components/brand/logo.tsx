import Image from "next/image";
import { cn } from "@/lib/utils";

/** `light` uses the white wordmark for gradient/dark backgrounds. */
export function Logo({
  className,
  priority,
  light,
}: {
  className?: string;
  priority?: boolean;
  light?: boolean;
}) {
  return (
    <Image
      src={light ? "/brand/logo-light.svg" : "/brand/logo.svg"}
      alt="Budget"
      width={363}
      height={100}
      priority={priority}
      className={cn("h-9 w-auto", className)}
    />
  );
}

export function Coin({ className }: { className?: string }) {
  return (
    <Image
      src="/brand/coin.svg"
      alt="Budget"
      width={75}
      height={75}
      className={cn("size-10", className)}
    />
  );
}
