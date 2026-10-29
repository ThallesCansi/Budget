import { createSerwistRoute } from "@serwist/turbopack";

const revision = crypto.randomUUID();

export const { dynamic, dynamicParams, revalidate, generateStaticParams, GET } = createSerwistRoute(
  {
    swSrc: "src/app/sw.ts",
    useNativeEsbuild: true,
    additionalPrecacheEntries: [{ url: "/~offline", revision }],
    // Landing-page illustrations are large and not needed offline.
    globIgnores: ["**/illustrations/**", "**/brand/favicon.ico"],
  },
);
