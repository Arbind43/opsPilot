import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import api from '@/lib/api';
import {
  CheckCircle2, AlertTriangle, Box, FileText, TrendingUp, TrendingDown,
  Users, ShieldCheck, Activity, ArrowUpRight,
  Zap, Database, BarChart3, UserCheck, UserX, Clock, Sparkles,
} from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { useAuthStore } from '@/store/authStore';

function SkeletonCard() {
  return (
    <div className="rounded-2xl border border-white/[0.06] p-6" style={{ background: 'rgba(10,18,40,0.7)' }}>
      <div className="flex justify-between items-start mb-4">
        <div className="skeleton h-3 w-24 rounded" />
        <div className="skeleton h-8 w-8 rounded-xl" />
      </div>
      <div className="skeleton h-9 w-20 rounded mb-2" />
      <div className="skeleton h-2.5 w-32 rounded" />
    </div>
  );
}

const ADMIN_METRICS = [
  {
    key: 'system_health', label: 'System Health', suffix: '%',
    icon: CheckCircle2,
    cardClass: 'metric-card-emerald',
    iconBg: 'rgba(16,185,129,0.15)',
    iconColor: '#10b981',
    glow: 'rgba(16,185,129,0.15)',
    sub: 'All systems nominal',
    trend: '+2.1%',
    up: true,
  },
  {
    key: 'total_assets', label: 'Total Resources', suffix: '',
    icon: Box,
    cardClass: 'metric-card-blue',
    iconBg: 'rgba(59,130,246,0.15)',
    iconColor: '#3b82f6',
    glow: 'rgba(59,130,246,0.15)',
    sub: 'All managed assets',
    trend: '+12 this month',
    up: true,
  },
  {
    key: 'open_incidents', label: 'Active Incidents', suffix: '',
    icon: AlertTriangle,
    cardClass: 'metric-card-rose',
    iconBg: 'rgba(244,63,94,0.15)',
    iconColor: '#f43f5e',
    glow: 'rgba(244,63,94,0.15)',
    sub: 'Requiring attention',
    trend: '-3 from last week',
    up: false,
  },
  {
    key: 'total_documents', label: 'Documents', suffix: '',
    icon: FileText,
    cardClass: 'metric-card-violet',
    iconBg: 'rgba(139,92,246,0.15)',
    iconColor: '#8b5cf6',
    glow: 'rgba(139,92,246,0.15)',
    sub: 'Vectorized & indexed',
    trend: '+8 uploaded',
    up: true,
  },
];

const MOCK_USERS = [
  { name: 'Priya Sharma',  role: 'engineer', status: 'active',   lastSeen: '2 min ago' },
  { name: 'Rahul Gupta',   role: 'operator', status: 'active',   lastSeen: '15 min ago' },
  { name: 'Ananya Patel',  role: 'viewer',   status: 'inactive', lastSeen: '3 hrs ago' },
  { name: 'Vikram Nair',   role: 'admin',    status: 'active',   lastSeen: 'Just now' },
];

const ROLE_STYLES: Record<string, { text: string; bg: string; border: string }> = {
  admin:    { text: '#f87171', bg: 'rgba(244,63,94,0.12)',   border: 'rgba(244,63,94,0.25)' },
  engineer: { text: '#60a5fa', bg: 'rgba(59,130,246,0.12)',  border: 'rgba(59,130,246,0.25)' },
  operator: { text: '#fbbf24', bg: 'rgba(245,158,11,0.12)',  border: 'rgba(245,158,11,0.25)' },
  viewer:   { text: '#34d399', bg: 'rgba(16,185,129,0.12)',  border: 'rgba(16,185,129,0.25)' },
};

const SYSTEM_METRICS = [
  { label: 'AI Engine Uptime', value: 99.8, color: '#10b981', track: 'rgba(16,185,129,0.15)' },
  { label: 'DB Query Latency', value: 72,   color: '#3b82f6', track: 'rgba(59,130,246,0.15)', suffix: 'ms' },
  { label: 'Vector Index',     value: 94,   color: '#8b5cf6', track: 'rgba(139,92,246,0.15)' },
  { label: 'Storage Used',     value: 61,   color: '#f59e0b', track: 'rgba(245,158,11,0.15)' },
];

