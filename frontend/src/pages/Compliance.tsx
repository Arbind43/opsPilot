import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import api from '@/lib/api';
import { ShieldCheck, Loader2, AlertCircle, CheckCircle2, ShieldAlert, TrendingUp } from 'lucide-react';

const STATUS_CONFIG: Record<string, {
  icon: JSX.Element;
  badgeCls: string;
  bgCls: string;
  label: string;
}> = {
  compliant: {
    icon: <CheckCircle2 size={16} className="text-emerald-400" />,
    badgeCls: 'bg-emerald-500/12 text-emerald-400 border-emerald-500/25',
    bgCls: 'from-emerald-500/10 to-emerald-500/5 border-emerald-500/25',
    label: 'Compliant',
  },
  warning: {
    icon: <AlertCircle size={16} className="text-amber-400" />,
    badgeCls: 'bg-amber-500/12 text-amber-400 border-amber-500/25',
    bgCls: 'from-amber-500/10 to-amber-500/5 border-amber-500/25',
    label: 'Warning',
  },
  'non-compliant': {
    icon: <ShieldAlert size={16} className="text-red-400" />,
    badgeCls: 'bg-red-500/12 text-red-400 border-red-500/25',
    bgCls: 'from-red-500/10 to-red-500/5 border-red-500/25',
    label: 'Non-Compliant',
  },
};

export default function Compliance() {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchReport = async () => {
    setLoading(true);
    try {
      const res = await api.get('/compliance/report');
      setReport(res.data);
    } catch {
      console.error('Failed to fetch compliance report');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchReport(); }, []);

  const overallCfg = STATUS_CONFIG[report?.status] || STATUS_CONFIG.compliant;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-wrap gap-4 items-end justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-5 bg-gradient-to-b from-indigo-400 to-violet-400 rounded-full" />
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Compliance</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100">Compliance Checking</h1>
          <p className="text-sm text-slate-500 mt-0.5">AI evaluation against regulatory standards and quality frameworks.</p>
        </div>
        <Button
          onClick={fetchReport}
          disabled={loading}
          size="sm"
          className="bg-gradient-to-r from-indigo-500 to-violet-500 shadow-[0_4px_14px_rgba(99,102,241,0.3)]"
        >
          {loading
            ? <Loader2 size={13} className="animate-spin mr-2" />
            : <ShieldCheck size={13} className="mr-2" />}
          Run Audit
        </Button>
      </div>

      {loading ? (
        <Card className="flex flex-col items-center justify-center py-20">
          <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mb-4">
            <Loader2 size={24} className="animate-spin text-indigo-400" />
          </div>
          <p className="text-sm font-medium text-slate-400">Running compliance audit...</p>
          <p className="text-xs text-slate-600 mt-1">Evaluating knowledge base against regulatory standards</p>
        </Card>
      ) : report ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {/* Score card */}
          <div className={`rounded-2xl p-6 bg-gradient-to-br border ${overallCfg.bgCls} flex flex-col items-center justify-center text-center animate-scale-in`}>
            <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-4">
              <ShieldCheck size={22} className="text-indigo-400" />
            </div>
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-3">Compliance Score</p>
            <div className={`text-6xl font-black font-mono mb-3 ${
              report.status === 'compliant' ? 'text-emerald-400'
              : report.status === 'warning' ? 'text-amber-400'
              : 'text-red-400'
            }`}>
              {report.overall_score}
            </div>
            <div className={`badge border ${overallCfg.badgeCls}`}>
              {overallCfg.icon}
              <span className="ml-1">{overallCfg.label}</span>
            </div>
            {/* Mini bar */}
            <div className="w-full mt-5 bg-white/5 rounded-full h-1.5">
              <div
                className={`h-1.5 rounded-full transition-all duration-700 ${
                  report.status === 'compliant'
                    ? 'bg-gradient-to-r from-emerald-500 to-teal-400'
                    : report.status === 'warning'
                    ? 'bg-gradient-to-r from-amber-500 to-yellow-400'
                    : 'bg-gradient-to-r from-red-500 to-orange-400'
                }`}
                style={{ width: `${report.overall_score}%` }}
              />
            </div>
            <div className="flex items-center gap-1 mt-2">
              <TrendingUp size={11} className="text-emerald-400" />
              <span className="text-[10px] text-slate-500">Based on {report.evaluations?.length || 0} evaluations</span>
            </div>
          </div>

          {/* Evaluations */}
          <Card className="md:col-span-2 animate-fade-in stagger-2">
            <CardHeader className="pb-4 border-b border-white/[0.06]">
              <CardTitle className="text-sm">Detailed Evaluations</CardTitle>
              <CardDescription className="text-xs">Results mapped to regulatory clauses</CardDescription>
            </CardHeader>
            <CardContent className="pt-4 p-0">
              <div className="divide-y divide-white/[0.04]">
                {report.evaluations?.map((evalItem: any, idx: number) => {
                  const cfg = STATUS_CONFIG[evalItem.status] || STATUS_CONFIG.compliant;
                  return (
                    <div
                      key={idx}
                      className="flex items-start gap-4 p-5 hover:bg-white/[0.02] transition-colors animate-fade-in"
                      style={{ animationDelay: `${idx * 0.06}s` }}
                    >
                      <div className="shrink-0 mt-0.5">{cfg.icon}</div>
                      <div className="flex-1 min-w-0">
                        <div className="flex flex-wrap items-start gap-2 justify-between mb-1.5">
                          <h3 className="text-sm font-semibold text-slate-200">{evalItem.standard}</h3>
                          <span className={`badge border text-[10px] shrink-0 ${cfg.badgeCls}`}>
                            {evalItem.status.replace('-', ' ')}
                          </span>
                        </div>
                        <p className="text-xs text-slate-500 font-medium mb-2">
                          Clause: <span className="text-slate-400">{evalItem.clause}</span>
                        </p>
                        <p className="text-xs text-slate-500 bg-white/[0.02] border border-white/[0.06] p-3 rounded-xl leading-relaxed">
                          {evalItem.details}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </div>
      ) : (
        <Card className="p-12 text-center text-slate-500">
          Failed to load compliance report.
        </Card>
      )}
    </div>
  );
}
