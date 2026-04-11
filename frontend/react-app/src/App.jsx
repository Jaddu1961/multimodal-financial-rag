import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import Navbar from './components/Navbar'
import './App.css'

function App() {
  const [sidebarOpen,      setSidebarOpen]      = useState(true)
  const [selectedQuestion, setSelectedQuestion] = useState(null)

  const handleQuestionSelect = (q) => {
    setSelectedQuestion(q)
    setTimeout(() => setSelectedQuestion(null), 100)
  }

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">

      {/* Sidebar */}
      <Sidebar
        isOpen           = {sidebarOpen}
        onQuestionSelect = {handleQuestionSelect}
      />

      {/* Main Content */}
      <div className="flex flex-col flex-1 overflow-hidden">
        <Navbar onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
        <ChatArea selectedQuestion={selectedQuestion} />
      </div>

    </div>
  )
}

export default App