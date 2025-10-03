import React, { useState, useEffect } from 'react'
import styled from 'styled-components'

// Qwen-optimized: TypeScript interfaces for better type safety
interface DashboardStats {
  totalProjects: number
  activeTasks: number
  completedTasks: number
  aiInteractions: number
}

interface Project {
  id: string
  name: string
  description: string
  status: 'active' | 'completed' | 'paused'
  progress: number
  lastUpdated: Date
}

// Qwen-optimized: Custom hooks for data management
const useDashboardData = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalProjects: 0,
    activeTasks: 0,
    completedTasks: 0,
    aiInteractions: 0
  })

  const [projects, setProjects] = useState<Project[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Qwen-optimized: Simulate API call with proper error handling
    const fetchData = async () => {
      try {
        // Simulate network delay for realistic UX
        await new Promise(resolve => setTimeout(resolve, 1000))

        // Mock data - replace with actual API calls
        setStats({
          totalProjects: 12,
          activeTasks: 8,
          completedTasks: 24,
          aiInteractions: 156
        })

        setProjects([
          {
            id: '1',
            name: 'Qwen Integration',
            description: 'Implement AI assistant integration',
            status: 'active',
            progress: 75,
            lastUpdated: new Date('2024-01-15')
          },
          {
            id: '2',
            name: 'Dashboard Redesign',
            description: 'Modernize dashboard UI/UX',
            status: 'active',
            progress: 45,
            lastUpdated: new Date('2024-01-14')
          },
          {
            id: '3',
            name: 'API Optimization',
            description: 'Improve API response times',
            status: 'completed',
            progress: 100,
            lastUpdated: new Date('2024-01-13')
          }
        ])
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error)
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [])

  return { stats, projects, isLoading }
}

// Qwen-optimized: Styled components with responsive design
const DashboardContainer = styled.div`
  color: white;
`

const WelcomeSection = styled.section`
  text-align: center;
  margin-bottom: 3rem;
`

const Title = styled.h1`
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #fff 0%, #a8edea 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;

  @media (max-width: 768px) {
    font-size: 2rem;
  }
`

const Subtitle = styled.p`
  font-size: 1.2rem;
  opacity: 0.8;
  margin-bottom: 2rem;
`

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
`

const StatCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-4px);
  }
`

const StatValue = styled.div`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
`

const StatLabel = styled.div`
  font-size: 0.9rem;
  opacity: 0.7;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`

const ProjectsSection = styled.section`
  margin-top: 3rem;
`

const ProjectsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`

const ProjectCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
`

const ProjectName = styled.h3`
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
`

const ProjectDescription = styled.p`
  opacity: 0.8;
  margin-bottom: 1.5rem;
  line-height: 1.5;
`

const ProgressBar = styled.div<{ progress: number }>`
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1rem;
`

const ProgressFill = styled.div<{ progress: number }>`
  height: 100%;
  width: ${props => props.progress}%;
  background: linear-gradient(90deg, #4ade80, #06b6d4);
  border-radius: 4px;
  transition: width 0.3s ease;
`

const ProjectMeta = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  opacity: 0.7;
`

const StatusBadge = styled.span<{ status: string }>`
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
  background: ${props => {
    switch (props.status) {
      case 'active': return 'rgba(74, 222, 128, 0.2)'
      case 'completed': return 'rgba(34, 197, 94, 0.2)'
      case 'paused': return 'rgba(251, 191, 36, 0.2)'
    }
  }};
  color: ${props => {
    switch (props.status) {
      case 'active': return '#4ade80'
      case 'completed': return '#22c55e'
      case 'paused': return '#fbbf24'
    }
  }};
`

const LoadingSpinner = styled.div`
  text-align: center;
  padding: 4rem;

  &::after {
    content: '';
    width: 40px;
    height: 40px;
    border: 4px solid rgba(255, 255, 255, 0.3);
    border-top: 4px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    display: inline-block;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`

const Dashboard: React.FC = () => {
  const { stats, projects, isLoading } = useDashboardData()

  if (isLoading) {
    return (
      <DashboardContainer>
        <LoadingSpinner />
      </DashboardContainer>
    )
  }

  return (
    <DashboardContainer>
      <WelcomeSection>
        <Title>Welcome to Qwen Web App</Title>
        <Subtitle>Your AI-powered development dashboard</Subtitle>
      </WelcomeSection>

      <StatsGrid>
        <StatCard>
          <StatValue>{stats.totalProjects}</StatValue>
          <StatLabel>Total Projects</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue>{stats.activeTasks}</StatValue>
          <StatLabel>Active Tasks</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue>{stats.completedTasks}</StatValue>
          <StatLabel>Completed Tasks</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue>{stats.aiInteractions}</StatValue>
          <StatLabel>AI Interactions</StatLabel>
        </StatCard>
      </StatsGrid>

      <ProjectsSection>
        <h2 style={{ fontSize: '2rem', marginBottom: '2rem', fontWeight: '600' }}>
          Recent Projects
        </h2>
        <ProjectsGrid>
          {projects.map(project => (
            <ProjectCard key={project.id}>
              <ProjectName>{project.name}</ProjectName>
              <ProjectDescription>{project.description}</ProjectDescription>
              <ProgressBar progress={project.progress}>
                <ProgressFill progress={project.progress} />
              </ProgressBar>
              <ProjectMeta>
                <span>{project.progress}% Complete</span>
                <StatusBadge status={project.status}>{project.status}</StatusBadge>
              </ProjectMeta>
            </ProjectCard>
          ))}
        </ProjectsGrid>
      </ProjectsSection>
    </DashboardContainer>
  )
}

export default Dashboard