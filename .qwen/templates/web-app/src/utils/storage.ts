// Qwen-optimized: Local storage utilities with type safety and error handling

import type { AppSettings, ChatSession, Project } from '@types'

// Qwen-optimized: Storage keys with versioning for migration support
const STORAGE_KEYS = {
  SETTINGS: 'qwen-settings-v1',
  SESSIONS: 'qwen-sessions-v1',
  PROJECTS: 'qwen-projects-v1',
  USER_PREFERENCES: 'qwen-preferences-v1',
  CACHE: 'qwen-cache-v1'
} as const

// Qwen-optimized: Generic storage utility with error handling
export const storage = {
  get: <T>(key: string): T | null => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : null
    } catch (error) {
      console.warn(`Failed to get item from storage (${key}):`, error)
      return null
    }
  },

  set: <T>(key: string, value: T): boolean => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
      return true
    } catch (error) {
      console.warn(`Failed to set item in storage (${key}):`, error)
      return false
    }
  },

  remove: (key: string): boolean => {
    try {
      localStorage.removeItem(key)
      return true
    } catch (error) {
      console.warn(`Failed to remove item from storage (${key}):`, error)
      return false
    }
  },

  clear: (): boolean => {
    try {
      localStorage.clear()
      return true
    } catch (error) {
      console.warn('Failed to clear storage:', error)
      return false
    }
  }
}

// Qwen-optimized: Settings management utilities
export const settingsStorage = {
  get: (): AppSettings | null => {
    return storage.get<AppSettings>(STORAGE_KEYS.SETTINGS)
  },

  set: (settings: AppSettings): boolean => {
    return storage.set(STORAGE_KEYS.SETTINGS, settings)
  },

  update: <K extends keyof AppSettings>(key: K, value: AppSettings[K]): boolean => {
    const current = settingsStorage.get()
    if (current) {
      const updated = { ...current, [key]: value }
      return settingsStorage.set(updated)
    }
    return false
  },

  reset: (): boolean => {
    return storage.remove(STORAGE_KEYS.SETTINGS)
  }
}

// Qwen-optimized: Chat sessions management
export const sessionsStorage = {
  getAll: (): ChatSession[] => {
    return storage.get<ChatSession[]>(STORAGE_KEYS.SESSIONS) || []
  },

  getById: (id: string): ChatSession | null => {
    const sessions = sessionsStorage.getAll()
    return sessions.find(session => session.id === id) || null
  },

  save: (session: ChatSession): boolean => {
    const sessions = sessionsStorage.getAll()
    const existingIndex = sessions.findIndex(s => s.id === session.id)

    if (existingIndex >= 0) {
      sessions[existingIndex] = { ...session, updatedAt: new Date() }
    } else {
      sessions.push(session)
    }

    return storage.set(STORAGE_KEYS.SESSIONS, sessions)
  },

  delete: (id: string): boolean => {
    const sessions = sessionsStorage.getAll()
    const filtered = sessions.filter(session => session.id !== id)
    return storage.set(STORAGE_KEYS.SESSIONS, filtered)
  },

  clear: (): boolean => {
    return storage.remove(STORAGE_KEYS.SESSIONS)
  }
}

// Qwen-optimized: Projects management
export const projectsStorage = {
  getAll: (): Project[] => {
    return storage.get<Project[]>(STORAGE_KEYS.PROJECTS) || []
  },

  getById: (id: string): Project | null => {
    const projects = projectsStorage.getAll()
    return projects.find(project => project.id === id) || null
  },

  save: (project: Project): boolean => {
    const projects = projectsStorage.getAll()
    const existingIndex = projects.findIndex(p => p.id === project.id)

    if (existingIndex >= 0) {
      projects[existingIndex] = { ...project, updatedAt: new Date() }
    } else {
      projects.push(project)
    }

    return storage.set(STORAGE_KEYS.PROJECTS, projects)
  },

  delete: (id: string): boolean => {
    const projects = projectsStorage.getAll()
    const filtered = projects.filter(project => project.id !== id)
    return storage.set(STORAGE_KEYS.PROJECTS, filtered)
  },

  getByStatus: (status: Project['status']): Project[] => {
    const projects = projectsStorage.getAll()
    return projects.filter(project => project.status === status)
  },

  getByPriority: (priority: Project['priority']): Project[] => {
    const projects = projectsStorage.getAll()
    return projects.filter(project => project.priority === priority)
  }
}

// Qwen-optimized: Cache management with TTL support
interface CacheItem<T> {
  value: T
  timestamp: number
  ttl: number // Time to live in milliseconds
}

