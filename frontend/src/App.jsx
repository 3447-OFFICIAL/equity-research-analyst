import { Activity, BarChart3, FileSearch, ShieldAlert, TrendingUp } from "lucide-react";

const metrics = [
  { label: "Revenue Trend", value: "+12.4%", icon: TrendingUp },
  { label: "Risk Score", value: "Medium", icon: ShieldAlert },
  { label: "Sentiment", value: "Positive", icon: Activity },
  { label: "DCF Value", value: "$214", icon: BarChart3 },
];

function App() {
  return (
    <main className="min-h-screen bg-slate-50 text-ink">
      <section className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-xl font-semibold">AI Equity Research Analyst</h1>
            <p className="text-sm text-slate-600">Institutional research workflow dashboard</p>
          </div>
          <button className="inline-flex items-center gap-2 rounded-md bg-accent px-4 py-2 text-sm font-medium text-white">
            <FileSearch size={16} />
            Research AAPL
          </button>
        </div>
      </section>

      <section className="mx-auto grid max-w-7xl gap-6 px-6 py-8 lg:grid-cols-[220px_1fr]">
        <nav className="space-y-1 text-sm">
          {["Dashboard", "Company Search", "Research Report", "Competitor Comparison", "Portfolio Analysis"].map(
            (item) => (
              <a
                className="block rounded-md px-3 py-2 font-medium text-slate-700 hover:bg-white hover:text-ink"
                href="#"
                key={item}
              >
                {item}
              </a>
            ),
          )}
        </nav>

        <div className="space-y-6">
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {metrics.map((metric) => {
              const Icon = metric.icon;
              return (
                <article className="rounded-lg border border-line bg-white p-4" key={metric.label}>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-slate-600">{metric.label}</span>
                    <Icon className="text-accent" size={18} />
                  </div>
                  <strong className="mt-3 block text-2xl">{metric.value}</strong>
                </article>
              );
            })}
          </div>

          <section className="rounded-lg border border-line bg-white p-5">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-semibold">Recommendation</h2>
              <span className="rounded-md bg-emerald-100 px-3 py-1 text-sm font-semibold text-emerald-800">
                BUY
              </span>
            </div>
            <p className="mt-4 max-w-3xl text-sm leading-6 text-slate-700">
              The dashboard shell is ready for live filing ingestion, RAG citations, valuation outputs,
              and LangGraph agent recommendations.
            </p>
          </section>
        </div>
      </section>
    </main>
  );
}

export default App;
