"use client";

import { onlineManager } from "@tanstack/react-query";
import { useSyncExternalStore } from "react";

export function useOnline() {
  return useSyncExternalStore(
    (cb) => onlineManager.subscribe(cb),
    () => onlineManager.isOnline(),
    () => true,
  );
}
