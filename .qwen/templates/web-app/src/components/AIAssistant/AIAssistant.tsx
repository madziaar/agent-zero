import React, { useState, useRef, useEffect } from 'react'
import styled from 'styled-components'

// Qwen-optimized: TypeScript interfaces for AI interaction
interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  isStreaming?: boolean
}

interface AIConfig {
  model: string
  temperature: number
  maxTokens: number
  systemPrompt: string
}

// Qwen-optimized: Custom hook for AI chat functionality
const useAIAssistant = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your Qwen AI assistant. How can I help you with your development tasks today?',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [config] = useState<AIConfig>({
    model: 'qwen-turbo',
    temperature: 0.7,
    maxTokens: 2048,
    systemPrompt: 'You are a helpful AI assistant specialized in coding and development tasks.'
  })

  // Qwen-optimized: Auto-scroll to bottom when new messages arrive
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Qwen-optimized: Simulate AI response (replace with actual API call)
  const sendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    // Simulate streaming response
    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: '',
      timestamp: new Date(),
      isStreaming: true
    }

    setMessages(prev => [...prev, assistantMessage])

    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Simulate streaming response (replace with actual streaming API)
      const mockResponse = `Thank you for your question: "${content}". This is a simulated response from Qwen AI. In a real implementation, this would be connected to the Qwen API with proper streaming support for real-time responses.`

      let streamedContent = ''
      const words = mockResponse.split(' ')

      for (let i = 0; i < words.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 50))
        streamedContent += words[i] + ' '

        setMessages(prev => prev.map(msg =>
          msg.id === assistantMessage.id
            ? { ...msg, content: streamedContent }
            : msg
        ))
      }

      // Mark as completed
      setMessages(prev => prev.map(msg =>
        msg.id === assistantMessage.id
          ? { ...msg, isStreaming: false }
          : msg
      ))

    } catch (error) {
      console.error('AI request failed:', error)
      setMessages(prev => prev.map(msg =>
        msg.id === assistantMessage.id
          ? { ...msg, content: 'Sorry, I encountered an error. Please try again.', isStreaming: false }
          : msg
      ))
    } finally {
      setIsLoading(false)
    }
  }

  return {
    messages,
    input,
    setInput,
    isLoading,
    sendMessage,
    config
  }
}

// Qwen-optimized: Styled components with AI-themed design
const AssistantContainer = styled.div`
  color: white;
  height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
`

const ChatHeader = styled.div`
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
`

const ChatTitle = styled.h2`
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
`

const ChatSubtitle = styled.p`
  opacity: 0.7;
  font-size: 0.9rem;
`

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  margin-bottom: 2rem;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
  }
`

const MessageBubble = styled.div<{ role: 'user' | 'assistant' }>`
  margin-bottom: 1.5rem;
  padding: 1rem 1.5rem;
  border-radius: 18px;
  max-width: 80%;
  word-wrap: break-word;

  ${props => props.role === 'user' ? `
    background: linear-gradient(135deg, #667eea, #764ba2);
    margin-left: auto;
    border-bottom-right-radius: 4px;
  ` : `
    background: rgba(255, 255, 255, 0.1);
    border-bottom-left-radius: 4px;
  `}
`

const MessageContent = styled.div`
  line-height: 1.6;
`

const MessageTimestamp = styled.div`
  font-size: 0.8rem;
  opacity: 0.6;
  margin-top: 0.5rem;
`

const InputContainer = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
`

const MessageInput = styled.input`
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 1rem;
  outline: none;

  &::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }

  &:focus {
    background: rgba(255, 255, 255, 0.15);
  }
`

const SendButton = styled.button<{ disabled: boolean }>`
  padding: 1rem 2rem;
  border: none;
  border-radius: 25px;
  background: ${props => props.disabled ? 'rgba(255, 255, 255, 0.3)' : 'linear-gradient(135deg, #667eea, #764ba2)'};
  color: white;
  font-weight: 600;
  cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }
`

const TypingIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  opacity: 0.7;
  font-style: italic;

  &::after {
    content: '';
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`

const AIAssistant: React.FC = () => {
  const { messages, input, setInput, isLoading, sendMessage, config } = useAIAssistant()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(input)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(input)
    }
  }

  return (
    <AssistantContainer>
      <ChatHeader>
        <ChatTitle>🤖 Qwen AI Assistant</ChatTitle>
        <ChatSubtitle>
          Model: {config.model} | Temperature: {config.temperature} | Max Tokens: {config.maxTokens}
        </ChatSubtitle>
      </ChatHeader>

      <MessagesContainer>
        {messages.map(message => (
          <MessageBubble key={message.id} role={message.role}>
            <MessageContent>
              {message.content}
              {message.isStreaming && <TypingIndicator />}
            </MessageContent>
            <MessageTimestamp>
              {message.timestamp.toLocaleTimeString()}
            </MessageTimestamp>
          </MessageBubble>
        ))}
        <div ref={messagesEndRef} />
      </MessagesContainer>

      <InputContainer>
        <MessageInput
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about your code or development tasks..."
          disabled={isLoading}
        />
        <SendButton
          onClick={handleSubmit}
          disabled={isLoading || !input.trim()}
        >
          {isLoading ? 'Thinking...' : 'Send'}
        </SendButton>
      </InputContainer>
    </AssistantContainer>
  )
}

export default AIAssistant