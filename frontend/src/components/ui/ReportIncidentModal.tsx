import React, { useState, useEffect } from 'react';
import { X, Loader2, AlertTriangle } from 'lucide-react';
import { Button } from './Button';
import api from '@/lib/api';
import toast from 'react-hot-toast';

interface ReportIncidentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export function ReportIncidentModal({ isOpen, onClose, onSuccess }: ReportIncidentModalProps) {
  const [loading, setLoading] = useState(false);
  const [assets, setAssets] = useState<any[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [severity, setSeverity] = useState('medium');
  const [assetId, setAssetId] = useState('');

  useEffect(() => {
    if (isOpen) {
      // Fetch assets to populate dropdown
      api.get('/assets')
        .then(res => {
          setAssets(res.data.items);
          if (res.data.items.length > 0) {
            setAssetId(res.data.items[0].id);
          }
        })
        .catch(() => toast.error('Failed to load assets'));
    } else {
      // Reset form
      setTitle('');
      setDescription('');
      setSeverity('medium');
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !assetId) {
      toast.error('Title and Asset are required');
      return;
    }

    setLoading(true);
    try {
      await api.post('/incidents', {
        title,
        description,
        severity,
        asset_id: assetId,
      });
      toast.success('Incident reported successfully');
      onSuccess();
      onClose();
    } catch (err) {
      toast.error('Failed to report incident');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-[#0b1227] border border-white/10 rounded-2xl w-full max-w-md shadow-2xl overflow-hidden animate-scale-in">
        <div className="flex items-center justify-between p-4 border-b border-white/5 bg-white/[0.02]">
          <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
            <AlertTriangle size={18} className="text-orange-400" />
            Report Anomaly
          </h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 transition-colors p-1 rounded-lg hover:bg-white/5">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full h-10 px-3 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-200 focus:outline-none focus:ring-1 focus:ring-orange-500/50 focus:border-orange-500/50"
              placeholder="e.g. Pump Vibration High"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">Asset</label>
            <select
              value={assetId}
              onChange={(e) => setAssetId(e.target.value)}
              className="w-full h-10 px-3 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-200 focus:outline-none focus:ring-1 focus:ring-orange-500/50 focus:border-orange-500/50 appearance-none"
              required
            >
              {assets.map(a => (
                <option key={a.id} value={a.id} className="bg-[#0b1227] text-slate-200">{a.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">Severity</label>
            <div className="grid grid-cols-4 gap-2">
              {['critical', 'high', 'medium', 'low'].map(s => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setSeverity(s)}
                  className={`py-1.5 rounded-lg text-xs font-medium border transition-colors capitalize ${
                    severity === s 
                    ? s === 'critical' ? 'bg-red-500/20 border-red-500/50 text-red-400' 
                    : s === 'high' ? 'bg-orange-500/20 border-orange-500/50 text-orange-400' 
                    : s === 'medium' ? 'bg-amber-500/20 border-amber-500/50 text-amber-400' 
                    : 'bg-emerald-500/20 border-emerald-500/50 text-emerald-400'
                    : 'bg-white/5 border-white/10 text-slate-400 hover:bg-white/10'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">Description (Optional)</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full h-24 p-3 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-200 focus:outline-none focus:ring-1 focus:ring-orange-500/50 focus:border-orange-500/50 resize-none"
              placeholder="Describe the anomaly..."
            />
          </div>

          <div className="pt-2 flex justify-end gap-3">
            <Button type="button" variant="ghost" onClick={onClose} disabled={loading} className="text-slate-400 hover:text-slate-300">
              Cancel
            </Button>
            <Button type="submit" disabled={loading} className="bg-orange-500 hover:bg-orange-600 text-white">
              {loading && <Loader2 size={14} className="animate-spin mr-2" />}
              Submit Report
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
