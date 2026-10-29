import { createAsyncStoragePersister } from "@tanstack/query-async-storage-persister";
import type { PersistedClient } from "@tanstack/react-query-persist-client";
import { del, get, set } from "idb-keyval";

const KEY = "budget-query-cache";

/**
 * Writes still in flight when the app is closed would be lost, since TanStack only restores
 * *paused* mutations. Marking every pending mutation as paused makes `resumePausedMutations()`
 * replay it on the next launch — safe because transaction writes are idempotent PUTs.
 */
function serialize(client: PersistedClient) {
  const mutations = client.clientState.mutations.map((m) =>
    m.state.status === "pending" ? { ...m, state: { ...m.state, isPaused: true } } : m,
  );
  return JSON.stringify({ ...client, clientState: { ...client.clientState, mutations } });
}

/** Persists the TanStack Query cache (and unsent writes) in IndexedDB. */
export const persister = createAsyncStoragePersister({
  key: KEY,
  storage:
    typeof window === "undefined"
      ? undefined
      : {
          getItem: (key) => get<string>(key).then((v) => v ?? null),
          setItem: (key, value) => set(key, value),
          removeItem: (key) => del(key),
        },
  serialize,
  throttleTime: 300,
});

export const clearPersistedCache = () => del(KEY);
