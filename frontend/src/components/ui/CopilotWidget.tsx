import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import {
  Send, Bot, User, Loader2, Sparkles, Database, Network, BookOpen,
  ChevronDown, ChevronUp, Copy, Check, X, Mic, MicOff
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { useAuthStore } from '@/store/authStore';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  context?: any[];
  confidence?: number;
  sources_count?: number;
}

function ConfidenceBadge({ confidence }: { confidence: number }) {
  const isHigh = confidence >= 0.8;
  const isMed = confidence >= 0.55;
  const label = isHigh ? 'High' : isMed ? 'Medium' : 'Low';
  const cls = isHigh
    ? 'bg-emerald-500/15 text-emerald-400 border-emerald-500/25'
    : isMed
    ? 'bg-amber-500/15 text-amber-400 border-amber-500/25'
    : 'bg-red-500/15 text-red-400 border-red-500/25';
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold border ${cls}`}>
      <div className={`w-1.5 h-1.5 rounded-full ${isHigh ? 'bg-emerald-400' : isMed ? 'bg-amber-400' : 'bg-red-400'}`} />
      {label} confidence
    </span>
  );
}

function SourcesPill({ context }: { context: any[] }) {
  const [open, setOpen] = useState(false);
  const vectorSources = context.filter(c => c.type !== 'graph_relation');
  const graphSources = context.filter(c => c.type === 'graph_relation');

  return (
    <div className="mt-2">
      <button
        onClick={() => setOpen(!open)}
        className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/5 border border-white/10 text-xs text-slate-400 hover:bg-white/8 hover:text-slate-300 transition-colors"
      >
        <BookOpen size={10} />
        {context.length} source{context.length !== 1 ? 's' : ''} consulted
        {open ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
      </button>
      {open && (
        <div className="mt-2 space-y-2 pl-2 border-l border-white/10 animate-fade-in">
          {vectorSources.map((src, i) => (
            <div key={i} className="flex items-start gap-2 text-xs text-slate-500">
              <Database size={10} className="mt-0.5 text-blue-400 shrink-0" />
              <div className="flex flex-col gap-1 w-full">
                <span className="italic text-slate-400 text-[11px] whitespace-pre-wrap break-words">
                  "{src.content}"
                </span>
                
                <div className="flex flex-wrap items-center gap-2 mt-0.5">
                  {(src.metadata?.document_id || src.metadata?.file_name) && (
                    <a href="/documents" className="text-blue-400 font-medium hover:underline flex items-center gap-1 no-underline hover:no-underline">
                      <BookOpen size={9} /> {src.metadata.file_name || 'Source Document'}
                    </a>
                  )}
                  {src.metadata?.page_no && (
                    <span className="text-[10px] px-1.5 py-0.5 bg-white/5 rounded border border-white/10 text-slate-300">
                      Page {src.metadata.page_no}
                    </span>
                  )}
                  {src.metadata?.section && (
                    <span className="text-[10px] px-1.5 py-0.5 bg-white/5 rounded border border-white/10 text-slate-300">
                      § {src.metadata.section}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))}
          {graphSources.map((src, i) => (
            <div key={i} className="flex items-start gap-2 text-xs text-slate-500">
              <Network size={10} className="mt-0.5 text-violet-400 shrink-0" />
              <span className="italic text-slate-400 whitespace-pre-wrap break-words">Graph: {src.content}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  const handle = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button
      onClick={handle}
      className="p-1.5 rounded-lg text-slate-600 hover:text-slate-400 hover:bg-white/5 transition-all duration-200"
      title="Copy"
    >
      {copied ? <Check size={11} className="text-emerald-400" /> : <Copy size={11} />}
    </button>
  );
}

const SUGGESTED_QUERIES = [
  { icon: '🔍', text: 'Root causes of operational failures?' },
  { icon: '📋', text: 'Procedures for routine inspections' },
  { icon: '🚨', text: 'Explain the last critical incident' },
];

export default function CopilotWidget({ onClose }: { onClose: () => void }) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: `Hello! I am **OpsPilot AI**.\n\nHow can I help you today?`,
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
      return;
    }
    
    // @ts-ignore - Web Speech API
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition is not supported in this browser.");
      return;
    }
    
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    
    recognition.onresult = (event: any) => {
      let transcript = '';
      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      setInput(transcript);
    };
    
    recognition.onerror = (event: any) => {
      console.error("Speech recognition error", event.error);
      setIsListening(false);
    };
    
    recognition.onend = () => {
      setIsListening(false);
    };
    
    recognitionRef.current = recognition;
    recognition.start();
    setIsListening(true);
  };

  const handleSend = async (query?: string) => {
    const userMessage = (query || input).trim();
    if (!userMessage) return;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const token = useAuthStore.getState().accessToken;
      const apiUrl = import.meta.env.VITE_API_URL || '/api/v1';
      const response = await fetch(`${apiUrl}/copilot/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ query: userMessage })
      });

      if (!response.ok) throw new Error('Network response was not ok');
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      
      if (!reader) throw new Error('No reader available');

      // Add a placeholder message for the assistant
      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6);
            if (dataStr === '[DONE]') {
               // Stream finished
               continue;
            }
            try {
              const data = JSON.parse(dataStr);
              if (data.type === 'context') {
                 setMessages(prev => {
                   const newMsgs = [...prev];
                   const last = newMsgs[newMsgs.length - 1];
                   if (last.role === 'assistant') {
                     newMsgs[newMsgs.length - 1] = {
                       ...last,
                       context: data.context_used,
                       sources_count: data.sources_count,
                       confidence: 0.9 // Or dynamic based on future enhancement
                     };
                   }
                   return newMsgs;
                 });
              } else if (data.type === 'chunk') {
                 setMessages(prev => {
                   const newMsgs = [...prev];
                   const last = newMsgs[newMsgs.length - 1];
                   if (last.role === 'assistant') {
                     newMsgs[newMsgs.length - 1] = {
                       ...last,
                       content: last.content + data.content
                     };
                   }
                   return newMsgs;
                 });
              }
            } catch (e) {
              console.error("Error parsing stream chunk:", e);
            }
          }
        }
      }
    } catch (e) {
      console.error(e);
      setMessages(prev => {
        const newMsgs = [...prev];
        const last = newMsgs[newMsgs.length - 1];
        if (last.role === 'assistant') {
           last.content = 'I encountered an error processing your request. Please try again.';
        }
        return newMsgs;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-[rgba(10,15,35,0.95)] backdrop-blur-xl border-l border-white/10 shadow-2xl animate-fade-in-right">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-white/10 shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-violet-500 flex items-center justify-center shadow-glow-sm">
            <Sparkles size={14} className="text-white" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-100">OpsPilot AI</h2>
            <p className="text-[10px] text-slate-400">Hybrid RAG (Vector + Graph)</p>
          </div>
        </div>
        <button onClick={onClose} className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors">
          <X size={16} />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
          >
            <div className={`flex max-w-[85%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'} gap-2`}>
              {/* Avatar */}
              <div className={`shrink-0 w-6 h-6 rounded-lg flex items-center justify-center mt-0.5
                ${msg.role === 'user'
                  ? 'bg-gradient-to-br from-blue-500 to-indigo-500'
                  : 'bg-gradient-to-br from-violet-500/30 to-blue-500/20 border border-violet-500/20'}`}>
                {msg.role === 'user'
                  ? <User size={12} className="text-white" />
                  : <Bot size={12} className="text-violet-300" />
                }
              </div>

              {/* Bubble */}
              <div className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`group relative px-3 py-2.5 rounded-xl text-sm leading-relaxed
                  ${msg.role === 'user'
                    ? 'bg-gradient-to-br from-blue-600 to-indigo-600 text-white rounded-tr-sm shadow-[0_4px_14px_rgba(99,102,241,0.25)]'
                    : 'bg-white/[0.05] text-slate-200 border border-white/[0.08] rounded-tl-sm'}`}>
                  {msg.role === 'user' ? (
                    <span>{msg.content}</span>
                  ) : (
                    <div className="prose prose-sm prose-invert max-w-none
                      prose-p:text-slate-300 prose-strong:text-slate-100 prose-code:text-blue-300
                      prose-li:text-slate-300 prose-headings:text-slate-100 text-xs">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                      {loading && msg.content === '' && (
                        <div className="flex items-center gap-1.5 h-4">
                          {[0, 1, 2].map(i => (
                            <div key={i} className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce"
                              style={{ animationDelay: `${i * 0.15}s` }} />
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                  {/* Copy button for assistant */}
                  {msg.role === 'assistant' && msg.content && (
                    <div className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <CopyButton text={msg.content} />
                    </div>
                  )}
                </div>

                {/* Metadata (assistant) */}
                {msg.role === 'assistant' && (
                  <div className="mt-1 flex flex-col gap-1 pl-1">
                    {msg.confidence !== undefined && (
                      <ConfidenceBadge confidence={msg.confidence} />
                    )}
                    {msg.context && msg.context.length > 0 && (
                      <SourcesPill context={msg.context} />
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested queries */}
      {messages.length === 1 && (
        <div className="px-4 py-2 border-t border-white/[0.05] flex flex-wrap gap-1.5">
          {SUGGESTED_QUERIES.map(q => (
            <button
              key={q.text}
              onClick={() => handleSend(q.text)}
              className="flex items-center gap-1 px-2 py-1.5 text-[10px] rounded-lg bg-white/4 border border-white/8
                         text-slate-400 hover:bg-white/8 hover:text-slate-200 hover:border-blue-500/30
                         transition-all duration-200"
            >
              <span>{q.icon}</span>
              <span className="max-w-[150px] truncate">{q.text}</span>
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="p-3 border-t border-white/10 bg-slate-900/50">
        <div className="flex items-center gap-2">
          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Ask Copilot..."
              className="w-full h-10 px-3 text-xs bg-white/5 border border-white/10 rounded-lg
                         text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1
                         focus:ring-blue-500/50 focus:border-blue-500/50 transition-all"
              disabled={loading}
            />
          </div>
          <div className="relative flex items-center justify-center">
            {isListening && (
              <>
                <div className="absolute inset-0 rounded-lg bg-red-500/40 animate-ping opacity-75" />
                <div className="absolute inset-[-4px] rounded-lg border border-red-500/50 animate-pulse" />
              </>
            )}
            <Button
              onClick={toggleListening}
              size="icon"
              variant="ghost"
              className={`relative z-10 h-10 w-10 shrink-0 rounded-lg transition-colors ${
                isListening ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30 hover:text-red-300' : 'text-slate-400 hover:text-slate-200 hover:bg-white/10'
              }`}
              title={isListening ? "Stop listening" : "Start voice input"}
            >
              {isListening ? <Mic size={14} className="animate-pulse" /> : <Mic size={14} />}
            </Button>
          </div>
          <Button
            onClick={() => handleSend()}
            disabled={!input.trim() || loading}
            size="icon"
            className="h-10 w-10 shrink-0 rounded-lg"
          >
            {loading ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
          </Button>
        </div>
      </div>
    </div>
  );
}