export default function AdminDashboard() {
  const user = useAuthStore(s => s.user);
  const [stats, setStats]         = useState<any>(null);
  const [activities, setActivities] = useState<any[]>([]);
  const [alerts, setAlerts]       = useState<any[]>([]);
  const [loading, setLoading]     = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const [s, a, al] = await Promise.all([
          api.get('/dashboard/stats'),
          api.get('/dashboard/activity'),
          api.get('/dashboard/alerts'),
        ]);
        setStats(s.data);
        setActivities(a.data.items);
        setAlerts(al.data.items);
      } catch { /* noop */ } finally { setLoading(false); }
    };
    fetch();
  }, []);

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';

  return (
    <div className="space-y-7 animate-fade-in">

      {/* ─── Header Banner ─────────────────────────────────── */}
      <div className="relative rounded-2xl overflow-hidden p-6 flex items-center justify-between"
        style={{
          background: 'linear-gradient(135deg, rgba(59,130,246,0.18) 0%, rgba(139,92,246,0.15) 50%, rgba(244,63,94,0.10) 100%)',
          border: '1px solid rgba(59,130,246,0.22)',
          boxShadow: '0 8px 32px rgba(59,130,246,0.12)',
        }}>
        {/* Decorative glows */}
        <div className="absolute top-0 left-0 w-48 h-48 rounded-full pointer-events-none"
          style={{ background: 'radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%)', transform: 'translate(-40%, -40%)' }} />
        <div className="absolute bottom-0 right-0 w-40 h-40 rounded-full pointer-events-none"
          style={{ background: 'radial-gradient(circle, rgba(139,92,246,0.12) 0%, transparent 70%)', transform: 'translate(30%, 30%)' }} />

        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-5 rounded-full" style={{ background: 'linear-gradient(180deg, #3b82f6, #8b5cf6)' }} />
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">Admin · Full Access</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-100 tracking-tight">
            {greeting}, <span className="gradient-text">{user?.full_name?.split(' ')[0]}</span> 👋
          </h1>
          <p className="text-sm text-slate-400 mt-1 font-medium">Here's your operations overview for today.</p>
        </div>
        <div className="relative z-10 hidden sm:flex gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-bold text-emerald-400"
            style={{ background: 'rgba(16,185,129,0.12)', border: '1px solid rgba(16,185,129,0.25)' }}>
            <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" style={{ boxShadow: '0 0 6px #10b981' }} />
            Live · Auto-refresh
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-bold text-rose-400"
            style={{ background: 'rgba(244,63,94,0.12)', border: '1px solid rgba(244,63,94,0.25)' }}>
            <ShieldCheck size={12} />
            Admin Mode
          </div>
        </div>
      </div>

      {/* ─── Metric Cards ───────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {loading
          ? [0,1,2,3].map(i => <SkeletonCard key={i} />)
          : ADMIN_METRICS.map((cfg, i) => {
              const Icon = cfg.icon;
              const val  = stats?.[cfg.key];
              return (
                <div key={cfg.key}
                  className={`metric-card ${cfg.cardClass} animate-fade-in stagger-${i+1}`}
                  style={{ boxShadow: `0 8px 24px ${cfg.glow}` }}>
                  <div className="flex items-start justify-between mb-5">
                    <div>
                      <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-0.5">{cfg.label}</p>
                    </div>
                    <div className="icon-box" style={{ background: cfg.iconBg, border: `1px solid ${cfg.iconColor}30` }}>
                      <Icon size={18} style={{ color: cfg.iconColor }} />
                    </div>
                  </div>
                  <div className="text-4xl font-extrabold text-slate-100 mono-num mb-2">
                    {val ?? '—'}{cfg.suffix}
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`stat-pill ${cfg.up ? 'stat-pill-up' : 'stat-pill-down'}`}>
                      {cfg.up ? <TrendingUp size={10} /> : <TrendingDown size={10} />}
                      {cfg.trend}
                    </span>
                    <span className="text-[11px] text-slate-500 font-medium">{cfg.sub}</span>
                  </div>
                  {/* Decorative corner */}
                  <div className="absolute -bottom-4 -right-4 w-20 h-20 rounded-full pointer-events-none opacity-30"
                    style={{ background: `radial-gradient(circle, ${cfg.iconColor} 0%, transparent 70%)` }} />
                </div>
              );
            })
        }
      </div>

      {/* ─── Alerts + Activity ─────────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">

        {/* Alerts */}
        <Card className="lg:col-span-2 animate-fade-in stagger-3">
          <CardHeader className="pb-4" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="icon-box-sm" style={{ background: 'rgba(244,63,94,0.15)', border: '1px solid rgba(244,63,94,0.25)' }}>
                  <AlertTriangle size={14} style={{ color: '#f43f5e' }} />
                </div>
                <div>
                  <CardTitle className="text-sm font-bold">Critical Alerts</CardTitle>
                  <CardDescription className="text-xs mt-0.5">Platform-wide — requires attention</CardDescription>
                </div>
              </div>
              {alerts.length > 0 && (
                <span className="badge text-rose-400" style={{ background: 'rgba(244,63,94,0.15)', border: '1px solid rgba(244,63,94,0.25)' }}>
                  {alerts.length} active
                </span>
              )}
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            {loading ? (
              <div className="space-y-3">{[1,2].map(i => <div key={i} className="skeleton h-16 rounded-xl" />)}</div>
            ) : alerts.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12">
                <div className="icon-box mb-3" style={{ background: 'rgba(16,185,129,0.12)', border: '1px solid rgba(16,185,129,0.22)' }}>
                  <CheckCircle2 size={20} style={{ color: '#10b981' }} />
                </div>
                <p className="text-sm font-bold text-slate-300">All systems nominal</p>
                <p className="text-xs text-slate-500 mt-1">No active alerts detected</p>
              </div>
            ) : (
              <div className="space-y-2.5">
                {alerts.map((alert, i) => (
                  <div key={alert.id}
                    className="flex items-start gap-3 p-4 rounded-xl hover:bg-rose-500/8 transition-colors animate-fade-in"
                    style={{ background: 'rgba(244,63,94,0.06)', border: '1px solid rgba(244,63,94,0.15)', animationDelay: `${i * 0.08}s` }}>
                    <div className="icon-box-sm shrink-0 mt-0.5" style={{ background: 'rgba(244,63,94,0.15)', border: '1px solid rgba(244,63,94,0.25)' }}>
                      <AlertTriangle size={13} style={{ color: '#f43f5e' }} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-bold text-slate-200 truncate">{alert.title}</p>
                      <p className="text-xs text-slate-500 mt-0.5">
                        {alert.timestamp ? formatDistanceToNow(new Date(alert.timestamp), { addSuffix: true }) : 'Just now'}
                      </p>
                    </div>
                    <button className="shrink-0 p-1.5 rounded-lg hover:bg-rose-500/20 text-slate-500 hover:text-rose-400 transition-colors">
                      <ArrowUpRight size={13} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Activity Feed */}
        <Card className="animate-fade-in stagger-4">
          <CardHeader className="pb-4" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
            <div className="flex items-center gap-3">
              <div className="icon-box-sm" style={{ background: 'rgba(59,130,246,0.15)', border: '1px solid rgba(59,130,246,0.25)' }}>
                <Activity size={14} style={{ color: '#3b82f6' }} />
              </div>
              <div>
                <CardTitle className="text-sm font-bold">Live Activity</CardTitle>
                <CardDescription className="text-xs mt-0.5">Recent system events</CardDescription>
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
              <div className="text-center py-8">
                <Zap size={24} className="mx-auto mb-2 text-slate-700" />
                <p className="text-sm text-slate-500">No recent activity</p>
              </div>
            ) : (
              <div className="space-y-4 relative">
                <div className="absolute left-[11px] top-3 bottom-3 w-px"
                  style={{ background: 'linear-gradient(180deg, #3b82f6 0%, rgba(59,130,246,0) 100%)' }} />
                {activities.map((act, idx) => (
                  <div key={act.id} className="flex gap-3 animate-fade-in" style={{ animationDelay: `${idx * 0.06}s` }}>
                    <div className="relative z-10 w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5"
                      style={{ background: 'rgba(59,130,246,0.2)', border: '1px solid rgba(59,130,246,0.4)' }}>
                      <Activity size={9} style={{ color: '#60a5fa' }} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-semibold text-slate-300 leading-snug">{act.title}</p>
                      <p className="text-[11px] text-slate-600 mt-0.5">
                        {act.timestamp ? formatDistanceToNow(new Date(act.timestamp), { addSuffix: true }) : ''}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* ─── Users + System Stats ───────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">

        {/* Platform Users */}
        <Card className="animate-fade-in stagger-5">
          <CardHeader className="pb-4" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="icon-box-sm" style={{ background: 'rgba(244,63,94,0.15)', border: '1px solid rgba(244,63,94,0.25)' }}>
                  <Users size={14} style={{ color: '#f43f5e' }} />
                </div>
                <div>
                  <CardTitle className="text-sm font-bold">Platform Users</CardTitle>
                  <CardDescription className="text-xs mt-0.5">Active user sessions</CardDescription>
                </div>
              </div>
              <Link to="/settings"
                className="flex items-center gap-1 text-xs font-bold transition-colors hover:text-blue-300"
                style={{ color: '#60a5fa' }}>
                Manage <ArrowUpRight size={11} />
              </Link>
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            <div className="space-y-2">
              {MOCK_USERS.map((u, i) => {
                const rs = ROLE_STYLES[u.role];
                return (
                  <div key={i}
                    className="flex items-center gap-3 p-3 rounded-xl hover-lift"
                    style={{ background: 'rgba(255,255,255,0.025)', border: '1px solid rgba(255,255,255,0.05)' }}>
                    <div className="w-9 h-9 rounded-xl flex items-center justify-center text-xs font-extrabold text-white shrink-0"
                      style={{ background: 'linear-gradient(135deg, rgba(59,130,246,0.3), rgba(139,92,246,0.3))', border: '1px solid rgba(255,255,255,0.1)' }}>
                      {u.name.split(' ').map(n => n[0]).join('').slice(0,2)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-bold text-slate-200 truncate">{u.name}</p>
                      <p className="text-[11px] text-slate-500 mt-0.5 flex items-center gap-1">
                        <Clock size={9} /> {u.lastSeen}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] px-2 py-0.5 rounded-lg font-bold capitalize"
                        style={{ color: rs.text, background: rs.bg, border: `1px solid ${rs.border}` }}>
                        {u.role}
                      </span>
                      {u.status === 'active'
                        ? <UserCheck size={13} className="text-emerald-400" />
                        : <UserX size={13} className="text-slate-500" />}
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* System Metrics */}
        <Card className="animate-fade-in stagger-5">
          <CardHeader className="pb-4" style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
            <div className="flex items-center gap-3">
              <div className="icon-box-sm" style={{ background: 'rgba(99,102,241,0.15)', border: '1px solid rgba(99,102,241,0.25)' }}>
                <BarChart3 size={14} style={{ color: '#818cf8' }} />
              </div>
              <div>
                <CardTitle className="text-sm font-bold">System Metrics</CardTitle>
                <CardDescription className="text-xs mt-0.5">Infrastructure health snapshot</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="pt-5">
            <div className="space-y-5">
              {SYSTEM_METRICS.map(item => (
                <div key={item.label}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-semibold text-slate-400">{item.label}</span>
                    <span className="text-sm font-extrabold mono-num" style={{ color: item.color }}>
                      {item.value}{item.suffix ?? '%'}
                    </span>
                  </div>
                  <div className="h-2 rounded-full overflow-hidden" style={{ background: item.track }}>
                    <div className="h-full rounded-full transition-all duration-1000"
                      style={{ width: `${Math.min(item.value, 100)}%`, background: `linear-gradient(90deg, ${item.color}, ${item.color}aa)`, boxShadow: `0 0 8px ${item.color}60` }} />
                  </div>
                </div>
              ))}
              <div className="flex items-center gap-2 pt-1 text-xs text-slate-600">
                <Database size={11} />
                <span>All metrics refreshed 30s ago</span>
                <div className="ml-auto flex items-center gap-1 text-emerald-500 font-semibold">
                  <Sparkles size={10} />
                  <span className="text-[10px]">AI Monitored</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
