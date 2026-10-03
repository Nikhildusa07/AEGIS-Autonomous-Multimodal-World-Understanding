import {
  Activity,
  Brain,
  CheckCircle2,
  Eye,
  FileText,
  Mic,
  Radio,
  RefreshCw,
  ScanSearch,
  ShieldCheck,
  Sparkles,
  Target,
  Zap,
} from "lucide-react";

import WorldView from "../components/WorldView";
import AutonomousControlLoop from "../components/AutonomousControlLoop";

const perceptionItems = [
  {
    icon: Eye,
    label: "Vision",
    value: "ACTIVE",
  },
  {
    icon: Mic,
    label: "Audio",
    value: "ACTIVE",
  },
  {
    icon: Radio,
    label: "Sensors",
    value: "2 INPUTS",
  },
  {
    icon: FileText,
    label: "OCR",
    value: "READY",
  },
];

const events = [
  {
    time: "23:02:03",
    type: "OBSERVATION",
    message: "Obstacle detected at 2.5 meters.",
    icon: Eye,
  },
  {
    time: "23:02:03",
    type: "REASONING",
    message: "Multimodal environment interpretation completed.",
    icon: Brain,
  },
  {
    time: "23:02:03",
    type: "PLANNING",
    message: "Avoid obstacle and select a safe path.",
    icon: Target,
  },
  {
    time: "23:02:03",
    type: "ACTION",
    message: "Safe path selected successfully.",
    icon: Zap,
  },
  {
    time: "23:02:03",
    type: "VERIFICATION",
    message: "Action verified with 94% confidence.",
    icon: CheckCircle2,
  },
];

function GlassPanel({ children, className = "" }) {
  return (
    <section
      className={`rounded-2xl border border-white/10 bg-slate-900/55 shadow-2xl shadow-black/20 backdrop-blur-xl ${className}`}
    >
      {children}
    </section>
  );
}

function PanelHeader({ eyebrow, title, icon: Icon }) {
  return (
    <div className="flex items-center justify-between border-b border-white/8 px-5 py-4">
      <div className="flex items-center gap-3">
        <div className="rounded-xl border border-cyan-400/15 bg-cyan-400/5 p-2">
          <Icon className="h-4 w-4 text-cyan-300" />
        </div>

        <div>
          <p className="text-[10px] font-semibold uppercase tracking-[0.22em] text-cyan-400/70">
            {eyebrow}
          </p>

          <h2 className="mt-0.5 text-sm font-semibold text-slate-100">
            {title}
          </h2>
        </div>
      </div>

      <span className="h-2 w-2 animate-pulse rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/60" />
    </div>
  );
}

