import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import api from '@/lib/api';
import {
  ChevronRight, ChevronDown, FolderTree, Box,
  FileText, Settings, AlertCircle, Sparkles, X, Plus,
} from 'lucide-react';

const AssetTreeNode = ({ node, level = 0, selectedId, onSelect }: any) => {
  const [expanded, setExpanded] = useState(false);
  const hasChildren = node.children && node.children.length > 0;
  const isSelected = selectedId === node.id;

  return (
    <div>
      <div
        className={`flex items-center py-2 px-2.5 cursor-pointer rounded-xl transition-all duration-150 group
          ${isSelected
            ? 'bg-blue-500/15 border border-blue-500/25 text-blue-300'
            : 'hover:bg-white/[0.04] text-slate-400 hover:text-slate-200 border border-transparent'}`}
        style={{ paddingLeft: `${level * 1.25 + 0.625}rem` }}
        onClick={() => { if (hasChildren) setExpanded(!expanded); onSelect(node.id); }}
      >
        <div className="w-4 flex items-center justify-center mr-1.5 shrink-0">
          {hasChildren ? (
            expanded
              ? <ChevronDown size={13} className="text-slate-500" />
              : <ChevronRight size={13} className="text-slate-600" />
          ) : <span className="w-3" />}
        </div>
        <div className={`w-5 h-5 rounded-md flex items-center justify-center mr-2 shrink-0 transition-colors
          ${isSelected ? 'bg-blue-500/20' : 'bg-white/5 group-hover:bg-white/8'}`}>
          <Box size={11} className={isSelected ? 'text-blue-400' : 'text-slate-500'} />
        </div>
        <span className="text-xs font-medium truncate">{node.name}</span>
      </div>

      {expanded && hasChildren && (
        <div className="ml-2 pl-2 border-l border-white/[0.06] animate-fade-in">
          {node.children.map((child: any) => (
            <AssetTreeNode
              key={child.id}
              node={child}
              level={level + 1}
              selectedId={selectedId}
              onSelect={onSelect}
            />
          ))}
        </div>
      )}
    </div>
  );
};

const RISK_COLOR = (score: number) =>
  score > 75 ? 'text-red-400' : score > 40 ? 'text-amber-400' : 'text-emerald-400';

const RISK_BG = (score: number) =>
  score > 75
    ? 'from-red-500/15 to-orange-500/8 border-red-500/20'
    : score > 40
    ? 'from-amber-500/15 to-yellow-500/8 border-amber-500/20'
    : 'from-emerald-500/15 to-teal-500/8 border-emerald-500/20';

