import { useEffect, useState } from 'react';
import api from '@/lib/api';
import {
  ChevronRight, ChevronDown, FolderTree, Box,
  FileText, Settings, Sparkles, X, Plus,
  Factory, Cpu, Wrench, LayoutGrid, MapPin, Hash,
  Activity, AlertTriangle, CheckCircle2, Clock, TrendingUp,
} from 'lucide-react';


// ─── Type icons ───────────────────────────────────────────────────────────
const TYPE_ICON: Record<string, any> = {
  plant:     Factory,
  area:      LayoutGrid,
  equipment: Cpu,
  component: Wrench,
};

const STATUS_STYLE: Record<string, { color: string; bg: string; border: string; dot: string }> = {
  operational: { color: '#10b981', bg: 'rgba(16,185,129,0.12)', border: 'rgba(16,185,129,0.25)', dot: '#10b981' },
  warning:     { color: '#f59e0b', bg: 'rgba(245,158,11,0.12)',  border: 'rgba(245,158,11,0.25)',  dot: '#f59e0b' },
  maintenance: { color: '#60a5fa', bg: 'rgba(59,130,246,0.12)',  border: 'rgba(59,130,246,0.25)',  dot: '#60a5fa' },
  offline:     { color: '#f43f5e', bg: 'rgba(244,63,94,0.12)',   border: 'rgba(244,63,94,0.25)',   dot: '#f43f5e' },
};

// ─── Tree Node ─────────────────────────────────────────────────────────────
const AssetTreeNode = ({ node, level = 0, selectedId, onSelect }: any) => {
  const [expanded, setExpanded] = useState(level === 0);
  const hasChildren = node.children && node.children.length > 0;
  const isSelected = selectedId === node.id;
  const Icon = TYPE_ICON[node.asset_type] ?? Box;
  const ss = STATUS_STYLE[node.status] ?? STATUS_STYLE.operational;

  return (
    <div>
      <div
        className="flex items-center py-2 px-2.5 cursor-pointer rounded-xl transition-all duration-150 group"
        style={{
          paddingLeft: `${level * 1.1 + 0.5}rem`,
          background: isSelected ? 'rgba(59,130,246,0.15)' : 'transparent',
          border: isSelected ? '1px solid rgba(59,130,246,0.3)' : '1px solid transparent',
        }}
        onMouseEnter={e => { if (!isSelected) (e.currentTarget as HTMLDivElement).style.background = 'rgba(255,255,255,0.04)'; }}
        onMouseLeave={e => { if (!isSelected) (e.currentTarget as HTMLDivElement).style.background = 'transparent'; }}
        onClick={() => { if (hasChildren) setExpanded(!expanded); onSelect(node.id); }}
      >
        <div className="w-4 flex items-center justify-center mr-1.5 shrink-0">
          {hasChildren ? (
            expanded
              ? <ChevronDown size={12} className="text-slate-500" />
              : <ChevronRight size={12} className="text-slate-600" />
          ) : <span className="w-3" />}
        </div>
        <div className="w-6 h-6 rounded-lg flex items-center justify-center mr-2 shrink-0"
          style={{ background: isSelected ? 'rgba(59,130,246,0.2)' : 'rgba(255,255,255,0.05)' }}>
          <Icon size={11} style={{ color: isSelected ? '#60a5fa' : '#64748b' }} />
        </div>
        <span className="text-xs font-semibold truncate flex-1" style={{ color: isSelected ? '#93c5fd' : '#94a3b8' }}>
          {node.name}
        </span>
        {/* Status dot */}
        <div className="w-1.5 h-1.5 rounded-full ml-2 shrink-0"
          style={{ background: ss.dot, boxShadow: `0 0 4px ${ss.dot}` }} />
      </div>

      {expanded && hasChildren && (
        <div className="ml-3 pl-2 border-l border-white/[0.05] animate-fade-in">
          {node.children.map((child: any) => (
            <AssetTreeNode key={child.id} node={child} level={level + 1}
              selectedId={selectedId} onSelect={onSelect} />
          ))}
        </div>
      )}
    </div>
  );
};

// ─── Risk helpers ──────────────────────────────────────────────────────────
const riskColor = (score: number) => score > 75 ? '#f43f5e' : score > 40 ? '#f59e0b' : '#10b981';
const riskBg    = (score: number) => score > 75
  ? 'rgba(244,63,94,0.10)' : score > 40
  ? 'rgba(245,158,11,0.10)' : 'rgba(16,185,129,0.10)';
