import path from "path";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src")
    }
  },
  server: {
    port: 3000,
    host: true,
    cors: true
  },
  build: {
    outDir: "dist",
    sourcemap: true
  },
  define: {
    global: "globalThis"
  },
  envPrefix: "VITE_"
});
