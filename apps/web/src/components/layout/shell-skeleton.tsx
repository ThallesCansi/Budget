import { Coin } from "@/components/brand/logo";
import { Shimmer } from "@/components/motion/skeleton";

/** Static app shell prerendered at build time; the real UI mounts on the client. */
export function ShellSkeleton() {
  return (
    <div role="status" aria-busy="true" aria-label="Carregando">
      <aside className="bg-sidebar fixed inset-y-0 left-0 hidden w-20 flex-col items-center py-5 md:flex lg:w-64">
        <Coin className="size-11" />
      </aside>
      <div className="md:pl-20 lg:pl-64">
        <div className="mx-auto max-w-6xl space-y-6 px-4 pt-6 md:px-8 md:pt-8">
          <div className="flex items-center gap-3">
            <Shimmer className="size-9 rounded-full md:hidden" />
            <Shimmer className="h-7 w-48" />
          </div>
          <div className="grid grid-cols-2 gap-3 md:grid-cols-3">
            <Shimmer className="col-span-2 h-36 md:col-span-1" />
            <Shimmer className="h-36" />
            <Shimmer className="h-36" />
          </div>
          <Shimmer className="h-64" />
        </div>
      </div>
      <div className="bg-card fixed inset-x-0 bottom-0 h-16 border-t md:hidden" />
    </div>
  );
}
