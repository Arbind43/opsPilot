import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import api from '@/lib/api';
import {
  CheckCircle2, AlertTriangle, Box, FileText, TrendingUp,
  Activity, ArrowUpRight, Zap, Cpu, Network, Shield,
  ClipboardCheck, Wrench,
} from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
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

const ENG_METRICS = [
  { key: 'system_health',   label: 'System Health',    suffix: '%', icon: CheckCircle2, gradient: 'from-emerald-500/20 to-teal-500/10', border: 'border-emerald-500/20', iconColor: 'text-emerald-400', sub: 'Infrastructure status' },
  { key: 'open_incidents',  label: 'Active Incidents', suffix: '',  icon: AlertTriangle, gradient: 'from-red-500/20 to-orange-500/10',  border: 'border-red-500/20',    iconColor: 'text-red-400',   sub: 'Awaiting resolution' },
  { key: 'total_assets',    label: 'Assets Tracked',   suffix: '',  icon: Box,           gradient: 'from-blue-500/20 to-cyan-500/10',   border: 'border-blue-500/20',   iconColor: 'text-blue-400',  sub: 'Monitored resources' },
  { key: 'total_documents', label: 'Knowledge Docs',   suffix: '',  icon: FileText,      gradient: 'from-violet-500/20 to-purple-500/10', border: 'border-violet-500/20', iconColor: 'text-violet-400', sub: 'In knowledge base' },
];

const TECH_STATUS = [
  { label: 'Compliance Score',   value: 94, color: 'bg-indigo-500', textColor: 'text-indigo-400' },
  { label: 'Incident MTTR',      value: 78, color: 'bg-blue-500',   textColor: 'text-blue-400',   suffix: 'min avg' },
  { label: 'Asset Health Index', value: 88, color: 'bg-emerald-500',textColor: 'text-emerald-400' },
  { label: 'Graph Coverage',     value: 72, color: 'bg-cyan-500',   textColor: 'text-cyan-400' },
];

