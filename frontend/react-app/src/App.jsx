import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import Navbar from './components/Navbar'
import './App.css'

// --- Generate unique chat ID ---
const generateId = () => `chat_${Date.now()}`

function App() {
  const [sidebarOpen,      setSidebarOpen]      = useState(true)
  const [selectedQuestion, setSelectedQuestion] = useState(null)
  const [currentChatId,    setCurrentChatId]    = useState(() => {
    // Load last chat ID or create new one
    return localStorage.getItem('current_chat_id') || generateId()
  })
  const [chatHistory, setChatHistory] = useState(() => {
    // Load chat history from localStorage
    const saved = localStorage.getItem('chat_history')
    return saved ? JSON.parse(saved) : {}
  })

  // Save current chat ID to localStorage
  useEffect(() => {
    localStorage.setItem('current_chat_id', currentChatId)
  }, [currentChatId])

  // Save chat history to localStorage
  useEffect(() => {
    localStorage.setItem('chat_history', JSON.stringify(chatHistory))
  }, [chatHistory])

  const handleQuestionSelect = (q) => {
    setSelectedQuestion(q)
    setTimeout(() => setSelectedQuestion(null), 100)
  }

  // --- Create new chat ---
  const handleNewChat = () => {
    const newId = generateId()
    setCurrentChatId(newId)
  }

  // --- Switch to existing chat ---
  const handleSelectChat = (chatId) => {
    setCurrentChatId(chatId)
  }

  // --- Delete a chat ---
  const handleDeleteChat = (chatId) => {
    setChatHistory(prev => {
      const updated = { ...prev }
      delete updated[chatId]
      return updated
    })
    if (chatId === currentChatId) {
      handleNewChat()
    }
  }

  // --- Update chat history when messages change ---
  const handleMessagesUpdate = (chatId, messages) => {
    if (messages.length > 1) {
      setChatHistory(prev => ({
        ...prev,
        [chatId]: {
          id:        chatId,
          messages:  messages,
          title:     messages[1]?.content?.slice(0, 40) + '...' || 'New Chat',
          updatedAt: new Date().toLocaleString(),
        }
      }))
    }
  }

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">

      {/* Sidebar */}
      <Sidebar
        isOpen           = {sidebarOpen}
        onQuestionSelect = {handleQuestionSelect}
        chatHistory      = {chatHistory}
        currentChatId    = {currentChatId}
        onNewChat        = {handleNewChat}
        onSelectChat     = {handleSelectChat}
        onDeleteChat     = {handleDeleteChat}
      />

      {/* Main Content */}
      <div className="flex flex-col flex-1 overflow-hidden">
        <Navbar
          onToggleSidebar = {() => setSidebarOpen(!sidebarOpen)}
          onNewChat       = {handleNewChat}
        />
        <ChatArea
          selectedQuestion   = {selectedQuestion}
          currentChatId      = {currentChatId}
          savedMessages      = {chatHistory[currentChatId]?.messages}
          onMessagesUpdate   = {handleMessagesUpdate}
        />
      </div>

    </div>
  )
}

export default App