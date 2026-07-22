import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import api from '@/lib/api';
import toast from 'react-hot-toast';
import { BrainCircuit, Eye, EyeOff, ArrowLeft, Shield, Cpu, Database, X } from 'lucide-react';
import { ROLE_META, isValidRole } from '@/lib/rbac';

/* ─── helpers ──────────────────────────────────────────── */
type Tab = 'signin' | 'signup';
type ForgotStep = 'email' | 'otp' | 'password';

function useField(initial = '') {
  const [value, setValue] = useState(initial);
  return { value, onChange: (e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value), setValue };
}

/* ─── small UI primitives ───────────────────────────────── */
function InputField({
  label, id, type = 'text', placeholder, field, required = true, children,
}: {
  label: string; id: string; type?: string; placeholder?: string;
  field: ReturnType<typeof useField>; required?: boolean; children?: React.ReactNode;
}) {
  const [show, setShow] = useState(false);
  const isPassword = type === 'password';
  return (
    <div className="space-y-1.5">
      <label htmlFor={id} className="block text-xs font-semibold text-slate-300 tracking-wide uppercase">{label}</label>
      <div className="relative group">
        <input
          id={id}
          type={isPassword ? (show ? 'text' : 'password') : type}
          placeholder={placeholder}
          value={field.value}
          onChange={field.onChange}
          required={required}
          className="w-full h-12 px-4 rounded-xl bg-slate-900/50 border border-slate-700/50 text-slate-100 placeholder-slate-500
                     focus:outline-none focus:ring-2 focus:ring-sky-500/50 focus:border-sky-500/50 focus:bg-slate-900/80
                     hover:border-slate-600 transition-all duration-300 shadow-inner"
        />
        {isPassword && (
          <button type="button" onClick={() => setShow(!show)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-sky-400 transition-colors bg-transparent p-1">
            {show ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        )}
      </div>
      {children}
    </div>
  );
}

function SubmitButton({ loading, children }: { loading: boolean; children: React.ReactNode }) {
  return (
    <button type="submit" disabled={loading}
      className="w-full h-12 rounded-xl bg-gradient-to-r from-sky-500 to-blue-600
                 hover:from-sky-400 hover:to-blue-500 disabled:opacity-60 disabled:cursor-not-allowed
                 text-white font-semibold text-base shadow-[0_0_20px_rgba(14,165,233,0.3)] hover:shadow-[0_0_25px_rgba(14,165,233,0.5)]
                 border border-sky-400/20
                 transition-all duration-300 active:scale-[.98]">
      {loading ? (
        <span className="flex items-center justify-center gap-2">
          <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
          </svg>
          Processing...
        </span>
      ) : children}
    </button>
  );
}

const GoogleIcon = () => (
  <svg viewBox="0 0 24 24" className="w-5 h-5" xmlns="http://www.w3.org/2000/svg">
    <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
    <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
    <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
    <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
  </svg>
);

/* ─── Forgot Password Modal ─────────────────────────────── */
function ForgotPasswordModal({ onClose }: { onClose: () => void }) {
  const [step, setStep] = useState<ForgotStep>('email');
  const [loading, setLoading] = useState(false);
  const emailField = useField();
  const otpField = useField();
  const newPassField = useField();
  const confirmPassField = useField();
  const [demoOtp, setDemoOtp] = useState<string | null>(null);

  const handleRequestOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post('/auth/forgot-password', { email: emailField.value });
      setDemoOtp(res.data.demo_otp);
      setStep('otp');
      toast.success('Reset code generated!');
    } catch {
      toast.error('Something went wrong. Try again.');
    } finally { setLoading(false); }
  };

  const handleVerifyOtp = (e: React.FormEvent) => {
    e.preventDefault();
    if (otpField.value.length !== 6) { toast.error('Enter the 6-digit code'); return; }
    setStep('password');
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassField.value !== confirmPassField.value) { toast.error('Passwords do not match'); return; }
    if (newPassField.value.length < 8) { toast.error('Password must be at least 8 characters'); return; }
    setLoading(true);
    try {
      await api.post('/auth/reset-password', {
        email: emailField.value,
        otp: otpField.value,
        new_password: newPassField.value,
      });
      toast.success('Password reset! Please sign in.');
      onClose();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Reset failed. Check your code.');
    } finally { setLoading(false); }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
      onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="w-full max-w-md bg-slate-900 border border-white/10 rounded-2xl shadow-2xl p-8 relative animate-fade-in">
        {/* Close */}
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors">
          <X size={20} />
        </button>

        {/* Header */}
        <div className="mb-6">
          {step !== 'email' && (
            <button onClick={() => setStep(step === 'password' ? 'otp' : 'email')}
              className="flex items-center gap-1.5 text-sm text-slate-400 hover:text-slate-200 mb-4 transition-colors">
              <ArrowLeft size={14} /> Back
            </button>
          )}
          <h2 className="text-xl font-bold text-white">
            {step === 'email' && 'Reset your password'}
            {step === 'otp' && 'Enter the reset code'}
            {step === 'password' && 'Set new password'}
          </h2>
          <p className="text-slate-400 text-sm mt-1">
            {step === 'email' && 'Enter your registered email address.'}
            {step === 'otp' && 'Enter the 6-digit code shown below.'}
            {step === 'password' && 'Choose a strong new password.'}
          </p>
        </div>

        {/* Step: Email */}
        {step === 'email' && (
          <form onSubmit={handleRequestOtp} className="space-y-4">
            <InputField label="Email Address" id="reset-email" type="email"
              placeholder="you@company.com" field={emailField} />
            <SubmitButton loading={loading}>Send Reset Code</SubmitButton>
          </form>
        )}

        {/* Step: OTP */}
        {step === 'otp' && (
          <form onSubmit={handleVerifyOtp} className="space-y-4">
            {/* Demo OTP display */}
            {demoOtp && (
              <div className="p-4 rounded-xl bg-sky-500/10 border border-sky-500/30 text-center">
                <p className="text-xs text-sky-300 mb-1 uppercase tracking-wider font-medium">Your Reset Code</p>
                <p className="text-3xl font-mono font-bold text-sky-400 tracking-widest">{demoOtp}</p>
                <p className="text-xs text-slate-400 mt-1">Valid for 15 minutes</p>
              </div>
            )}
            <InputField label="6-Digit Reset Code" id="reset-otp"
              placeholder="123456" field={otpField} />
            <SubmitButton loading={false}>Verify Code</SubmitButton>
          </form>
        )}

        {/* Step: New Password */}
        {step === 'password' && (
          <form onSubmit={handleResetPassword} className="space-y-4">
            <InputField label="New Password" id="reset-newpw" type="password"
              placeholder="Min. 8 characters" field={newPassField} />
            <InputField label="Confirm New Password" id="reset-confirmpw" type="password"
              placeholder="Repeat your password" field={confirmPassField} />
            <SubmitButton loading={loading}>Reset Password</SubmitButton>
          </form>
        )}
      </div>
    </div>
  );
}