export default function EngineerDashboard() {
  const user = useAuthStore(s => s.user);
  const [stats, setStats] = useState<any>(null);
  const [activities, setActivities] = useState<any[]>([]);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, activityRes, alertsRes] = await Promise.all([
          api.get('/dashboard/stats'),
          api.get('/dashboard/activity'),
          api.get('/dashboard/alerts'),
        ]);
        setStats(statsRes.data);
        setActivities(activityRes.data.items);
        setAlerts(alertsRes.data.items);
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
            <div className="w-1.5 h-5 bg-gradient-to-b from-blue-400 to-indigo-400 rounded-full" />
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Engineering · Technical Access</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Engineering Dashboard</h1>
          <p className="text-sm text-slate-500 mt-0.5">Hey {user?.full_name} — here's your technical snapshot</p>
        </div>
        <div className="flex gap-3">
          <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full">
            <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
            Live
          </div>
          <div className="flex items-center gap-2 text-xs text-blue-400 bg-blue-500/10 border border-blue-500/20 px-3 py-1.5 rounded-full">
            <Cpu size={11} />
            Engineer Mode
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {loading
          ? [0,1,2,3].map(i => <SkeletonCard key={i} />)
          : ENG_METRICS.map((cfg, i) => {
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

      {/* Engineer Quick Access Modules */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { icon: AlertTriangle, label: 'Incidents', path: '/incidents', color: 'text-red-400', bg: 'bg-red-500/10 border-red-500/20' },
          { icon: Shield,        label: 'Compliance', path: '/compliance', color: 'text-indigo-400', bg: 'bg-indigo-500/10 border-indigo-500/20' },
          { icon: Network,       label: 'Knowledge Graph', path: '/graph', color: 'text-cyan-400', bg: 'bg-cyan-500/10 border-cyan-500/20' },
          { icon: Wrench,        label: 'Maintenance', path: '/maintenance', color: 'text-orange-400', bg: 'bg-orange-500/10 border-orange-500/20' },
        ].map((item) => (
          <a key={item.path} href={item.path}
            className={`flex flex-col items-center justify-center gap-2 p-4 rounded-xl border ${item.bg} hover:scale-[1.03] transition-all duration-200 cursor-pointer`}>
            <item.icon size={20} className={item.color} />
            <span className="text-xs font-medium text-slate-300 text-center">{item.label}</span>
          </a>
        ))}
      </div>

      {/* Lower Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Alerts */}
        <Card className="lg:col-span-2 animate-fade-in stagger-3">
          <CardHeader className="pb-4 border-b border-white/[0.06]">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-red-500/15 flex items-center justify-center">
                  <AlertTriangle size={14} className="text-red-400" />
                </div>
                <div>
                  <CardTitle className="text-sm">Technical Alerts</CardTitle>
                  <CardDescription className="text-xs mt-0.5">Engineering-level issues requiring attention</CardDescription>
                </div>
              </div>
              {alerts.length > 0 && <span className="badge bg-red-500/15 text-red-400 border border-red-500/20">{alerts.length} active</span>}
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            {loading ? (
              <div className="space-y-3">{[1,2].map(i => <div key={i} className="skeleton h-14 rounded-xl" />)}</div>
            ) : alerts.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-10 text-slate-500">
                <CheckCircle2 size={32} className="text-emerald-500/40 mb-2" />
                <p className="text-sm font-medium text-slate-400">All systems nominal</p>
                <p className="text-xs text-slate-500 mt-1">No active alerts detected</p>
              </div>
            ) : (
              <div className="space-y-2.5">
                {alerts.map((alert, i) => (
                  <div key={alert.id}
                    className="flex items-start gap-3 p-3.5 rounded-xl bg-red-500/8 border border-red-500/15 hover:bg-red-500/12 transition-colors animate-fade-in"
                    style={{ animationDelay: `${i * 0.08}s` }}>
                    <div className="w-7 h-7 rounded-lg bg-red-500/15 flex items-center justify-center shrink-0 mt-0.5">
                      <AlertTriangle size={13} className="text-red-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-red-200 truncate">{alert.title}</p>
                      <p className="text-xs text-red-400/70 mt-0.5">
                        {alert.timestamp ? formatDistanceToNow(new Date(alert.timestamp), { addSuffix: true }) : 'Just now'}
                      </p>
                    </div>
                    <button className="shrink-0 p-1.5 rounded-lg hover:bg-red-500/20 text-red-400 transition-colors">
                      <ArrowUpRight size={12} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Technical Health */}
        <Card className="animate-fade-in stagger-4">
          <CardHeader className="pb-4 border-b border-white/[0.06]">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-blue-500/15 flex items-center justify-center">
                <Cpu size={14} className="text-blue-400" />
              </div>
              <div>
                <CardTitle className="text-sm">Technical Health</CardTitle>
                <CardDescription className="text-xs mt-0.5">Engineering KPIs</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            <div className="space-y-4">
              {TECH_STATUS.map(item => (
                <div key={item.label}>
                  <div className="flex justify-between mb-1.5">
                    <span className="text-xs text-slate-400">{item.label}</span>
                    <span className={`text-xs font-semibold font-mono ${item.textColor}`}>
                      {item.value}{item.suffix ? ` ${item.suffix}` : '%'}
                    </span>
                  </div>
                  <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                    <div className={`h-full rounded-full ${item.color} transition-all duration-1000`}
                      style={{ width: `${Math.min(item.value, 100)}%` }} />
                  </div>
                </div>
              ))}
            </div>

            {/* Recent activity below */}
            <div className="pt-5 border-t border-white/[0.05] mt-5">
              <p className="text-[10px] font-semibold text-slate-600 uppercase tracking-widest mb-3">Recent Activity</p>
              {loading ? (
                <div className="space-y-3">{[1,2,3].map(i => <div key={i} className="skeleton h-3 rounded" />)}</div>
              ) : (
                <div className="space-y-3">
                  {activities.slice(0,4).map((a, idx) => (
                    <div key={a.id} className="flex gap-2">
                      <div className="relative z-10 w-4 h-4 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center shrink-0 mt-0.5">
                        <Activity size={8} className="text-blue-400" />
                      </div>
                      <div>
                        <p className="text-[11px] text-slate-300 leading-snug">{a.title}</p>
                        <p className="text-[10px] text-slate-600 mt-0.5">
                          {a.timestamp ? formatDistanceToNow(new Date(a.timestamp), { addSuffix: true }) : ''}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
