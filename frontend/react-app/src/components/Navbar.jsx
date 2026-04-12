import { Menu, Brain, Activity, Plus } from 'lucide-react'
import { useState, useEffect } from 'react'
import { checkHealth } from '../services/api'

export default function Navbar({ onToggleSidebar, onNewChat }) {
  const [online, setOnline] = useState(false)

  useEffect(() => {
    checkHealth().then(r => setOnline(r.online))
    const interval = setInterval(() => {
      checkHealth().then(r => setOnline(r.online))
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <nav className="h-14 bg-white border-b border-slate-200 flex items-center justify-between px-4 shadow-sm flex-shrink-0">

      {/* Left */}
      <div className="flex items-center gap-3">
        <button
          onClick   = {onToggleSidebar}
          className = "p-2 rounded-lg hover:bg-slate-100 transition-colors"
        >
          <Menu size={20} className="text-slate-600" />
        </button>

        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <Brain size={16} className="text-white" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-slate-800 leading-none">
              Tesla Financial Intelligence
            </h1>
            <p className="text-xs text-slate-400 leading-none mt-0.5">
              Powered by Multimodal RAG
            </p>
          </div>
        </div>
      </div>

      {/* Right */}
      <div className="flex items-center gap-2">

        {/* New Chat Button */}
        <button
          onClick   = {onNewChat}
          className = "flex items-center gap-1.5 px-3 py-1.5 bg-blue-50 hover:bg-blue-100 text-blue-600 rounded-lg text-xs font-medium transition-colors border border-blue-200"
        >
          <Plus size={12} />
          New Chat
        </button>

        {/* Status */}
        <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium ${
          online
            ? 'bg-green-50 text-green-700 border border-green-200'
            : 'bg-red-50 text-red-700 border border-red-200'
        }`}>
          <Activity size={12} />
          {online ? 'Backend Online' : 'Backend Offline'}
        </div>
      </div>

    </nav>
  )
}