"use client";

import { useSyncExternalStore } from "react";

const noop = () => () => {};

/** False during prerender/SSR and the hydration pass, true afterwards. */
export const useIsClient = () =>
  useSyncExternalStore(
    noop,
    () => true,
    () => false,
  );
