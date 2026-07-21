import { createContext, useContext, useState } from 'react';
import { cn } from '@/lib/utils';

const TabsContext = createContext<{ value: string; onValueChange: (v: string) => void }>({
  value: '',
  onValueChange: () => {},
});

export function Tabs({ defaultValue, value, onValueChange, className, children }: any) {
  const [internalValue, setInternalValue] = useState(value || defaultValue);

  const handleValueChange = (v: string) => {
    setInternalValue(v);
    if (onValueChange) onValueChange(v);
  };

  return (
    <TabsContext.Provider
      value={{ value: value !== undefined ? value : internalValue, onValueChange: handleValueChange }}
    >
      <div className={className}>{children}</div>
    </TabsContext.Provider>
  );
}

export function TabsList({ className, children }: any) {
  return (
    <div className={cn('flex flex-wrap gap-1', className)}>
      {children}
    </div>
  );
}

export function TabsTrigger({ value, className, children }: any) {
  const context = useContext(TabsContext);
  const isActive = context.value === value;

  return (
    <button
      className={cn(
        'inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium transition-all duration-200',
        isActive
          ? 'bg-blue-500/20 text-blue-300 border border-blue-500/25'
          : 'text-slate-400 hover:text-slate-200 hover:bg-white/5',
        className
      )}
      onClick={() => context.onValueChange(value)}
      data-state={isActive ? 'active' : 'inactive'}
    >
      {children}
    </button>
  );
}

export function TabsContent({ value, className, children }: any) {
  const context = useContext(TabsContext);
  if (context.value !== value) return null;
  return <div className={cn('animate-fade-in', className)}>{children}</div>;
}
