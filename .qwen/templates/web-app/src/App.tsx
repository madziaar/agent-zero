import React from 'react'
import { Routes, Route } from 'react-router-dom'
import styled from 'styled-components'
import Header from '@components/Header/Header'
import Dashboard from '@components/Dashboard/Dashboard'
import AIAssistant from '@components/AIAssistant/AIAssistant'
import Settings from '@components/Settings/Settings'

// Qwen-optimized: Global styles with AI-optimized color scheme
const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
`

const MainContent = styled.main`
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;

  @media (max-width: 768px) {
    padding: 1rem;
  }
`

const App: React.FC = () => {
  return (
    <AppContainer>
      <Header />
      <MainContent>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/assistant" element={<AIAssistant />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </MainContent>
    </AppContainer>
  )
}

export default App