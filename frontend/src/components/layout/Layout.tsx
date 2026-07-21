import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import {
  getNavItemsForRole, ROLE_META, isValidRole, type UserRole,
} from '@/lib/rbac';
import {
  LayoutDashboard,
  Files,
  AlertTriangle,
  Wrench,
  CheckSquare,
  PieChart,
  Settings,
  LogOut,
  BrainCircuit,
  Box,
  Network,
  Search,
  Bell,
  ChevronRight,
  Menu,
  X,
  Sparkles,
  Shield,
  ShieldCheck,
  Cpu,
  Eye,
  Bot
} from 'lucide-react';
import CopilotWidget from '@/components/ui/CopilotWidget';

// Map icon name → component
const ICON_MAP: Record<string, React.ComponentType<any>> = {
  LayoutDashboard,
  Files,
  AlertTriangle,
  Wrench,
  CheckSquare,
  PieChart,
  Settings,
  BrainCircuit,
  Box,
  Network,
  ShieldCheck,
  Cpu,
  Eye,
};

const PAGE_TITLES: Record<string, { title: string; subtitle: string }> = {
  '/':           { title: 'Dashboard',              subtitle: 'Real-time pulse of your operations' },
  '/documents':  { title: 'Knowledge Base',         subtitle: 'Upload and manage your document corpus' },
  '/assets':     { title: 'Resource Management',    subtitle: 'Hierarchical view of all operational entities' },
  '/graph':      { title: 'Knowledge Graph',        subtitle: 'Explore relational intelligence across your data' },
  '/incidents':  { title: 'Incident Management',    subtitle: 'Track anomalies and AI-driven root cause analysis' },
  '/maintenance':{ title: 'Maintenance Intelligence', subtitle: 'Predictive, preventive, and corrective task records' },
  '/compliance': { title: 'Compliance Checking',    subtitle: 'Automated AI evaluation against regulatory standards' },
  '/reports':    { title: 'Reporting Engine',        subtitle: 'Generate and export AI-driven operational insights' },
  '/settings':   { title: 'System Settings',         subtitle: 'Configure platform and view security audits' },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  const user    = useAuthStore(state => state.user);
  const logout  = useAuthStore(state => state.logout);
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen]   = useState(false);
  const [searchFocused, setSearchFocused] = useState(false);
  const [scrolled, setScrolled]         = useState(false);
  const [showCopilot, setShowCopilot]   = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  const currentPage = PAGE_TITLES[location.pathname] || { title: 'OpsPilot AI', subtitle: '' };

  // Role-based nav items
  const role      = (user?.role ?? 'viewer') as UserRole;
  const roleMeta  = isValidRole(role) ? ROLE_META[role] : ROLE_META.viewer;
  const navItems  = getNavItemsForRole(role);

  // Split into main nav (everything except /settings) and system nav (/settings)
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

  useEffect(() => { setSidebarOpen(false); }, [location.pathname]);

  const initials = user?.full_name?.split(' ').map((n: string) => n[0]).join('').toUpperCase().slice(0, 2) || 'U';

  return (
    <div className="flex h-screen bg-background overflow-hidden mesh-bg">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)} />
      )}

      {/* ── Sidebar ── */}
      <aside className={`
        fixed lg:static inset-y-0 left-0 z-30
        flex flex-col w-[240px] shrink-0
        transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}
        style={{
          background: 'linear-gradient(180deg, #060c1e 0%, #080e22 50%, #060c1e 100%)',
          borderRight: '1px solid rgba(99,155,255,0.1)',
        }}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-5 py-5 border-b border-white/[0.06]">
          <div className="relative">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center shadow-glow-sm">
              <BrainCircuit size={18} className="text-white" />
            </div>
            <div className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-[#060c1e]" />
          </div>
          <div>
            <span className="text-white font-bold text-sm tracking-tight">OpsPilot AI</span>
            <p className="text-[10px] text-slate-500 font-medium tracking-wider uppercase">Enterprise Platform</p>
          </div>
          <button
            className="ml-auto lg:hidden text-slate-500 hover:text-slate-300 transition-colors"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={16} />
          </button>
        </div>

        {/* Role Badge */}
        <div className="mx-3 mt-3">
          <div className={`flex items-center gap-2 px-3 py-2 rounded-xl border ${roleMeta.bgColor} ${roleMeta.borderColor}`}>
            <div className="w-2 h-2 rounded-full shrink-0" style={{ background: roleMeta.badgeGradient }} />
            <span className={`text-xs font-semibold ${roleMeta.color}`}>{roleMeta.label}</span>
            <span className="ml-auto text-[10px] text-slate-600 font-medium">Access Level</span>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto no-scrollbar py-4 px-3 space-y-0.5">
          <p className="text-[10px] font-semibold text-slate-600 uppercase tracking-widest px-3 pb-2 pt-1">
            Navigation
          </p>
          {mainNav.map((item, i) => {
            const Icon = ICON_MAP[item.icon] ?? LayoutDashboard;
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
                    <Icon
                      size={16}
                      className={`shrink-0 transition-colors ${isActive ? 'text-blue-400' : item.color + ' opacity-60 group-hover:opacity-100'}`}
                    />
                    <span className="flex-1 text-sm">{item.label}</span>
                    {item.badge && (
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-md bg-violet-500/20 text-violet-400 border border-violet-500/30 tracking-wider">
                        {item.badge}
                      </span>
                    )}
                    {isActive && <ChevronRight size={12} className="text-blue-400 opacity-60" />}
                  </>
                )}
              </NavLink>
            );
          })}

          {/* System section — only if the role has access to settings */}
          {systemNav.length > 0 && (
            <>
              <div className="pt-4 pb-2">
                <div className="h-px bg-white/[0.05]" />
              </div>
              <p className="text-[10px] font-semibold text-slate-600 uppercase tracking-widest px-3 pb-2 pt-1">
                System
              </p>
              {systemNav.map((item) => {
                const Icon = ICON_MAP[item.icon] ?? Settings;
                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive }) => `nav-item group ${isActive ? 'active' : ''}`}
                  >
                    {({ isActive }) => (
                      <>
                        <Icon size={16} className={`shrink-0 ${isActive ? 'text-blue-400' : 'text-slate-500 group-hover:text-slate-300'}`} />
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

        {/* AI Status pill */}
        <div className="mx-3 mb-3">
          <div className="flex items-center gap-2 px-3 py-2.5 rounded-xl bg-emerald-500/8 border border-emerald-500/15">
            <Sparkles size={12} className="text-emerald-400" />
            <span className="text-xs text-emerald-400 font-medium">AI Engine Online</span>
            <div className="ml-auto flex gap-0.5">
              {[1,2,3].map(i => (
                <div key={i} className="w-1 bg-emerald-400 rounded-full animate-bounce-soft" style={{ height: `${6 + i * 2}px`, animationDelay: `${i * 0.1}s` }} />
              ))}
            </div>
          </div>
        </div>

        {/* User card */}
        <div className="p-3 border-t border-white/[0.06]">
          <div className="flex items-center gap-3 p-2.5 rounded-xl hover:bg-white/5 transition-colors cursor-pointer group">
            <div className="relative shrink-0">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center text-xs font-bold text-white shadow-glow-sm">
                {initials}
              </div>
              <div className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-[#060c1e]" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-slate-200 truncate">{user?.full_name}</p>
              <p className={`text-[10px] capitalize truncate font-medium ${roleMeta.color}`}>{roleMeta.label}</p>
            </div>
            <button
              onClick={handleLogout}
              className="opacity-0 group-hover:opacity-100 transition-opacity text-slate-500 hover:text-red-400 p-1 rounded-lg hover:bg-red-500/10"
              title="Sign out"
            >
              <LogOut size={13} />
            </button>
          </div>
        </div>
      </aside>

      {/* ── Main Area ── */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Header */}
        <header className={`
          h-14 flex items-center justify-between px-5 lg:px-7 shrink-0
          transition-all duration-200 relative z-40
          ${scrolled
            ? 'bg-[rgba(6,12,30,0.9)] backdrop-blur-md border-b border-white/[0.06] shadow-[0_1px_20px_rgba(0,0,0,0.3)]'
            : 'bg-[rgba(6,12,30,0.4)] backdrop-blur-sm border-b border-white/[0.04]'}
        `}>
          {/* Left */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-white/8 transition-colors"
            >
              <Menu size={18} />
            </button>
            <div>
              <h2 className="text-sm font-semibold text-slate-100 leading-none">{currentPage.title}</h2>
              <p className="text-[11px] text-slate-500 mt-0.5 hidden sm:block">{currentPage.subtitle}</p>
            </div>
          </div>

          {/* Right */}
          <div className="flex items-center gap-2">
            {/* Search */}
            <div className={`relative transition-all duration-300 ${searchFocused ? 'w-64' : 'w-44'} hidden sm:block`}>
              <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="text"
                placeholder="Ask Copilot..."
                onFocus={() => setSearchFocused(true)}
                onBlur={() => setSearchFocused(false)}
                className="w-full h-8 pl-8 pr-3 text-xs bg-white/5 border border-white/8 rounded-lg text-slate-300 placeholder-slate-600
                           focus:outline-none focus:ring-1 focus:ring-blue-500/50 focus:border-blue-500/40 focus:bg-white/8 transition-all"
              />
            </div>

            {/* Notifications */}
            <div className="relative">
              <button 
                onClick={() => setShowNotifications(!showNotifications)}
                className="relative p-2 rounded-lg text-slate-500 hover:text-slate-200 hover:bg-white/8 transition-all duration-200"
              >
                <Bell size={16} />
                <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-blue-400 rounded-full" />
              </button>
              
              {showNotifications && (
                <>
                  <div className="fixed inset-0 z-40" onClick={() => setShowNotifications(false)} />
                  <div className="absolute right-0 mt-2 w-80 bg-[#060c1e] border border-white/20 rounded-xl shadow-[0_8px_30px_rgb(0,0,0,1)] z-50 overflow-hidden animate-fade-in">
                    <div className="p-3 border-b border-white/10 bg-[#0a1128] flex items-center justify-between">
                      <span className="text-sm font-semibold text-white">Notifications</span>
                      <button className="text-xs text-blue-400 hover:text-blue-300 font-medium">Mark all as read</button>
                    </div>
                    <div className="max-h-[300px] overflow-y-auto no-scrollbar bg-[#060c1e]">
                      {[
                        { title: 'New Incident Logged', desc: 'Pump Vibration High detected.', time: 'Just now', icon: <AlertTriangle size={14} className="text-orange-400" /> },
                        { title: 'RCA Completed', desc: 'AI has finished analyzing Incident #402.', time: '10m ago', icon: <Sparkles size={14} className="text-violet-400" /> },
                        { title: 'System Update', desc: 'OpsPilot agent updated to latest version.', time: '1h ago', icon: <Cpu size={14} className="text-blue-400" /> },
                      ].map((notif, i) => (
                        <div key={i} className="flex gap-3 p-3 border-b border-white/5 hover:bg-white/10 cursor-pointer transition-colors bg-[#060c1e]">
                          <div className="mt-0.5 shrink-0 p-1.5 rounded-lg bg-[#0a1128] border border-white/10">{notif.icon}</div>
                          <div>
                            <p className="text-xs font-semibold text-slate-100">{notif.title}</p>
                            <p className="text-[11px] text-slate-400 mt-0.5 leading-snug">{notif.desc}</p>
                            <p className="text-[10px] text-slate-500 mt-1">{notif.time}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="p-2 bg-[#0a1128] border-t border-white/10 text-center">
                      <button className="text-xs text-slate-300 hover:text-slate-200 font-medium">View all notifications</button>
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Role indicator pill */}
            <div className={`hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-lg border text-xs font-medium ${roleMeta.bgColor} ${roleMeta.borderColor} ${roleMeta.color}`}>
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

      {/* ── Copilot Floating Action Button ── */}
      <button
        onClick={() => setShowCopilot(true)}
        className={`fixed bottom-6 right-6 z-40 w-14 h-14 rounded-full bg-gradient-to-br from-blue-500 to-violet-500 
                   flex items-center justify-center shadow-lg shadow-blue-500/20 hover:scale-105 hover:shadow-blue-500/40 
                   transition-all duration-300 border border-white/10 ${showCopilot ? 'scale-0 opacity-0 pointer-events-none' : 'scale-100 opacity-100'}`}
        title="Open AI Copilot"
      >
        <Sparkles className="text-white" size={24} />
      </button>

      {/* ── Copilot Sliding Drawer ── */}
      <div 
        className={`fixed top-0 right-0 h-full w-[400px] max-w-full z-50 transition-transform duration-300 ease-in-out transform
                   ${showCopilot ? 'translate-x-0' : 'translate-x-full'}`}
      >
        <CopilotWidget onClose={() => setShowCopilot(false)} />
      </div>

    </div>
  );
}
