"use client";

import { createContext, type ReactNode, useCallback, useContext, useEffect, useState } from "react";

const STORAGE_KEY = "budget:privacy";
const PrivacyContext = createContext<{ hidden: boolean; toggle: () => void }>({
  hidden: false,
  toggle: () => {},
});

/** Privacy mode blurs every `[data-money]` element (see globals.css). */
export function PrivacyProvider({ children }: { children: ReactNode }) {
  const [hidden, setHidden] = useState(false);

  useEffect(() => {
    setHidden(localStorage.getItem(STORAGE_KEY) === "on");
  }, []);

  useEffect(() => {
    document.documentElement.dataset.privacy = hidden ? "on" : "off";
  }, [hidden]);

  const toggle = useCallback(() => {
    setHidden((value) => {
      localStorage.setItem(STORAGE_KEY, value ? "off" : "on");
      return !value;
    });
  }, []);

  return <PrivacyContext value={{ hidden, toggle }}>{children}</PrivacyContext>;
}

export const usePrivacy = () => useContext(PrivacyContext);
