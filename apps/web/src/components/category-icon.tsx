import { iconFor } from "@/lib/icons";
import { cn } from "@/lib/utils";

interface CategoryIconProps {
  icon?: string | null;
  color?: string | null;
  className?: string;
  size?: "sm" | "md" | "lg";
}

const sizes = {
  sm: "size-8 [&_svg]:size-4",
  md: "size-10 [&_svg]:size-5",
  lg: "size-12 [&_svg]:size-6",
};

/** Icon on a tinted rounded square — the visual language of the original dashboard cards. */
export function CategoryIcon({ icon, color, className, size = "md" }: CategoryIconProps) {
  const Icon = iconFor(icon);
  const tint = color ?? "#98a6af";
  return (
    <span
      className={cn(
        "inline-flex shrink-0 items-center justify-center rounded-xl",
        sizes[size],
        className,
      )}
      style={{ backgroundColor: `${tint}22`, color: tint }}
    >
      <Icon aria-hidden />
    </span>
  );
}
