import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "./index.css";
import App from "./App.jsx";

// Auto-reload when a new Vercel deployment replaces cached chunks
if (typeof window !== "undefined") {
  window.addEventListener("vite:preloadError", (event) => {
    event?.preventDefault?.();
    window.location.reload();
  });

  window.addEventListener("error", (event) => {
    const msg = String(event?.message || "");
    if (
      msg.includes("Failed to fetch dynamically imported module") ||
      msg.includes("Expected a JavaScript-or-Wasm module script")
    ) {
      const retryKey = "chunk_preload_retried";
      if (!sessionStorage.getItem(retryKey)) {
        sessionStorage.setItem(retryKey, "true");
        window.location.reload();
      }
    }
  });
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 10 * 60 * 1000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>
);