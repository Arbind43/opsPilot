import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import api from '@/lib/api';
import {
  FileText, BarChart3, Eye, TrendingUp, PieChart,
  ArrowUpRight, Download, Calendar, CheckCircle2,
} from 'lucide-react';
import { useAuthStore } from '@/store/authStore';

function SkeletonCard() {
  return (
    <div className="rounded-2xl border border-white/[0.07] bg-[rgba(17,25,50,0.7)] p-6">
      <div className="flex justify-between items-start mb-4">
        <div className="skeleton h-3 w-24 rounded" />
        <div className="skeleton h-6 w-6 rounded-lg" />
      </div>
      <div className="skeleton h-8 w-20 rounded mb-2" />
      <div className="skeleton h-2.5 w-32 rounded" />
    </div>
  );
}

const VIEWER_METRICS = [
  { key: 'system_health',   label: 'System Health',  suffix: '%', icon: CheckCircle2, gradient: 'from-emerald-500/20 to-teal-500/10', border: 'border-emerald-500/20', iconColor: 'text-emerald-400', sub: 'Overall platform status' },
  { key: 'total_documents', label: 'Documents',       suffix: '',  icon: FileText,     gradient: 'from-violet-500/20 to-purple-500/10', border: 'border-violet-500/20', iconColor: 'text-violet-400', sub: 'In knowledge base' },
  { key: 'total_assets',    label: 'Monitored Assets', suffix: '', icon: BarChart3,    gradient: 'from-blue-500/20 to-cyan-500/10',    border: 'border-blue-500/20',   iconColor: 'text-blue-400',  sub: 'Total tracked resources' },
];

const MOCK_REPORTS = [
  { title: 'Monthly Operations Summary',  date: 'Jul 20, 2026', type: 'Operations', status: 'ready' },
  { title: 'Asset Health Report Q2',      date: 'Jul 15, 2026', type: 'Assets',     status: 'ready' },
  { title: 'Compliance Audit — Jul 2026', date: 'Jul 10, 2026', type: 'Compliance', status: 'ready' },
  { title: 'Incident Analysis Report',    date: 'Jul 05, 2026', type: 'Incidents',  status: 'ready' },
];

const REPORT_TYPE_COLORS: Record<string, string> = {
  Operations:  'text-blue-400 bg-blue-500/10 border-blue-500/20',
  Assets:      'text-amber-400 bg-amber-500/10 border-amber-500/20',
  Compliance:  'text-indigo-400 bg-indigo-500/10 border-indigo-500/20',
  Incidents:   'text-red-400 bg-red-500/10 border-red-500/20',
};

