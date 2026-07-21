import { useState, useEffect, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import api from '@/lib/api';
import {
  FileUp, File, CheckCircle2, AlertCircle, Loader2,
  Trash2, Search, BrainCircuit, FileText,
} from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import toast from 'react-hot-toast';

const STATUS_CONFIG: Record<string, { icon: JSX.Element; label: string; cls: string }> = {
  completed: {
    icon: <CheckCircle2 size={13} className="text-emerald-400" />,
    label: 'Completed',
    cls: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  },
  processing: {
    icon: <Loader2 size={13} className="animate-spin text-blue-400" />,
    label: 'Processing',
    cls: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
  },
  failed: {
    icon: <AlertCircle size={13} className="text-red-400" />,
    label: 'Failed',
    cls: 'text-red-400 bg-red-500/10 border-red-500/20',
  },
};

export default function Documents() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [gaps, setGaps] = useState<any[]>([]);
  const [loadingGaps, setLoadingGaps] = useState(true);
  const [search, setSearch] = useState('');

  const fetchDocuments = async () => {
    try {
      const res = await api.get('/documents');
      setDocuments(res.data.items);
    } catch {
      console.error('Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
    const interval = setInterval(fetchDocuments, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const fetchGaps = async () => {
      try {
        const res = await api.get('/documents/gaps');
        setGaps(res.data.gaps);
      } catch {
        console.error('Failed to load knowledge gaps');
      } finally {
        setLoadingGaps(false);
      }
    };
    fetchGaps();
  }, []);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (!acceptedFiles.length) return;
    setUploading(true);
    for (const file of acceptedFiles) {
      const formData = new FormData();
      formData.append('file', file);
      try {
        await api.post('/documents/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        toast.success(`Uploaded ${file.name}`);
      } catch (error: any) {
        toast.error(`Failed: ${file.name}`);
      }
    }
    setUploading(false);
    fetchDocuments();
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'image/png': ['.png'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'text/plain': ['.txt'],
    },
  });

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this document?')) return;
    try {
      await api.delete(`/documents/${id}`);
      toast.success('Document deleted');
      fetchDocuments();
    } catch {
      toast.error('Failed to delete document');
    }
  };

  const filtered = documents.filter(d =>
    d.title?.toLowerCase().includes(search.toLowerCase())
  );

  const PRIORITY_COLORS: Record<string, string> = {
    high: 'bg-red-500/12 text-red-400 border-red-500/20',
    medium: 'bg-amber-500/12 text-amber-400 border-amber-500/20',
    low: 'bg-slate-500/12 text-slate-400 border-slate-500/20',
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-1.5 h-5 bg-gradient-to-b from-emerald-400 to-teal-400 rounded-full" />
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Knowledge Base</span>
        </div>
        <h1 className="text-2xl font-bold text-slate-100">Document Management</h1>
        <p className="text-sm text-slate-500 mt-0.5">Upload and manage documents, reports, and reference materials.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Left column */}
        <div className="space-y-4">
          {/* Upload zone */}
          <Card>
            <CardHeader className="pb-3 border-b border-white/[0.06]">
              <CardTitle className="text-sm flex items-center gap-2">
                <FileUp size={14} className="text-emerald-400" /> Upload Document
              </CardTitle>
              <CardDescription className="text-xs">Drag & drop to ingest into the AI knowledge base</CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              <div
                {...getRootProps()}
                className={`relative border-2 border-dashed rounded-2xl p-7 text-center cursor-pointer transition-all duration-300
                  ${isDragActive
                    ? 'border-blue-500/60 bg-blue-500/8 scale-[1.02]'
                    : 'border-white/10 hover:border-blue-500/30 hover:bg-white/[0.02]'}
                  ${uploading ? 'opacity-50 pointer-events-none' : ''}`}
              >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center gap-3">
                  <div className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all
                    ${isDragActive ? 'bg-blue-500/20 text-blue-400' : 'bg-white/5 text-slate-500'}`}>
                    {uploading
                      ? <Loader2 size={22} className="animate-spin text-blue-400" />
                      : <FileUp size={22} />}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-300">
                      {isDragActive ? 'Drop files here' : 'Click or drag & drop'}
                    </p>
                    <p className="text-xs text-slate-600 mt-0.5">PDF, DOCX, XLSX, PNG, JPG, TXT</p>
                  </div>
                  {!isDragActive && (
                    <span className="text-xs px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400">
                      Up to 50MB per file
                    </span>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Knowledge Gaps */}
          <Card className="border-violet-500/15 bg-gradient-to-br from-violet-500/5 to-transparent">
            <CardHeader className="pb-3 border-b border-violet-500/15">
              <CardTitle className="text-sm flex items-center gap-2 text-violet-300">
                <BrainCircuit size={14} className="text-violet-400" /> AI Knowledge Gaps
              </CardTitle>
              <CardDescription className="text-xs text-violet-400/60">Based on current corpus analysis</CardDescription>
            </CardHeader>
            <CardContent className="pt-4">
              {loadingGaps ? (
                <div className="space-y-2">
                  {[1,2].map(i => <div key={i} className="skeleton h-12 rounded-xl" />)}
                </div>
              ) : gaps.length === 0 ? (
                <div className="text-center py-4">
                  <CheckCircle2 size={20} className="mx-auto text-emerald-500/50 mb-1" />
                  <p className="text-xs text-slate-500">No gaps detected</p>
                </div>
              ) : (
                <ul className="space-y-2.5">
                  {gaps.map((gap, i) => (
                    <li key={i} className="p-3 rounded-xl bg-white/[0.03] border border-white/[0.06] hover:border-violet-500/20 transition-colors">
                      <div className="flex items-start justify-between gap-2 mb-1">
                        <span className="text-xs font-semibold text-slate-300">{gap.document_type}</span>
                        <span className={`badge border text-[10px] ${PRIORITY_COLORS[gap.priority] || PRIORITY_COLORS.low}`}>
                          {gap.priority}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-500 leading-snug">{gap.reason}</p>
                    </li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right column: Document list */}
        <Card className="lg:col-span-2 flex flex-col" style={{ height: 'calc(100vh - 13rem)' }}>
          <CardHeader className="pb-4 border-b border-white/[0.06] shrink-0">
            <div className="flex items-center justify-between gap-4">
              <CardTitle className="text-sm flex items-center gap-2">
                <FileText size={14} className="text-emerald-400" /> Documents
                {!loading && (
                  <span className="badge bg-white/5 border border-white/8 text-slate-400 text-[10px]">
                    {documents.length}
                  </span>
                )}
              </CardTitle>
              {/* Search */}
              <div className="relative">
                <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  type="text"
                  value={search}
                  onChange={e => setSearch(e.target.value)}
                  placeholder="Search documents..."
                  className="h-8 w-52 pl-8 pr-3 text-xs bg-white/5 border border-white/8 rounded-lg text-slate-300
                             placeholder-slate-600 focus:outline-none focus:ring-1 focus:ring-blue-500/40
                             focus:border-blue-500/40 transition-all"
                />
              </div>
            </div>
          </CardHeader>
          <div className="flex-1 overflow-auto">
            {loading ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <Loader2 size={24} className="animate-spin text-blue-400 mx-auto mb-2" />
                  <p className="text-sm text-slate-500">Loading documents...</p>
                </div>
              </div>
            ) : filtered.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-slate-500">
                <div className="w-14 h-14 rounded-2xl bg-white/4 border border-white/8 flex items-center justify-center mb-3">
                  <File size={24} className="text-slate-600" />
                </div>
                <p className="text-sm font-medium text-slate-400">
                  {search ? 'No documents match your search' : 'No documents uploaded yet'}
                </p>
                <p className="text-xs text-slate-600 mt-1">Upload files using the panel on the left</p>
              </div>
            ) : (
              <table className="data-table w-full">
                <thead>
                  <tr>
                    <th>Document Name</th>
                    <th>Category</th>
                    <th>Status</th>
                    <th>Uploaded</th>
                    <th className="text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((doc, i) => {
                    const status = STATUS_CONFIG[doc.processing_status] || STATUS_CONFIG.processing;
                    return (
                      <tr key={doc.id} className="group animate-fade-in" style={{ animationDelay: `${i * 0.04}s` }}>
                        <td>
                          <div className="flex items-center gap-2.5">
                            <div className="w-7 h-7 rounded-lg bg-blue-500/10 border border-blue-500/15 flex items-center justify-center shrink-0">
                              <FileText size={12} className="text-blue-400" />
                            </div>
                            <span className="text-sm font-medium text-slate-300 truncate max-w-[180px]" title={doc.title}>
                              {doc.title}
                            </span>
                          </div>
                        </td>
                        <td>
                          <span className="text-xs text-slate-400 capitalize">{doc.doc_category}</span>
                        </td>
                        <td>
                          <span className={`badge border ${status.cls}`}>
                            {status.icon}
                            {status.label}
                          </span>
                        </td>
                        <td>
                          <span className="text-xs text-slate-500">
                            {doc.created_at
                              ? formatDistanceToNow(new Date(doc.created_at), { addSuffix: true })
                              : ''}
                          </span>
                        </td>
                        <td className="text-right">
                          <button
                            onClick={() => handleDelete(doc.id)}
                            className="p-1.5 rounded-lg text-slate-600 hover:text-red-400 hover:bg-red-500/10
                                       opacity-0 group-hover:opacity-100 transition-all duration-200"
                          >
                            <Trash2 size={13} />
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}
