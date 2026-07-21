import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import api from '@/lib/api';
import {
  AlertTriangle, Box, CheckCircle2, TrendingUp, Wrench,
  Activity, ArrowUpRight, Zap, ClipboardList, Calendar,
  PlayCircle, Clock, CheckSquare,
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

const OP_METRICS = [
  { key: 'total_assets',  label: 'Assets in Scope',  suffix: '', icon: Box,           gradient: 'from-amber-500/20 to-orange-500/10', border: 'border-amber-500/20',  iconColor: 'text-amber-400',   sub: 'Operational resources' },
  { key: 'open_incidents', label: 'Open Incidents',  suffix: '', icon: AlertTriangle,  gradient: 'from-red-500/20 to-orange-500/10',   border: 'border-red-500/20',    iconColor: 'text-red-400',     sub: 'Needs attention' },
  { key: 'system_health', label: 'Ops Health',       suffix: '%', icon: CheckCircle2,  gradient: 'from-emerald-500/20 to-teal-500/10', border: 'border-emerald-500/20', iconColor: 'text-emerald-400', sub: 'Overall status' },
  { key: 'total_documents', label: 'Runbooks',       suffix: '', icon: ClipboardList,  gradient: 'from-orange-500/20 to-amber-500/10', border: 'border-orange-500/20', iconColor: 'text-orange-400',  sub: 'Available procedures' },
];

const MOCK_TASKS = [
  { task: 'Inspect Pump Station 3', priority: 'high',   status: 'in-progress', due: 'Today 14:00' },
  { task: 'Replace Filter Unit F-12', priority: 'medium', status: 'pending',   due: 'Tomorrow 09:00' },
  { task: 'Calibrate Sensor Array', priority: 'low',    status: 'pending',     due: 'Jul 25' },
  { task: 'Emergency Valve Check',  priority: 'high',   status: 'overdue',     due: 'Yesterday' },
];

const PRIORITY_STYLES: Record<string, string> = {
  high:   'text-red-400 bg-red-500/10 border-red-500/20',
  medium: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  low:    'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
};

const STATUS_ICON: Record<string, React.ReactNode> = {
  'in-progress': <PlayCircle size={12} className="text-blue-400" />,
  'pending':     <Clock      size={12} className="text-amber-400" />,
  'overdue':     <AlertTriangle size={12} className="text-red-400" />,
  'done':        <CheckSquare  size={12} className="text-emerald-400" />,
};

export default function OperatorDashboard() {
  const user = useAuthStore(s => s.user);
  const [stats, setStats] = useState<any>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [activities, setActivities] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, alertsRes, activityRes] = await Promise.all([
          api.get('/dashboard/stats'),
          api.get('/dashboard/alerts'),
          api.get('/dashboard/activity'),
        ]);
        setStats(statsRes.data);
        setAlerts(alertsRes.data.items);
        setActivities(activityRes.data.items);
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
            <div className="w-1.5 h-5 bg-gradient-to-b from-amber-400 to-orange-400 rounded-full" />
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-widest">Operations · Field Access</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Operations Dashboard</h1>
          <p className="text-sm text-slate-500 mt-0.5">Good to see you, {user?.full_name} — your shift at a glance</p>
        </div>
        <div className="flex gap-3">
          <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full">
            <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse" />
            Live
          </div>
          <div className="flex items-center gap-2 text-xs text-amber-400 bg-amber-500/10 border border-amber-500/20 px-3 py-1.5 rounded-full">
            <Wrench size={11} />
            Operator Mode
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {loading
          ? [0,1,2,3].map(i => <SkeletonCard key={i} />)
          : OP_METRICS.map((cfg, i) => {
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

      {/* Quick Actions */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {[
          { icon: AlertTriangle, label: 'Log Incident',    color: 'text-red-400',    bg: 'bg-red-500/10 border-red-500/20' },
          { icon: Wrench,        label: 'Add Maintenance', color: 'text-orange-400', bg: 'bg-orange-500/10 border-orange-500/20' },
          { icon: Calendar,      label: 'Schedule Task',   color: 'text-blue-400',   bg: 'bg-blue-500/10 border-blue-500/20' },
        ].map((item) => (
          <button key={item.label}
            className={`flex items-center justify-center gap-2.5 p-3.5 rounded-xl border ${item.bg} hover:scale-[1.02] hover:brightness-110 transition-all duration-200`}>
            <item.icon size={16} className={item.color} />
            <span className="text-sm font-medium text-slate-300">{item.label}</span>
          </button>
        ))}
      </div>

      {/* Lower Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Maintenance Tasks — operator primary view */}
        <Card className="lg:col-span-2 animate-fade-in stagger-3">
          <CardHeader className="pb-4 border-b border-white/[0.06]">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-7 h-7 rounded-lg bg-amber-500/15 flex items-center justify-center">
                  <Wrench size={14} className="text-amber-400" />
                </div>
                <div>
                  <CardTitle className="text-sm">My Task Queue</CardTitle>
                  <CardDescription className="text-xs mt-0.5">Maintenance tasks assigned to you</CardDescription>
                </div>
              </div>
              <a href="/maintenance" className="text-xs text-blue-400 hover:text-blue-300 transition-colors flex items-center gap-1">
                View All <ArrowUpRight size={11} />
              </a>
            </div>
          </CardHeader>
          <CardContent className="pt-4">
            <div className="space-y-3">
              {MOCK_TASKS.map((task, i) => (
                <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-white/3 border border-white/[0.06] hover:bg-white/5 transition-colors">
                  <div className="flex items-center gap-1.5 shrink-0">
                    {STATUS_ICON[task.status]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-slate-200 truncate">{task.task}</p>
                    <p className="text-[11px] text-slate-500 mt-0.5 flex items-center gap-1">
                      <Clock size={9} /> Due: {task.due}
                    </p>
                  </div>
                  <span className={`text-[10px] px-2 py-0.5 rounded-md border font-medium capitalize ${PRIORITY_STYLES[task.priority]}`}>
                    {task.priority}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Active Alerts + Activity */}
        <div className="space-y-5">
          <Card className="animate-fade-in stagger-4">
            <CardHeader className="pb-3 border-b border-white/[0.06]">
              <div className="flex items-center gap-2.5">
                <div className="w-6 h-6 rounded-lg bg-red-500/15 flex items-center justify-center">
                  <AlertTriangle size={13} className="text-red-400" />
                </div>
                <CardTitle className="text-sm">Active Alerts</CardTitle>
                {alerts.length > 0 && <span className="ml-auto badge bg-red-500/15 text-red-400 border border-red-500/20">{alerts.length}</span>}
              </div>
            </CardHeader>
            <CardContent className="pt-3">
              {loading ? (
                <div className="space-y-2">{[1,2].map(i => <div key={i} className="skeleton h-10 rounded-lg" />)}</div>
              ) : alerts.length === 0 ? (
                <div className="py-6 text-center">
                  <CheckCircle2 size={24} className="text-emerald-500/40 mx-auto mb-1.5" />
                  <p className="text-xs text-slate-400">All clear</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {alerts.slice(0, 3).map((alert, i) => (
                    <div key={alert.id} className="flex items-start gap-2.5 p-2.5 rounded-lg bg-red-500/8 border border-red-500/15">
                      <AlertTriangle size={12} className="text-red-400 mt-0.5 shrink-0" />
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-medium text-red-200 truncate">{alert.title}</p>
                        <p className="text-[10px] text-red-400/60 mt-0.5">
                          {alert.timestamp ? formatDistanceToNow(new Date(alert.timestamp), { addSuffix: true }) : 'Just now'}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="animate-fade-in stagger-5">
            <CardHeader className="pb-3 border-b border-white/[0.06]">
              <div className="flex items-center gap-2.5">
                <div className="w-6 h-6 rounded-lg bg-blue-500/15 flex items-center justify-center">
                  <Activity size={13} className="text-blue-400" />
                </div>
                <CardTitle className="text-sm">Shift Activity</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="pt-3">
              {loading ? (
                <div className="space-y-3">{[1,2,3].map(i => <div key={i} className="skeleton h-3 rounded" />)}</div>
              ) : activities.length === 0 ? (
                <div className="py-4 text-center">
                  <Zap size={20} className="text-slate-600 mx-auto mb-1" />
                  <p className="text-xs text-slate-500">No activity yet</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {activities.slice(0, 4).map((a, idx) => (
                    <div key={a.id} className="flex gap-2">
                      <div className="w-4 h-4 rounded-full bg-amber-500/20 border border-amber-500/30 flex items-center justify-center shrink-0 mt-0.5">
                        <Activity size={8} className="text-amber-400" />
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
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