export default function Assets() {
  const [treeData, setTreeData] = useState<any[]>([]);
  const [selectedAssetId, setSelectedAssetId] = useState<string | null>(null);
  const [assetDetails, setAssetDetails] = useState<any>(null);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [predictiveAnalysis, setPredictiveAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [loadingPredictive, setLoadingPredictive] = useState(false);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [newAsset, setNewAsset] = useState({
    name: '', asset_type: 'equipment', location: '', serial_number: '', description: '',
  });

  useEffect(() => {
    const fetchTree = async () => {
      try {
        const res = await api.get('/assets/tree');
        setTreeData(res.data.children);
      } catch {
        console.error('Failed to load asset tree');
      } finally {
        setLoading(false);
      }
    };
    fetchTree();
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

  useEffect(() => {
    if (!selectedAssetId) return;
    const fetchAsset = async () => {
      try {
        const [detailRes, timelineRes] = await Promise.all([
          api.get(`/assets/${selectedAssetId}`),
          api.get(`/assets/${selectedAssetId}/timeline`),
        ]);
        setAssetDetails(detailRes.data);
        setTimeline(timelineRes.data.events);
        setLoadingPredictive(true);
        setPredictiveAnalysis(null);
        try {
          const predRes = await api.get(`/assets/${selectedAssetId}/predictive-analysis`);
          setPredictiveAnalysis(predRes.data);
        } catch {
          console.error('Failed predictive analysis');
        } finally {
          setLoadingPredictive(false);
        }
      } catch {
        console.error('Failed to load asset details');
      }
    };
    fetchAsset();
  }, [selectedAssetId]);

  const inputCls = "w-full h-9 px-3 text-sm bg-white/5 border border-white/10 rounded-xl text-slate-200 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500/40 transition-all";
  const labelCls = "block text-xs font-medium text-slate-400 mb-1.5";

  return (
    <div className="h-[calc(100vh-7rem)] flex flex-col gap-5 animate-fade-in">
      {/* Header */}
      <div className="flex items-end justify-between shrink-0">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-5 bg-gradient-to-b from-amber-400 to-orange-400 rounded-full" />
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Resources</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100">Resource Management</h1>
        </div>
        <Button size="sm" onClick={() => setIsAddModalOpen(true)}>
          <Plus size={13} className="mr-1.5" /> Add Resource
        </Button>
      </div>

      <div className="flex-1 flex gap-5 min-h-0">
        {/* Tree pane */}
        <Card className="w-60 flex flex-col shrink-0">
          <CardHeader className="py-3.5 border-b border-white/[0.06] shrink-0">
            <CardTitle className="text-xs flex items-center gap-2">
              <FolderTree size={13} className="text-amber-400" /> Resource Explorer
            </CardTitle>
          </CardHeader>
          <div className="flex-1 overflow-y-auto p-2.5 space-y-0.5 scrollbar-thin">
            {loading ? (
              <div className="space-y-1.5 p-1">
                {[1,2,3,4].map(i => <div key={i} className="skeleton h-8 rounded-xl" />)}
              </div>
            ) : treeData.length === 0 ? (
              <div className="text-center py-8 text-slate-600 text-xs">No resources found</div>
            ) : (
              treeData.map(node => (
                <AssetTreeNode
                  key={node.id}
                  node={node}
                  selectedId={selectedAssetId}
                  onSelect={setSelectedAssetId}
                />
              ))
            )}
          </div>
        </Card>

        {/* Detail pane */}
        <Card className="flex-1 flex flex-col overflow-hidden">
          {selectedAssetId && assetDetails ? (
            <>
              <CardHeader className="border-b border-white/[0.06] shrink-0 py-4">
                <div className="flex justify-between items-start gap-4">
                  <div>
                    <h2 className="text-lg font-bold text-slate-100">{assetDetails.name}</h2>
                    <div className="flex flex-wrap items-center gap-2 mt-2">
                      <span className="badge bg-white/5 border border-white/8 text-slate-400 capitalize">
                        {assetDetails.asset_type}
                      </span>
                      {assetDetails.serial_number && (
                        <span className="badge bg-white/5 border border-white/8 text-slate-500 text-[10px]">
                          S/N: {assetDetails.serial_number}
                        </span>
                      )}
                      {assetDetails.location && (
                        <span className="badge bg-white/5 border border-white/8 text-slate-500 text-[10px]">
                          📍 {assetDetails.location}
                        </span>
                      )}
                      <span className="badge bg-emerald-500/10 border-emerald-500/20 text-emerald-400">
                        <div className="status-dot online" />
                        {assetDetails.status?.toUpperCase()}
                      </span>
                    </div>
                  </div>
                  <Button variant="outline" size="sm" className="text-xs shrink-0">
                    <Settings size={12} className="mr-1.5" /> Configure
                  </Button>
                </div>
              </CardHeader>
              <div className="flex-1 overflow-y-auto p-5 space-y-6 scrollbar-thin">
                {/* Description */}
                {assetDetails.description && (
                  <p className="text-sm text-slate-400 leading-relaxed">{assetDetails.description}</p>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  {/* Docs */}
                  <div className="space-y-3">
                    <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                      <FileText size={12} className="text-indigo-400" /> Associated Documents
                    </h4>
                    <div className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.06] text-xs text-slate-500 italic">
                      No documents attached. Upload via Knowledge Base.
                    </div>
                  </div>

                  {/* Metadata */}
                  <div className="space-y-3">
                    <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                      <Settings size={12} className="text-slate-500" /> Attributes & Metadata
                    </h4>
                    {assetDetails.metadata_json && Object.keys(assetDetails.metadata_json).length > 0 ? (
                      <dl className="grid grid-cols-2 gap-x-4 gap-y-2.5">
                        {Object.entries(assetDetails.metadata_json).map(([key, value]: any) => (
                          <div key={key}>
                            <dt className="text-[11px] text-slate-600 capitalize">{key.replace(/_/g, ' ')}</dt>
                            <dd className="text-xs font-medium text-slate-300 mt-0.5">{value}</dd>
                          </div>
                        ))}
                      </dl>
                    ) : (
                      <div className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.06] text-xs text-slate-500 italic">
                        No metadata attributes.
                      </div>
                    )}
                  </div>
                </div>

                {/* AI Predictive Analysis */}
                <div className="space-y-3">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                    <Sparkles size={12} className="text-blue-400" /> AI Predictive Risk Analysis
                  </h4>
                  {loadingPredictive ? (
                    <div className="flex items-center gap-3 p-5 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                      <div className="w-4 h-4 rounded-full border-2 border-blue-500 border-t-transparent animate-spin shrink-0" />
                      <span className="text-xs text-slate-500 italic">Analyzing operational history...</span>
                    </div>
                  ) : predictiveAnalysis ? (
                    <div className={`flex flex-col md:flex-row gap-5 p-5 rounded-2xl bg-gradient-to-br border ${RISK_BG(predictiveAnalysis.failure_risk_score)}`}>
                      <div className="flex flex-col items-center justify-center shrink-0 md:w-28 md:border-r md:border-white/8 md:pr-5">
                        <div className={`text-4xl font-black font-mono ${RISK_COLOR(predictiveAnalysis.failure_risk_score)}`}>
                          {predictiveAnalysis.failure_risk_score}
                        </div>
                        <div className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider text-center mt-1">
                          Risk Score
                        </div>
                        <div className="mt-2 text-xs text-slate-400 capitalize">
                          {predictiveAnalysis.trend} trend
                        </div>
                      </div>
                      <div className="flex-1">
                        <h5 className="text-xs font-semibold text-slate-300 mb-2.5">Recommendations</h5>
                        <ul className="space-y-1.5">
                          {predictiveAnalysis.recommendations.map((rec: string, idx: number) => (
                            <li key={idx} className="flex items-start gap-2 text-xs text-slate-400">
                              <div className="w-1 h-1 rounded-full bg-blue-400 mt-1.5 shrink-0" />
                              {rec}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ) : (
                    <div className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.06] text-xs text-slate-500 italic">
                      Predictive analysis unavailable.
                    </div>
                  )}
                </div>

                {/* Timeline */}
                <div className="space-y-3">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                    <AlertCircle size={12} className="text-amber-400" /> Operational History
                  </h4>
                  {timeline.length === 0 ? (
                    <div className="p-6 rounded-xl bg-white/[0.02] border border-white/[0.06] text-center text-xs text-slate-500 italic">
                      No incidents, inspections, or records found.
                    </div>
                  ) : (
                    <div className="space-y-3" />
                  )}
                </div>
              </div>
            </>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-slate-500 gap-3">
              <div className="w-16 h-16 rounded-2xl bg-white/4 border border-white/8 flex items-center justify-center">
                <FolderTree size={28} className="text-slate-600" />
              </div>
              <p className="text-sm text-slate-400">Select a resource to view details</p>
              <p className="text-xs text-slate-600">Click any item in the explorer panel</p>
            </div>
          )}
        </Card>
      </div>

      {/* Add Resource Modal */}
      {isAddModalOpen && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-md flex items-center justify-center z-50 p-4 animate-fade-in">
          <div className="w-full max-w-md rounded-2xl border border-white/10 bg-[rgba(12,18,40,0.95)] shadow-modal animate-scale-in">
            <div className="flex items-center justify-between px-6 py-4 border-b border-white/[0.07]">
              <h3 className="text-sm font-semibold text-slate-100">Add New Resource</h3>
              <button
                onClick={() => setIsAddModalOpen(false)}
                className="p-1.5 rounded-lg text-slate-500 hover:text-slate-300 hover:bg-white/8 transition-colors"
              >
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
                  <select className={inputCls + ' cursor-pointer appearance-none'}
                    value={newAsset.asset_type} onChange={e => setNewAsset({ ...newAsset, asset_type: e.target.value })}>
                    <option value="plant">Organization / Site</option>
                    <option value="area">Department / Area</option>
                    <option value="equipment">Resource / Entity</option>
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
                  className="w-full px-3 py-2.5 text-sm bg-white/5 border border-white/10 rounded-xl text-slate-200 placeholder-slate-600
                             focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500/40 transition-all resize-none h-20"
                  placeholder="Brief description..."
                  value={newAsset.description}
                  onChange={e => setNewAsset({ ...newAsset, description: e.target.value })}
                />
              </div>
              <div className="flex justify-end gap-3 pt-2 border-t border-white/[0.06]">
                <Button type="button" variant="outline" size="sm" onClick={() => setIsAddModalOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit" size="sm">
                  <Plus size={13} className="mr-1" /> Create Resource
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
