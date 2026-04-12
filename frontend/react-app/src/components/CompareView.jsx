import ReactMarkdown from 'react-markdown'
import { GitCompare, FileText } from 'lucide-react'

const MarkdownContent = ({ content }) => (
  <ReactMarkdown
    components={{
      h2: ({node, ...props}) => (
        <h2 className="text-sm font-semibold text-slate-700 mb-2 mt-3" {...props} />
      ),
      p: ({node, ...props}) => (
        <p className="text-sm text-slate-600 leading-relaxed mb-2" {...props} />
      ),
      strong: ({node, ...props}) => (
        <strong className="font-semibold text-slate-900" {...props} />
      ),
      ul: ({node, ...props}) => (
        <ul className="space-y-1 mb-2" {...props} />
      ),
      li: ({node, ...props}) => (
        <li className="text-sm text-slate-600 flex items-start gap-2">
          <span className="text-blue-400 mt-1">•</span>
          <span {...props} />
        </li>
      ),
    }}
  >
    {content}
  </ReactMarkdown>
)

export default function CompareView({ result }) {
  if (!result) return null

  const doc1Name = result.document_1
    .replace('TSLA-', '')
    .replace('.pdf', '')
  const doc2Name = result.document_2
    .replace('TSLA-', '')
    .replace('.pdf', '')

  return (
    <div className="fade-in">

      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <div className="w-7 h-7 bg-purple-100 rounded-full flex items-center justify-center">
          <GitCompare size={14} className="text-purple-600" />
        </div>
        <div>
          <p className="text-xs font-semibold text-purple-600">
            Comparison Mode
          </p>
          <p className="text-xs text-slate-400">{result.question}</p>
        </div>
      </div>

      {/* Side by Side */}
      <div className="grid grid-cols-2 gap-3 mb-3">

        {/* Document 1 */}
        <div className="bg-white border border-blue-200 rounded-2xl p-4">
          <div className="flex items-center gap-2 mb-3 pb-2 border-b border-slate-100">
            <div className="w-6 h-6 bg-blue-100 rounded-lg flex items-center justify-center">
              <FileText size={11} className="text-blue-600" />
            </div>
            <span className="text-xs font-semibold text-blue-700">
              {doc1Name}
            </span>
          </div>
          <MarkdownContent content={result.answer_1} />
        </div>

        {/* Document 2 */}
        <div className="bg-white border border-green-200 rounded-2xl p-4">
          <div className="flex items-center gap-2 mb-3 pb-2 border-b border-slate-100">
            <div className="w-6 h-6 bg-green-100 rounded-lg flex items-center justify-center">
              <FileText size={11} className="text-green-600" />
            </div>
            <span className="text-xs font-semibold text-green-700">
              {doc2Name}
            </span>
          </div>
          <MarkdownContent content={result.answer_2} />
        </div>

      </div>

      {/* Combined Analysis */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-2xl p-4">
        <div className="flex items-center gap-2 mb-3">
          <GitCompare size={14} className="text-purple-600" />
          <span className="text-xs font-semibold text-purple-700">
            Comparative Analysis
          </span>
        </div>
        <MarkdownContent content={result.combined_analysis} />
      </div>

      {/* Metadata */}
      <p className="text-xs text-slate-400 mt-2 text-center">
        ⏱️ {result.processing_time_seconds}s
      </p>

    </div>
  )
}