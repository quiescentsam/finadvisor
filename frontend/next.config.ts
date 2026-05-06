import path from "path";
import { fileURLToPath } from "url";
import type { NextConfig } from "next";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Monorepo / stray lockfiles: trace from repo root (parent of `frontend/`)
  outputFileTracingRoot: path.join(__dirname, ".."),
};

export default nextConfig;
