import { useEffect, useState, useRef } from 'react'
import {
  Database, FileText, Lightbulb, Settings,
  ChevronRight, MessageSquare, X, Upload,
  CheckCircle, AlertCircle, Loader2
} from 'lucide-react'
import { getStats, getDocuments, uploadDocument } from '../services/api'

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
  const [stats,         setStats]         = useState(null)
  const [docs,          setDocs]          = useState([])
  const [nResults,      setNResults]      = useState(8)
  const [uploading,     setUploading]     = useState(false)
  const [uploadProgress,setUploadProgress]= useState(0)
  const [uploadStatus,  setUploadStatus]  = useState(null) // 'success' | 'error' | null
  const [uploadMessage, setUploadMessage] = useState('')
  const [dragOver,      setDragOver]      = useState(false)
  const [fiscalQuarter, setFiscalQuarter] = useState('')
  const [extractGraphs, setExtractGraphs] = useState(false)
  const fileInputRef = useRef(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = () => {
    getStats().then(setStats).catch(() => {})
    getDocuments().then(d => setDocs(d.documents || [])).catch(() => {})
  }

  const handleFileUpload = async (file) => {
    if (!file) return
    if (!file.name.endsWith('.pdf')) {
      setUploadStatus('error')
      setUploadMessage('Only PDF files are supported')
      return
    }

    setUploading(true)
    setUploadProgress(0)
    setUploadStatus(null)
    setUploadMessage('')

    try {
      const result = await uploadDocument(
        file,
        fiscalQuarter,
        extractGraphs,
        (pct) => setUploadProgress(pct)
      )

      if (result.success) {
        setUploadStatus('success')
        setUploadMessage(
          `✅ Ingested ${result.filename} — ${result.chunks_stored} chunks stored`
        )
        fetchData() // Refresh stats
      } else {
        setUploadStatus('error')
        setUploadMessage(result.message || 'Upload failed')
      }
    } catch (err) {
      setUploadStatus('error')
      setUploadMessage(
        err.response?.data?.detail || 'Upload failed. Try again.'
      )
    } finally {
      setUploading(false)
      setUploadProgress(0)
      setTimeout(() => {
        setUploadStatus(null)
        setUploadMessage('')
      }, 5000)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFileUpload(file)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setDragOver(true)
  }

  const handleDragLeave = () => setDragOver(false)

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) handleFileUpload(file)
    e.target.value = ''
  }

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

      {/* Document Upload */}
      <div className="p-4 border-b border-slate-100">
        <div className="flex items-center gap-2 mb-3">
          <Upload size={14} className="text-blue-600" />
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Upload Document
          </span>
        </div>

        {/* Fiscal Quarter Input */}
        <input
          type        = "text"
          placeholder = "Fiscal quarter (e.g. Q3-2023)"
          value       = {fiscalQuarter}
          onChange    = {e => setFiscalQuarter(e.target.value)}
          className   = "w-full text-xs border border-slate-200 rounded-lg px-3 py-2 mb-2 outline-none focus:border-blue-400 text-slate-600 placeholder-slate-300"
        />

        {/* Extract Graphs Toggle */}
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs text-slate-500">
            Extract graphs (slower)
          </span>
          <button
            onClick   = {() => setExtractGraphs(!extractGraphs)}
            className = {`w-10 h-5 rounded-full transition-colors relative ${
              extractGraphs ? 'bg-blue-600' : 'bg-slate-200'
            }`}
          >
            <div className={`w-4 h-4 bg-white rounded-full absolute top-0.5 transition-all shadow-sm ${
              extractGraphs ? 'left-5' : 'left-0.5'
            }`} />
          </button>
        </div>

        {/* Drop Zone */}
        <div
          onDrop      = {handleDrop}
          onDragOver  = {handleDragOver}
          onDragLeave = {handleDragLeave}
          onClick     = {() => !uploading && fileInputRef.current?.click()}
          className   = {`border-2 border-dashed rounded-xl p-4 text-center cursor-pointer transition-all ${
            dragOver
              ? 'border-blue-400 bg-blue-50'
              : uploading
              ? 'border-slate-200 bg-slate-50 cursor-not-allowed'
              : 'border-slate-200 hover:border-blue-300 hover:bg-blue-50'
          }`}
        >
          {uploading ? (
            <div>
              <Loader2
                size={20}
                className="text-blue-600 animate-spin mx-auto mb-2"
              />
              <p className="text-xs text-blue-600 font-medium mb-2">
                Processing PDF...
              </p>
              {/* Progress Bar */}
              <div className="w-full bg-slate-200 rounded-full h-1.5">
                <div
                  className="bg-blue-600 h-1.5 rounded-full transition-all"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
              <p className="text-xs text-slate-400 mt-1">
                {uploadProgress}% uploaded
              </p>
            </div>
          ) : (
            <div>
              <Upload
                size={20}
                className="text-slate-300 mx-auto mb-2"
              />
              <p className="text-xs text-slate-500 font-medium">
                Drop PDF here
              </p>
              <p className="text-xs text-slate-300 mt-0.5">
                or click to browse
              </p>
            </div>
          )}
        </div>

        {/* Hidden file input */}
        <input
          ref      = {fileInputRef}
          type     = "file"
          accept   = ".pdf"
          onChange = {handleFileSelect}
          className= "hidden"
        />

        {/* Upload Status */}
        {uploadStatus && (
          <div className={`flex items-start gap-2 mt-2 p-2 rounded-lg text-xs ${
            uploadStatus === 'success'
              ? 'bg-green-50 text-green-700 border border-green-200'
              : 'bg-red-50 text-red-700 border border-red-200'
          }`}>
            {uploadStatus === 'success'
              ? <CheckCircle size={12} className="flex-shrink-0 mt-0.5" />
              : <AlertCircle size={12} className="flex-shrink-0 mt-0.5" />
            }
            {uploadMessage}
          </div>
        )}
      </div>

      {/* Documents List */}
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
            No documents ingested yet
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