export default function ViewerDashboard() {
  const user = useAuthStore(s => s.user);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const statsRes = await api.get('/dashboard/stats');
        setStats(statsRes.data);
      } catch (err) {
        console.error('Dashboard fetch error:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="space-y-7 animate-fade-in">
      {/* Header */}
      <div className="flex items-end justify-between flex-wrap gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-5 bg-gradient-to-b from-emerald-400 to-teal-400 rounded-full" />
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Viewer · Read-Only Access</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Reports Overview</h1>
          <p className="text-sm text-slate-500 mt-0.5">Hello, {user?.full_name} — platform summary at a glance</p>
        </div>
        <div className="flex gap-3">
          <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full">
            <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
            Live
          </div>
          <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full">
            <Eye size={11} />
            Viewer Mode
          </div>
        </div>
      </div>

      {/* Info banner — read-only notice */}
      <div className="flex items-center gap-3 p-4 rounded-xl bg-emerald-500/8 border border-emerald-500/15">
        <Eye size={15} className="text-emerald-400 shrink-0" />
        <p className="text-sm text-emerald-300">
          You have <span className="font-semibold">read-only access</span>. You can view reports and documents, but cannot modify platform data.
        </p>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {loading
          ? [0,1,2].map(i => <SkeletonCard key={i} />)
          : VIEWER_METRICS.map((cfg, i) => {
              const Icon = cfg.icon;
              const value = stats?.[cfg.key];
              return (
                <div key={cfg.key} className={`metric-card bg-gradient-to-br ${cfg.gradient} border ${cfg.border} animate-fade-in stagger-${i+1} group cursor-default`}>
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-xs font-medium text-slate-400">{cfg.label}</span>
                    <div className={`w-8 h-8 rounded-xl bg-white/5 flex items-center justify-center ${cfg.iconColor} group-hover:scale-110 transition-transform`}>
                      <Icon size={15} />
                    </div>
                  </div>
                  <div className="text-3xl font-bold text-slate-100 mb-1 font-mono tracking-tight">
                    {value ?? '—'}{cfg.suffix}
                  </div>
                  <div className="flex items-center gap-1">
                    <TrendingUp size={11} className="text-emerald-400" />
                    <span className="text-[11px] text-slate-500">{cfg.sub}</span>
                  </div>
                  <div className={`absolute bottom-0 right-0 w-20 h-20 rounded-tl-3xl bg-gradient-to-br ${cfg.gradient} opacity-30 pointer-events-none`} />
                </div>
              );
            })}
      </div>

      {/* Reports List + Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Available Reports */}
        <Card className="lg:col-span-2 animate-fade-in stagger-3">
          <CardHeader className="pb-4 border-b border-white/[0.06]">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-pink-500/15 flex items-center justify-center">
                  <PieChart size={14} className="text-pink-400" />
                </div>
                <div>
                  <CardTitle className="text-sm">Available Reports</CardTitle>
                  <CardDescription className="text-xs mt-0.5">Download and review platform reports</CardDescription>
                </div>
              </div>
              <a href="/reports" className="text-xs text-blue-400 hover:text-blue-300 transition-colors flex items-center gap-1">
                All Reports <ArrowUpRight size={11} />
              </a>
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            <div className="space-y-3">
              {MOCK_REPORTS.map((report, i) => (
                <div key={i} className="flex items-center gap-3 p-3.5 rounded-xl bg-white/3 border border-white/[0.06] hover:bg-white/6 transition-colors">
                  <div className="w-9 h-9 rounded-xl bg-pink-500/10 border border-pink-500/15 flex items-center justify-center shrink-0">
                    <FileText size={14} className="text-pink-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-200 truncate">{report.title}</p>
                    <p className="text-[11px] text-slate-500 mt-0.5 flex items-center gap-1">
                      <Calendar size={9} /> {report.date}
                    </p>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className={`text-[10px] px-2 py-0.5 rounded-md border font-medium ${REPORT_TYPE_COLORS[report.type] ?? 'text-slate-400 bg-white/5 border-white/10'}`}>
                      {report.type}
                    </span>
                    <button className="p-1.5 rounded-lg bg-white/5 hover:bg-blue-500/15 text-slate-400 hover:text-blue-400 transition-colors">
                      <Download size={12} />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Platform Summary */}
        <Card className="animate-fade-in stagger-4">
          <CardHeader className="pb-4 border-b border-white/[0.06]">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-emerald-500/15 flex items-center justify-center">
                <BarChart3 size={14} className="text-emerald-400" />
              </div>
              <div>
                <CardTitle className="text-sm">Platform Summary</CardTitle>
                <CardDescription className="text-xs mt-0.5">High-level overview</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            <div className="space-y-4">
              {[
                { label: 'Platform Uptime',   value: 99.9, color: 'bg-emerald-500', textColor: 'text-emerald-400' },
                { label: 'Report Accuracy',   value: 97,   color: 'bg-blue-500',    textColor: 'text-blue-400' },
                { label: 'Data Freshness',    value: 92,   color: 'bg-violet-500',  textColor: 'text-violet-400' },
                { label: 'Coverage Index',    value: 85,   color: 'bg-pink-500',    textColor: 'text-pink-400' },
              ].map(item => (
                <div key={item.label}>
                  <div className="flex justify-between mb-1.5">
                    <span className="text-xs text-slate-400">{item.label}</span>
                    <span className={`text-xs font-semibold font-mono ${item.textColor}`}>{item.value}%</span>
                  </div>
                  <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                    <div className={`h-full rounded-full ${item.color} transition-all duration-1000`}
                      style={{ width: `${item.value}%` }} />
                  </div>
                </div>
              ))}

              <div className="pt-3 space-y-2 border-t border-white/[0.05] mt-3">
                {[
                  { label: 'Documents accessible', value: stats?.total_documents ?? '—' },
                  { label: 'Assets visible',       value: stats?.total_assets ?? '—' },
                ].map(item => (
                  <div key={item.label} className="flex justify-between text-xs">
                    <span className="text-slate-500">{item.label}</span>
                    <span className="text-slate-300 font-mono">{loading ? '…' : item.value}</span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
