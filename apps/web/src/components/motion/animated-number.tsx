"use client";

import { animate, useMotionValue, useReducedMotion } from "motion/react";
import { useEffect, useRef } from "react";

interface AnimatedNumberProps {
  value: number;
  format: (value: number) => string;
  className?: string;
}

/** Counts from the previous value to the new one (BRL formatting stays exact on every frame). */
export function AnimatedNumber({ value, format, className }: AnimatedNumberProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const motionValue = useMotionValue(value);
  const reduce = useReducedMotion();
  const first = useRef(true);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const from = first.current ? 0 : motionValue.get();
    first.current = false;
    if (reduce) {
      motionValue.set(value);
      node.textContent = format(value);
      return;
    }
    // Fixed-duration tween (not a spring): it always lands exactly on `value`, which matters for money.
    const controls = animate(from, value, {
      duration: 0.8,
      ease: [0.16, 1, 0.3, 1],
      onUpdate: (latest) => {
        motionValue.set(latest);
        node.textContent = format(Math.round(latest));
      },
      onComplete: () => {
        node.textContent = format(value);
      },
    });
    return () => {
      controls.stop();
      node.textContent = format(value);
    };
  }, [value, format, motionValue, reduce]);

  return (
    <span ref={ref} className={className}>
      {format(value)}
    </span>
  );
}
