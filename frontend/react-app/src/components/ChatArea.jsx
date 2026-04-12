import { useState, useRef, useEffect } from 'react'
import { Send, Loader2, Bot } from 'lucide-react'
import MessageBubble from './MessageBubble'
import { askQuestion } from '../services/api'

const WELCOME_MESSAGE = {
  role:    'assistant',
  content: "👋 Hello! I'm your Tesla Financial Intelligence assistant. Ask me anything about Tesla's Q3 2023 financial report — revenue, margins, deliveries, charts, and more!",
  sources:  [],
  metadata: {},
}

export default function ChatArea({
  selectedQuestion,
  currentChatId,
  savedMessages,
  onMessagesUpdate,
}) {
  const [messages,     setMessages]     = useState(savedMessages || [WELCOME_MESSAGE])
  const [input,        setInput]        = useState('')
  const [loading,      setLoading]      = useState(false)
  const [loadingSteps, setLoadingSteps] = useState([])
  const bottomRef = useRef(null)
  const inputRef  = useRef(null)

  // --- Load messages when chat changes ---
  useEffect(() => {
    setMessages(savedMessages || [WELCOME_MESSAGE])
  }, [currentChatId])

  // --- Auto scroll to bottom ---
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  // --- Handle sample question from sidebar ---
  useEffect(() => {
    if (selectedQuestion) {
      handleSend(selectedQuestion)
    }
  }, [selectedQuestion])

  // --- Save messages when they change ---
  useEffect(() => {
    if (onMessagesUpdate && messages.length > 1) {
      onMessagesUpdate(currentChatId, messages)
    }
  }, [messages])

  const handleSend = async (questionOverride = null) => {
    const question = questionOverride || input.trim()
    if (!question || loading) return

    setInput('')
    setLoading(true)

    // --- Initialize loading steps ---
    const steps = [
      { label: '⚡ Embedding your question...',   active: true,  done: false },
      { label: '🔍 Searching knowledge base...',  active: false, done: false },
      { label: '🤖 Generating answer with AI...', active: false, done: false },
      { label: '✅ Formatting response...',        active: false, done: false },
    ]
    setLoadingSteps(steps)

    // Add user message
    setMessages(prev => [...prev, {
      role:    'user',
      content: question,
    }])

    try {
      // --- Step 1: Embedding ---
      await new Promise(r => setTimeout(r, 600))
      setLoadingSteps(prev => prev.map((s, i) =>
        i === 0 ? { ...s, active: false, done: true } :
        i === 1 ? { ...s, active: true }              : s
      ))

      // --- Step 2: Searching ---
      await new Promise(r => setTimeout(r, 600))
      setLoadingSteps(prev => prev.map((s, i) =>
        i === 1 ? { ...s, active: false, done: true } :
        i === 2 ? { ...s, active: true }              : s
      ))

      // --- Step 3: API Call ---
      const data = await askQuestion(question, 8)

      // --- Step 4: Formatting ---
      setLoadingSteps(prev => prev.map((s, i) =>
        i === 2 ? { ...s, active: false, done: true } :
        i === 3 ? { ...s, active: true }              : s
      ))
      await new Promise(r => setTimeout(r, 400))
      setLoadingSteps(prev => prev.map((s, i) =>
        i === 3 ? { ...s, active: false, done: true } : s
      ))

      // --- Add answer ---
      setMessages(prev => [...prev, {
        role:    'assistant',
        content: data.answer,
        sources: data.sources || [],
        metadata: {
          total_chunks_used:       data.total_chunks_used,
          processing_time_seconds: data.processing_time_seconds,
          types_used:              data.types_used,
        },
      }])

    } catch (err) {
      setMessages(prev => [...prev, {
        role:     'assistant',
        content:  '❌ Error: Could not connect to backend. Make sure the FastAPI server is running.',
        sources:  [],
        metadata: {},
      }])
    } finally {
      setLoading(false)
      setLoadingSteps([])
      inputRef.current?.focus()
    }
  }

  return (
    <div className="flex flex-col flex-1 overflow-hidden">

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 chat-scroll">
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {/* Loading Steps */}
        {loading && (
          <div className="flex items-start gap-2 mb-4 fade-in">
            <div className="w-7 h-7 bg-slate-100 rounded-full flex items-center justify-center flex-shrink-0">
              <Bot size={14} className="text-blue-600" />
            </div>
            <div className="bg-white border border-slate-200 px-4 py-3 rounded-2xl rounded-tl-sm shadow-sm min-w-64">
              <div className="space-y-2">
                {loadingSteps.map((step, i) => (
                  <div key={i} className="flex items-center gap-2">
                    {step.done ? (
                      <div className="w-4 h-4 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0">
                        <span className="text-green-600 text-xs">✓</span>
                      </div>
                    ) : step.active ? (
                      <Loader2 size={14} className="text-blue-600 animate-spin flex-shrink-0" />
                    ) : (
                      <div className="w-4 h-4 rounded-full bg-slate-100 flex-shrink-0" />
                    )}
                    <span className={`text-xs ${
                      step.done
                        ? 'text-green-600 font-medium'
                        : step.active
                        ? 'text-blue-600 font-medium'
                        : 'text-slate-300'
                    }`}>
                      {step.label}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-slate-200 bg-white p-4">
        <div className="flex items-center gap-3 bg-slate-50 border border-slate-200 rounded-2xl px-4 py-3 focus-within:border-blue-400 focus-within:bg-white transition-all">
          <input
            ref         = {inputRef}
            type        = "text"
            value       = {input}
            onChange    = {e => setInput(e.target.value)}
            onKeyDown   = {e => e.key === 'Enter' && !e.shiftKey && handleSend()}
            placeholder = "Ask about Tesla's financials..."
            className   = "flex-1 bg-transparent text-sm text-slate-700 placeholder-slate-400 outline-none"
            disabled    = {loading}
          />
          <button
            onClick   = {() => handleSend()}
            disabled  = {!input.trim() || loading}
            className = {`w-8 h-8 rounded-xl flex items-center justify-center transition-all ${
              input.trim() && !loading
                ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-sm'
                : 'bg-slate-200 text-slate-400 cursor-not-allowed'
            }`}
          >
            <Send size={14} />
          </button>
        </div>
        <p className="text-center text-xs text-slate-400 mt-2">
          Powered by Multimodal RAG · 📝 Text · 📊 Tables · 📈 Charts
        </p>
      </div>

    </div>
  )
}