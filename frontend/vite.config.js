import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const apiOrigin = process.env.DEVSPACE_API_ORIGIN || 'http://localhost';

export default defineConfig({
  plugins: [react()],
  server: { proxy: { '/api': apiOrigin, '/media': apiOrigin } },
});
