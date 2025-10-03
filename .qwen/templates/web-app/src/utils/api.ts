// Qwen-optimized: API utility functions with advanced error handling and retry logic

import type { ApiResponse, AppError } from '@types'

// Qwen-optimized: Configurable API client with retry mechanism
class ApiClient {
  private baseURL: string
  private defaultHeaders: Record<string, string>
  private retryAttempts: number = 3
  private retryDelay: number = 1000

  constructor(baseURL: string = '/api') {
    this.baseURL = baseURL
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'X-Client-Version': '1.0.0',
      'X-Timestamp': new Date().toISOString()
    }
  }

  private async sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  private async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`
    const headers = {
      ...this.defaultHeaders,
      ...options.headers
    }

    let lastError: Error | null = null

    for (let attempt = 0; attempt <= this.retryAttempts; attempt++) {
      try {
        const response = await fetch(url, {
          ...options,
          headers
        })

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }

        const data = await response.json()
        return {
          success: true,
          data,
          timestamp: new Date().toISOString()
        }
      } catch (error) {
        lastError = error as Error

        // Don't retry on client errors (4xx)
        if (error instanceof Error && error.message.includes('HTTP 4')) {
          break
        }

        if (attempt < this.retryAttempts) {
          await this.sleep(this.retryDelay * (attempt + 1))
        }
      }
    }

    return {
      success: false,
      error: lastError?.message || 'Unknown error occurred',
      timestamp: new Date().toISOString()
    }
  }

  async get<T>(endpoint: string, params?: Record<string, string>): Promise<ApiResponse<T>> {
    const searchParams = params ? new URLSearchParams(params).toString() : ''
    const url = searchParams ? `${endpoint}?${searchParams}` : endpoint

    return this.makeRequest<T>(url, { method: 'GET' })
  }

  async post<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.makeRequest<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  async put<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.makeRequest<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.makeRequest<T>(endpoint, { method: 'DELETE' })
  }
}

// Qwen-optimized: Singleton API client instance
export const apiClient = new ApiClient()

// Qwen-optimized: Specialized API functions for common operations
export const api = {
  // AI-related API calls
  ai: {
    async sendMessage(content: string, config?: any) {
      return apiClient.post('/ai/chat', { content, config })
    },

    async getModels() {
      return apiClient.get('/ai/models')
    },

    async validateApiKey(key: string) {
      return apiClient.post('/ai/validate-key', { key })
    }
  },

  // Project management
  projects: {
    async getAll() {
      return apiClient.get('/projects')
    },

    async getById(id: string) {
      return apiClient.get(`/projects/${id}`)
    },

    async create(project: any) {
      return apiClient.post('/projects', project)
    },

    async update(id: string, project: any) {
      return apiClient.put(`/projects/${id}`, project)
    },

    async delete(id: string) {
      return apiClient.delete(`/projects/${id}`)
    }
  },

  // Settings management
  settings: {
    async get() {
      return apiClient.get('/settings')
    },

    async update(settings: any) {
      return apiClient.put('/settings', settings)
    },

    async export() {
      return apiClient.get('/settings/export')
    },

    async import(settings: any) {
      return apiClient.post('/settings/import', settings)
    }
  }
}

// Qwen-optimized: Error handling utility
export const handleApiError = (error: unknown): AppError => {
  if (error instanceof Error) {
    return {
      code: 'API_ERROR',
      message: error.message,
      details: error,
      stack: error.stack,
      timestamp: new Date()
    }
  }

  return {
    code: 'UNKNOWN_ERROR',
    message: 'An unknown error occurred',
    details: error,
    timestamp: new Date()
  }
}

// Qwen-optimized: Request deduplication utility
const pendingRequests = new Map<string, Promise<any>>()

export const dedupeRequest = async <T>(
  key: string,
  requestFn: () => Promise<T>
): Promise<T> => {
  if (pendingRequests.has(key)) {
    return pendingRequests.get(key)!
  }

  const promise = requestFn().finally(() => {
    pendingRequests.delete(key)
  })

  pendingRequests.set(key, promise)
  return promise
}