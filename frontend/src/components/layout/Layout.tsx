import React, { useState, useEffect, useCallback } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import {
  getNavItemsForRole, ROLE_META, isValidRole, type UserRole,
} from '@/lib/rbac';
import {
  LayoutDashboard, Files, AlertTriangle, Wrench, CheckSquare,
  PieChart, Settings, LogOut, BrainCircuit, Box, Network,
  Search, Bell, ChevronRight, Menu, X, Sparkles, Shield,
  ShieldCheck, Cpu, Eye, Zap, Command,
} from 'lucide-react';
import CopilotWidget from '@/components/ui/CopilotWidget';

const ICON_MAP: Record<string, React.ComponentType<any>> = {
  LayoutDashboard, Files, AlertTriangle, Wrench, CheckSquare,
  PieChart, Settings, BrainCircuit, Box, Network, ShieldCheck, Cpu, Eye,
};

const PAGE_TITLES: Record<string, { title: string; subtitle: string; color: string }> = {
  '/':            { title: 'Dashboard',              subtitle: 'Real-time pulse of your operations',                color: '#3b82f6' },
  '/documents':   { title: 'Knowledge Base',         subtitle: 'Upload and manage your document corpus',            color: '#8b5cf6' },
  '/assets':      { title: 'Resource Management',    subtitle: 'Hierarchical view of all operational entities',     color: '#06b6d4' },
  '/graph':       { title: 'Knowledge Graph',        subtitle: 'Explore relational intelligence across your data',  color: '#f59e0b' },
  '/incidents':   { title: 'Incident Management',    subtitle: 'Track anomalies and AI-driven root cause analysis', color: '#f43f5e' },
  '/maintenance': { title: 'Maintenance Intelligence',subtitle: 'Predictive, preventive, and corrective tasks',     color: '#10b981' },
  '/compliance':  { title: 'Compliance Checking',    subtitle: 'Automated AI evaluation against regulatory standards', color: '#22c55e' },
  '/reports':     { title: 'Reporting Engine',       subtitle: 'Generate and export AI-driven operational insights', color: '#a855f7' },
  '/settings':    { title: 'System Settings',        subtitle: 'Configure platform and view security audits',       color: '#64748b' },
};

const NAV_ICON_COLORS: Record<string, string> = {
  '/':            '#60a5fa',
  '/documents':   '#a78bfa',
  '/assets':      '#22d3ee',
  '/graph':       '#fbbf24',
  '/incidents':   '#f87171',
  '/maintenance': '#34d399',
  '/compliance':  '#4ade80',
  '/reports':     '#c084fc',
  '/settings':    '#94a3b8',
};

