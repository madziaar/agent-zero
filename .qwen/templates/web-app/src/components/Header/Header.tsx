import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import styled from 'styled-components'

// Qwen-optimized: Styled components with AI-themed design
const HeaderContainer = styled.header`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;

  @media (max-width: 768px) {
    padding: 1rem;
  }
`

const Logo = styled(Link)`
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &::before {
    content: '🚀';
    font-size: 1.2rem;
  }
`

const Navigation = styled.nav`
  display: flex;
  gap: 2rem;
  align-items: center;

  @media (max-width: 768px) {
    gap: 1rem;
  }
`

const NavLink = styled(Link)<{ active: string }>`
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-weight: 500;

  background: ${props => props.active === 'true' ? 'rgba(255, 255, 255, 0.2)' : 'transparent'};

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
  }

  @media (max-width: 768px) {
    padding: 0.5rem;
    font-size: 0.9rem;
  }
`

const StatusIndicator = styled.div<{ status: 'online' | 'offline' | 'loading' }>`
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: ${props => {
    switch (props.status) {
      case 'online': return '#4ade80'
      case 'loading': return '#fbbf24'
      case 'offline': return '#ef4444'
    }
  }};
  animation: ${props => props.status === 'loading' ? 'pulse 2s infinite' : 'none'};

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
`

const Header: React.FC = () => {
  const location = useLocation()

  return (
    <HeaderContainer>
      <Logo to="/">
        Qwen Web App
      </Logo>

      <Navigation>
        <NavLink to="/" active={location.pathname === '/' ? 'true' : 'false'}>
          Dashboard
        </NavLink>
        <NavLink to="/assistant" active={location.pathname === '/assistant' ? 'true' : 'false'}>
          AI Assistant
        </NavLink>
        <NavLink to="/settings" active={location.pathname === '/settings' ? 'true' : 'false'}>
          Settings
        </NavLink>
        <StatusIndicator status="online" />
      </Navigation>
    </HeaderContainer>
  )
}

export default Header