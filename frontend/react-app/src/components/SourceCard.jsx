import { useState } from 'react'
import { ChevronDown, ChevronUp, FileText, Table, BarChart2, Image } from 'lucide-react'

const TYPE_CONFIG = {
  text:  { icon: FileText,  color: 'blue',   label: 'Text'  },
  table: { icon: Table,     color: 'purple',  label: 'Table' },
  graph: { icon: BarChart2, color: 'green',   label: 'Graph' },
}

const COLOR_CLASSES = {
  blue: {
    bg:     'bg-blue-50',
    text:   'text-blue-700',
    border: 'border-blue-200',
    bar:    'bg-blue-500',
    ring:   'ring-blue-400',
    activeBg: 'bg-blue-100',
  },
  purple: {
    bg:     'bg-purple-50',
    text:   'text-purple-700',
    border: 'border-purple-200',
    bar:    'bg-purple-500',
    ring:   'ring-purple-400',
    activeBg: 'bg-purple-100',
  },
  green: {
    bg:     'bg-green-50',
    text:   'text-green-700',
    border: 'border-green-200',
    bar:    'bg-green-500',
    ring:   'ring-green-400',
    activeBg: 'bg-green-100',
  },
}

const API_BASE = 'http://localhost:8000'

export default function SourceCard({
  source,
  index,
  onHover,
  onLeave,
  isActive,
}) {
  const [expanded,   setExpanded]   = useState(false)
  const [imgError,   setImgError]   = useState(false)
  const [imgLoading, setImgLoading] = useState(true)

  const type   = source.chunk_type || 'text'
  const config = TYPE_CONFIG[type] || TYPE_CONFIG.text
  const colors = COLOR_CLASSES[config.color]
  const Icon   = config.icon
  const pct    = Math.round((source.relevance || 0) * 100)

  // Build image URL for graph chunks
  const isGraph   = type === 'graph'
  const docId     = source.document_id || ''
  const pageNum   = source.page_number || 1
  const imageUrl  = `${API_BASE}/ingest/image/${docId}/${pageNum}`

  return (
    <div
      className={`border ${colors.border} rounded-xl overflow-hidden mb-2 transition-all ${
        isActive ? `ring-2 ring-offset-1 ${colors.ring}` : ''
      }`}
      onMouseEnter={() => onHover && onHover(index, config.color)}
      onMouseLeave={() => onLeave && onLeave()}
    >
      {/* Header */}
      <div
        className={`flex items-center justify-between p-3 cursor-pointer transition-colors ${
          isActive ? colors.activeBg : colors.bg
        }`}
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-2">
          <div className={`w-6 h-6 rounded-lg ${colors.bg} border ${colors.border} flex items-center justify-center`}>
            <Icon size={12} className={colors.text} />
          </div>
          <span className={`text-xs font-semibold ${colors.text}`}>
            Source {index} — {config.label}
          </span>
          <span className="text-xs text-slate-400">
            Page {source.page_number}
          </span>
          {isGraph && (
            <span className="text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded-full flex items-center gap-1">
              <Image size={10} />
              Chart
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1">
            <div className="w-16 h-1.5 bg-white rounded-full overflow-hidden">
              <div
                className={`h-full ${colors.bar} rounded-full`}
                style={{ width: `${pct}%` }}
              />
            </div>
            <span className={`text-xs ${colors.text} font-semibold`}>
              {pct}%
            </span>
          </div>
          {expanded
            ? <ChevronUp size={14} className="text-slate-400" />
            : <ChevronDown size={14} className="text-slate-400" />
          }
        </div>
      </div>

      {/* Expanded Content */}
      {expanded && (
        <div className="bg-white border-t border-slate-100">

          {/* Graph: Show Image + Description */}
          {isGraph && docId && !imgError ? (
            <div className="p-3">

              {/* Chart Image */}
              <div className="mb-3">
                <p className="text-xs font-semibold text-green-700 mb-2 flex items-center gap-1">
                  <Image size={12} />
                  Chart from Page {pageNum}
                </p>
                <div className="relative bg-slate-50 rounded-xl overflow-hidden border border-slate-200">
                  {imgLoading && (
                    <div className="absolute inset-0 flex items-center justify-center bg-slate-50">
                      <div className="text-xs text-slate-400 animate-pulse">
                        Loading chart...
                      </div>
                    </div>
                  )}
                  <img
                    src       = {imageUrl}
                    alt       = {`Chart from page ${pageNum}`}
                    className = "w-full h-auto rounded-xl"
                    onLoad    = {() => setImgLoading(false)}
                    onError   = {() => {
                      setImgError(true)
                      setImgLoading(false)
                    }}
                    style={{ display: imgLoading ? 'none' : 'block' }}
                  />
                </div>
              </div>

              {/* AI Analysis */}
              <div className="bg-green-50 border border-green-200 rounded-xl p-3">
                <p className="text-xs font-semibold text-green-700 mb-1.5 flex items-center gap-1">
                  🤖 AI Chart Analysis
                </p>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {source.preview}
                </p>
              </div>

              <p className="text-xs text-slate-400 mt-2">
                {source.source_file}
              </p>
            </div>

          ) : (
            /* Text/Table: Show preview */
            <div className="p-3">
              <p className="text-xs text-slate-400 mb-1">
                {source.source_file}
              </p>
              <p className="text-xs text-slate-600 font-mono bg-slate-50 p-2 rounded-lg leading-relaxed">
                {source.preview}
              </p>
            </div>
          )}

        </div>
      )}
    </div>
  )
}