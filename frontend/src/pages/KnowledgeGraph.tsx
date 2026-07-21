import { useEffect, useState, useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  Handle,
  Position,
} from 'reactflow';
import 'reactflow/dist/style.css';
import api from '@/lib/api';
import { Network, Database, FileText, AlertCircle, RefreshCw, Layers } from 'lucide-react';
import { Button } from '@/components/ui/Button';

const AssetNode = ({ data }: any) => (
  <div className="px-4 py-2.5 rounded-xl bg-[rgba(17,25,50,0.95)] border-2 border-blue-500/60 w-44 shadow-[0_4px_14px_rgba(59,130,246,0.2)] backdrop-blur-sm">
    <Handle type="target" position={Position.Top} className="!bg-blue-500 !border-blue-400" />
    <div className="flex items-center gap-2">
      <div className="w-5 h-5 rounded-lg bg-blue-500/20 flex items-center justify-center shrink-0">
        <Database size={10} className="text-blue-400" />
      </div>
      <div className="font-semibold text-blue-200 text-xs truncate">{data.label}</div>
    </div>
    {data.properties?.type && (
      <div className="text-[10px] text-slate-500 mt-0.5 capitalize ml-7">{data.properties.type}</div>
    )}
    <Handle type="source" position={Position.Bottom} className="!bg-blue-500 !border-blue-400" />
  </div>
);

const DocumentNode = ({ data }: any) => (
  <div className="px-4 py-2.5 rounded-xl bg-[rgba(17,25,50,0.95)] border-2 border-violet-500/60 w-44 shadow-[0_4px_14px_rgba(139,92,246,0.2)] backdrop-blur-sm">
    <Handle type="target" position={Position.Top} className="!bg-violet-500 !border-violet-400" />
    <div className="flex items-center gap-2">
      <div className="w-5 h-5 rounded-lg bg-violet-500/20 flex items-center justify-center shrink-0">
        <FileText size={10} className="text-violet-400" />
      </div>
      <div className="font-semibold text-violet-200 text-xs truncate">{data.label}</div>
    </div>
    <Handle type="source" position={Position.Bottom} className="!bg-violet-500 !border-violet-400" />
  </div>
);

const DefaultNode = ({ data }: any) => (
  <div className="px-3 py-2 rounded-xl bg-[rgba(17,25,50,0.95)] border border-white/15 w-36 shadow-card backdrop-blur-sm">
    <Handle type="target" position={Position.Top} className="!bg-slate-500" />
    <div className="text-center font-medium text-slate-400 text-xs truncate">{data.label}</div>
    <Handle type="source" position={Position.Bottom} className="!bg-slate-500" />
  </div>
);

const nodeTypes = {
  Asset: AssetNode,
  Document: DocumentNode,
  Component: AssetNode,
  Section: DefaultNode,
  Parameter: DefaultNode,
  Person: DefaultNode,
};

