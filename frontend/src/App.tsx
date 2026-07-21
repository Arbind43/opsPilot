import './App.css';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';
import { canAccess, isValidRole } from '@/lib/rbac';
import Auth from '@/pages/Auth';
import Layout from '@/components/layout/Layout';
import Unauthorized from '@/pages/Unauthorized';

import Dashboard  from '@/pages/Dashboard';
import Assets     from '@/pages/Assets';
import Documents  from '@/pages/Documents';
import Incidents  from '@/pages/Incidents';
import Maintenance from '@/pages/Maintenance';
import Compliance from '@/pages/Compliance';
import Reports    from '@/pages/Reports';
import Settings   from '@/pages/Settings';
import KnowledgeGraph from '@/pages/KnowledgeGraph';

// ─── Protected Route — requires authentication ────────────────────────────
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <Layout>{children}</Layout>;
};

// ─── Role Guard — requires auth + specific role permission ────────────────
function RoleGuard({ path, children }: { path: string; children: React.ReactNode }) {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated);
  const user            = useAuthStore(state => state.user);

  if (!isAuthenticated) return <Navigate to="/login" replace />;

  const role = user?.role ?? 'viewer';
  const hasAccess = isValidRole(role) ? canAccess(role, path) : false;

  if (!hasAccess) return <Navigate to="/unauthorized" replace />;

  return <Layout>{children}</Layout>;
}

function App() {
  return (
    <>
      <Router>
        <Routes>
          {/* Auth routes */}
          <Route path="/login"  element={<Auth />} />
          <Route path="/signup" element={<Auth />} />

          {/* 403 page — accessible regardless of auth state */}
          <Route path="/unauthorized" element={<Unauthorized />} />

          {/* Protected routes with role-based access control */}
          <Route path="/"           element={<RoleGuard path="/"><Dashboard /></RoleGuard>} />
          <Route path="/documents"  element={<RoleGuard path="/documents"><Documents /></RoleGuard>} />
          <Route path="/assets"     element={<RoleGuard path="/assets"><Assets /></RoleGuard>} />
          <Route path="/graph"      element={<RoleGuard path="/graph"><KnowledgeGraph /></RoleGuard>} />
          <Route path="/incidents"  element={<RoleGuard path="/incidents"><Incidents /></RoleGuard>} />
          <Route path="/maintenance" element={<RoleGuard path="/maintenance"><Maintenance /></RoleGuard>} />
          <Route path="/compliance" element={<RoleGuard path="/compliance"><Compliance /></RoleGuard>} />
          <Route path="/reports"    element={<RoleGuard path="/reports"><Reports /></RoleGuard>} />
          <Route path="/settings"   element={<RoleGuard path="/settings"><Settings /></RoleGuard>} />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
      <Toaster
        position="top-right"
        gutter={8}
        toastOptions={{
          duration: 4000,
          style: {
            background: 'rgba(12, 18, 40, 0.95)',
            color: '#e2e8f0',
            border: '1px solid rgba(99, 155, 255, 0.15)',
            borderRadius: '14px',
            fontSize: '13px',
            fontFamily: 'Inter, sans-serif',
            backdropFilter: 'blur(16px)',
            boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
            padding: '12px 16px',
          },
          success: {
            iconTheme: { primary: '#34d399', secondary: 'rgba(52,211,153,0.15)' },
            style: { borderColor: 'rgba(52, 211, 153, 0.2)' },
          },
          error: {
            iconTheme: { primary: '#f87171', secondary: 'rgba(248,113,113,0.15)' },
            style: { borderColor: 'rgba(248, 113, 113, 0.2)' },
          },
        }}
      />
    </>
  );
}

export default App;
