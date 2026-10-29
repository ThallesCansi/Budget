import type { Transition, Variants } from "motion/react";

/** Shared springs so every animation in the app feels like the same physical system. */
export const spring = {
  snappy: { type: "spring", stiffness: 500, damping: 35, mass: 0.8 },
  gentle: { type: "spring", stiffness: 220, damping: 28 },
  bouncy: { type: "spring", stiffness: 380, damping: 18 },
} satisfies Record<string, Transition>;

export const fadeUp: Variants = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0, transition: spring.gentle },
};

export const stagger = (step = 0.04, delay = 0): Variants => ({
  hidden: {},
  show: { transition: { staggerChildren: step, delayChildren: delay } },
});

/** Horizontal slide used when moving between months (direction = +1 next, -1 previous). */
export const slide: Variants = {
  enter: (direction: number) => ({ x: direction * 48, opacity: 0 }),
  center: { x: 0, opacity: 1, transition: spring.gentle },
  exit: (direction: number) => ({ x: direction * -48, opacity: 0, transition: { duration: 0.15 } }),
};
