import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import api from '@/lib/api';
import {
  CheckCircle2, AlertTriangle, Box, FileText, TrendingUp,
  Users, ShieldCheck, Activity, Settings, ArrowUpRight,
  Zap, Database, BarChart3, UserCheck, UserX, Clock,
} from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { useAuthStore } from '@/store/authStore';

// ─── Skeleton ─────────────────────────────────────────────────────────────
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

const ADMIN_METRICS = [
  { key: 'system_health', label: 'System Health', suffix: '%', icon: CheckCircle2, gradient: 'from-emerald-500/20 to-teal-500/10', border: 'border-emerald-500/20', iconColor: 'text-emerald-400', sub: 'Optimal performance' },
  { key: 'total_assets',  label: 'Total Resources', suffix: '', icon: Box, gradient: 'from-blue-500/20 to-cyan-500/10', border: 'border-blue-500/20', iconColor: 'text-blue-400', sub: 'All managed resources' },
  { key: 'open_incidents', label: 'Active Incidents', suffix: '', icon: AlertTriangle, gradient: 'from-red-500/20 to-orange-500/10', border: 'border-red-500/20', iconColor: 'text-red-400', sub: 'Requiring attention' },
  { key: 'total_documents', label: 'Documents', suffix: '', icon: FileText, gradient: 'from-violet-500/20 to-purple-500/10', border: 'border-violet-500/20', iconColor: 'text-violet-400', sub: 'Vectorized & mapped' },
];

const MOCK_USERS = [
  { name: 'Priya Sharma', role: 'engineer', status: 'active', lastSeen: '2 min ago' },
  { name: 'Rahul Gupta',  role: 'operator', status: 'active', lastSeen: '15 min ago' },
  { name: 'Ananya Patel', role: 'viewer',   status: 'inactive', lastSeen: '3 hrs ago' },
  { name: 'Vikram Nair',  role: 'admin',    status: 'active', lastSeen: 'Just now' },
];

const ROLE_COLORS: Record<string, string> = {
  admin:    'text-rose-400 bg-rose-500/10 border-rose-500/20',
  engineer: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
  operator: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  viewer:   'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
};

