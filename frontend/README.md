# SkyOps Intelligence - Frontend Service

Next.js 14 Progressive Web App for airline ground crew, ramp leads, and station dispatchers.

---

## 1. Local Setup Instructions

### Prerequisites
- Node.js 18.17+ (tested on Node v22)
- npm or pnpm

### Step 1: Install Dependencies
```bash
npm install
```

### Step 2: Configure Environment
```bash
cp .env.example .env.local
```

### Step 3: Run Development Server
```bash
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 2. Health Check & Diagnostics
- **Frontend Health Endpoint:** `http://localhost:3000/api/health`
- **Lint Check:** `npm run lint`
- **Type Check:** `npx tsc --noEmit`

