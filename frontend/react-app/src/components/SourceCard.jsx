import { useState } from 'react'
import { ChevronDown, ChevronUp, FileText, Table, BarChart2 } from 'lucide-react'

const TYPE_CONFIG = {
  text:  { icon: FileText,  color: 'blue',   label: 'Text'  },
  table: { icon: Table,     color: 'purple',  label: 'Table' },
  graph: { icon: BarChart2, color: 'green',   label: 'Graph' },
}

const COLOR_CLASSES = {
  blue:   {
    bg:     'bg-blue-50',
    text:   'text-blue-700',
    border: 'border-blue-200',
    bar:    'bg-blue-500',
  },
  purple: {
    bg:     'bg-purple-50',
    text:   'text-purple-700',
    border: 'border-purple-200',
    bar:    'bg-purple-500',
  },
  green:  {
    bg:     'bg-green-50',
    text:   'text-green-700',
    border: 'border-green-200',
    bar:    'bg-green-500',
  },
}

export default function SourceCard({ source, index }) {
  const [expanded, setExpanded] = useState(false)

  const type   = source.chunk_type || 'text'
  const config = TYPE_CONFIG[type] || TYPE_CONFIG.text
  const colors = COLOR_CLASSES[config.color]
  const Icon   = config.icon
  const pct    = Math.round((source.relevance || 0) * 100)

  return (
    <div className={`border ${colors.border} rounded-xl overflow-hidden mb-2`}>

      {/* Header */}
      <div
        className={`flex items-center justify-between p-3 ${colors.bg} cursor-pointer`}
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
        </div>

        <div className="flex items-center gap-2">
          {/* Relevance bar */}
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
        <div className="p-3 bg-white border-t border-slate-100">
          <p className="text-xs text-slate-400 mb-1">
            {source.source_file}
          </p>
          <p className="text-xs text-slate-600 font-mono bg-slate-50 p-2 rounded-lg leading-relaxed">
            {source.preview}
          </p>
        </div>
      )}

    </div>
  )
}