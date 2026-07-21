/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
        violet: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        sidebar: {
          bg: '#080e1f',
          border: 'rgba(99,155,255,0.1)',
        },
        surface: {
          1: 'rgba(255,255,255,0.03)',
          2: 'rgba(255,255,255,0.05)',
          3: 'rgba(255,255,255,0.08)',
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
        xl: '1rem',
        '2xl': '1.25rem',
        '3xl': '1.5rem',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
      fontSize: {
        '2xs': ['0.65rem', { lineHeight: '1rem' }],
      },
      boxShadow: {
        'glow-sm': '0 0 10px rgba(99,155,255,0.15)',
        'glow': '0 0 20px rgba(99,155,255,0.2), 0 0 40px rgba(99,155,255,0.1)',
        'glow-lg': '0 0 40px rgba(99,155,255,0.25), 0 0 80px rgba(99,155,255,0.15)',
        'glow-violet': '0 0 20px rgba(167,139,250,0.2), 0 0 40px rgba(167,139,250,0.1)',
        'card': '0 4px 24px rgba(0,0,0,0.4)',
        'card-hover': '0 8px 40px rgba(0,0,0,0.5)',
        'modal': '0 24px 80px rgba(0,0,0,0.6)',
        'inner-light': 'inset 0 1px 0 rgba(255,255,255,0.07)',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-primary': 'linear-gradient(135deg, #3b82f6 0%, #6366f1 100%)',
        'gradient-success': 'linear-gradient(135deg, #34d399 0%, #059669 100%)',
        'gradient-danger': 'linear-gradient(135deg, #f87171 0%, #dc2626 100%)',
        'gradient-warning': 'linear-gradient(135deg, #fbbf24 0%, #d97706 100%)',
        'gradient-violet': 'linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%)',
        'gradient-surface': 'linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)',
        'mesh': `
          radial-gradient(ellipse at 20% 50%, rgba(99,155,255,0.08) 0%, transparent 50%),
          radial-gradient(ellipse at 80% 20%, rgba(167,139,250,0.08) 0%, transparent 50%),
          radial-gradient(ellipse at 50% 80%, rgba(52,211,153,0.05) 0%, transparent 50%)
        `,
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease-out both',
        'slide-up': 'slideUp 0.4s ease-out both',
        'slide-in-left': 'slideInLeft 0.35s ease-out both',
        'scale-in': 'scaleIn 0.3s ease-out both',
        'glow-pulse': 'glowPulse 2s ease-in-out infinite',
        'shimmer': 'shimmer 1.5s infinite',
        'bounce-soft': 'bounceSoft 0.6s ease-out',
        'in': 'fadeIn 0.3s ease-out both',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInLeft: {
          '0%': { opacity: '0', transform: 'translateX(-16px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 10px rgba(99,155,255,0.2)' },
          '50%': { boxShadow: '0 0 25px rgba(99,155,255,0.4), 0 0 50px rgba(99,155,255,0.2)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        bounceSoft: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-4px)' },
        },
      },
      transitionDuration: {
        '250': '250ms',
        '400': '400ms',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
