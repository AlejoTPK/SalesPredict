# SalesPredict Frontend

Next.js 15 App Router frontend for SalesPredict AI CRM.

## Quick Start

```bash
cd frontend
pnpm install
pnpm dev
```

## Build

```bash
pnpm build
pnpm start
```

## Lint

```bash
pnpm lint
```

## Architecture

- **App Router**: Exclusive use of App Router. No `pages/` directory.
- **Server Components**: Prefer React Server Components and native `fetch`.
- **Client Components**: Use `"use client"` only when client-side state is unavoidable.
- **Zero TanStack**: No React Query, no TanStack Table. Use native `useState`/`useEffect` or custom hooks.
- **Styling**: Tailwind CSS utility-first. No inline styles unless dynamic.

## Structure

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Landing page
└── (dashboard)/        # Route group (authenticated)
    ├── layout.tsx      # Dashboard layout with sidebar
    ├── dashboard/      # Main dashboard
    ├── predictions/    # Predictions page
    └── settings/       # Settings page

components/
├── ui/                 # shadcn/ui primitives
├── dashboard/          # Dashboard-specific components
└── layout/             # Layout components (sidebar, nav)

lib/
├── api-client.ts       # Native fetch wrapper
├── auth.ts             # Token management
├── utils.ts            # Utility functions (cn)
└── hooks/              # Custom React hooks
```

## Environment Variables

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```