export default function AdminDashboard() {
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
            <div className="w-1.5 h-5 bg-gradient-to-b from-rose-400 to-pink-400 rounded-full" />
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Admin · Full Access</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Admin Control Center</h1>
          <p className="text-sm text-slate-500 mt-0.5">Welcome back, {user?.full_name} — all systems visible</p>
        </div>
        <div className="flex gap-3">
          <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full">
            <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
            Live · Auto-refreshing
          </div>
          <div className="flex items-center gap-2 text-xs text-rose-400 bg-rose-500/10 border border-rose-500/20 px-3 py-1.5 rounded-full">
            <ShieldCheck size={11} />
            Admin Mode
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {loading
          ? [0,1,2,3].map(i => <SkeletonCard key={i} />)
          : ADMIN_METRICS.map((cfg, i) => {
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

      {/* Admin-specific: System Overview + Users */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Alerts — 2 cols */}
        <Card className="lg:col-span-2 animate-fade-in stagger-3">
          <CardHeader className="pb-4 border-b border-white/[0.06]">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-red-500/15 flex items-center justify-center">
                  <AlertTriangle size={14} className="text-red-400" />
                </div>
                <div>
                  <CardTitle className="text-sm">Critical Alerts</CardTitle>
                  <CardDescription className="text-xs mt-0.5">Platform-wide — immediate action required</CardDescription>
                </div>
              </div>
              {alerts.length > 0 && (
                <span className="badge bg-red-500/15 text-red-400 border border-red-500/20">
                  {alerts.length} active
                </span>
              )}
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

        {/* Activity Feed */}
        <Card className="animate-fade-in stagger-4">
          <CardHeader className="pb-4 border-b border-white/[0.06]">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-blue-500/15 flex items-center justify-center">
                <Activity size={14} className="text-blue-400" />
              </div>
              <div>
                <CardTitle className="text-sm">Platform Activity</CardTitle>
                <CardDescription className="text-xs mt-0.5">All recent system events</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            {loading ? (
              <div className="space-y-4">{[1,2,3].map(i => (
                <div key={i} className="flex gap-3">
                  <div className="skeleton w-6 h-6 rounded-full shrink-0" />
                  <div className="flex-1 space-y-1.5">
                    <div className="skeleton h-3 w-full rounded" />
                    <div className="skeleton h-2.5 w-2/3 rounded" />
                  </div>
                </div>
              ))}</div>
            ) : activities.length === 0 ? (
              <div className="text-center py-8 text-slate-500">
                <Zap size={24} className="mx-auto mb-2 opacity-30" />
                <p className="text-sm">No recent activity</p>
              </div>
            ) : (
              <div className="space-y-4 relative">
                <div className="absolute left-[11px] top-3 bottom-3 w-px bg-gradient-to-b from-blue-500/30 via-blue-500/20 to-transparent" />
                {activities.map((activity, idx) => (
                  <div key={activity.id} className="flex gap-3 animate-fade-in" style={{ animationDelay: `${idx * 0.06}s` }}>
                    <div className="relative z-10 w-5 h-5 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center shrink-0 mt-0.5">
                      <Activity size={9} className="text-blue-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-medium text-slate-300 leading-snug">{activity.title}</p>
                      <p className="text-[11px] text-slate-600 mt-0.5">
                        {activity.timestamp ? formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true }) : ''}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Admin-only: User Management Preview + System Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* User Overview */}
        <Card className="animate-fade-in stagger-5">
          <CardHeader className="pb-4 border-b border-white/[0.06]">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-rose-500/15 flex items-center justify-center">
                  <Users size={14} className="text-rose-400" />
                </div>
                <div>
                  <CardTitle className="text-sm">Platform Users</CardTitle>
                  <CardDescription className="text-xs mt-0.5">Active user sessions</CardDescription>
                </div>
              </div>
              <button className="text-xs text-blue-400 hover:text-blue-300 transition-colors flex items-center gap-1">
                Manage <ArrowUpRight size={11} />
              </button>
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            <div className="space-y-3">
              {MOCK_USERS.map((u, i) => (
                <div key={i} className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-white/4 transition-colors">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500/30 to-violet-500/30 flex items-center justify-center text-xs font-bold text-white shrink-0">
                    {u.name.split(' ').map(n => n[0]).join('').slice(0,2)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-slate-200 truncate">{u.name}</p>
                    <p className="text-[11px] text-slate-500 mt-0.5 flex items-center gap-1">
                      <Clock size={9} /> {u.lastSeen}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] px-2 py-0.5 rounded-md border font-medium capitalize ${ROLE_COLORS[u.role]}`}>
                      {u.role}
                    </span>
                    {u.status === 'active'
                      ? <UserCheck size={13} className="text-emerald-400" />
                      : <UserX size={13} className="text-slate-500" />}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* System Stats — Admin only */}
        <Card className="animate-fade-in stagger-5">
          <CardHeader className="pb-4 border-b border-white/[0.06]">
            <div className="flex items-center gap-2.5">
              <div className="w-7 h-7 rounded-lg bg-indigo-500/15 flex items-center justify-center">
                <BarChart3 size={14} className="text-indigo-400" />
              </div>
              <div>
                <CardTitle className="text-sm">System Metrics</CardTitle>
                <CardDescription className="text-xs mt-0.5">Infrastructure health</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            <div className="space-y-4">
              {[
                { label: 'AI Engine Uptime',  value: 99.8, color: 'bg-emerald-500', textColor: 'text-emerald-400' },
                { label: 'DB Query Latency', value: 72,   color: 'bg-blue-500',    textColor: 'text-blue-400', suffix: 'ms' },
                { label: 'Vector Index',     value: 94,   color: 'bg-violet-500',  textColor: 'text-violet-400' },
                { label: 'Storage Used',     value: 61,   color: 'bg-amber-500',   textColor: 'text-amber-400' },
              ].map((item) => (
                <div key={item.label}>
                  <div className="flex justify-between mb-1.5">
                    <span className="text-xs text-slate-400">{item.label}</span>
                    <span className={`text-xs font-semibold font-mono ${item.textColor}`}>
                      {item.value}{item.suffix ?? '%'}
                    </span>
                  </div>
                  <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                    <div
                      className={`h-full rounded-full ${item.color} transition-all duration-1000`}
                      style={{ width: `${Math.min(item.value, 100)}%` }}
                    />
                  </div>
                </div>
              ))}
              <div className="pt-2 flex items-center gap-2 text-xs text-slate-500">
                <Database size={11} />
                <span>All metrics refreshed 30s ago</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
