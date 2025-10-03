# Qwen Web App Template

🚀 **A modern, AI-optimized React TypeScript web application template designed for Qwen AI development workflows.**

This template provides a complete, production-ready foundation with Qwen-specific optimizations, modern development practices, and AI-first design patterns.

## ✨ Features

### Core Technologies
- ⚡ **Vite** - Lightning-fast build tool and dev server
- ⚛️ **React 18** - Latest React with concurrent features
- 🔷 **TypeScript** - Full type safety and IntelliSense
- 🎨 **Styled Components** - CSS-in-JS with theming support
- 🛣️ **React Router** - Client-side routing
- 🧪 **Vitest** - Fast unit testing framework

### Qwen-Optimized Features
- 🤖 **AI Assistant Integration** - Built-in chat interface for AI interactions
- 📊 **Smart Dashboard** - Project management with AI insights
- ⚙️ **Advanced Settings** - Comprehensive configuration management
- 🔧 **Type-Safe APIs** - Robust API client with retry logic and error handling
- 💾 **Intelligent Storage** - Local storage with TTL caching and quota management
- 🎯 **Performance Monitoring** - Built-in performance tracking utilities

## 🚀 Quick Start

### Prerequisites
- Node.js 16.0.0 or higher
- npm 8.0.0 or higher (or yarn/pnpm)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd .qwen/templates/web-app
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000` to see your app running!

### Available Scripts

```bash
# Start development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage

# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Type checking
npm run type-check
```

## 📁 Project Structure

```
.qwen/templates/web-app/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/         # React components
│   │   ├── Header/        # Navigation header
│   │   ├── Dashboard/     # Main dashboard
│   │   ├── AIAssistant/   # AI chat interface
│   │   └── Settings/      # Settings management
│   ├── styles/            # Global styles and CSS
│   │   └── index.css      # Main stylesheet
│   ├── types/             # TypeScript definitions
│   │   └── index.ts       # Centralized type definitions
│   ├── utils/             # Utility functions
│   │   ├── api.ts         # API client and utilities
│   │   ├── storage.ts     # Storage management
│   │   └── index.ts       # Utility exports
│   ├── App.tsx            # Main app component
│   └── main.tsx           # Application entry point
├── package.json           # Dependencies and scripts
├── vite.config.ts         # Vite configuration
└── README.md             # This file
```

## 🎨 Qwen-Optimized Patterns

### 1. **AI-First Architecture**
```typescript
// Example: AIAssistant component with streaming support
interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  isStreaming?: boolean
}
```

### 2. **Type-Safe API Layer**
```typescript
// Example: Robust API client with retry logic
class ApiClient {
  private retryAttempts: number = 3
  private retryDelay: number = 1000

  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    // Automatic retry with exponential backoff
  }
}
```

### 3. **Intelligent Storage Management**
```typescript
// Example: TTL-based caching system
interface CacheItem<T> {
  value: T
  timestamp: number
  ttl: number // Time to live in milliseconds
}
```

### 4. **Performance Monitoring**
```typescript
// Example: Built-in performance tracking
export const performanceUtils = {
  measure: <T>(fn: () => T): { result: T; duration: number } => {
    const start = performance.now()
    const result = fn()
    return { result, duration: performance.now() - start }
  }
}
```

## 🧩 Component Architecture

### Header Component
- Responsive navigation with active state tracking
- Glass morphism design with backdrop blur
- Real-time status indicators

### Dashboard Component
- Statistics overview with animated counters
- Project cards with progress visualization
- Responsive grid layout with hover effects

### AI Assistant Component
- Real-time chat interface with streaming simulation
- Message history with timestamps
- Configurable AI model settings
- Responsive input handling

### Settings Component
- Comprehensive configuration management
- Real-time setting updates
- Data export/import functionality
- Form validation and error handling

## 🎯 Development Guidelines

### Code Organization
- **Components**: Feature-based organization in separate directories
- **Types**: Centralized type definitions for consistency
- **Utils**: Reusable utilities with clear separation of concerns
- **Styles**: CSS custom properties for easy theming

### Best Practices
1. **Type Safety**: Use TypeScript interfaces for all data structures
2. **Error Handling**: Implement proper error boundaries and fallbacks
3. **Performance**: Use React.memo, useMemo, and useCallback where appropriate
4. **Accessibility**: Include ARIA labels and keyboard navigation
5. **Responsive Design**: Mobile-first approach with breakpoint management

### Qwen-Specific Patterns

#### 1. **API Integration Pattern**
```typescript
// Use the provided API client for all external requests
import { api } from '@utils/api'

const fetchData = async () => {
  const response = await api.projects.getAll()
  if (response.success) {
    setProjects(response.data)
  }
}
```

#### 2. **Storage Management Pattern**
```typescript
// Use the storage utilities for persistent data
import { settingsStorage } from '@utils/storage'

const saveSettings = (settings: AppSettings) => {
  const success = settingsStorage.set(settings)
  if (success) {
    // Handle success
  }
}
```

#### 3. **Performance Optimization Pattern**
```typescript
// Use performance utilities for monitoring
import { performanceUtils } from '@utils'

const expensiveOperation = () => {
  return performanceUtils.measure(() => {
    // Your expensive operation here
  })
}
```

## 🔧 Customization

### Theming
The template uses CSS custom properties for easy theming:

```css
:root {
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --bg-glass: rgba(255, 255, 255, 0.1);
  --text-primary: #ffffff;
  /* ... more variables */
}
```

### Adding New Components
1. Create a new directory under `src/components/`
2. Include `index.ts` for clean imports
3. Use TypeScript interfaces for props
4. Follow the existing styling patterns

### API Integration
1. Add new API methods to `src/utils/api.ts`
2. Define response types in `src/types/`
3. Handle loading and error states in components

## 🚨 Troubleshooting

### Common Issues

**Build Errors:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**TypeScript Errors:**
```bash
# Run type checking
npm run type-check
```

**Port Already in Use:**
```bash
# Kill process using port 3000
npx kill-port 3000
# Or use different port
npm run dev -- --port 3001
```

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Styled Components Docs](https://styled-components.com/docs)
- [Qwen AI Documentation](https://qwen.ai/docs)

## 🤝 Contributing

1. Fork the template
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - feel free to use this template for your projects!

---

**Built with ❤️ for the Qwen AI developer community**