/* ─── Main Auth Page ─────────────────────────────────────── */
export default function Auth() {
  const location = useLocation();
  const [tab, setTab] = useState<Tab>(location.pathname === '/signup' ? 'signup' : 'signin');
  const [loading, setLoading] = useState(false);
  const [showForgot, setShowForgot] = useState(false);
  const navigate = useNavigate();
  const setTokens = useAuthStore((s) => s.setTokens);
  const setUser = useAuthStore((s) => s.setUser);

  // Sign in fields
  const siEmail = useField();
  const siPassword = useField();

  // Sign up fields
  const suName = useField();
  const suEmail = useField();
  const suPassword = useField();
  const suConfirm = useField();
  const [suRole, setSuRole] = useState('engineer');

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post('/auth/login', { email: siEmail.value, password: siPassword.value });
      setTokens(res.data.access_token, res.data.refresh_token);
      const userRes = await api.get('/auth/me');
      setUser(userRes.data);
      const role = userRes.data.role;
      const roleMeta = isValidRole(role) ? ROLE_META[role] : null;
      const roleLabel = roleMeta ? roleMeta.label : role;
      toast.success(`Welcome back, ${userRes.data.full_name}! Logged in as ${roleLabel}.`);
      navigate('/');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Invalid credentials. Please try again.');
    } finally { setLoading(false); }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (suPassword.value !== suConfirm.value) { toast.error('Passwords do not match'); return; }
    setLoading(true);
    try {
      await api.post('/auth/register', {
        email: suEmail.value,
        password: suPassword.value,
        full_name: suName.value,
        role: suRole,
      });
      toast.success('Account created! Please sign in.');
      setTab('signin');
      siEmail.setValue(suEmail.value);
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Registration failed. Email may already be in use.');
    } finally { setLoading(false); }
  };

  const handleGoogleSignIn = async () => {
    setLoading(true);
    try {
      // Mock Google Auth: Register a dummy account if it doesn't exist, then log in.
      try {
        await api.post('/auth/register', {
          email: 'google.demo@opspilot.ai',
          password: 'google_mock_password',
          full_name: 'Google User',
          role: 'admin',
        });
      } catch (e: any) {
        // If it fails with 409, it already exists, which is fine.
        // Otherwise, it might be a real error (like network down), so throw it.
        if (e.response?.status !== 409 && e.response?.status !== 400) {
          throw e;
        }
      }
      
      const res = await api.post('/auth/login', { email: 'google.demo@opspilot.ai', password: 'google_mock_password' });
      setTokens(res.data.access_token, res.data.refresh_token);
      
      const userRes = await api.get('/auth/me');
      setUser(userRes.data);
      
      toast.success(`Signed in with Google! Welcome ${userRes.data.full_name}.`);
      navigate('/');
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Google Sign In failed.';
      toast.error(`Google Sign In failed: ${msg}`);
    } finally { setLoading(false); }
  };

  return (
    <>
      {showForgot && <ForgotPasswordModal onClose={() => setShowForgot(false)} />}

      <div className="min-h-screen flex relative overflow-hidden bg-[#030712]">
        {/* Animated Background Mesh */}
        <div className="absolute inset-0 z-0">
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/20 blur-[120px] animate-pulse-slow" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-violet-600/20 blur-[120px] animate-pulse-slow" style={{ animationDelay: '2s' }} />
          <div className="absolute top-[40%] left-[30%] w-[20%] h-[20%] rounded-full bg-sky-400/10 blur-[80px]" />
        </div>

        {/* ── Left Panel: Branding ── */}
        <div className="hidden lg:flex lg:w-1/2 flex-col justify-between p-16 relative z-10">
          <div className="relative">
            <div className="flex items-center gap-3 mb-16 animate-fade-in">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-violet-500 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/25">
                <BrainCircuit size={28} className="text-white" />
              </div>
              <span className="text-white font-bold text-2xl tracking-tight">OpsPilot AI</span>
            </div>
            
            <h1 className="text-5xl font-extrabold text-white leading-[1.15] mb-6 animate-slide-in-left">
              Enterprise Knowledge<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-sky-400 to-violet-400">
                Intelligence Platform
              </span>
            </h1>
            <p className="text-slate-400 text-lg leading-relaxed max-w-md animate-slide-in-left stagger-1">
              AI-powered knowledge management: real-time insights, predictive intelligence,
              and automated root-cause analysis for any industry.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-5 animate-slide-in-left stagger-2">
            {[
              { icon: <Cpu size={20} />, title: 'Hybrid RAG Engine', desc: 'Vector + Knowledge Graph search' },
              { icon: <Shield size={20} />, title: 'Compliance Intelligence', desc: 'Automated regulatory tracking' },
              { icon: <Database size={20} />, title: 'Resource Intelligence', desc: 'Predictive insights for any domain' },
            ].map((f) => (
              <div key={f.title} className="flex items-start gap-4 p-5 rounded-2xl bg-white/[0.02] border border-white/[0.05] backdrop-blur-md hover:bg-white/[0.04] transition-colors group">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500/20 to-violet-500/20 border border-blue-500/30 rounded-xl flex items-center justify-center text-blue-400 shrink-0 group-hover:scale-110 transition-transform">
                  {f.icon}
                </div>
                <div>
                  <p className="text-slate-200 font-semibold text-sm">{f.title}</p>
                  <p className="text-slate-500 text-xs mt-1 leading-snug">{f.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* ── Right Panel: Auth Form ── */}
        <div className="flex-1 flex items-center justify-center p-6 lg:p-12 relative z-10">
          <div className="w-full max-w-md">
            
            {/* Mobile logo */}
            <div className="flex lg:hidden items-center gap-3 justify-center mb-10">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-violet-500 rounded-2xl flex items-center justify-center shadow-lg">
                <BrainCircuit size={28} className="text-white" />
              </div>
              <span className="text-white font-bold text-2xl tracking-tight">OpsPilot AI</span>
            </div>

            {/* Form Card */}
            <div className="bg-white/[0.02] backdrop-blur-2xl border border-white/[0.08] rounded-3xl p-8 shadow-2xl">
              
              {/* Tab switcher */}
              <div className="flex bg-black/40 border border-white/5 rounded-xl p-1 mb-8">
                {(['signin', 'signup'] as Tab[]).map((t) => (
                  <button key={t} onClick={() => setTab(t)}
                    className={`flex-1 py-2.5 rounded-lg text-sm font-semibold transition-all duration-300
                      ${tab === t
                        ? 'bg-gradient-to-r from-blue-600 to-violet-600 text-white shadow-lg'
                        : 'text-slate-400 hover:text-slate-200'
                      }`}>
                    {t === 'signin' ? 'Sign In' : 'Sign Up'}
                  </button>
                ))}
              </div>

              {/* ── Sign In Form ── */}
              {tab === 'signin' && (
                <form onSubmit={handleSignIn} className="space-y-5 animate-fade-in">
                  <button
                    type="button"
                    onClick={handleGoogleSignIn}
                    disabled={loading}
                    className="w-full h-12 rounded-xl bg-white flex items-center justify-center gap-3 text-sm font-bold text-slate-900 hover:bg-slate-100 hover:scale-[1.02] transition-all duration-300 shadow-lg shadow-white/5"
                  >
                    <GoogleIcon />
                    Sign in with Google
                  </button>

                  <div className="flex items-center gap-4 my-6 opacity-70">
                    <div className="h-px bg-gradient-to-r from-transparent via-white/20 to-white/20 flex-1" />
                    <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-widest">Or continue with email</span>
                    <div className="h-px bg-gradient-to-l from-transparent via-white/20 to-white/20 flex-1" />
                  </div>

                  <InputField label="Email Address" id="si-email" type="email"
                    placeholder="you@company.com" field={siEmail} />
                  <InputField label="Password" id="si-password" type="password"
                    placeholder="Your password" field={siPassword}>
                    <button type="button" onClick={() => setShowForgot(true)}
                      className="absolute right-0 -top-7 text-xs text-blue-400 hover:text-blue-300 transition-colors font-medium">
                      Forgot password?
                    </button>
                  </InputField>
                  
                  <div className="pt-2">
                    <SubmitButton loading={loading}>Sign In</SubmitButton>
                  </div>
                  
                  <p className="text-center text-sm text-slate-400 mt-4">
                    New to OpsPilot?{' '}
                    <button type="button" onClick={() => setTab('signup')}
                      className="text-blue-400 hover:text-blue-300 font-semibold transition-colors">
                      Create an account
                    </button>
                  </p>
                </form>
              )}

              {/* ── Sign Up Form ── */}
              {tab === 'signup' && (
                <form onSubmit={handleSignUp} className="space-y-4 animate-fade-in">
                  <button
                    type="button"
                    onClick={handleGoogleSignIn}
                    disabled={loading}
                    className="w-full h-12 rounded-xl bg-white flex items-center justify-center gap-3 text-sm font-bold text-slate-900 hover:bg-slate-100 hover:scale-[1.02] transition-all duration-300 shadow-lg shadow-white/5"
                  >
                    <GoogleIcon />
                    Sign up with Google
                  </button>

                  <div className="flex items-center gap-4 my-6 opacity-70">
                    <div className="h-px bg-gradient-to-r from-transparent via-white/20 to-white/20 flex-1" />
                    <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-widest">Or continue with email</span>
                    <div className="h-px bg-gradient-to-l from-transparent via-white/20 to-white/20 flex-1" />
                  </div>

                  <InputField label="Full Name" id="su-name" placeholder="Jane Smith" field={suName} />
                  <InputField label="Email Address" id="su-email" type="email"
                    placeholder="jane@company.com" field={suEmail} />

                  {/* Role selector */}
                  <div className="space-y-1.5">
                    <label className="block text-xs font-semibold text-slate-300 tracking-wide uppercase">Role</label>
                    <div className="grid grid-cols-2 gap-2">
                      {(['engineer', 'operator', 'viewer', 'admin'] as const).map((r) => (
                        <button key={r} type="button" onClick={() => setSuRole(r)}
                          className={`py-2.5 px-3 rounded-xl text-xs font-bold capitalize border transition-all duration-200
                            ${suRole === r
                              ? 'bg-blue-500/20 border-blue-500/50 text-blue-300 shadow-[0_0_15px_rgba(59,130,246,0.15)]'
                              : 'bg-black/20 border-white/10 text-slate-400 hover:text-slate-200 hover:bg-white/5'
                            }`}>
                          {r}
                        </button>
                      ))}
                    </div>
                  </div>

                  <InputField label="Password" id="su-password" type="password"
                    placeholder="Min. 8 characters" field={suPassword} />
                  <InputField label="Confirm Password" id="su-confirm" type="password"
                    placeholder="Repeat your password" field={suConfirm} />
                  
                  <div className="pt-2">
                    <SubmitButton loading={loading}>Sign Up</SubmitButton>
                  </div>
                  
                  <p className="text-center text-sm text-slate-400 mt-4">
                    Already have an account?{' '}
                    <button type="button" onClick={() => setTab('signin')}
                      className="text-blue-400 hover:text-blue-300 font-semibold transition-colors">
                      Sign in
                    </button>
                  </p>
                </form>
              )}
            </div>

            <p className="text-center text-xs text-slate-600 mt-8 font-medium">
              OpsPilot AI — Enterprise Knowledge Intelligence Platform
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
