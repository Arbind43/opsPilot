import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import api from '@/lib/api';
import {
  FileBarChart, Loader2, Plus, Download, FileText, Activity, Sparkles,
} from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import toast from 'react-hot-toast';

const REPORT_ICONS: Record<string, React.ReactElement> = {
  summary: <FileBarChart size={15} className="text-violet-400" />,
  rca: <Activity size={15} className="text-orange-400" />,
  default: <FileText size={15} className="text-slate-400" />,
};

export default function Reports() {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  const fetchReports = async () => {
    try {
      const res = await api.get('/reports');
      setReports(res.data.items);
    } catch {
      toast.error('Failed to fetch reports');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchReports(); }, []);

  const handleGenerateReport = async () => {
    setGenerating(true);
    try {
      await api.post('/reports/generate', {
        title: `Operational Summary — ${new Date().toLocaleDateString()}`,
        report_type: 'summary',
      });
      toast.success('Report generated successfully');
      fetchReports();
    } catch {
      toast.error('Failed to generate report');
    } finally {
      setGenerating(false);
    }
  };

  const handleExport = (report: any) => {
    const dataStr = JSON.stringify(report.content, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `report_${report.id}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    toast.success('Report exported successfully');
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-wrap gap-4 items-end justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-5 bg-gradient-to-b from-pink-400 to-rose-400 rounded-full" />
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Analytics</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100">Reporting Engine</h1>
          <p className="text-sm text-slate-500 mt-0.5">Generate, view, and export AI-driven operational insights.</p>
        </div>
        <Button
          onClick={handleGenerateReport}
          disabled={generating}
          size="sm"
          className="bg-gradient-to-r from-pink-500 to-rose-500 shadow-[0_4px_14px_rgba(236,72,153,0.3)]"
        >
          {generating
            ? <Loader2 size={13} className="animate-spin mr-2" />
            : <Sparkles size={13} className="mr-2" />}
          Generate Report
        </Button>
      </div>

      {/* Reports grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {loading ? (
          [1,2,3].map(i => (
            <div key={i} className="rounded-2xl border border-white/[0.07] bg-[rgba(17,25,50,0.7)] p-6 space-y-4">
              <div className="skeleton h-4 w-3/4 rounded" />
              <div className="skeleton h-3 w-1/2 rounded" />
              <div className="skeleton h-20 w-full rounded-xl" />
              <div className="skeleton h-8 w-full rounded-xl" />
            </div>
          ))
        ) : reports.length === 0 ? (
          <div className="col-span-full flex flex-col items-center justify-center py-20 text-slate-500
                          rounded-2xl border-2 border-dashed border-white/[0.06] bg-white/[0.01]">
            <div className="w-14 h-14 rounded-2xl bg-white/4 border border-white/8 flex items-center justify-center mb-4">
              <FileBarChart size={24} className="text-slate-600" />
            </div>
            <p className="text-sm font-medium text-slate-400">No reports generated yet</p>
            <p className="text-xs text-slate-600 mt-1 mb-5">Click Generate Report to create your first analysis</p>
            <Button size="sm" onClick={handleGenerateReport} disabled={generating}>
              <Plus size={13} className="mr-1.5" /> Generate Now
            </Button>
          </div>
        ) : (
          reports.map((report, i) => (
            <Card
              key={report.id}
              className="flex flex-col hover:border-white/[0.12] hover:-translate-y-0.5 transition-all duration-300 animate-fade-in"
              style={{ animationDelay: `${i * 0.08}s` }}
            >
              <CardHeader className="pb-3 border-b border-white/[0.06]">
                <div className="flex items-start gap-2.5">
                  <div className="w-8 h-8 rounded-xl bg-white/5 border border-white/8 flex items-center justify-center shrink-0">
                    {REPORT_ICONS[report.type] || REPORT_ICONS.default}
                  </div>
                  <div className="flex-1 min-w-0">
                    <CardTitle className="text-sm leading-snug truncate">{report.title}</CardTitle>
                    <CardDescription className="text-[11px] mt-0.5">
                      {report.asset_name && <span className="text-blue-400">{report.asset_name} · </span>}
                      {report.created_at
                        ? formatDistanceToNow(new Date(report.created_at), { addSuffix: true })
                        : 'Just now'}
                    </CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-4 flex-1 flex flex-col">
                <div className="flex-1 bg-white/[0.02] border border-white/[0.06] rounded-xl p-3.5 mb-4">
                  <p className="text-xs font-semibold text-slate-400 mb-2">Key Findings</p>
                  <ul className="space-y-1.5">
                    {report.content?.recommendations?.slice(0, 3).map((rec: string, i: number) => (
                      <li key={i} className="flex items-start gap-1.5 text-xs text-slate-400">
                        <div className="w-1 h-1 rounded-full bg-pink-400 mt-1.5 shrink-0" />
                        <span className="line-clamp-2">{rec}</span>
                      </li>
                    )) || (
                      <li className="text-xs text-slate-600 italic">No specific findings.</li>
                    )}
                  </ul>
                </div>
                <div className="flex items-center justify-between">
                  <span className="badge bg-emerald-500/10 border-emerald-500/20 text-emerald-400 text-[10px]">
                    <div className="status-dot online" />
                    {report.status}
                  </span>
                  <Button variant="outline" size="xs" className="text-[11px]" onClick={() => handleExport(report)}>
                    <Download size={11} className="mr-1" /> Export Data
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
