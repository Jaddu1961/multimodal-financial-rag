import { useEffect, useState } from 'react'
import {
  Database, FileText, Lightbulb,
  Settings, ChevronRight, MessageSquare, X
} from 'lucide-react'
import { getStats, getDocuments } from '../services/api'

const SAMPLE_QUESTIONS = [
  "What was Tesla's total revenue in Q3 2023?",
  "What is Tesla's gross profit margin?",
  "What do charts show about revenue growth?",
  "How did operating expenses change?",
  "What is Tesla's free cash flow?",
  "How many vehicles were delivered?",
]

export default function Sidebar({
  isOpen,
  onQuestionSelect,
  chatHistory = {},
  currentChatId,
  onNewChat,
  onSelectChat,
  onDeleteChat,
}) {
  const [stats,    setStats]    = useState(null)
  const [docs,     setDocs]     = useState([])
  const [nResults, setNResults] = useState(8)

  useEffect(() => {
    getStats().then(setStats).catch(() => {})
    getDocuments().then(d => setDocs(d.documents || [])).catch(() => {})
  }, [])

  if (!isOpen) return null

  return (
    <aside className="w-72 bg-white border-r border-slate-200 flex flex-col h-full overflow-y-auto flex-shrink-0">

      {/* Knowledge Base Stats */}
      <div className="p-4 border-b border-slate-100">
        <div className="flex items-center gap-2 mb-3">
          <Database size={14} className="text-blue-600" />
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Knowledge Base
          </span>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div className="bg-blue-50 rounded-xl p-3 text-center">
            <p className="text-2xl font-extrabold text-blue-600">
              {stats?.total_chunks || 0}
            </p>
            <p className="text-xs text-slate-500 mt-0.5">Chunks</p>
          </div>
          <div className="bg-slate-50 rounded-xl p-3 text-center">
            <p className="text-2xl font-extrabold text-slate-700">
              {docs.length}
            </p>
            <p className="text-xs text-slate-500 mt-0.5">Documents</p>
          </div>
        </div>

        {/* Source Types */}
        <div className="flex gap-2 mt-2">
          {['📝 Text', '📊 Tables', '📈 Graphs'].map(t => (
            <span
              key={t}
              className="flex-1 text-center text-xs bg-slate-50 text-slate-600 py-1 rounded-lg border border-slate-100"
            >
              {t}
            </span>
          ))}
        </div>
      </div>

      {/* Documents */}
      <div className="p-4 border-b border-slate-100">
        <div className="flex items-center gap-2 mb-3">
          <FileText size={14} className="text-blue-600" />
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Documents
          </span>
        </div>
        {docs.length > 0 ? (
          docs.map(doc => (
            <div
              key={doc.document_id}
              className="flex items-start gap-2 p-2.5 bg-slate-50 rounded-xl border border-slate-100 mb-2"
            >
              <div className="w-7 h-7 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <FileText size={12} className="text-blue-600" />
              </div>
              <div className="min-w-0">
                <p className="text-xs font-semibold text-slate-700 truncate">
                  {doc.filename}
                </p>
                <p className="text-xs text-slate-400 mt-0.5">
                  {doc.ingested_at}
                </p>
              </div>
            </div>
          ))
        ) : (
          <p className="text-xs text-slate-400 text-center py-2">
            No documents ingested
          </p>
        )}
      </div>

      {/* Chat History */}
      {Object.keys(chatHistory).length > 0 && (
        <div className="p-4 border-b border-slate-100">
          <div className="flex items-center gap-2 mb-3">
            <MessageSquare size={14} className="text-blue-600" />
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
              Recent Chats
            </span>
          </div>
          <div className="space-y-1">
            {Object.values(chatHistory)
              .sort((a, b) => b.id.localeCompare(a.id))
              .slice(0, 5)
              .map(chat => (
                <div
                  key       = {chat.id}
                  className = {`flex items-center justify-between p-2 rounded-xl cursor-pointer transition-all group ${
                    chat.id === currentChatId
                      ? 'bg-blue-50 border border-blue-200'
                      : 'hover:bg-slate-50 border border-transparent'
                  }`}
                  onClick={() => onSelectChat(chat.id)}
                >
                  <div className="min-w-0 flex-1">
                    <p className={`text-xs truncate ${
                      chat.id === currentChatId
                        ? 'text-blue-700 font-medium'
                        : 'text-slate-600'
                    }`}>
                      {chat.title}
                    </p>
                    <p className="text-xs text-slate-400 mt-0.5">
                      {chat.updatedAt}
                    </p>
                  </div>
                  <button
                    onClick={e => {
                      e.stopPropagation()
                      onDeleteChat(chat.id)
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-100 rounded-lg transition-all ml-1"
                  >
                    <X size={10} className="text-red-400" />
                  </button>
                </div>
              ))
            }
          </div>
        </div>
      )}

      {/* Sample Questions */}
      <div className="p-4 border-b border-slate-100 flex-1">
        <div className="flex items-center gap-2 mb-3">
          <Lightbulb size={14} className="text-blue-600" />
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Try These
          </span>
        </div>
        <div className="space-y-1.5">
          {SAMPLE_QUESTIONS.map((q, i) => (
            <button
              key={i}
              onClick={() => onQuestionSelect && onQuestionSelect(q)}
              className="w-full text-left text-xs text-slate-600 p-2.5 rounded-xl hover:bg-blue-50 hover:text-blue-700 border border-transparent hover:border-blue-100 transition-all flex items-center gap-2 group"
            >
              <ChevronRight
                size={12}
                className="text-slate-300 group-hover:text-blue-500 flex-shrink-0"
              />
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Settings */}
      <div className="p-4">
        <div className="flex items-center gap-2 mb-3">
          <Settings size={14} className="text-blue-600" />
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Settings
          </span>
        </div>
        <div>
          <label className="text-xs text-slate-500 mb-1 block">
            Results to retrieve:{" "}
            <span className="text-blue-600 font-semibold">{nResults}</span>
          </label>
          <input
            type     = "range"
            min      = "3"
            max      = "10"
            value    = {nResults}
            onChange = {e => setNResults(Number(e.target.value))}
            className= "w-full accent-blue-600"
          />
        </div>
      </div>

    </aside>
  )
}