export default function Layout({ children }: { children: React.ReactNode }) {
  const user    = useAuthStore(s => s.user);
  const logout  = useAuthStore(s => s.logout);
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen]   = useState(false);
  const [scrolled, setScrolled]         = useState(false);
  const [showCopilot, setShowCopilot]   = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [copilotWidth, setCopilotWidth] = useState(420);

  const handleDrag = useCallback((e: MouseEvent) => {
    const nw = window.innerWidth - e.clientX;
    if (nw > 320 && nw < window.innerWidth * 0.8) setCopilotWidth(nw);
  }, []);
  const handleDragEnd = useCallback(() => {
    document.removeEventListener('mousemove', handleDrag);
    document.removeEventListener('mouseup', handleDragEnd);
    document.body.style.cursor = 'default';
  }, [handleDrag]);
  const startDrag = (e: React.MouseEvent) => {
    e.preventDefault();
    document.addEventListener('mousemove', handleDrag);
    document.addEventListener('mouseup', handleDragEnd);
    document.body.style.cursor = 'ew-resize';
  };

  const currentPage = PAGE_TITLES[location.pathname] ?? { title: 'OpsPilot AI', subtitle: '', color: '#3b82f6' };
  const role      = (user?.role ?? 'viewer') as UserRole;
  const roleMeta  = isValidRole(role) ? ROLE_META[role] : ROLE_META.viewer;
  const navItems  = getNavItemsForRole(role);
  const mainNav   = navItems.filter(i => i.path !== '/settings');
  const systemNav = navItems.filter(i => i.path === '/settings');

  const handleLogout = () => { logout(); navigate('/login'); };

  useEffect(() => {
    const el = document.getElementById('main-content');
    if (!el) return;
    const onScroll = () => setScrolled(el.scrollTop > 8);
    el.addEventListener('scroll', onScroll);
    return () => el.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    const fn = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); setShowCopilot(true); }
    };
    window.addEventListener('keydown', fn);
    return () => window.removeEventListener('keydown', fn);
  }, []);

  useEffect(() => { setSidebarOpen(false); }, [location.pathname]);

  const initials = user?.full_name?.split(' ').map((n: string) => n[0]).join('').toUpperCase().slice(0, 2) || 'U';

  return (
    <div className="flex h-screen bg-background overflow-hidden mesh-bg">

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)} />
      )}

      {/* ─────────────────── SIDEBAR ─────────────────────── */}
      <aside className={`
        fixed lg:static inset-y-0 left-0 z-30 flex flex-col w-[252px] shrink-0
        transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}
        style={{
          background: 'linear-gradient(180deg, #050a18 0%, #070d1e 60%, #050a18 100%)',
          borderRight: '1px solid rgba(255,255,255,0.06)',
        }}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-5 py-5" style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
          <div className="relative">
            <div className="w-9 h-9 rounded-xl flex items-center justify-center"
              style={{ background: 'linear-gradient(135deg, #3b82f6 0%, #7c3aed 100%)', boxShadow: '0 4px 16px rgba(59,130,246,0.4)' }}>
              <BrainCircuit size={18} className="text-white" />
            </div>
            <div className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-[#050a18]"
              style={{ boxShadow: '0 0 6px #10b981' }} />
          </div>
          <div>
            <span className="text-white font-extrabold text-sm tracking-tight"
              style={{ background: 'linear-gradient(135deg,#fff 0%,#94a3b8 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              OpsPilot AI
            </span>
            <p className="text-[10px] text-slate-600 font-semibold tracking-widest uppercase mt-0.5">Enterprise Platform</p>
          </div>
          <button className="ml-auto lg:hidden text-slate-600 hover:text-slate-300 transition-colors"
            onClick={() => setSidebarOpen(false)}>
            <X size={16} />
          </button>
        </div>

        {/* Role Badge */}
        <div className="mx-3 mt-3">
          <div className={`flex items-center gap-2 px-3 py-2 rounded-xl border ${roleMeta.bgColor} ${roleMeta.borderColor}`}
            style={{ boxShadow: '0 2px 8px rgba(0,0,0,0.2)' }}>
            <div className="w-2 h-2 rounded-full shrink-0 animate-pulse" style={{ background: roleMeta.badgeGradient, boxShadow: `0 0 6px ${roleMeta.badgeGradient}` }} />
            <span className={`text-xs font-bold ${roleMeta.color}`}>{roleMeta.label}</span>
            <span className="ml-auto text-[10px] text-slate-600 font-medium">Access</span>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto no-scrollbar py-4 px-3 space-y-0.5">
          <p className="text-[10px] font-bold text-slate-700 uppercase tracking-widest px-3 pb-2 pt-1">Navigation</p>
          {mainNav.map((item, i) => {
            const Icon = ICON_MAP[item.icon] ?? LayoutDashboard;
            const iconColor = NAV_ICON_COLORS[item.path] ?? '#94a3b8';
            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `nav-item group animate-slide-in-left stagger-${Math.min(i + 1, 5)} ${isActive ? 'active' : ''}`
                }
              >
                {({ isActive }) => (
                  <>
                    <div className="icon-box-sm"
                      style={{
                        background: isActive ? `${iconColor}18` : 'rgba(255,255,255,0.04)',
                        border: `1px solid ${isActive ? iconColor + '30' : 'rgba(255,255,255,0.05)'}`,
                      }}>
                      <Icon size={14} style={{ color: isActive ? iconColor : '#64748b' }}
                        className="transition-colors group-hover:!text-white" />
                    </div>
                    <span className="flex-1 text-sm">{item.label}</span>
                    {item.badge && (
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-md tracking-wider"
                        style={{ background: 'rgba(139,92,246,0.2)', color: '#a78bfa', border: '1px solid rgba(139,92,246,0.3)' }}>
                        {item.badge}
                      </span>
                    )}
                    {isActive && <ChevronRight size={12} style={{ color: iconColor }} className="opacity-70" />}
                  </>
                )}
              </NavLink>
            );
          })}

          {systemNav.length > 0 && (
            <>
              <div className="pt-4 pb-2">
                <div className="h-px" style={{ background: 'linear-gradient(90deg,transparent,rgba(255,255,255,0.06),transparent)' }} />
              </div>
              <p className="text-[10px] font-bold text-slate-700 uppercase tracking-widest px-3 pb-2 pt-1">System</p>
              {systemNav.map((item) => {
                const Icon = ICON_MAP[item.icon] ?? Settings;
                return (
                  <NavLink key={item.path} to={item.path}
                    className={({ isActive }) => `nav-item group ${isActive ? 'active' : ''}`}>
                    {({ isActive }) => (
                      <>
                        <Icon size={15} className={`shrink-0 transition-colors ${isActive ? 'text-blue-400' : 'text-slate-600 group-hover:text-slate-300'}`} />
                        <span className="flex-1 text-sm">{item.label}</span>
                        {isActive && <ChevronRight size={12} className="text-blue-400 opacity-60" />}
                      </>
                    )}
                  </NavLink>
                );
              })}
            </>
          )}
        </nav>

        {/* AI Status */}
        <div className="mx-3 mb-3">
          <div className="flex items-center gap-2 px-3 py-2.5 rounded-xl"
            style={{ background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.18)', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.04)' }}>
            <Sparkles size={12} className="text-emerald-400" />
            <span className="text-xs font-semibold text-emerald-400">AI Engine Online</span>
            <div className="ml-auto flex items-end gap-0.5">
              {[3,5,4,6,3].map((h, i) => (
                <div key={i} className="w-0.5 bg-emerald-400 rounded-full"
                  style={{ height: `${h}px`, animation: `bounceDot 1.2s ease-in-out infinite`, animationDelay: `${i * 0.12}s`, opacity: 0.8 }} />
              ))}
            </div>
          </div>
        </div>

        {/* User Card */}
        <div className="p-3" style={{ borderTop: '1px solid rgba(255,255,255,0.05)' }}>
          <div className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-white/5 transition-all duration-200 cursor-pointer group">
            <div className="relative shrink-0">
              <div className="w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold text-white"
                style={{ background: 'linear-gradient(135deg, #3b82f6 0%, #7c3aed 100%)', boxShadow: '0 0 12px rgba(59,130,246,0.4)' }}>
                {initials}
              </div>
              <div className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-[#050a18]" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-bold text-slate-200 truncate">{user?.full_name}</p>
              <p className={`text-[10px] capitalize truncate font-semibold ${roleMeta.color}`}>{roleMeta.label}</p>
            </div>
            <button onClick={handleLogout}
              className="opacity-0 group-hover:opacity-100 transition-all text-slate-600 hover:text-red-400 p-1.5 rounded-lg hover:bg-red-500/10"
              title="Sign out">
              <LogOut size={13} />
            </button>
          </div>
        </div>
      </aside>

      {/* ─────────────────── MAIN ─────────────────────────── */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">

        {/* Header */}
        <header className={`
          h-[60px] flex items-center justify-between px-5 lg:px-7 shrink-0
          transition-all duration-300 relative z-40
          ${scrolled
            ? 'bg-[rgba(5,10,24,0.92)] backdrop-blur-xl border-b shadow-[0_2px_24px_rgba(0,0,0,0.4)]'
            : 'bg-[rgba(5,10,24,0.5)] backdrop-blur-sm border-b'}
        `}
          style={{ borderColor: 'rgba(255,255,255,0.06)' }}>

          {/* Left */}
          <div className="flex items-center gap-3">
            <button onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 rounded-lg text-slate-500 hover:text-slate-200 hover:bg-white/8 transition-colors">
              <Menu size={18} />
            </button>
            <div className="flex items-center gap-3">
              <div className="w-1 h-6 rounded-full hidden sm:block"
                style={{ background: `linear-gradient(180deg, ${currentPage.color}, transparent)` }} />
              <div>
                <h2 className="text-sm font-extrabold text-slate-100 leading-none tracking-tight">{currentPage.title}</h2>
                <p className="text-[11px] text-slate-500 mt-0.5 hidden sm:block font-medium">{currentPage.subtitle}</p>
              </div>
            </div>
          </div>

          {/* Right */}
          <div className="flex items-center gap-2">
            {/* Copilot search bar */}
            <button
              onClick={() => setShowCopilot(true)}
              className={`hidden sm:flex items-center gap-2 h-9 px-3 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-200 transition-all duration-200 cursor-text`}
              style={{
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.08)',
                minWidth: 200,
              }}>
              <Search size={13} className="text-slate-500" />
              <span className="flex-1 text-left">Ask Copilot...</span>
              <kbd className="flex items-center gap-0.5 text-[10px] px-1.5 py-0.5 rounded bg-white/8 text-slate-600 font-mono border border-white/8">
                <Command size={9} />K
              </kbd>
            </button>

            {/* Notifications */}
            <div className="relative">
              <button
                onClick={() => setShowNotifications(!showNotifications)}
                className="relative p-2 rounded-xl text-slate-500 hover:text-slate-200 hover:bg-white/8 transition-all duration-200">
                <Bell size={17} />
                <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full animate-pulse"
                  style={{ background: '#3b82f6', boxShadow: '0 0 6px #3b82f6' }} />
              </button>

              {showNotifications && (
                <>
                  <div className="fixed inset-0 z-40" onClick={() => setShowNotifications(false)} />
                  <div className="absolute right-0 top-full mt-2 w-80 rounded-2xl shadow-[0_16px_48px_rgba(0,0,0,0.7)] z-50 overflow-hidden animate-scale-in"
                    style={{ background: '#070d1e', border: '1px solid rgba(255,255,255,0.1)' }}>
                    <div className="p-4 flex items-center justify-between"
                      style={{ borderBottom: '1px solid rgba(255,255,255,0.06)', background: 'rgba(255,255,255,0.02)' }}>
                      <span className="text-sm font-bold text-white">Notifications</span>
                      <button className="text-xs font-semibold" style={{ color: '#60a5fa' }}>Clear all</button>
                    </div>
                    <div className="max-h-[320px] overflow-y-auto no-scrollbar">
                      {[
                        { title: 'New Incident Logged', desc: 'Pump Vibration High detected on Unit 4.', time: 'Just now', color: '#f87171', bg: 'rgba(244,63,94,0.08)' },
                        { title: 'RCA Completed', desc: 'AI finished analyzing Incident #402.', time: '10m ago', color: '#c084fc', bg: 'rgba(192,132,252,0.08)' },
                        { title: 'System Updated', desc: 'OpsPilot agent updated to v2.4.1.', time: '1h ago', color: '#60a5fa', bg: 'rgba(96,165,250,0.08)' },
                      ].map((n, i) => (
                        <div key={i} className="flex gap-3 p-4 cursor-pointer transition-colors"
                          style={{ background: i === 0 ? n.bg : 'transparent', borderBottom: '1px solid rgba(255,255,255,0.04)' }}
                          onMouseEnter={e => (e.currentTarget.style.background = n.bg)}
                          onMouseLeave={e => (e.currentTarget.style.background = i === 0 ? n.bg : 'transparent')}>
                          <div className="w-8 h-8 rounded-xl flex items-center justify-center shrink-0"
                            style={{ background: n.bg, border: `1px solid ${n.color}30` }}>
                            <Zap size={13} style={{ color: n.color }} />
                          </div>
                          <div>
                            <p className="text-xs font-bold text-slate-100">{n.title}</p>
                            <p className="text-[11px] text-slate-400 mt-0.5">{n.desc}</p>
                            <p className="text-[10px] text-slate-600 mt-1">{n.time}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="p-3 text-center" style={{ borderTop: '1px solid rgba(255,255,255,0.05)' }}>
                      <button className="text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors">View all</button>
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Role pill */}
            <div className={`hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl border text-xs font-bold ${roleMeta.bgColor} ${roleMeta.borderColor} ${roleMeta.color}`}>
              <Shield size={11} />
              {roleMeta.label}
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div id="main-content" className="flex-1 overflow-auto">
          <div className="p-5 lg:p-7 min-h-full">
            {children}
          </div>
        </div>
      </main>

      {/* ─── FAB ─── */}
      <button
        onClick={() => setShowCopilot(true)}
        className={`fixed bottom-6 right-6 z-40 w-14 h-14 rounded-2xl flex items-center justify-center
                   transition-all duration-300 ${showCopilot ? 'scale-0 opacity-0 pointer-events-none' : 'scale-100 opacity-100'}`}
        style={{
          background: 'linear-gradient(135deg, #3b82f6 0%, #7c3aed 100%)',
          boxShadow: '0 8px 32px rgba(59,130,246,0.45), 0 0 0 1px rgba(255,255,255,0.1)',
        }}
        title="Open AI Copilot (Ctrl+K)"
        onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.transform = 'scale(1.08) translateY(-2px)'; }}
        onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.transform = 'scale(1)'; }}>
        <Sparkles className="text-white" size={22} />
      </button>

      {/* ─── Copilot Drawer ─── */}
      <div className={`fixed top-0 right-0 h-full max-w-full z-50 transition-transform duration-300 ease-in-out flex
                     ${showCopilot ? 'translate-x-0' : 'translate-x-full'}`}
        style={{ width: copilotWidth }}>
        <div onMouseDown={startDrag}
          className="w-1.5 h-full cursor-ew-resize absolute left-0 top-0 z-10 hover:bg-blue-500/40 transition-colors" />
        <div className="flex-1 h-full relative">
          <CopilotWidget onClose={() => setShowCopilot(false)} />
        </div>
      </div>
    </div>
  );
}
