import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 p-24 bg-[hsl(var(--bg-page))]">
      <h1 className="font-heading text-4xl font-bold text-foreground">
        SalesPredict AI CRM
      </h1>
      <p className="font-body text-lg text-secondary">
        AI-powered sales forecasting and analytics platform
      </p>
      <Link
        href="/login"
        className="inline-flex items-center justify-center rounded bg-gold px-6 py-3 font-heading text-sm font-medium text-[hsl(var(--bg-page))] hover:bg-gold-light transition-colors duration-200 shadow-[0_0_12px_hsl(var(--gold)/0.2)]"
      >
        Sign In
      </Link>
    </main>
  );
}
