"use client";

import { animate, motion, type PanInfo, useMotionValue, useTransform } from "motion/react";
import type { ReactNode } from "react";
import { haptic } from "@/lib/haptics";
import { spring } from "@/lib/motion";

interface SwipeAction {
  label: string;
  icon: ReactNode;
  className: string; // background color of the revealed action
  onTrigger: () => void;
}

interface SwipeRowProps {
  children: ReactNode;
  left?: SwipeAction; // revealed when swiping right
  right?: SwipeAction; // revealed when swiping left
}

const THRESHOLD = 96;

/** Row that reveals an action on horizontal swipe (touch) — keyboard/mouse users get buttons elsewhere. */
export function SwipeRow({ children, left, right }: SwipeRowProps) {
  const x = useMotionValue(0);
  const leftOpacity = useTransform(x, [0, THRESHOLD], [0, 1]);
  const rightOpacity = useTransform(x, [-THRESHOLD, 0], [1, 0]);
  const leftScale = useTransform(x, [0, THRESHOLD], [0.6, 1]);
  const rightScale = useTransform(x, [-THRESHOLD, 0], [1, 0.6]);

  const onDragEnd = (_: unknown, info: PanInfo) => {
    const offset = info.offset.x;
    if (offset > THRESHOLD && left) {
      haptic("success");
      left.onTrigger();
    } else if (offset < -THRESHOLD && right) {
      haptic("warning");
      right.onTrigger();
    }
    animate(x, 0, spring.snappy);
  };

  return (
    <div className="relative overflow-hidden rounded-xl">
      {left && (
        <motion.div
          style={{ opacity: leftOpacity }}
          className={`absolute inset-0 flex items-center gap-2 pl-5 text-sm font-medium text-white ${left.className}`}
        >
          <motion.span style={{ scale: leftScale }} className="flex items-center gap-2">
            {left.icon}
            {left.label}
          </motion.span>
        </motion.div>
      )}
      {right && (
        <motion.div
          style={{ opacity: rightOpacity }}
          className={`absolute inset-0 flex items-center justify-end gap-2 pr-5 text-sm font-medium text-white ${right.className}`}
        >
          <motion.span style={{ scale: rightScale }} className="flex items-center gap-2">
            {right.label}
            {right.icon}
          </motion.span>
        </motion.div>
      )}
      <motion.div
        drag="x"
        dragDirectionLock
        dragConstraints={{ left: right ? -160 : 0, right: left ? 160 : 0 }}
        dragElastic={0.15}
        dragSnapToOrigin={false}
        style={{ x }}
        onDragEnd={onDragEnd}
        className="bg-card relative touch-pan-y"
      >
        {children}
      </motion.div>
    </div>
  );
}
