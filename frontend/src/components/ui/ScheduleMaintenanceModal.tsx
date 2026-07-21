import React, { useState, useEffect } from 'react';
import { X, Loader2, Calendar } from 'lucide-react';
import { Button } from './Button';
import api from '@/lib/api';
import toast from 'react-hot-toast';

interface ScheduleMaintenanceModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export function ScheduleMaintenanceModal({ isOpen, onClose, onSuccess }: ScheduleMaintenanceModalProps) {
  const [loading, setLoading] = useState(false);
  const [assets, setAssets] = useState<any[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [maintenanceType, setMaintenanceType] = useState('preventive');
  const [assetId, setAssetId] = useState('');
  const [scheduledAt, setScheduledAt] = useState('');

  useEffect(() => {
    if (isOpen) {
      api.get('/assets')
        .then(res => {
          setAssets(res.data.items);
          if (res.data.items.length > 0) {
            setAssetId(res.data.items[0].id);
          }
        })
        .catch(() => toast.error('Failed to load assets'));
      
      const today = new Date();
      today.setDate(today.getDate() + 1);
      setScheduledAt(today.toISOString().split('T')[0]);
    } else {
      setTitle('');
      setDescription('');
      setMaintenanceType('preventive');
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
      await api.post('/maintenance', {
        title,
        description,
        maintenance_type: maintenanceType,
        asset_id: assetId,
        scheduled_at: scheduledAt ? new Date(scheduledAt).toISOString() : null,
      });
      toast.success('Task scheduled successfully');
      onSuccess();
      onClose();
    } catch (err) {
      toast.error('Failed to schedule task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="bg-[#0b1227] border border-white/10 rounded-2xl w-full max-w-md shadow-2xl overflow-hidden animate-scale-in">
        <div className="flex items-center justify-between p-4 border-b border-white/5 bg-white/[0.02]">
          <h2 className="text-lg font-semibold text-slate-100 flex items-center gap-2">
            <Calendar size={18} className="text-blue-400" />
            Schedule Task
          </h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200 transition-colors p-1 rounded-lg hover:bg-white/5">
            <X size={18} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">Task Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full h-10 px-3 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-500/50 focus:border-blue-500/50"
              placeholder="e.g. Pump Lubrication"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">Asset</label>
            <select
              value={assetId}
              onChange={(e) => setAssetId(e.target.value)}
              className="w-full h-10 px-3 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-500/50 focus:border-blue-500/50 appearance-none"
              required
            >
              {assets.map(a => (
                <option key={a.id} value={a.id} className="bg-[#0b1227] text-slate-200">{a.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">Date</label>
            <input
              type="date"
              value={scheduledAt}
              onChange={(e) => setScheduledAt(e.target.value)}
              className="w-full h-10 px-3 bg-white/5 border border-white/10 rounded-lg text-sm text-slate-200 focus:outline-none focus:ring-1 focus:ring-blue-500/50 focus:border-blue-500/50"
              style={{ colorScheme: 'dark' }}
              required
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">Type</label>
            <div className="grid grid-cols-3 gap-2">
              {['preventive', 'predictive', 'corrective'].map(t => (
                <button
                  key={t}
                  type="button"
                  onClick={() => setMaintenanceType(t)}
                  className={`py-1.5 rounded-lg text-xs font-medium border transition-colors capitalize ${
                    maintenanceType === t 
                    ? t === 'preventive' ? 'bg-blue-500/20 border-blue-500/50 text-blue-400' 
                    : t === 'predictive' ? 'bg-violet-500/20 border-violet-500/50 text-violet-400' 
                    : 'bg-orange-500/20 border-orange-500/50 text-orange-400'
                    : 'bg-white/5 border-white/10 text-slate-400 hover:bg-white/10'
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          <div className="pt-2 flex justify-end gap-3">
            <Button type="button" variant="ghost" onClick={onClose} disabled={loading} className="text-slate-400 hover:text-slate-300">
              Cancel
            </Button>
            <Button type="submit" disabled={loading} className="bg-blue-500 hover:bg-blue-600 text-white">
              {loading && <Loader2 size={14} className="animate-spin mr-2" />}
              Schedule
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
