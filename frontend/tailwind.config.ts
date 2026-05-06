import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-geist-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-geist-mono)", "ui-monospace", "monospace"],
      },
      colors: {
        surface: {
          DEFAULT: "#0c1222",
          raised: "#111827",
          border: "#1f2937",
        },
        accent: {
          DEFAULT: "#22d3ee",
          muted: "#0891b2",
        },
      },
    },
  },
  plugins: [],
};

export default config;
