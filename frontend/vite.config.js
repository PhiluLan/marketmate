// frontend/vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    proxy: {
      // Alle Aufrufe /api/* werden an Django auf Port 8000 geschickt
      '/api': 'http://localhost:8000'
    },
    alias: {
      // '@' → /path/to/frontend/src
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  extensions: ['.js', '.ts', '.vue', '.json'],
  server: {
    host: '0.0.0.0',
    port: 3001,
    proxy: {
      '/api': {
        target: process.env.VITE_API_PROXY_TARGET || 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: path => path.replace(/^\/api/, '/api'),
      }
    }
  }
})
