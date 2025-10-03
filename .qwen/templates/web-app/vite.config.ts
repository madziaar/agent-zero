import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
    // Qwen-optimized: Enable HMR for faster development feedback
    hmr: {
      overlay: true
    }
  },
  build: {
    // Qwen-optimized: Enable source maps for better debugging
    sourcemap: true,
    // Optimize chunk splitting for better loading performance
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['styled-components']
        }
      }
    },
    // Qwen-optimized: Set reasonable chunk size warnings
    chunkSizeWarningLimit: 1000
  },
  // Qwen-optimized: Path resolution for cleaner imports
  resolve: {
    alias: {
      '@': '/src',
      '@components': '/src/components',
      '@types': '/src/types',
      '@utils': '/src/utils',
      '@styles': '/src/styles'
    }
  },
  // Qwen-optimized: Enable CSS code splitting
  css: {
    devSourcemap: true
  },
  // Qwen-optimized: Test configuration for Vitest
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: true
  }
})