export const cacheStorage = {
  set: <T>(key: string, value: T, ttlMinutes: number = 60): boolean => {
    const item: CacheItem<T> = {
      value,
      timestamp: Date.now(),
      ttl: ttlMinutes * 60 * 1000
    }
    return storage.set(key, item)
  },

  get: <T>(key: string): T | null => {
    const item = storage.get<CacheItem<T>>(key)
    if (!item) return null

    // Check if item has expired
    if (Date.now() - item.timestamp > item.ttl) {
      storage.remove(key)
      return null
    }

    return item.value
  },

  remove: (key: string): boolean => {
    return storage.remove(key)
  },

  clear: (): boolean => {
    return storage.remove(STORAGE_KEYS.CACHE)
  },

  // Clean expired items from cache
  cleanup: (): void => {
    try {
      const keys = Object.keys(localStorage)
      keys.forEach(key => {
        if (key.startsWith('cache_')) {
          const item = storage.get<CacheItem<any>>(key)
          if (item && Date.now() - item.timestamp > item.ttl) {
            storage.remove(key)
          }
        }
      })
    } catch (error) {
      console.warn('Failed to cleanup cache:', error)
    }
  }
}

// Qwen-optimized: Storage quota management
export const storageUtils = {
  getUsage: (): { used: number; available: number; percentage: number } => {
    try {
      let used = 0
      for (const key in localStorage) {
        if (localStorage.hasOwnProperty(key)) {
          used += localStorage.getItem(key)?.length || 0
        }
      }

      // Estimate available space (5MB for most browsers)
      const available = 5 * 1024 * 1024
      const percentage = (used / available) * 100

      return { used, available, percentage }
    } catch (error) {
      console.warn('Failed to get storage usage:', error)
      return { used: 0, available: 0, percentage: 0 }
    }
  },

  isQuotaExceeded: (): boolean => {
    try {
      const testKey = '__test_quota__'
      localStorage.setItem(testKey, 'x'.repeat(1000))
      localStorage.removeItem(testKey)
      return false
    } catch (error) {
      return true
    }
  },

  optimize: (): void => {
    try {
      // Remove expired cache items
      cacheStorage.cleanup()

      // If still over quota, remove oldest sessions
      if (storageUtils.isQuotaExceeded()) {
        const sessions = sessionsStorage.getAll()
        if (sessions.length > 0) {
          // Remove oldest session
          sessions.sort((a, b) => a.updatedAt.getTime() - b.updatedAt.getTime())
          sessionsStorage.delete(sessions[0].id)
        }
      }
    } catch (error) {
      console.warn('Failed to optimize storage:', error)
    }
  }
}

// Qwen-optimized: Data export/import utilities
export const dataBackup = {
  exportAll: (): string => {
    const data = {
      settings: settingsStorage.get(),
      sessions: sessionsStorage.getAll(),
      projects: projectsStorage.getAll(),
      exportedAt: new Date().toISOString(),
      version: '1.0.0'
    }
    return JSON.stringify(data, null, 2)
  },

  importAll: (jsonData: string): { success: boolean; errors?: string[] } => {
    try {
      const data = JSON.parse(jsonData)
      const errors: string[] = []

      // Validate data structure
      if (!data.version || !data.exportedAt) {
        return { success: false, errors: ['Invalid backup file format'] }
      }

      // Import settings
      if (data.settings) {
        if (!settingsStorage.set(data.settings)) {
          errors.push('Failed to import settings')
        }
      }

      // Import sessions
      if (data.sessions && Array.isArray(data.sessions)) {
        data.sessions.forEach((session: ChatSession) => {
          if (!sessionsStorage.save(session)) {
            errors.push(`Failed to import session: ${session.title}`)
          }
        })
      }

      // Import projects
      if (data.projects && Array.isArray(data.projects)) {
        data.projects.forEach((project: Project) => {
          if (!projectsStorage.save(project)) {
            errors.push(`Failed to import project: ${project.name}`)
          }
        })
      }

      return { success: errors.length === 0, errors: errors.length > 0 ? errors : undefined }
    } catch (error) {
      return { success: false, errors: ['Invalid JSON format'] }
    }
  }
}

// Qwen-optimized: Initialize storage cleanup on module load
if (typeof window !== 'undefined') {
  // Clean up expired cache items periodically
  setInterval(() => {
    cacheStorage.cleanup()
  }, 5 * 60 * 1000) // Every 5 minutes
}