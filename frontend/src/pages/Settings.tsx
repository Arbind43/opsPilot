import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/Tabs';
import api from '@/lib/api';
import {
  Settings as SettingsIcon, Shield, Database, Users, Loader2, Activity, Building2, CheckCircle2,
} from 'lucide-react';
import { format, parseISO } from 'date-fns';

const INDUSTRIES = [
  { id: 'manufacturing', label: 'Manufacturing', emoji: '🏭', desc: 'Equipment, maintenance, production lines' },
  { id: 'healthcare', label: 'Healthcare', emoji: '🏥', desc: 'Clinical docs, compliance, patient workflows' },
  { id: 'finance', label: 'Finance', emoji: '🏦', desc: 'Risk, compliance, regulatory documents' },
  { id: 'logistics', label: 'Logistics', emoji: '🚚', desc: 'Fleet, routes, inventory, SOPs' },
  { id: 'legal', label: 'Legal', emoji: '⚖️', desc: 'Contracts, case files, precedents' },
  { id: 'energy', label: 'Energy', emoji: '⚡', desc: 'Grid ops, safety, environmental compliance' },
  { id: 'retail', label: 'Retail', emoji: '🛒', desc: 'Product catalogs, supplier docs, audits' },
  { id: 'custom', label: 'Custom', emoji: '🔧', desc: 'General purpose — any domain' },
];

const ACTION_COLORS: Record<string, string> = {
  create: 'bg-emerald-500/12 text-emerald-400 border-emerald-500/25',
  update: 'bg-blue-500/12 text-blue-400 border-blue-500/25',
  delete: 'bg-red-500/12 text-red-400 border-red-500/25',
  login: 'bg-violet-500/12 text-violet-400 border-violet-500/25',
  export: 'bg-amber-500/12 text-amber-400 border-amber-500/25',
};

