import axios from 'axios'

const BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 60000,
})

export const checkHealth = async () => {
  try {
    const res = await api.get('/health')
    return { online: true, data: res.data }
  } catch {
    return { online: false, data: null }
  }
}

export const askQuestion = async (question, nResults = 8, filterType = null) => {
  const res = await api.post('/query/ask', {
    question,
    n_results:   nResults,
    filter_type: filterType,
  })
  return res.data
}

export const getDocuments = async () => {
  const res = await api.get('/documents/list')
  return res.data
}

export const getStats = async () => {
  const res = await api.get('/ingest/stats')
  return res.data
}