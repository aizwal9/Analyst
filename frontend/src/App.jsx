import { useEffect, useRef, useState } from 'react'
import './App.css'
import { Activity, Bot, Database, Send } from 'lucide-react'
import { Message } from './components/Message'
import { Sidebar } from './components/Sidebar';

const API_URL = "http://localhost:8000";

const CustomScrollbar = () => (
  <style>{`
    /* Webkit (Chrome, Edge, Safari) */
    ::-webkit-scrollbar {
      width: 10px;
      height: 10px;
    }
    ::-webkit-scrollbar-track {
      background: transparent; 
    }
    ::-webkit-scrollbar-thumb {
      background: #334155; 
      border-radius: 5px;
      border: 2px solid #0f172a; /* Creates padding effect against dark background */
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #475569; 
    }
    
    /* Firefox */
    * {
      scrollbar-width: thin;
      scrollbar-color: #334155 #0f172a;
    }
  `}</style>
);

function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const [threadId, setThreadId] = useState(() => `thread_${Math.random().toString(36).substring(2, 9)}`)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(scrollToBottom, [messages])


  useEffect(() => {
    const loadSession = async () => {
      setIsLoading(true)
      try {
        const res = await fetch(`${API_URL}/history/${threadId}`)
        if (res.ok) {
          const data = await res.json()
          setMessages(data)
        }
      } catch (e) {
        console.error("Failed to load session", e)
        setMessages([])
      } finally {
        setIsLoading(false)
      }
    }

    loadSession()
  }, [threadId])

  const handleNewChat = () => {
    const newId = `thread_${Math.random().toString(36).substring(2, 9)}`
    setThreadId(newId);
    setMessages([])
  }


  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMsg = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setIsLoading(true)


    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input, thread_id: threadId })
      })

      const data = await response.json()
      const botMsg = {
        role: 'assistant',
        content: data.sql_query ? "I've analyzed the data for you." : "I couldn't find any relevant data.",
        sql_query: data.sql_query,
        visualization_spec: data.visualization_spec,
        email_draft: data.email_draft,
        needs_approval: data.needs_approval,
        thread_id: threadId,
        steps: [data.sql_query ? "SQL Generated" : null, data.sql_query ? "Data Fetched" : null, data.visualization_spec ? "Chart Rendered" : null, data.email_draft ? "Draft Created" : null].filter(Boolean)
      };

      setMessages(prev => [...prev, botMsg])
    } catch (error) {
      console.error(error)
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error connecting to the analyst brain." }]);
    } finally {
      setIsLoading(false)
    }
  }

  const handleApprove = async (tId, approved) => {
    try {
      await fetch(`${API_URL}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ thread_id: tId, approved })
      })
    } catch (error) {
      console.error(error);
      throw error;
    }
  }


  return (
    <div className="flex h-screen bg-[#0f172a] text-slate-200 font-sans selection:bg-indigo-500/30">
      <CustomScrollbar />

      {/* Sidebar */}

      <Sidebar
        currentThreadId={threadId}
        onSelectThread={setThreadId}
        onNewChat={handleNewChat}
      />

      {/* <div className="w-20 lg:w-64 border-r border-slate-800 bg-[#0f172a] flex-shrink-0 flex flex-col items-center lg:items-stretch py-6 px-0 lg:px-4 hidden md:flex">
        <div className="flex items-center gap-3 px-2 lg:px-4 mb-10">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Database size={20} className="text-white" />
          </div>
          <div className="hidden lg:block">
            <h1 className="font-bold text-lg text-white leading-tight">DataMind</h1>
            <p className="text-xs text-slate-500 font-medium">Analyst Agent</p>
          </div>
        </div>

        <nav className='space-y-2 w-full'>
          <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg bg-slate-800/50 text-indigo-400 border border-slate-700/50 transition-all">
            <Bot size={20} />
            <span className="hidden lg:inline text-sm font-medium">Chat Analyst</span>
          </button>
          <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:bg-slate-800/50 transition-all">
            <Activity size={20} />
            <span className="hidden lg:inline text-sm font-medium">History</span>
          </button>
        </nav>
      </div> */}

      {/* Main Content */}
      <div className="flex-1 flex flex-col h-screen relative overflow-hidden bg-gradient-to-b from-[#0f172a] to-[#1e293b]">

        {/* Header */}
        <header className="h-16 border-b border-slate-800/80 bg-[#0f172a]/80 backdrop-blur-md flex items-center justify-between px-6 z-10 sticky top-0">
          <div className="flex items-center gap-3">
            <span className="md:hidden">
              <Database size={24} className="text-indigo-500" />
            </span>
            <h2 className="text-sm font-semibold text-slate-300">
              {messages.length > 0 ? "Active Session" : "New Analysis Session"}
            </h2>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-xs font-medium text-emerald-400">System Online</span>
            </div>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6">
          {messages.length === 0 && !isLoading ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-8 opacity-50">
              <div className="w-24 h-24 rounded-full bg-slate-800 flex items-center justify-center mb-6">
                <Bot size={48} className="text-slate-600" />
              </div>
              <h3 className="text-xl font-medium text-slate-300 mb-2">How can I help you today?</h3>
              <p className="text-slate-500 max-w-md">
                Ask me to analyze customer churn, sales trends, or draft marketing emails based on your data.
              </p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <Message key={idx} message={msg} onApprove={handleApprove} />
            ))
          )}
          {isLoading && (
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center">
                <Bot size={20} />
              </div>
              <div className="flex items-center gap-1 h-10">
                <div className="w-2 h-2 bg-slate-600 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
                <div className="w-2 h-2 bg-slate-600 rounded-full animate-bounce" style={{ animationDelay: '0.15s' }} />
                <div className="w-2 h-2 bg-slate-600 rounded-full animate-bounce" style={{ animationDelay: '0.3s' }} />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>


        {/* Input Area */}
        <div className="p-4 md:p-6 bg-[#0f172a] border-t border-slate-800">
          <form
            onSubmit={handleSubmit}
            className="max-w-4xl mx-auto relative flex items-center gap-4 bg-slate-800/50 p-2 rounded-xl border border-slate-700 focus-within:border-indigo-500/50 focus-within:ring-2 focus-within:ring-indigo-500/20 transition-all"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about your data..."
              className="flex-1 bg-transparent border-none outline-none text-slate-200 placeholder-slate-500 px-4 py-2"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="p-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send size={18} />
            </button>
          </form>
          <p className="text-center text-slate-600 text-xs mt-3">
            AI can make mistakes. Verify critical data.
          </p>
        </div>
      </div>
    </div>
  )

}

export default App
