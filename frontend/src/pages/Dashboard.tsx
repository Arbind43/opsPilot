/**
 * Dashboard — Role-dispatching gateway
 * =====================================
 * Reads the authenticated user's role and renders the
 * appropriate role-specific dashboard component.
 */
import { useAuthStore } from '@/store/authStore';
import { isValidRole } from '@/lib/rbac';

import AdminDashboard    from '@/pages/dashboards/AdminDashboard';
import EngineerDashboard from '@/pages/dashboards/EngineerDashboard';
import OperatorDashboard from '@/pages/dashboards/OperatorDashboard';
import ViewerDashboard   from '@/pages/dashboards/ViewerDashboard';

export default function Dashboard() {
  const user = useAuthStore(s => s.user);
  const role = user?.role ?? 'viewer';

  if (!isValidRole(role)) return <ViewerDashboard />;

  switch (role) {
    case 'admin':    return <AdminDashboard />;
    case 'engineer': return <EngineerDashboard />;
    case 'operator': return <OperatorDashboard />;
    case 'viewer':   return <ViewerDashboard />;
    default:         return <ViewerDashboard />;
  }
}
