import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("framer-motion")) {
            return "motion";
          }
          if (id.includes("react-datepicker") || id.includes("date-fns")) {
            return "calendar";
          }
          return undefined;
        },
      },
    },
  },
});
