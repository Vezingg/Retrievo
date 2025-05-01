import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0", // Change this to your desired host, e.g., 'localhost'
    port: 3000, // Change this to your desired port
  },
});
