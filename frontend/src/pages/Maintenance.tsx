import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import api from '@/lib/api';
import { Wrench, Plus, Calendar, Settings, Zap } from 'lucide-react';
import { format, parseISO } from 'date-fns';
import toast from 'react-hot-toast';
import { ScheduleMaintenanceModal } from '@/components/ui/ScheduleMaintenanceModal';

const TYPE_CONFIG: Record<string, { label: string; icon: React.ReactElement; cls: string }> = {
  predictive: {
    label: 'Predictive',
    icon: <Zap size={11} />,
    cls: 'bg-violet-500/12 text-violet-400 border-violet-500/25',
  },
  preventive: {
    label: 'Preventive',
    icon: <Calendar size={11} />,
    cls: 'bg-blue-500/12 text-blue-400 border-blue-500/25',
  },
  corrective: {
    label: 'Corrective',
    icon: <Settings size={11} />,
    cls: 'bg-orange-500/12 text-orange-400 border-orange-500/25',
  },
};

const STATUS_CONFIG: Record<string, { label: string; cls: string; dot: string }> = {
  completed: { label: 'Completed', cls: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20', dot: 'bg-emerald-400' },
  in_progress: { label: 'In Progress', cls: 'text-blue-400 bg-blue-500/10 border-blue-500/20', dot: 'bg-blue-400' },
  scheduled: { label: 'Scheduled', cls: 'text-amber-400 bg-amber-500/10 border-amber-500/20', dot: 'bg-amber-400' },
};

export default function Maintenance() {
  const [records, setRecords] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isScheduleModalOpen, setIsScheduleModalOpen] = useState(false);

  const fetchRecords = async () => {
    try {
      const res = await api.get('/maintenance');
      setRecords(res.data.items);
    } catch {
      toast.error('Failed to fetch maintenance records');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  const typeCounts = Object.keys(TYPE_CONFIG).reduce((acc, type) => {
    acc[type] = records.filter(r => r.type === type).length;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-wrap gap-4 items-end justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-5 bg-gradient-to-b from-orange-400 to-amber-400 rounded-full" />
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Operations</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100">Maintenance Intelligence</h1>
          <p className="text-sm text-slate-500 mt-0.5">Scheduled, predictive, and corrective task records.</p>
        </div>
        <Button size="sm" onClick={() => setIsScheduleModalOpen(true)}>
          <Plus size={13} className="mr-1.5" /> Schedule Task
        </Button>
      </div>

      <ScheduleMaintenanceModal 
        isOpen={isScheduleModalOpen} 
        onClose={() => setIsScheduleModalOpen(false)} 
        onSuccess={fetchRecords} 
      />

      {/* Type breakdown */}
      <div className="grid grid-cols-3 gap-3">
        {Object.entries(TYPE_CONFIG).map(([type, cfg]) => (
          <div key={type} className={`p-4 rounded-xl border bg-gradient-to-br ${cfg.cls} flex items-center gap-3`}
            style={{ background: undefined }}
          >
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${cfg.cls}`}>
              {cfg.icon}
            </div>
            <div>
              <div className="text-xl font-bold font-mono text-slate-200">{typeCounts[type] || 0}</div>
              <div className="text-xs text-slate-500">{cfg.label}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Table */}
      <Card>
        <CardHeader className="pb-4 border-b border-white/[0.06]">
          <CardTitle className="text-sm flex items-center gap-2">
            <Wrench size={14} className="text-orange-400" />
            Task Schedules
            {!loading && (
              <span className="badge bg-white/5 border border-white/8 text-slate-400 text-[10px] ml-1">
                {records.length} total
              </span>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {loading ? (
            <div className="p-6 space-y-3">
              {[1,2,3].map(i => <div key={i} className="skeleton h-12 rounded-xl" />)}
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="data-table w-full">
                <thead>
                  <tr>
                    <th>Task</th>
                    <th>Asset</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Scheduled Date</th>
                    <th className="text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {records.map((record, i) => {
                    const type = TYPE_CONFIG[record.type];
                    const status = STATUS_CONFIG[record.status] || STATUS_CONFIG.scheduled;
                    return (
                      <tr key={record.id} className="animate-fade-in" style={{ animationDelay: `${i * 0.04}s` }}>
                        <td>
                          <span className="text-sm font-medium text-slate-300">{record.title}</span>
                        </td>
                        <td>
                          <span className="text-xs text-blue-400 font-medium">{record.asset_name}</span>
                        </td>
                        <td>
                          {type && (
                            <span className={`badge border ${type.cls}`}>
                              {type.icon}
                              {type.label}
                            </span>
                          )}
                        </td>
                        <td>
                          <span className={`badge border ${status.cls}`}>
                            <div className={`status-dot ${status.dot}`} />
                            {status.label}
                          </span>
                        </td>
                        <td>
                          <span className="text-xs text-slate-400">
                            {record.scheduled_at
                              ? format(parseISO(record.scheduled_at), 'MMM dd, yyyy')
                              : 'TBD'}
                          </span>
                        </td>
                        <td className="text-right">
                          <Button variant="ghost" size="xs" className="text-blue-400 hover:text-blue-300 text-xs">
                            View Details
                          </Button>
                        </td>
                      </tr>
                    );
                  })}
                  {records.length === 0 && (
                    <tr>
                      <td colSpan={6} className="px-5 py-14 text-center">
                        <div className="flex flex-col items-center gap-3 text-slate-500">
                          <div className="w-12 h-12 rounded-2xl bg-white/4 border border-white/8 flex items-center justify-center">
                            <Wrench size={22} className="text-slate-600" />
                          </div>
                          <p className="text-sm text-slate-400">No maintenance records</p>
                          <p className="text-xs text-slate-600">Schedule your first task to get started</p>
                        </div>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