const riskBorder = (score: number) => score > 75
  ? 'rgba(244,63,94,0.25)' : score > 40
  ? 'rgba(245,158,11,0.25)' : 'rgba(16,185,129,0.25)';
const riskLabel  = (score: number) => score > 75 ? 'HIGH RISK' : score > 40 ? 'MEDIUM RISK' : 'LOW RISK';

export default function Assets() {
  const [treeData, setTreeData]           = useState<any[]>([]);
  const [selectedAssetId, setSelectedAssetId] = useState<string | null>(null);
  const [assetDetails, setAssetDetails]   = useState<any>(null);
  const [timeline, setTimeline]           = useState<any[]>([]);
  const [predictiveAnalysis, setPredictiveAnalysis] = useState<any>(null);
  const [loading, setLoading]             = useState(true);
  const [loadingPredictive, setLoadingPredictive]   = useState(false);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [newAsset, setNewAsset]           = useState({
    name: '', asset_type: 'equipment', location: '', serial_number: '', description: '',
  });

  // Fetch tree ──────────────────────────────────────────────
  useEffect(() => {
    const fetchTree = async () => {
      try {
        const res = await api.get('/assets/tree');
        const nodes = res.data.children ?? [];
        setTreeData(nodes);
      } catch {
        console.error('Failed to load asset tree');
      } finally {
        setLoading(false);
      }
    };
    fetchTree();
  }, []);

  // Select asset ────────────────────────────────────────────────────────────
  const handleSelect = async (id: string) => {
    setSelectedAssetId(id);

    try {
      const [detailRes, timelineRes] = await Promise.all([
        api.get(`/assets/${id}`),
        api.get(`/assets/${id}/timeline`),
      ]);
      setAssetDetails(detailRes.data);
      setTimeline(timelineRes.data.events);
      setLoadingPredictive(true);
      setPredictiveAnalysis(null);
      try {
        const pred = await api.get(`/assets/${id}/predictive-analysis`);
        setPredictiveAnalysis(pred.data);
      } catch { /* noop */ } finally {
        setLoadingPredictive(false);
      }
    } catch { /* noop */ }
  };

  useEffect(() => {
    if (selectedAssetId) handleSelect(selectedAssetId);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleAddAsset = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/assets', newAsset);
      setIsAddModalOpen(false);
      setNewAsset({ name: '', asset_type: 'equipment', location: '', serial_number: '', description: '' });
      const res = await api.get('/assets/tree');
      setTreeData(res.data.children);
    } catch {
      alert('Failed to add resource.');
    }
  };

  const inputCls = "w-full h-9 px-3 text-sm rounded-xl text-slate-200 placeholder-slate-600 focus:outline-none transition-all"
    + " bg-white/5 border border-white/10 focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500/40";
  const labelCls = "block text-xs font-bold text-slate-400 mb-1.5 uppercase tracking-wider";

  const typeLabel: Record<string, string> = { plant: 'Organization', area: 'Department/Area', equipment: 'Equipment', component: 'Component' };
  const TypeIcon = assetDetails ? (TYPE_ICON[assetDetails.asset_type] ?? Box) : Box;
  const ss = assetDetails ? (STATUS_STYLE[assetDetails.status] ?? STATUS_STYLE.operational) : STATUS_STYLE.operational;

  return (
    <div className="h-[calc(100vh-7rem)] flex flex-col gap-5 animate-fade-in">

      {/* Header */}
      <div className="flex items-center justify-between shrink-0">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-5 rounded-full" style={{ background: 'linear-gradient(180deg, #f59e0b, #f97316)' }} />
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Resources</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-100 tracking-tight">Resource Management</h1>
        </div>
        <button onClick={() => setIsAddModalOpen(true)}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold text-white transition-all"
          style={{ background: 'linear-gradient(135deg, #3b82f6, #7c3aed)', boxShadow: '0 4px 16px rgba(59,130,246,0.35)' }}
          onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.transform = 'translateY(-1px)'; }}
          onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.transform = ''; }}>
          <Plus size={14} /> Add Resource
        </button>
      </div>

      <div className="flex-1 flex gap-5 min-h-0">

        {/* ─── Tree Pane ─────────────────────────────────────────── */}
        <div className="w-64 flex flex-col shrink-0 rounded-2xl overflow-hidden"
          style={{ background: 'rgba(8,14,30,0.9)', border: '1px solid rgba(255,255,255,0.07)' }}>
          <div className="px-4 py-3.5 flex items-center gap-2.5 shrink-0"
            style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
            <div className="w-6 h-6 rounded-lg flex items-center justify-center"
              style={{ background: 'rgba(245,158,11,0.15)', border: '1px solid rgba(245,158,11,0.25)' }}>
              <FolderTree size={12} style={{ color: '#f59e0b' }} />
            </div>
            <span className="text-xs font-bold text-slate-300">Resource Explorer</span>
            <span className="ml-auto text-[10px] font-bold text-slate-600">{treeData.length} items</span>
          </div>
          <div className="flex-1 overflow-y-auto p-2 space-y-0.5 scrollbar-thin">
            {loading ? (
              <div className="space-y-2 p-2">
                {[1,2,3,4,5].map(i => <div key={i} className="skeleton h-8 rounded-xl" />)}
              </div>
            ) : (
              treeData.map(node => (
                <AssetTreeNode key={node.id} node={node}
                  selectedId={selectedAssetId} onSelect={handleSelect} />
              ))
            )}
          </div>
        </div>

        {/* ─── Detail Pane ───────────────────────────────────────── */}
        <div className="flex-1 flex flex-col overflow-hidden rounded-2xl"
          style={{ background: 'rgba(8,14,30,0.9)', border: '1px solid rgba(255,255,255,0.07)' }}>

          {selectedAssetId && assetDetails ? (
            <>
              {/* Asset header */}
              <div className="px-6 py-4 shrink-0 flex items-start justify-between gap-4"
                style={{ borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-2xl flex items-center justify-center shrink-0"
                    style={{ background: 'rgba(59,130,246,0.15)', border: '1px solid rgba(59,130,246,0.25)' }}>
                    <TypeIcon size={22} style={{ color: '#60a5fa' }} />
                  </div>
                  <div>
                    <h2 className="text-lg font-extrabold text-slate-100 tracking-tight">{assetDetails.name}</h2>
                    <div className="flex flex-wrap items-center gap-2 mt-2">
                      <span className="text-[11px] font-bold px-2.5 py-1 rounded-lg"
                        style={{ background: 'rgba(255,255,255,0.06)', color: '#94a3b8', border: '1px solid rgba(255,255,255,0.08)' }}>
                        {typeLabel[assetDetails.asset_type] ?? assetDetails.asset_type}
                      </span>
                      {assetDetails.serial_number && (
                        <span className="flex items-center gap-1 text-[11px] font-bold px-2.5 py-1 rounded-lg"
                          style={{ background: 'rgba(255,255,255,0.04)', color: '#64748b', border: '1px solid rgba(255,255,255,0.06)' }}>
                          <Hash size={9} /> {assetDetails.serial_number}
                        </span>
                      )}
                      {assetDetails.location && (
                        <span className="flex items-center gap-1 text-[11px] font-bold px-2.5 py-1 rounded-lg"
                          style={{ background: 'rgba(255,255,255,0.04)', color: '#64748b', border: '1px solid rgba(255,255,255,0.06)' }}>
                          <MapPin size={9} /> {assetDetails.location}
                        </span>
                      )}
                      <span className="flex items-center gap-1.5 text-[11px] font-bold px-2.5 py-1 rounded-lg capitalize"
                        style={{ background: ss.bg, color: ss.color, border: `1px solid ${ss.border}` }}>
                        <div className="w-1.5 h-1.5 rounded-full" style={{ background: ss.dot, boxShadow: `0 0 5px ${ss.dot}` }} />
                        {assetDetails.status}
                      </span>
                    </div>
                  </div>
                </div>
                <button className="flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-bold transition-colors shrink-0 text-slate-400 hover:text-slate-200"
                  style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.08)' }}>
                  <Settings size={12} /> Configure
                </button>
              </div>

              {/* Scrollable content */}
              <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">
                {assetDetails.description && (
                  <p className="text-sm text-slate-400 leading-relaxed">{assetDetails.description}</p>
                )}

                {/* Attributes grid */}
                {assetDetails.metadata_json && Object.keys(assetDetails.metadata_json).length > 0 && (
                  <div>
                    <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2 mb-3">
                      <Settings size={11} className="text-slate-600" /> Attributes & Metadata
                    </h4>
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                      {Object.entries(assetDetails.metadata_json).map(([key, value]: any) => (
                        <div key={key} className="p-3 rounded-xl"
                          style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                          <dt className="text-[10px] font-bold text-slate-600 uppercase tracking-wider capitalize mb-1">{key.replace(/_/g, ' ')}</dt>
                          <dd className="text-sm font-bold text-slate-200">{value}</dd>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* AI Predictive Analysis */}
                <div>
                  <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2 mb-3">
                    <Sparkles size={11} style={{ color: '#8b5cf6' }} /> AI Predictive Risk Analysis
                  </h4>
                  {loadingPredictive ? (
                    <div className="flex items-center gap-3 p-5 rounded-2xl"
                      style={{ background: 'rgba(139,92,246,0.06)', border: '1px solid rgba(139,92,246,0.15)' }}>
                      <div className="w-5 h-5 rounded-full border-2 border-violet-500 border-t-transparent animate-spin shrink-0" />
                      <div>
                        <p className="text-xs font-bold text-slate-300">Analyzing operational history...</p>
                        <p className="text-[11px] text-slate-500 mt-0.5">AI agent is calculating failure probability and risk factors</p>
                      </div>
                    </div>
                  ) : predictiveAnalysis ? (
                    <div className="rounded-2xl p-5"
                      style={{ background: riskBg(predictiveAnalysis.failure_risk_score), border: `1px solid ${riskBorder(predictiveAnalysis.failure_risk_score)}` }}>
                      <div className="flex items-start gap-6">
                        <div className="text-center shrink-0">
                          <div className="text-5xl font-black mono-num" style={{ color: riskColor(predictiveAnalysis.failure_risk_score) }}>
                            {predictiveAnalysis.failure_risk_score}
                          </div>
                          <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1">Risk Score</div>
                          <div className="mt-2 text-xs font-bold px-2 py-0.5 rounded-full"
                            style={{ background: riskBg(predictiveAnalysis.failure_risk_score), color: riskColor(predictiveAnalysis.failure_risk_score) }}>
                            {riskLabel(predictiveAnalysis.failure_risk_score)}
                          </div>
                          <div className="mt-1 text-xs text-slate-500 flex items-center gap-1 justify-center">
                            <TrendingUp size={10} /> {predictiveAnalysis.trend}
                          </div>
                        </div>
                        <div className="flex-1">
                          <p className="text-xs font-bold text-slate-300 mb-3">AI Recommendations</p>
                          <ul className="space-y-2">
                            {predictiveAnalysis.recommendations.map((rec: string, i: number) => (
                              <li key={i} className="flex items-start gap-2.5 text-sm text-slate-400">
                                <div className="w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5 text-[11px] font-black"
                                  style={{ background: riskBg(predictiveAnalysis.failure_risk_score), color: riskColor(predictiveAnalysis.failure_risk_score) }}>
                                  {i + 1}
                                </div>
                                {rec}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="p-4 rounded-xl text-xs text-slate-500 italic"
                      style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
                      No predictive data available for this asset type.
                    </div>
                  )}
                </div>

                {/* Timeline */}
                <div>
                  <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2 mb-3">
                    <Activity size={11} className="text-amber-400" /> Operational History
                  </h4>
                  {timeline.length === 0 ? (
                    <div className="p-6 rounded-2xl text-center"
                      style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
                      <Clock size={24} className="mx-auto mb-2 text-slate-700" />
                      <p className="text-sm text-slate-500">No incidents or maintenance records found.</p>
                    </div>
                  ) : (
                    <div className="space-y-2.5 relative">
                      <div className="absolute left-4 top-4 bottom-4 w-px"
                        style={{ background: 'linear-gradient(180deg, rgba(59,130,246,0.4), transparent)' }} />
                      {timeline.map((event) => {
                        const isInc = event.type === 'incident';
                        const evColor = isInc ? '#f87171' : '#60a5fa';
                        const evBg = isInc ? 'rgba(244,63,94,0.08)' : 'rgba(59,130,246,0.08)';
                        const evBorder = isInc ? 'rgba(244,63,94,0.18)' : 'rgba(59,130,246,0.18)';
                        return (
                          <div key={event.id} className="flex gap-4 ml-1">
                            <div className="relative z-10 w-7 h-7 rounded-full flex items-center justify-center shrink-0"
                              style={{ background: evBg, border: `1px solid ${evBorder}` }}>
                              {isInc
                                ? <AlertTriangle size={11} style={{ color: evColor }} />
                                : <CheckCircle2 size={11} style={{ color: evColor }} />}
                            </div>
                            <div className="flex-1 p-3 rounded-xl"
                              style={{ background: evBg, border: `1px solid ${evBorder}` }}>
                              <div className="flex items-start justify-between gap-2">
                                <div>
                                  <p className="text-xs font-bold" style={{ color: evColor }}>{event.title}</p>
                                  <p className="text-[11px] text-slate-500 mt-0.5 capitalize">
                                    {event.type} · {event.status?.replace(/_/g, ' ')}
                                    {isInc && event.severity && ` · ${event.severity} severity`}
                                    {!isInc && event.maintenance_type && ` · ${event.maintenance_type}`}
                                  </p>
                                </div>
                                <span className="text-[10px] text-slate-600 shrink-0">
                                  {event.timestamp ? new Date(event.timestamp).toLocaleDateString() : ''}
                                </span>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Documents */}
                <div>
                  <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest flex items-center gap-2 mb-3">
                    <FileText size={11} className="text-indigo-400" /> Associated Documents
                  </h4>
                  <div className="p-4 rounded-xl text-xs text-slate-500 italic"
                    style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
                    No documents attached. Upload via the Knowledge Base module.
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center gap-4">
              <div className="w-20 h-20 rounded-3xl flex items-center justify-center"
                style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.07)' }}>
                <FolderTree size={32} className="text-slate-700" />
              </div>
              <div className="text-center">
                <p className="text-sm font-bold text-slate-400">Select a resource to view details</p>
                <p className="text-xs text-slate-600 mt-1">Click any item in the explorer panel</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ─── Add Resource Modal ──────────────────────────────────── */}
      {isAddModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center z-50 p-4 animate-fade-in"
          style={{ background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(12px)' }}>
          <div className="w-full max-w-md rounded-2xl animate-scale-in"
            style={{ background: 'rgba(8,14,35,0.98)', border: '1px solid rgba(255,255,255,0.1)', boxShadow: '0 24px 64px rgba(0,0,0,0.8)' }}>
            <div className="flex items-center justify-between px-6 py-4"
              style={{ borderBottom: '1px solid rgba(255,255,255,0.07)' }}>
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-xl flex items-center justify-center"
                  style={{ background: 'rgba(59,130,246,0.15)', border: '1px solid rgba(59,130,246,0.25)' }}>
                  <Plus size={14} style={{ color: '#60a5fa' }} />
                </div>
                <h3 className="text-sm font-extrabold text-slate-100">Add New Resource</h3>
              </div>
              <button onClick={() => setIsAddModalOpen(false)}
                className="p-1.5 rounded-lg text-slate-500 hover:text-slate-300 hover:bg-white/8 transition-colors">
                <X size={15} />
              </button>
            </div>
            <form onSubmit={handleAddAsset} className="p-6 space-y-4">
              <div>
                <label className={labelCls}>Name *</label>
                <input required className={inputCls} placeholder="Resource name"
                  value={newAsset.name} onChange={e => setNewAsset({ ...newAsset, name: e.target.value })} />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className={labelCls}>Type *</label>
                  <select className={inputCls + ' cursor-pointer'}
                    value={newAsset.asset_type} onChange={e => setNewAsset({ ...newAsset, asset_type: e.target.value })}>
                    <option value="plant">Organization / Site</option>
                    <option value="area">Department / Area</option>
                    <option value="equipment">Equipment / Entity</option>
                    <option value="component">Sub-component</option>
                  </select>
                </div>
                <div>
                  <label className={labelCls}>Location</label>
                  <input className={inputCls} placeholder="e.g. Floor 2, Bay A"
                    value={newAsset.location} onChange={e => setNewAsset({ ...newAsset, location: e.target.value })} />
                </div>
              </div>
              <div>
                <label className={labelCls}>Serial Number</label>
                <input className={inputCls} placeholder="Optional identifier"
                  value={newAsset.serial_number} onChange={e => setNewAsset({ ...newAsset, serial_number: e.target.value })} />
              </div>
              <div>
                <label className={labelCls}>Description</label>
                <textarea
                  className="w-full px-3 py-2.5 text-sm rounded-xl text-slate-200 placeholder-slate-600 focus:outline-none resize-none h-20 transition-all bg-white/5 border border-white/10 focus:ring-2 focus:ring-blue-500/40"
                  placeholder="Brief description..."
                  value={newAsset.description}
                  onChange={e => setNewAsset({ ...newAsset, description: e.target.value })} />
              </div>
              <div className="flex justify-end gap-3 pt-2" style={{ borderTop: '1px solid rgba(255,255,255,0.06)' }}>
                <button type="button" onClick={() => setIsAddModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-sm font-bold text-slate-400 hover:text-slate-200 transition-colors"
                  style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.08)' }}>
                  Cancel
                </button>
                <button type="submit"
                  className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-white transition-all"
                  style={{ background: 'linear-gradient(135deg, #3b82f6, #7c3aed)', boxShadow: '0 4px 12px rgba(59,130,246,0.3)' }}>
                  <Plus size={13} /> Create Resource
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
