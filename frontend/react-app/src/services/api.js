import axios from 'axios'

const BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 300000, // 5 mins for large PDFs
})

// --- Health Check ---
export const checkHealth = async () => {
  try {
    const res = await api.get('/health')
    return { online: true, data: res.data }
  } catch {
    return { online: false, data: null }
  }
}

// --- Ask Question ---
export const askQuestion = async (
  question,
  nResults    = 8,
  filterType  = null
) => {
  const res = await api.post('/query/ask', {
    question,
    n_results:   nResults,
    filter_type: filterType,
  })
  return res.data
}

// --- Get Documents ---
export const getDocuments = async () => {
  const res = await api.get('/documents/list')
  return res.data
}

// --- Get Stats ---
export const getStats = async () => {
  const res = await api.get('/ingest/stats')
  return res.data
}

// --- Upload Document ---
export const uploadDocument = async (
  file,
  fiscalQuarter  = '',
  extractGraphs  = true,
  onProgress     = null,
) => {
  const formData = new FormData()
  formData.append('file', file)

  const params = new URLSearchParams({
    extract_graphs:  extractGraphs,
    skip_duplicates: true,
    ...(fiscalQuarter && { fiscal_quarter: fiscalQuarter }),
  })

  const res = await api.post(
    `/ingest/upload?${params.toString()}`,
    formData,
    {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const pct = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(pct)
        }
      },
      timeout: 600000, // 10 mins for graph extraction
    }
  )
  return res.data
}
// --- Compare Documents ---
export const compareDocuments = async (
  question,
  document1,
  document2,
  nResults = 5,
) => {
  const res = await api.post('/query/compare', {
    question,
    document_1: document1,
    document_2: document2,
    n_results:  nResults,
  })
  return res.data
}

// --- Delete Document ---
export const deleteDocument = async (documentId) => {
  const res = await api.delete(`/ingest/document/${documentId}`)
  return res.data
}