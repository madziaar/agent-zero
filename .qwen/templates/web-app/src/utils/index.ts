// Qwen-optimized: Utility functions barrel export

export * from './api'
export * from './storage'

// Qwen-optimized: Common utility functions
export const formatDate = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

export const formatDateTime = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date
  return d.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

export const formatDuration = (ms: number): string => {
  if (ms < 1000) return `${ms}ms`

  const seconds = Math.floor(ms / 1000)
  if (seconds < 60) return `${seconds}s`

  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `${minutes}m`

  const hours = Math.floor(minutes / 60)
  return `${hours}h`
}

// Qwen-optimized: Debounce utility for performance optimization
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: NodeJS.Timeout

  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

// Qwen-optimized: Throttle utility for rate limiting
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  limit: number
): ((...args: Parameters<T>) => void) => {
  let inThrottle: boolean

  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

// Qwen-optimized: Deep clone utility
export const deepClone = <T>(obj: T): T => {
  if (obj === null || typeof obj !== 'object') return obj
  if (obj instanceof Date) return new Date(obj.getTime()) as any
  if (obj instanceof Array) return obj.map(item => deepClone(item)) as any

  const cloned = {} as T
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      cloned[key] = deepClone(obj[key])
    }
  }
  return cloned
}

// Qwen-optimized: Object comparison utility
export const shallowEqual = (obj1: any, obj2: any): boolean => {
  const keys1 = Object.keys(obj1)
  const keys2 = Object.keys(obj2)

  if (keys1.length !== keys2.length) return false

  for (const key of keys1) {
    if (obj1[key] !== obj2[key]) return false
  }

  return true
}

// Qwen-optimized: Array utilities
export const arrayUtils = {
  unique: <T>(array: T[]): T[] => [...new Set(array)],

  groupBy: <T>(array: T[], keyFn: (item: T) => string): Record<string, T[]> => {
    return array.reduce((groups, item) => {
      const key = keyFn(item)
      if (!groups[key]) groups[key] = []
      groups[key].push(item)
      return groups
    }, {} as Record<string, T[]>)
  },

  sortBy: <T>(array: T[], keyFn: (item: T) => any): T[] => {
    return [...array].sort((a, b) => {
      const aVal = keyFn(a)
      const bVal = keyFn(b)
      if (aVal < bVal) return -1
      if (aVal > bVal) return 1
      return 0
    })
  },

  chunk: <T>(array: T[], size: number): T[][] => {
    const chunks: T[][] = []
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size))
    }
    return chunks
  }
}

// Qwen-optimized: String utilities
export const stringUtils = {
  capitalize: (str: string): string => {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
  },

  camelCase: (str: string): string => {
    return str.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase())
  },

  kebabCase: (str: string): string => {
    return str.replace(/([A-Z])/g, '-$1').toLowerCase()
  },

  truncate: (str: string, length: number): string => {
    return str.length > length ? str.slice(0, length) + '...' : str
  },

  slugify: (str: string): string => {
    return str
      .toLowerCase()
      .replace(/[^\w ]+/g, '')
      .replace(/ +/g, '-')
  }
}

// Qwen-optimized: Validation utilities
export const validators = {
  email: (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  },

  url: (url: string): boolean => {
    try {
      new URL(url)
      return true
    } catch {
      return false
    }
  },

  required: (value: any): boolean => {
    if (typeof value === 'string') return value.trim().length > 0
    if (Array.isArray(value)) return value.length > 0
    return value != null
  }
}

// Qwen-optimized: Performance monitoring utilities
export const performanceUtils = {
  measure: <T>(fn: () => T): { result: T; duration: number } => {
    const start = performance.now()
    const result = fn()
    const duration = performance.now() - start
    return { result, duration }
  },

  measureAsync: async <T>(fn: () => Promise<T>): Promise<{ result: T; duration: number }> => {
    const start = performance.now()
    const result = await fn()
    const duration = performance.now() - start
    return { result, duration }
  }
}

// Qwen-optimized: Error handling utilities
export const errorUtils = {
  isError: (value: any): value is Error => {
    return value instanceof Error
  },

  safeExecute: <T>(fn: () => T, fallback?: T): T | undefined => {
    try {
      return fn()
    } catch (error) {
      console.warn('Safe execution failed:', error)
      return fallback
    }
  },

  safeExecuteAsync: async <T>(fn: () => Promise<T>, fallback?: T): Promise<T | undefined> => {
    try {
      return await fn()
    } catch (error) {
      console.warn('Safe async execution failed:', error)
      return fallback
    }
  }
}

// Qwen-optimized: Browser detection utilities
export const browserUtils = {
  isMobile: (): boolean => {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  },

  isIOS: (): boolean => {
    return /iPad|iPhone|iPod/.test(navigator.userAgent)
  },

  isAndroid: (): boolean => {
    return /Android/i.test(navigator.userAgent)
  },

  supportsWebGL: (): boolean => {
    try {
      const canvas = document.createElement('canvas')
      return !!(canvas.getContext('webgl') || canvas.getContext('experimental-webgl'))
    } catch {
      return false
    }
  }
}

// Qwen-optimized: Color manipulation utilities
export const colorUtils = {
  hexToRgb: (hex: string): { r: number; g: number; b: number } | null => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null
  },

  rgbToHex: (r: number, g: number, b: number): string => {
    return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`
  },

  lighten: (hex: string, percent: number): string => {
    const rgb = colorUtils.hexToRgb(hex)
    if (!rgb) return hex

    const lighten = (value: number) => Math.min(255, Math.floor(value + (255 - value) * percent))

    return colorUtils.rgbToHex(
      lighten(rgb.r),
      lighten(rgb.g),
      lighten(rgb.b)
    )
  },

  darken: (hex: string, percent: number): string => {
    const rgb = colorUtils.hexToRgb(hex)
    if (!rgb) return hex

    const darken = (value: number) => Math.max(0, Math.floor(value * (1 - percent)))

    return colorUtils.rgbToHex(
      darken(rgb.r),
      darken(rgb.g),
      darken(rgb.b)
    )
  }
}