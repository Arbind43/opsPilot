import { useNavigate } from 'react-router-dom';
import { ShieldX, ArrowLeft } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { ROLE_META, isValidRole } from '@/lib/rbac';

export default function Unauthorized() {
  const navigate = useNavigate();
  const user = useAuthStore(s => s.user);
  const role = user?.role ?? 'viewer';
  const meta = isValidRole(role) ? ROLE_META[role] : ROLE_META.viewer;

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6">
      <div className="w-full max-w-md text-center animate-fade-in">
        {/* Icon */}
        <div className="mx-auto w-20 h-20 rounded-2xl bg-red-500/10 border border-red-500/20 flex items-center justify-center mb-6">
          <ShieldX size={36} className="text-red-400" />
        </div>

        {/* Heading */}
        <h1 className="text-4xl font-bold text-white mb-2">403</h1>
        <h2 className="text-xl font-semibold text-slate-200 mb-3">Access Denied</h2>
        <p className="text-slate-400 text-sm leading-relaxed mb-2">
          Your current role{' '}
          <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border ${meta.bgColor} ${meta.color} ${meta.borderColor}`}>
            {meta.label}
          </span>{' '}
          does not have permission to view this page.
        </p>
        <p className="text-slate-500 text-xs mb-8">
          Contact your administrator if you believe this is an error.
        </p>

        {/* Actions */}
        <div className="flex gap-3 justify-center">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/5 border border-white/10
                       text-slate-300 hover:text-white hover:bg-white/10 transition-all text-sm font-medium"
          >
            <ArrowLeft size={15} />
            Go Back
          </button>
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl
                       bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500
                       text-white text-sm font-semibold shadow-lg shadow-sky-500/25 transition-all"
          >
            Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
