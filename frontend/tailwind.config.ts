import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          DEFAULT: "hsl(var(--gold))",
          light: "hsl(var(--gold-light))",
          dark: "hsl(var(--gold-dark))",
        },
        red: {
          DEFAULT: "hsl(var(--red))",
          light: "hsl(var(--red-light))",
        },
        purple: {
          DEFAULT: "hsl(var(--purple))",
          light: "hsl(var(--purple-light))",
        },
        green: {
          DEFAULT: "hsl(var(--green))",
          light: "hsl(var(--green-light))",
        },
        border: "hsl(var(--border))",
        "border-light": "hsl(var(--border-light))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--bg-page))",
        sidebar: "hsl(var(--bg-sidebar))",
        card: "hsl(var(--bg-card))",
        "card-header": "hsl(var(--bg-card-header))",
        hover: "hsl(var(--bg-hover))",
        "table-alt": "hsl(var(--bg-table-alt))",
        input: "hsl(var(--bg-input))",
        foreground: "hsl(var(--text-primary))",
        secondary: "hsl(var(--text-secondary))",
        muted: "hsl(var(--text-muted))",
      },
      fontFamily: {
        heading: ["var(--font-heading)", "sans-serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      borderRadius: {
        DEFAULT: "var(--radius)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
