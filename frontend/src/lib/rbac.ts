/**
 * OpsPilot — Role-Based Access Control (RBAC) Configuration
 * ==========================================================
 * Defines roles, their permissions, accessible routes,
 * and navigation items. Single source of truth for all RBAC.
 */

export type UserRole = 'admin' | 'engineer' | 'operator' | 'viewer';

// ─── Route Permissions ──────────────────────────────────────────────────────

/** Map of route path → roles allowed to access it */
export const ROUTE_PERMISSIONS: Record<string, UserRole[]> = {
  '/':            ['admin', 'engineer', 'operator', 'viewer'],
  '/documents':   ['admin', 'engineer', 'operator', 'viewer'],
  '/assets':      ['admin', 'engineer', 'operator', 'viewer'],
  '/graph':       ['admin', 'engineer'],
  '/incidents':   ['admin', 'engineer', 'operator'],
  '/maintenance': ['admin', 'engineer', 'operator'],
  '/compliance':  ['admin', 'engineer'],
  '/reports':     ['admin', 'engineer', 'operator', 'viewer'],
  '/settings':    ['admin'],
};

// ─── Nav Item Permissions ───────────────────────────────────────────────────

export interface NavItemConfig {
  icon: string;           // lucide icon name
  label: string;
  path: string;
  color: string;
  badge?: string;
  roles: UserRole[];      // which roles can see this item
}

export const NAV_ITEMS_CONFIG: NavItemConfig[] = [
  { icon: 'LayoutDashboard', label: 'Dashboard',      path: '/',           color: 'text-blue-400',   roles: ['admin','engineer','operator','viewer'] },
  { icon: 'Files',           label: 'Documents',      path: '/documents',  color: 'text-emerald-400', roles: ['admin','engineer','operator','viewer'] },
  { icon: 'Box',             label: 'Resources',      path: '/assets',     color: 'text-amber-400',  roles: ['admin','engineer','operator','viewer'] },
  { icon: 'Network',         label: 'Knowledge Graph', path: '/graph',     color: 'text-cyan-400',   roles: ['admin','engineer'] },
  { icon: 'AlertTriangle',   label: 'Incidents',      path: '/incidents',  color: 'text-red-400',    roles: ['admin','engineer','operator'] },
  { icon: 'Wrench',          label: 'Maintenance',    path: '/maintenance', color: 'text-orange-400', roles: ['admin','engineer','operator'] },
  { icon: 'CheckSquare',     label: 'Compliance',     path: '/compliance', color: 'text-indigo-400', roles: ['admin','engineer'] },
  { icon: 'PieChart',        label: 'Reports',        path: '/reports',    color: 'text-pink-400',   roles: ['admin','engineer','operator','viewer'] },
  { icon: 'Settings',        label: 'Settings',       path: '/settings',   color: 'text-slate-400',  roles: ['admin'] },
];

// ─── Role Metadata ──────────────────────────────────────────────────────────

export interface RoleMeta {
  label: string;
  description: string;
  color: string;           // tailwind text color class
  bgColor: string;         // tailwind bg class
  borderColor: string;     // tailwind border class
  badgeGradient: string;   // CSS gradient for the role badge
  icon: string;            // lucide icon name
  dashboardTitle: string;
  dashboardSubtitle: string;
}

export const ROLE_META: Record<UserRole, RoleMeta> = {
  admin: {
    label: 'Administrator',
    description: 'Full platform access — users, settings, all modules',
    color: 'text-rose-400',
    bgColor: 'bg-rose-500/10',
    borderColor: 'border-rose-500/25',
    badgeGradient: 'linear-gradient(135deg, #f43f5e 0%, #e11d48 100%)',
    icon: 'ShieldCheck',
    dashboardTitle: 'Admin Control Center',
    dashboardSubtitle: 'Full platform visibility — users, health, and all operations',
  },
  engineer: {
    label: 'Engineer',
    description: 'Technical access — assets, incidents, compliance, AI tools',
    color: 'text-blue-400',
    bgColor: 'bg-blue-500/10',
    borderColor: 'border-blue-500/25',
    badgeGradient: 'linear-gradient(135deg, #3b82f6 0%, #6366f1 100%)',
    icon: 'Cpu',
    dashboardTitle: 'Engineering Dashboard',
    dashboardSubtitle: 'Technical health, incidents, and compliance status at a glance',
  },
  operator: {
    label: 'Operator',
    description: 'Operational access — resources, maintenance, incidents',
    color: 'text-amber-400',
    bgColor: 'bg-amber-500/10',
    borderColor: 'border-amber-500/25',
    badgeGradient: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
    icon: 'Wrench',
    dashboardTitle: 'Operations Dashboard',
    dashboardSubtitle: 'Resource status, maintenance tasks, and incident queue',
  },
  viewer: {
    label: 'Viewer',
    description: 'Read-only access — reports and documents',
    color: 'text-emerald-400',
    bgColor: 'bg-emerald-500/10',
    borderColor: 'border-emerald-500/25',
    badgeGradient: 'linear-gradient(135deg, #10b981 0%, #14b8a6 100%)',
    icon: 'Eye',
    dashboardTitle: 'Reports Overview',
    dashboardSubtitle: 'Read-only view of platform performance and reports',
  },
};

// ─── Permission Helpers ─────────────────────────────────────────────────────

export function canAccess(role: UserRole | string, path: string): boolean {
  const allowed = ROUTE_PERMISSIONS[path];
  if (!allowed) return false;
  return allowed.includes(role as UserRole);
}

export function getNavItemsForRole(role: UserRole | string): NavItemConfig[] {
  return NAV_ITEMS_CONFIG.filter(item =>
    item.roles.includes(role as UserRole)
  );
}

export function isValidRole(role: string): role is UserRole {
  return ['admin', 'engineer', 'operator', 'viewer'].includes(role);
}
