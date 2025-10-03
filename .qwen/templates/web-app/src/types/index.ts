// Qwen-optimized: Centralized TypeScript type definitions

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
  timestamp: string
}

// AI Model Types
export interface AIModel {
  id: string
  name: string
  provider: 'qwen' | 'openai' | 'anthropic'
  contextLength: number
  maxTokens: number
  supportsStreaming: boolean
  capabilities: string[]
}

export interface AIConfig {
  model: string
  temperature: number
  maxTokens: number
  topP?: number
  frequencyPenalty?: number
  presencePenalty?: number
  systemPrompt?: string
}

// Chat Types
export interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
  metadata?: {
    model?: string
    tokens?: number
    processingTime?: number
    [key: string]: any
  }
}

export interface ChatSession {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
  updatedAt: Date
  config: AIConfig
}

// Project Types
export interface Project {
  id: string
  name: string
  description: string
  status: 'active' | 'completed' | 'paused' | 'archived'
  progress: number
  priority: 'low' | 'medium' | 'high'
  tags: string[]
  createdAt: Date
  updatedAt: Date
  dueDate?: Date
  assignee?: string
}

// Dashboard Types
export interface DashboardStats {
  totalProjects: number
  activeProjects: number
  completedTasks: number
  aiInteractions: number
  avgResponseTime: number
  successRate: number
}

export interface ActivityItem {
  id: string
  type: 'project_created' | 'task_completed' | 'ai_interaction' | 'system_update'
  title: string
  description: string
  timestamp: Date
  metadata?: Record<string, any>
}

// Settings Types
export interface AppSettings {
  theme: 'light' | 'dark' | 'auto'
  language: string
  timezone: string
  dateFormat: string
  notifications: {
    enabled: boolean
    sound: boolean
    desktop: boolean
    email: boolean
  }
  ai: {
    defaultModel: string
    defaultConfig: AIConfig
    apiKeys: Record<string, string>
  }
  privacy: {
    analytics: boolean
    crashReporting: boolean
    dataCollection: boolean
  }
}

// Component Props Types
export interface BaseComponentProps {
  className?: string
  children?: React.ReactNode
  testId?: string
}

// Error Types
export interface AppError {
  code: string
  message: string
  details?: any
  stack?: string
  timestamp: Date
}

// Utility Types
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}

export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>

export type RequireAtLeastOne<T> = {
  [K in keyof T]-?: Required<Pick<T, K>> & Partial<Omit<T, K>>
}[keyof T]

// Event Types
export interface CustomEvent<T = any> {
  type: string
  payload: T
  timestamp: Date
}

// Theme Types
export interface ThemeColors {
  primary: string
  secondary: string
  background: string
  surface: string
  text: string
  textSecondary: string
  border: string
  success: string
  warning: string
  error: string
  info: string
}

export interface Theme {
  name: string
  colors: ThemeColors
  spacing: Record<string, string>
  typography: {
    fontFamily: string
    fontSize: Record<string, string>
    fontWeight: Record<string, number>
    lineHeight: Record<string, number>
  }
  breakpoints: Record<string, string>
  borderRadius: Record<string, string>
  shadows: Record<string, string>
}

// API Endpoint Types
export interface ApiEndpoint {
  path: string
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  description: string
  parameters?: Record<string, any>
  responseType?: string
}

// Hook Return Types
export interface UseApiReturn<T> {
  data: T | null
  loading: boolean
  error: string | null
  refetch: () => Promise<void>
}

export interface UseLocalStorageReturn<T> {
  value: T
  setValue: (value: T) => void
  removeValue: () => void
}

// Form Types
export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'textarea' | 'checkbox'
  required?: boolean
  placeholder?: string
  options?: Array<{ label: string; value: string }>
  validation?: {
    min?: number
    max?: number
    pattern?: string
    custom?: (value: any) => string | null
  }
}

export interface FormConfig {
  fields: FormField[]
  submitLabel?: string
  onSubmit: (data: Record<string, any>) => Promise<void>
}

// Animation Types
export interface AnimationConfig {
  duration: number
  easing: string
  delay?: number
  direction?: 'normal' | 'reverse' | 'alternate'
  iterations?: number
}

// Performance Types
export interface PerformanceMetrics {
  renderTime: number
  memoryUsage: number
  apiLatency: number
  userInteractionTime: number
}

// Accessibility Types
export interface A11yProps {
  'aria-label'?: string
  'aria-labelledby'?: string
  'aria-describedby'?: string
  'aria-expanded'?: boolean
  'aria-selected'?: boolean
  role?: string
  tabIndex?: number
}

// Export commonly used React types
export type ReactFC<T = {}> = React.FC<T & BaseComponentProps>
export type ReactComponent<T = {}> = React.ComponentType<T & BaseComponentProps>