export default function KnowledgeGraph() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [loading, setLoading] = useState(true);

  const fetchGraph = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get('/graph/explore');
      const { nodes: rawNodes, edges: rawEdges } = res.data;

      const initialNodes = rawNodes.map((n: any) => {
        const x = Math.random() * 900;
        const y = Math.random() * 650;
        let type = 'default';
        if (n.label === 'Asset' || n.label === 'Component') type = 'Asset';
        if (n.label === 'Document') type = 'Document';
        return {
          id: n.id,
          type: nodeTypes[type as keyof typeof nodeTypes] ? type : 'default',
          position: { x, y },
          data: { label: n.id, properties: n.properties, fullLabel: n.label },
        };
      });

      const initialEdges = rawEdges.map((e: any) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        label: e.type,
        animated: true,
        style: { stroke: 'rgba(99,155,255,0.4)', strokeWidth: 1.5 },
        labelStyle: { fill: '#94a3b8', fontSize: 9, fontFamily: 'Inter' },
        labelBgStyle: { fill: 'rgba(10,15,35,0.8)', rx: 4, ry: 4 },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: 'rgba(99,155,255,0.5)',
          width: 16,
          height: 16,
        },
      }));

      setNodes(initialNodes);
      setEdges(initialEdges);
    } catch {
      console.error('Failed to load graph');
    } finally {
      setLoading(false);
    }
  }, [setNodes, setEdges]);

  useEffect(() => { fetchGraph(); }, [fetchGraph]);

  return (
    <div className="h-[calc(100vh-7rem)] flex flex-col gap-4 animate-fade-in">
      {/* Header */}
      <div className="flex items-end justify-between shrink-0">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className="w-1.5 h-5 bg-gradient-to-b from-cyan-400 to-blue-400 rounded-full" />
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Graph Explorer</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-100">Knowledge Graph</h1>
          <p className="text-sm text-slate-500 mt-0.5">
            {nodes.length > 0
              ? `${nodes.length} nodes · ${edges.length} relationships`
              : 'Explore relationships between assets, documents, and operational data'}
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={fetchGraph}
          disabled={loading}
          className="text-xs"
        >
          <RefreshCw size={13} className={`mr-1.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {/* Graph canvas */}
      <div className="flex-1 rounded-2xl border border-white/[0.07] overflow-hidden relative shadow-card"
        style={{ background: 'rgba(5,9,24,0.9)' }}>
        {/* Legend */}
        <div className="absolute top-4 left-4 z-10 flex gap-2">
          {[
            { color: '#3b82f6', label: 'Assets', shadow: 'shadow-[0_0_8px_rgba(59,130,246,0.3)]' },
            { color: '#8b5cf6', label: 'Documents', shadow: 'shadow-[0_0_8px_rgba(139,92,246,0.3)]' },
            { color: '#94a3b8', label: 'Other', shadow: '' },
          ].map(item => (
            <div key={item.label}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[rgba(10,15,35,0.85)] border border-white/10 backdrop-blur-sm text-xs text-slate-300 ${item.shadow}`}>
              <div className="w-2 h-2 rounded-full" style={{ background: item.color }} />
              {item.label}
            </div>
          ))}
        </div>

        {/* Node count badge */}
        {nodes.length > 0 && (
          <div className="absolute top-4 right-4 z-10 flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[rgba(10,15,35,0.85)] border border-white/10 backdrop-blur-sm text-xs text-slate-300">
            <Layers size={12} className="text-blue-400" />
            {nodes.length} entities
          </div>
        )}

        {loading && nodes.length === 0 ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-400">
            <Network size={40} className="mb-3 opacity-30 animate-pulse" />
            <p className="text-sm font-medium text-slate-400">Querying Neo4j Graph...</p>
            <p className="text-xs text-slate-600 mt-1">Building relationship map</p>
          </div>
        ) : nodes.length === 0 ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-400">
            <div className="w-16 h-16 rounded-2xl bg-white/4 border border-white/8 flex items-center justify-center mb-4">
              <AlertCircle size={28} className="text-amber-500/60" />
            </div>
            <p className="text-sm font-medium text-slate-400">Graph is empty</p>
            <p className="text-xs text-slate-600 mt-1 max-w-xs text-center">
              Upload technical documents to automatically generate knowledge connections
            </p>
          </div>
        ) : (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            nodeTypes={nodeTypes}
            fitView
            fitViewOptions={{ padding: 0.2 }}
            attributionPosition="bottom-left"
            minZoom={0.15}
            maxZoom={2}
          >
            <Controls
              className="!bg-[rgba(10,15,35,0.9)] !border-white/10 !rounded-xl !shadow-card"
              style={{ borderRadius: '12px' }}
            />
            <MiniMap
              nodeColor={n => {
                if (n.type === 'Asset') return '#3b82f6';
                if (n.type === 'Document') return '#8b5cf6';
                return '#475569';
              }}
              maskColor="rgba(5,9,24,0.7)"
              style={{
                background: 'rgba(10,15,35,0.9)',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: '12px',
              }}
            />
            <Background
              color="rgba(99,155,255,0.08)"
              gap={28}
              style={{ backgroundColor: 'transparent' }}
            />
          </ReactFlow>
        )}
      </div>
    </div>
  );
}
