import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import api from '@/lib/api';
import { AlertTriangle, Plus, Loader2, Sparkles, CheckCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import toast from 'react-hot-toast';
import { ReportIncidentModal } from '@/components/ui/ReportIncidentModal';

const SEVERITY_CONFIG: Record<string, { label: string; cls: string; dot: string }> = {
  critical: {
    label: 'Critical',
    cls: 'bg-red-500/15 text-red-400 border-red-500/25',
    dot: 'bg-red-400',
  },
  high: {
    label: 'High',
    cls: 'bg-orange-500/15 text-orange-400 border-orange-500/25',
    dot: 'bg-orange-400',
  },
  medium: {
    label: 'Medium',
    cls: 'bg-amber-500/15 text-amber-400 border-amber-500/25',
    dot: 'bg-amber-400',
  },
  low: {
    label: 'Low',
    cls: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/25',
    dot: 'bg-emerald-400',
  },
};

function SeverityBadge({ severity }: { severity: string }) {
  const cfg = SEVERITY_CONFIG[severity] || SEVERITY_CONFIG.medium;
  return (
    <span className={`badge border ${cfg.cls}`}>
      <div className={`status-dot ${cfg.dot}`} />
      {cfg.label}
    </span>
  );
}

function IncidentCard({ incident, onGenerateRca, generatingRcaId }: any) {
  const [rcaOpen, setRcaOpen] = useState(false);
  const isGenerating = generatingRcaId === incident.id;

  return (
    <div className="p-5 rounded-xl bg-white/[0.02] border border-white/[0.06] hover:border-white/10 transition-all duration-200 animate-fade-in">
      <div className="flex items-start justify-between gap-4 mb-3">
        <div className="flex-1 min-w-0">
          <div className="flex flex-wrap items-center gap-2 mb-1.5">
            <h3 className="text-sm font-semibold text-slate-200 truncate">{incident.title}</h3>
            <SeverityBadge severity={incident.severity} />
          </div>
          <div className="flex items-center gap-3 text-xs text-slate-500">
            <span>
              Asset: <span className="text-blue-400 font-medium">{incident.asset_name}</span>
            </span>
            <span className="text-slate-700">·</span>
            <span>
              {incident.created_at
                ? formatDistanceToNow(new Date(incident.created_at), { addSuffix: true })
                : 'Recently'}
            </span>
          </div>
        </div>
        <div className="shrink-0">
          {incident.root_cause ? (
            <button
              onClick={() => setRcaOpen(!rcaOpen)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium hover:bg-emerald-500/15 transition-colors"
            >
              <CheckCircle size={12} />
              RCA Complete
              {rcaOpen ? <ChevronUp size={11} /> : <ChevronDown size={11} />}
            </button>
          ) : (
            <Button
              size="sm"
              variant="outline"
              onClick={() => onGenerateRca(incident.id)}
              disabled={isGenerating}
              className="text-xs border-violet-500/30 text-violet-400 hover:bg-violet-500/10 hover:border-violet-500/50"
            >
              {isGenerating ? (
                <Loader2 size={12} className="animate-spin mr-1" />
              ) : (
                <Sparkles size={12} className="mr-1" />
              )}
              Generate RCA
            </Button>
          )}
        </div>
      </div>

      {/* RCA Panel */}
      {incident.root_cause && rcaOpen && (
        <div className="mt-3 p-4 rounded-xl bg-gradient-to-br from-violet-500/8 to-blue-500/5 border border-violet-500/15 animate-fade-in">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Sparkles size={13} className="text-violet-400" />
              <span className="text-xs font-semibold text-violet-300">AI Root Cause Analysis</span>
            </div>
            <span className="badge bg-white/5 border border-white/10 text-slate-400 text-[10px]">
              Confidence: {(incident.root_cause.confidence * 100).toFixed(0)}%
            </span>
          </div>
          <div className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">
            {incident.root_cause.root_cause_analysis}
          </div>
        </div>
      )}
    </div>
  );
}

export default function Incidents() {
  const [incidents, setIncidents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [generatingRcaId, setGeneratingRcaId] = useState<string | null>(null);
  const [systemicAnalysis, setSystemicAnalysis] = useState<string | null>(null);
  const [generatingSystemic, setGeneratingSystemic] = useState(false);
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);

  const fetchIncidents = async () => {
    try {
      const res = await api.get('/incidents');
      setIncidents(res.data.items);
    } catch {
      toast.error('Failed to fetch incidents');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchIncidents(); }, []);

  const handleGenerateRca = async (id: string) => {
    setGeneratingRcaId(id);
    try {
      await api.post(`/incidents/${id}/rca`);
      toast.success('RCA Generated successfully');
      fetchIncidents();
    } catch {
      toast.error('Failed to generate RCA');
    } finally {
      setGeneratingRcaId(null);
    }
  };

  const handleGenerateSystemic = async () => {
    setGeneratingSystemic(true);
    try {
      const res = await api.get('/incidents/systemic-rca');
      setSystemicAnalysis(res.data.analysis);
      toast.success('Systemic pattern analysis completed');
    } catch {
      toast.error('Failed to analyze systemic patterns');
    } finally {
      setGeneratingSystemic(false);
    }
  };

  const criticalCount = incidents.filter(i => i.severity === 'critical').length;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-wrap gap-4 items-end justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-5 bg-gradient-to-b from-red-400 to-orange-400 rounded-full" />
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Incident Management</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100">Incidents & RCA</h1>
          <p className="text-sm text-slate-500 mt-0.5">Track anomalies and generate AI-driven root cause analyses.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={handleGenerateSystemic}
            disabled={generatingSystemic}
            className="text-xs border-violet-500/30 text-violet-400 hover:bg-violet-500/10"
          >
            {generatingSystemic
              ? <Loader2 size={13} className="animate-spin mr-2" />
              : <Sparkles size={13} className="mr-2" />}
            Systemic Patterns
          </Button>
          <Button size="sm" className="text-xs" onClick={() => setIsReportModalOpen(true)}>
            <Plus size={13} className="mr-1.5" /> Report Anomaly
          </Button>
        </div>
      </div>

      <ReportIncidentModal 
        isOpen={isReportModalOpen} 
        onClose={() => setIsReportModalOpen(false)} 
        onSuccess={fetchIncidents} 
      />

      {/* Stats bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { label: 'Total', value: incidents.length, color: 'text-slate-300' },
          { label: 'Critical', value: criticalCount, color: 'text-red-400' },
          { label: 'With RCA', value: incidents.filter(i => i.root_cause).length, color: 'text-emerald-400' },
          { label: 'Pending RCA', value: incidents.filter(i => !i.root_cause).length, color: 'text-amber-400' },
        ].map(s => (
          <div key={s.label} className="p-3.5 rounded-xl bg-white/[0.03] border border-white/[0.06] text-center">
            <div className={`text-xl font-bold font-mono ${s.color}`}>{s.value}</div>
            <div className="text-xs text-slate-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Systemic Analysis */}
      {systemicAnalysis && (
        <Card className="border-violet-500/20 bg-gradient-to-br from-violet-500/8 to-blue-500/5 animate-scale-in">
          <CardHeader className="pb-3 border-b border-violet-500/15">
            <CardTitle className="flex items-center gap-2 text-sm text-violet-300">
              <Sparkles size={15} className="text-violet-400" />
              AI Systemic Failure Patterns Report
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-4">
            <div className="text-sm text-slate-300 leading-relaxed whitespace-pre-wrap">{systemicAnalysis}</div>
          </CardContent>
        </Card>
      )}

      {/* Incidents List */}
      <Card>
        <CardHeader className="pb-4 border-b border-white/[0.06]">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm flex items-center gap-2">
              <AlertTriangle size={15} className="text-orange-400" />
              Active Incidents
            </CardTitle>
            {!loading && (
              <span className="text-xs text-slate-500">{incidents.length} total</span>
            )}
          </div>
        </CardHeader>
        <CardContent className="pt-4">
          {loading ? (
            <div className="space-y-3">
              {[1,2,3].map(i => <div key={i} className="skeleton h-20 rounded-xl" />)}
            </div>
          ) : incidents.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-14 text-slate-500">
              <div className="w-14 h-14 rounded-2xl bg-white/4 border border-white/8 flex items-center justify-center mb-4">
                <AlertTriangle size={24} className="text-slate-600" />
              </div>
              <p className="text-sm font-medium text-slate-400">No active incidents</p>
              <p className="text-xs text-slate-600 mt-1">The system is operating normally</p>
            </div>
          ) : (
            <div className="space-y-2.5">
              {incidents.map(incident => (
                <IncidentCard
                  key={incident.id}
                  incident={incident}
                  onGenerateRca={handleGenerateRca}
                  generatingRcaId={generatingRcaId}
                />
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
