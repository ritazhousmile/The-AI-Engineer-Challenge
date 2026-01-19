'use client'

import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

// Message type definition for type safety
interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export default function Home() {
  // Get API URL from environment variable or default to localhost
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  
  // State management for chat functionality
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [conversationId, setConversationId] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Handle sending messages to the backend with streaming
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!inputMessage.trim()) return

    // Add user message to chat
    const userMessage: Message = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    const currentMessage = inputMessage
    setInputMessage('')
    setIsLoading(true)
    setError(null)

    // Create a placeholder for the assistant's streaming response
    const assistantMessageIndex = messages.length + 1
    const assistantMessage: Message = {
      role: 'assistant',
      content: '',
      timestamp: new Date()
    }
    setMessages(prev => [...prev, assistantMessage])

    try {
      // Call the FastAPI backend with streaming
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: currentMessage,
          conversation_id: conversationId || undefined
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get response from server')
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      let accumulatedContent = ''

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          // Decode the chunk
          const chunk = decoder.decode(value, { stream: true })
          
          // Parse Server-Sent Events format
          const lines = chunk.split('\n')
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6))
                
                if (data.error) {
                  setError(data.error)
                  break
                }
                
                if (data.content) {
                  accumulatedContent += data.content
                  // Update the message in real-time
                  setMessages(prev => {
                    const newMessages = [...prev]
                    newMessages[assistantMessageIndex] = {
                      ...newMessages[assistantMessageIndex],
                      content: accumulatedContent
                    }
                    return newMessages
                  })
                }
                
                // Store conversation ID if provided
                if (data.conversation_id && !conversationId) {
                  setConversationId(data.conversation_id)
                }
                
                if (data.done) {
                  // Ensure conversation ID is set
                  if (data.conversation_id) {
                    setConversationId(data.conversation_id)
                  }
                  break
                }
              } catch (e) {
                // Skip invalid JSON
                console.warn('Failed to parse chunk:', e)
              }
            }
          }
        }
      }
    } catch (err) {
      console.error('Error sending message:', err)
      setError(`Failed to get a response. Make sure the backend is running on ${API_URL}`)
      // Remove the empty assistant message on error
      setMessages(prev => prev.slice(0, -1))
    } finally {
      setIsLoading(false)
    }
  }

  // Handle clearing the chat
  const handleClearChat = () => {
    setMessages([])
    setError(null)
    setConversationId(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 dark:from-gray-900 dark:via-purple-900 dark:to-blue-900">
      {/* Header */}
      <header className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md shadow-lg border-b border-purple-100 dark:border-purple-800">
        <div className="max-w-5xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-2xl">🧠</span>
              </div>
              <div>
                <h1 className="text-3xl font-bold gradient-text">Mental Coach AI</h1>
                <p className="text-sm text-gray-600 dark:text-gray-300">Your supportive guide</p>
              </div>
            </div>
            {messages.length > 0 && (
              <button
                onClick={handleClearChat}
                className="px-4 py-2 text-sm font-medium text-purple-600 hover:text-purple-700 dark:text-purple-400 dark:hover:text-purple-300 hover:bg-purple-50 dark:hover:bg-purple-900/30 rounded-lg transition-all duration-200"
              >
                Clear Chat
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Chat Container */}
      <main className="max-w-5xl mx-auto px-4 py-8">
        <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl rounded-3xl shadow-2xl border border-purple-100 dark:border-purple-800 overflow-hidden">
          
          {/* Messages Container */}
          <div className="h-[600px] overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              // Welcome Screen
              <div className="h-full flex flex-col items-center justify-center text-center space-y-6 animate-fade-in">
                <div className="w-24 h-24 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full flex items-center justify-center shadow-2xl animate-pulse-soft">
                  <span className="text-5xl">🌟</span>
                </div>
                <div className="space-y-2">
                  <h2 className="text-3xl font-bold text-gray-800 dark:text-white">
                    Welcome to Your Mental Coach
                  </h2>
                  <p className="text-gray-600 dark:text-gray-300 max-w-md">
                    I'm here to support you on your journey. Share what's on your mind, and let's work through it together.
                  </p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl">
                  {[
                    "I'm feeling overwhelmed today",
                    "I need help staying motivated",
                    "I want to build better habits",
                    "I'm struggling with anxiety"
                  ].map((suggestion, idx) => (
                    <button
                      key={idx}
                      onClick={() => setInputMessage(suggestion)}
                      className="px-4 py-3 bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-900/30 dark:to-pink-900/30 hover:from-purple-200 hover:to-pink-200 dark:hover:from-purple-800/40 dark:hover:to-pink-800/40 rounded-xl text-sm text-gray-700 dark:text-gray-200 transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-1"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              // Messages Display
              <>
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-slide-up message-enter`}
                  >
                    <div className={`flex items-start space-x-3 max-w-[80%] ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                      {/* Avatar */}
                      <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg ${
                        message.role === 'user' 
                          ? 'bg-gradient-to-br from-blue-500 to-cyan-500' 
                          : 'bg-gradient-to-br from-purple-500 to-pink-500'
                      }`}>
                        <span className="text-lg">
                          {message.role === 'user' ? '👤' : '🧠'}
                        </span>
                      </div>
                      
                      {/* Message Bubble */}
                      <div className={`rounded-2xl px-5 py-3 shadow-lg ${
                        message.role === 'user'
                          ? 'bg-gradient-to-br from-blue-500 to-cyan-500 text-white'
                          : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-white border border-gray-200 dark:border-gray-600'
                      }`}>
                        <div className="text-sm leading-relaxed">
                          {message.role === 'user' ? (
                            <p className="whitespace-pre-wrap">{message.content}</p>
                          ) : (
                            <div className="markdown-content">
                              <ReactMarkdown
                                remarkPlugins={[remarkGfm]}
                                components={{
                                  // Custom styling for markdown elements
                                  p: ({node, ...props}) => <p className="mb-3 last:mb-0" {...props} />,
                                  strong: ({node, ...props}) => <strong className="font-bold text-purple-600 dark:text-purple-400" {...props} />,
                                  em: ({node, ...props}) => <em className="italic" {...props} />,
                                  ul: ({node, ...props}) => <ul className="list-disc list-inside mb-3 space-y-1" {...props} />,
                                  ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-3 space-y-1" {...props} />,
                                  li: ({node, ...props}) => <li className="ml-2" {...props} />,
                                  h1: ({node, ...props}) => <h1 className="text-xl font-bold mb-2 mt-4 first:mt-0" {...props} />,
                                  h2: ({node, ...props}) => <h2 className="text-lg font-bold mb-2 mt-3 first:mt-0" {...props} />,
                                  h3: ({node, ...props}) => <h3 className="text-base font-bold mb-2 mt-2 first:mt-0" {...props} />,
                                  code: ({node, inline, ...props}: any) => 
                                    inline ? (
                                      <code className="bg-gray-100 dark:bg-gray-800 px-1.5 py-0.5 rounded text-sm font-mono" {...props} />
                                    ) : (
                                      <code className="block bg-gray-100 dark:bg-gray-800 p-3 rounded-lg text-sm font-mono overflow-x-auto my-2" {...props} />
                                    ),
                                  blockquote: ({node, ...props}) => (
                                    <blockquote className="border-l-4 border-purple-400 pl-4 italic my-3 text-gray-600 dark:text-gray-300" {...props} />
                                  ),
                                  a: ({node, ...props}) => (
                                    <a className="text-blue-500 hover:text-blue-600 underline" target="_blank" rel="noopener noreferrer" {...props} />
                                  ),
                                }}
                              >
                                {message.content || ''}
                              </ReactMarkdown>
                            </div>
                          )}
                        </div>
                        <span className={`text-xs mt-2 block ${
                          message.role === 'user' 
                            ? 'text-blue-100' 
                            : 'text-gray-500 dark:text-gray-400'
                        }`}>
                          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
                
                {/* Loading Indicator */}
                {isLoading && (
                  <div className="flex justify-start animate-slide-up">
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
                        <span className="text-lg">🧠</span>
                      </div>
                      <div className="bg-white dark:bg-gray-700 rounded-2xl px-5 py-3 shadow-lg border border-gray-200 dark:border-gray-600">
                        <div className="flex space-x-2">
                          <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                          <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                          <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Error Display */}
          {error && (
            <div className="px-6 py-3 bg-red-50 dark:bg-red-900/30 border-t border-red-200 dark:border-red-800">
              <p className="text-sm text-red-600 dark:text-red-400">
                ⚠️ {error}
              </p>
            </div>
          )}

          {/* Input Form */}
          <form onSubmit={handleSendMessage} className="p-6 bg-gray-50 dark:bg-gray-900/50 border-t border-purple-100 dark:border-purple-800">
            <div className="flex space-x-3">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Share what's on your mind..."
                disabled={isLoading}
                className="flex-1 px-5 py-4 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-2xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed text-gray-800 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 shadow-sm transition-all duration-200"
              />
              <button
                type="submit"
                disabled={isLoading || !inputMessage.trim()}
                className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-medium rounded-2xl shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 active:scale-95"
              >
                {isLoading ? (
                  <span className="flex items-center space-x-2">
                    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                  </span>
                ) : (
                  <span className="flex items-center space-x-2">
                    <span>Send</span>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  </span>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Footer */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            💜 Built with Next.js and FastAPI • Powered by OpenAI
          </p>
        </div>
      </main>
    </div>
  )
}