function Dashboard() {
  return (
    <div className="min-h-screen overflow-x-hidden bg-[#020617] text-slate-100">
      <div className="pointer-events-none fixed inset-0 opacity-[0.035]">
        <div
          className="h-full w-full"
          style={{
            backgroundImage:
              "linear-gradient(rgba(56,189,248,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(56,189,248,0.5) 1px, transparent 1px)",
            backgroundSize: "50px 50px",
          }}
        />
      </div>

      <div className="relative mx-auto max-w-[1800px] px-4 py-4 sm:px-6 lg:px-8">
        <header className="mb-4 flex flex-col gap-4 rounded-2xl border border-white/10 bg-slate-900/65 px-5 py-4 shadow-2xl shadow-black/20 backdrop-blur-xl lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-center gap-4">
            <div className="relative flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-400/30 bg-cyan-400/5">
              <Sparkles className="h-6 w-6 text-cyan-300" />

              <span className="absolute -right-1 -top-1 h-3 w-3 animate-pulse rounded-full border-2 border-slate-950 bg-cyan-400" />
            </div>

            <div>
              <div className="flex items-center gap-3">
                <h1 className="text-xl font-bold tracking-[0.18em] text-white">
                  AEGIS
                </h1>

                <span className="rounded-full border border-emerald-400/20 bg-emerald-400/5 px-2.5 py-1 text-[9px] font-bold tracking-[0.18em] text-emerald-300">
                  ONLINE
                </span>
              </div>

              <p className="mt-1 text-xs text-slate-500">
                Autonomous Environment Grounded Intelligence System
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div className="rounded-xl border border-white/8 bg-white/[0.03] px-4 py-2">
              <p className="text-[9px] uppercase tracking-[0.2em] text-slate-500">
                Environment
              </p>

              <p className="mt-1 text-xs font-medium text-slate-200">
                WAREHOUSE / ZONE A
              </p>
            </div>

            <div className="rounded-xl border border-white/8 bg-white/[0.03] px-4 py-2">
              <p className="text-[9px] uppercase tracking-[0.2em] text-slate-500">
                Autonomous Cycle
              </p>

              <p className="mt-1 text-xs font-medium text-cyan-300">
                #001
              </p>
            </div>

            <button
              type="button"
              className="rounded-xl border border-cyan-400/20 bg-cyan-400/5 p-3 text-cyan-300 transition hover:border-cyan-300/40 hover:bg-cyan-400/10"
            >
              <Activity className="h-4 w-4" />
            </button>
          </div>
        </header>

        <div className="grid gap-4 xl:grid-cols-[250px_minmax(0,1fr)_300px]">
          <GlassPanel>
            <PanelHeader
              eyebrow="INPUT LAYER"
              title="Multimodal Perception"
              icon={ScanSearch}
            />

            <div className="space-y-2 p-4">
              {perceptionItems.map((item) => {
                const Icon = item.icon;

                return (
                  <div
                    key={item.label}
                    className="group flex items-center justify-between rounded-xl border border-white/7 bg-white/[0.025] px-3 py-3 transition hover:border-cyan-400/20 hover:bg-cyan-400/[0.04]"
                  >
                    <div className="flex items-center gap-3">
                      <Icon className="h-4 w-4 text-cyan-300/80 transition group-hover:text-cyan-300" />

                      <span className="text-xs font-medium text-slate-300">
                        {item.label}
                      </span>
                    </div>

                    <span className="text-[9px] font-bold tracking-wider text-emerald-300">
                      {item.value}
                    </span>
                  </div>
                );
              })}
            </div>

            <div className="border-t border-white/8 p-4">
              <div className="rounded-xl border border-cyan-400/10 bg-cyan-400/[0.03] p-4">
                <div className="mb-3 flex items-center justify-between">
                  <span className="text-[9px] uppercase tracking-[0.18em] text-slate-500">
                    World Confidence
                  </span>

                  <span className="text-sm font-bold text-cyan-300">
                    94.25%
                  </span>
                </div>

                <div className="h-1.5 overflow-hidden rounded-full bg-slate-800">
                  <div className="h-full w-[94.25%] rounded-full bg-cyan-400 shadow-lg shadow-cyan-400/40" />
                </div>

                <div className="mt-3 flex items-center justify-between text-[9px] text-slate-500">
                  <span>LOW UNCERTAINTY</span>
                  <span>0.0575</span>
                </div>
              </div>
            </div>
          </GlassPanel>

          <GlassPanel className="min-h-[500px] overflow-hidden">
            <PanelHeader
              eyebrow="ENVIRONMENT MODEL"
              title="Live World View"
              icon={Radio}
            />

            <div className="relative min-h-[440px] overflow-hidden bg-[#030b18]">
              <WorldView />

              <div className="pointer-events-none absolute bottom-5 left-5 z-10 flex items-center gap-2 rounded-lg border border-white/8 bg-black/30 px-3 py-2 backdrop-blur">
                <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />

                <span className="text-[9px] uppercase tracking-[0.18em] text-slate-400">
                  World model synchronized
                </span>
              </div>

              <div className="pointer-events-none absolute bottom-5 right-5 z-10 rounded-lg border border-white/8 bg-black/30 px-3 py-2 backdrop-blur">
                <span className="text-[9px] uppercase tracking-[0.18em] text-slate-500">
                  OBJECTS
                </span>

                <span className="ml-2 text-xs font-semibold text-slate-200">
                  3
                </span>
              </div>
            </div>
          </GlassPanel>

          <GlassPanel>
            <PanelHeader
              eyebrow="COGNITIVE LAYER"
              title="AI Brain"
              icon={Brain}
            />

            <div className="space-y-4 p-4">
              <div className="rounded-xl border border-white/8 bg-white/[0.025] p-4">
                <div className="flex items-center justify-between">
                  <span className="text-[9px] uppercase tracking-[0.18em] text-slate-500">
                    Reasoning
                  </span>

                  <span className="text-[9px] font-bold text-emerald-300">
                    GROUNDED
                  </span>
                </div>

                <p className="mt-3 text-xs leading-5 text-slate-300">
                  The environment contains a person and laptop.
                  Multimodal evidence confirms an obstacle in Zone A.
                </p>
              </div>

              <div className="rounded-xl border border-white/8 bg-white/[0.025] p-4">
                <div className="mb-4 flex items-center justify-between">
                  <span className="text-[9px] uppercase tracking-[0.18em] text-slate-500">
                    Confidence
                  </span>

                  <span className="text-lg font-bold text-cyan-300">
                    94.25%
                  </span>
                </div>

                <div className="space-y-3">
                  {[
                    ["Perception", "92.5%"],
                    ["Sensors", "95.0%"],
                    ["Events", "90.0%"],
                    ["Action", "100%"],
                    ["Verification", "100%"],
                  ].map(([label, value]) => (
                    <div key={label}>
                      <div className="mb-1 flex justify-between text-[9px]">
                        <span className="text-slate-500">
                          {label}
                        </span>

                        <span className="text-slate-300">
                          {value}
                        </span>
                      </div>

                      <div className="h-1 overflow-hidden rounded-full bg-slate-800">
                        <div
                          className="h-full rounded-full bg-cyan-400"
                          style={{
                            width: value,
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-xl border border-emerald-400/15 bg-emerald-400/[0.03] p-4">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="h-5 w-5 text-emerald-300" />

                  <div>
                    <p className="text-xs font-semibold text-emerald-200">
                      Action Verified
                    </p>

                    <p className="mt-1 text-[9px] text-slate-500">
                      Safe path selected · 94% confidence
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </GlassPanel>
        </div>

        <div className="mt-4">
          <AutonomousControlLoop />
        </div>

        <GlassPanel className="mt-4">
          <PanelHeader
            eyebrow="SYSTEM TELEMETRY"
            title="Live Event Stream"
            icon={Activity}
          />

          <div className="divide-y divide-white/6">
            {events.map((event) => {
              const Icon = event.icon;

              return (
                <div
                  key={`${event.time}-${event.type}`}
                  className="flex items-center gap-4 px-5 py-3.5 transition hover:bg-white/[0.02]"
                >
                  <span className="w-16 shrink-0 font-mono text-[9px] text-slate-600">
                    {event.time}
                  </span>

                  <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-white/8 bg-white/[0.03]">
                    <Icon className="h-3.5 w-3.5 text-cyan-300" />
                  </div>

                  <span className="w-24 shrink-0 text-[9px] font-bold tracking-[0.15em] text-cyan-400/70">
                    {event.type}
                  </span>

                  <p className="text-xs text-slate-400">
                    {event.message}
                  </p>
                </div>
              );
            })}
          </div>
        </GlassPanel>

        <footer className="flex flex-col items-center justify-between gap-2 px-2 py-5 text-[9px] uppercase tracking-[0.18em] text-slate-600 sm:flex-row">
          <span>
            AEGIS · Autonomous Environment Grounded Intelligence
          </span>

          <span>
            Backend status · Connected architecture ready
          </span>
        </footer>
      </div>
    </div>
  );
}

export default Dashboard;