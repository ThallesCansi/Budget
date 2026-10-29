// Generates PWA / Apple icons from the brand coin. Run: pnpm --filter @budget/web icons
import { readFile, writeFile } from "node:fs/promises";
import sharp from "sharp";

const coin = await readFile(new URL("../public/brand/coin.svg", import.meta.url), "utf8");
const coinInner = coin.replace(/<svg[^>]*>/, "").replace("</svg>", "");

/** Gradient tile with the coin; `scale` is the coin size relative to the tile. */
function tile(size, { scale, radius }) {
  const coinSize = size * scale;
  const offset = (size - coinSize) / 2;
  return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#2b478b"/><stop offset="1" stop-color="#56ab91"/>
  </linearGradient></defs>
  <rect width="${size}" height="${size}" rx="${radius * size}" fill="url(#g)"/>
  <svg x="${offset}" y="${offset}" width="${coinSize}" height="${coinSize}" viewBox="0 0 100 100">${coinInner}</svg>
</svg>`);
}

const outputs = [
  ["icon-192.png", 192, { scale: 0.62, radius: 0.22 }],
  ["icon-512.png", 512, { scale: 0.62, radius: 0.22 }],
  ["icon-maskable-512.png", 512, { scale: 0.5, radius: 0 }],
  ["apple-touch-icon.png", 180, { scale: 0.6, radius: 0 }],
  ["badge-96.png", 96, { scale: 0.8, radius: 0.5 }],
];

for (const [name, size, opts] of outputs) {
  await writeFile(
    new URL(`../public/icons/${name}`, import.meta.url),
    await sharp(tile(size, opts)).png().toBuffer(),
  );
  console.log(`public/icons/${name}`);
}