export default function Settings() {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedIndustry, setSelectedIndustry] = useState<string>(
    () => localStorage.getItem('opspilot_industry') || 'manufacturing'
  );
  const [industrySaved, setIndustrySaved] = useState(false);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await api.get('/settings/audit-logs');
        setLogs(res.data.items);
      } catch {
        console.error('Failed to fetch audit logs');
      } finally {
        setLoading(false);
      }
    };
    fetchLogs();
  }, []);

  const handleSaveIndustry = (id: string) => {
    setSelectedIndustry(id);
    localStorage.setItem('opspilot_industry', id);
    setIndustrySaved(true);
    setTimeout(() => setIndustrySaved(false), 2500);
  };

  const selectedIndustryData = INDUSTRIES.find(i => i.id === selectedIndustry);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-1.5 h-5 bg-gradient-to-b from-slate-400 to-slate-600 rounded-full" />
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Configuration</span>
        </div>
        <h1 className="text-2xl font-bold text-slate-100">System Settings</h1>
        <p className="text-sm text-slate-500 mt-0.5">Manage platform configuration and security audits.</p>
      </div>

      <Tabs defaultValue="industry" className="space-y-5">
        <TabsList className="bg-white/4 border border-white/8 p-1 rounded-xl gap-0.5 flex-wrap h-auto">
          {[
            { value: 'industry', icon: <Building2 size={13} />, label: 'Industry' },
            { value: 'general', icon: <SettingsIcon size={13} />, label: 'General' },
            { value: 'users', icon: <Users size={13} />, label: 'Users & Roles' },
            { value: 'integrations', icon: <Database size={13} />, label: 'Integrations' },
            { value: 'audit', icon: <Shield size={13} />, label: 'Audit Log' },
          ].map(tab => (
            <TabsTrigger
              key={tab.value}
              value={tab.value}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium text-slate-400
                         data-[state=active]:bg-blue-500/20 data-[state=active]:text-blue-300
                         data-[state=active]:border data-[state=active]:border-blue-500/25
                         hover:text-slate-200 transition-all duration-200"
            >
              {tab.icon}
              {tab.label}
            </TabsTrigger>
          ))}
        </TabsList>

        {/* Industry Profile */}
        <TabsContent value="industry" className="animate-fade-in">
          <Card>
            <CardHeader className="border-b border-white/[0.06]">
              <CardTitle className="text-sm flex items-center gap-2">
                <Building2 size={15} className="text-blue-400" /> Industry Profile
              </CardTitle>
              <CardDescription className="text-xs">
                Select your industry to tailor the AI Copilot, compliance frameworks, and terminology.
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-5">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
                {INDUSTRIES.map(industry => {
                  const isSelected = selectedIndustry === industry.id;
                  return (
                    <button
                      key={industry.id}
                      onClick={() => handleSaveIndustry(industry.id)}
                      className={`relative text-left p-4 rounded-2xl border-2 transition-all duration-200 group
                        ${isSelected
                          ? 'border-blue-500/50 bg-blue-500/10 shadow-[0_0_20px_rgba(59,130,246,0.15)]'
                          : 'border-white/[0.07] bg-white/[0.02] hover:border-blue-500/25 hover:bg-white/[0.04]'}`}
                    >
                      {isSelected && (
                        <CheckCircle2 size={13} className="absolute top-3 right-3 text-blue-400" />
                      )}
                      <div className="text-2xl mb-2.5">{industry.emoji}</div>
                      <p className={`text-xs font-semibold mb-0.5 ${isSelected ? 'text-blue-300' : 'text-slate-300'}`}>
                        {industry.label}
                      </p>
                      <p className="text-[10px] text-slate-500 leading-relaxed">{industry.desc}</p>
                    </button>
                  );
                })}
              </div>

              {/* Saved notification */}
              {industrySaved && (
                <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-xl px-4 py-3 mb-4 animate-scale-in">
                  <CheckCircle2 size={13} />
                  Industry set to <strong>{selectedIndustryData?.label}</strong> — AI Copilot will adapt its context.
                </div>
              )}

              {/* Active indicator */}
              <div className="flex items-center gap-3 p-4 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                <span className="text-xl">{selectedIndustryData?.emoji}</span>
                <div>
                  <p className="text-xs font-semibold text-slate-300">{selectedIndustryData?.label}</p>
                  <p className="text-[11px] text-slate-500 mt-0.5">
                    Active profile — Copilot, compliance modules, and graph use domain-specific context.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* General */}
        <TabsContent value="general" className="animate-fade-in">
          <Card>
            <CardHeader className="border-b border-white/[0.06]">
              <CardTitle className="text-sm">Workspace General Settings</CardTitle>
              <CardDescription className="text-xs">Configure your organization's core operating parameters.</CardDescription>
            </CardHeader>
            <CardContent className="pt-5">
              <p className="text-sm text-slate-500">Settings panel configuration coming soon.</p>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Users */}
        <TabsContent value="users" className="animate-fade-in">
          <Card>
            <CardHeader className="border-b border-white/[0.06]">
              <CardTitle className="text-sm">User Management</CardTitle>
              <CardDescription className="text-xs">Manage team members, roles, and access permissions.</CardDescription>
            </CardHeader>
            <CardContent className="pt-5">
              <p className="text-sm text-slate-500">User management table coming soon.</p>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Integrations */}
        <TabsContent value="integrations" className="animate-fade-in">
          <Card>
            <CardHeader className="border-b border-white/[0.06]">
              <CardTitle className="text-sm">AI & Database Integrations</CardTitle>
              <CardDescription className="text-xs">Manage connections to Neo4j, ChromaDB, and LLM APIs.</CardDescription>
            </CardHeader>
            <CardContent className="pt-5">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {[
                  { name: 'Gemini 1.5 Pro', desc: 'LLM Engine', color: 'blue', status: 'Connected' },
                  { name: 'ChromaDB', desc: 'Vector Store', color: 'violet', status: 'Connected' },
                  { name: 'Neo4j', desc: 'Graph Database', color: 'emerald', status: 'Connected' },
                ].map(int => (
                  <div key={int.name} className="p-4 rounded-xl bg-white/[0.02] border border-white/[0.06]">
                    <p className="text-sm font-semibold text-slate-300">{int.name}</p>
                    <p className="text-xs text-slate-500 mt-0.5 mb-3">{int.desc}</p>
                    <span className="badge bg-emerald-500/10 border-emerald-500/20 text-emerald-400 text-[10px]">
                      <div className="status-dot online" /> {int.status}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Audit Log */}
        <TabsContent value="audit" className="animate-fade-in">
          <Card>
            <CardHeader className="border-b border-white/[0.06]">
              <CardTitle className="text-sm flex items-center gap-2">
                <Activity size={14} className="text-indigo-400" /> Global Audit Log
              </CardTitle>
              <CardDescription className="text-xs">Immutable ledger of all critical system events.</CardDescription>
            </CardHeader>
            <CardContent className="p-0">
              {loading ? (
                <div className="p-6 space-y-3">
                  {[1,2,3,4].map(i => <div key={i} className="skeleton h-12 rounded-xl" />)}
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="data-table w-full">
                    <thead>
                      <tr>
                        <th>Timestamp</th>
                        <th>User ID</th>
                        <th>Action</th>
                        <th>Resource</th>
                        <th>IP Address</th>
                      </tr>
                    </thead>
                    <tbody>
                      {logs.map((log, i) => (
                        <tr key={log.id} className="animate-fade-in" style={{ animationDelay: `${i * 0.03}s` }}>
                          <td>
                            <span className="text-xs text-slate-400 font-mono">
                              {log.timestamp ? format(parseISO(log.timestamp), 'MMM dd, HH:mm:ss') : 'N/A'}
                            </span>
                          </td>
                          <td>
                            <span className="text-xs font-mono text-slate-500">
                              {log.user_id?.substring(0, 8)}...
                            </span>
                          </td>
                          <td>
                            <span className={`badge border text-[10px] uppercase tracking-wider
                              ${ACTION_COLORS[log.action] || 'bg-white/5 text-slate-400 border-white/8'}`}>
                              {log.action}
                            </span>
                          </td>
                          <td>
                            <span className="text-xs text-slate-300 capitalize">{log.resource_type}</span>
                          </td>
                          <td>
                            <span className="text-xs font-mono text-slate-600">{log.ip_address || '127.0.0.1'}</span>
                          </td>
                        </tr>
                      ))}
                      {logs.length === 0 && (
                        <tr>
                          <td colSpan={5} className="px-5 py-14 text-center">
                            <div className="flex flex-col items-center gap-3 text-slate-500">
                              <Shield size={24} className="text-slate-600" />
                              <p className="text-sm text-slate-400">No audit events recorded yet</p>
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
        </TabsContent>
      </Tabs>
    </div>
  );
}
