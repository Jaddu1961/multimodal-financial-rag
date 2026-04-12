import { useState } from 'react'
import { User, Bot, ChevronDown, ChevronUp, Clock, Layers } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import SourceCard from './SourceCard'

// --- Color map for highlight ---
const HIGHLIGHT_COLORS = {
  blue:   'bg-blue-50 border-l-2 border-blue-300 pl-2 rounded-r',
  purple: 'bg-purple-50 border-l-2 border-purple-300 pl-2 rounded-r',
  green:  'bg-green-50 border-l-2 border-green-300 pl-2 rounded-r',
}

export default function MessageBubble({ message }) {
  const [showSources,    setShowSources]    = useState(false)
  const [activeSource,   setActiveSource]   = useState(null)
  const [highlightColor, setHighlightColor] = useState(null)

  const isUser = message.role === 'user'

  const handleSourceHover = (index, color) => {
    setActiveSource(index)
    setHighlightColor(color)
  }

  const handleSourceLeave = () => {
    setActiveSource(null)
    setHighlightColor(null)
  }

  if (isUser) {
    return (
      <div className="flex justify-end mb-4 fade-in">
        <div className="flex items-end gap-2 max-w-xl">
          <div className="bg-blue-600 text-white px-4 py-3 rounded-2xl rounded-br-sm shadow-sm">
            <p className="text-sm leading-relaxed">{message.content}</p>
          </div>
          <div className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
            <User size={14} className="text-white" />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start mb-4 fade-in">
      <div className="flex items-start gap-2 max-w-2xl w-full">

        {/* Bot Icon */}
        <div className="w-7 h-7 bg-slate-100 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
          <Bot size={14} className="text-blue-600" />
        </div>

        <div className="flex-1">

          {/* Answer with Markdown + Highlight */}
          <div className={`bg-white border px-4 py-4 rounded-2xl rounded-tl-sm shadow-sm transition-all ${
            highlightColor
              ? `border-${highlightColor}-200`
              : 'border-slate-200'
          }`}>

            {/* Highlight indicator */}
            {activeSource && highlightColor && (
              <div className={`flex items-center gap-2 mb-3 px-3 py-1.5 rounded-lg text-xs font-medium ${
                highlightColor === 'blue'
                  ? 'bg-blue-50 text-blue-700'
                  : highlightColor === 'purple'
                  ? 'bg-purple-50 text-purple-700'
                  : 'bg-green-50 text-green-700'
              }`}>
                <div className={`w-2 h-2 rounded-full ${
                  highlightColor === 'blue'   ? 'bg-blue-500'   :
                  highlightColor === 'purple' ? 'bg-purple-500' :
                                                'bg-green-500'
                }`} />
                Highlighting content from Source {activeSource}
              </div>
            )}

            <div className={`prose prose-sm max-w-none transition-all ${
              activeSource ? 'opacity-90' : ''
            }`}>
              <ReactMarkdown
                components={{
                  h1: ({node, ...props}) => (
                    <h1
                      className={`text-lg font-bold text-slate-800 mb-2 mt-1 transition-all ${
                        activeSource ? `px-2 py-1 rounded ${
                          highlightColor ? HIGHLIGHT_COLORS[highlightColor] : ''
                        }` : ''
                      }`}
                      {...props}
                    />
                  ),
                  h2: ({node, ...props}) => (
                    <h2
                      className="text-base font-semibold text-slate-700 mb-2 mt-3 pb-1 border-b border-slate-100"
                      {...props}
                    />
                  ),
                  h3: ({node, ...props}) => (
                    <h3
                      className="text-sm font-semibold text-slate-600 mb-1 mt-2"
                      {...props}
                    />
                  ),
                  p: ({node, ...props}) => (
                    <p
                      className={`text-sm text-slate-700 leading-relaxed mb-2 transition-all rounded ${
                        activeSource && highlightColor
                          ? `${HIGHLIGHT_COLORS[highlightColor]} py-0.5`
                          : ''
                      }`}
                      {...props}
                    />
                  ),
                  strong: ({node, ...props}) => (
                    <strong
                      className="font-semibold text-slate-900"
                      {...props}
                    />
                  ),
                  ul: ({node, ...props}) => (
                    <ul className="space-y-1 mb-2 ml-1" {...props} />
                  ),
                  ol: ({node, ...props}) => (
                    <ol className="space-y-1 mb-2 ml-4 list-decimal" {...props} />
                  ),
                  li: ({node, ...props}) => (
                    <li className={`text-sm text-slate-700 flex items-start gap-2 transition-all rounded ${
                      activeSource && highlightColor
                        ? `${HIGHLIGHT_COLORS[highlightColor]} py-0.5 pr-1`
                        : ''
                    }`}>
                      <span className={`mt-1 flex-shrink-0 ${
                        activeSource && highlightColor
                          ? highlightColor === 'blue'   ? 'text-blue-400'   :
                            highlightColor === 'purple' ? 'text-purple-400' :
                                                          'text-green-400'
                          : 'text-blue-400'
                      }`}>•</span>
                      <span {...props} />
                    </li>
                  ),
                  blockquote: ({node, ...props}) => (
                    <blockquote
                      className="border-l-4 border-blue-300 pl-3 py-1 my-2 bg-blue-50 rounded-r-lg text-sm text-slate-600 italic"
                      {...props}
                    />
                  ),
                  code: ({node, ...props}) => (
                    <code
                      className="bg-slate-100 text-blue-700 px-1.5 py-0.5 rounded text-xs font-mono"
                      {...props}
                    />
                  ),
                  hr: ({node, ...props}) => (
                    <hr className="border-slate-200 my-3" {...props} />
                  ),
                }}
              >
                {message.content}
              </ReactMarkdown>
            </div>

            {/* Metadata bar */}
            {message.metadata && message.metadata.total_chunks_used > 0 && (
              <div className="flex items-center gap-3 mt-3 pt-3 border-t border-slate-100">
                <div className="flex items-center gap-1 text-xs text-slate-400">
                  <Clock size={11} />
                  {message.metadata.processing_time_seconds}s
                </div>
                <div className="flex items-center gap-1 text-xs text-slate-400">
                  <Layers size={11} />
                  {message.metadata.total_chunks_used} chunks
                </div>
                {Object.entries(message.metadata.types_used || {}).map(
                  ([type, count]) => (
                    <span
                      key={type}
                      className="text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full"
                    >
                      {type === 'text' ? '📝' : type === 'table' ? '📊' : '📈'} {count}
                    </span>
                  )
                )}
              </div>
            )}
          </div>

          {/* Sources Toggle */}
          {message.sources && message.sources.length > 0 && (
            <div className="mt-2">
              <button
                onClick={() => setShowSources(!showSources)}
                className="flex items-center gap-1.5 text-xs text-blue-600 hover:text-blue-700 font-medium px-2 py-1 rounded-lg hover:bg-blue-50 transition-colors"
              >
                {showSources
                  ? <ChevronUp size={12} />
                  : <ChevronDown size={12} />
                }
                {showSources ? 'Hide' : 'View'} Sources ({message.sources.length})
                {!showSources && (
                  <span className="text-slate-400 font-normal">
                    — hover to highlight
                  </span>
                )}
              </button>

              {showSources && (
                <div className="mt-2 space-y-1">
                  <p className="text-xs text-slate-400 px-2 mb-2">
                    💡 Hover over a source to highlight related content
                  </p>
                  {message.sources.map((source, i) => (
                    <SourceCard
                      key      = {i}
                      source   = {source}
                      index    = {i + 1}
                      onHover  = {handleSourceHover}
                      onLeave  = {handleSourceLeave}
                      isActive = {activeSource === i + 1}
                    />
                  ))}
                </div>
              )}
            </div>
          )}

        </div>
      </div>
    </div>
  )
}