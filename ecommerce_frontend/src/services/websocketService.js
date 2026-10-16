export const getWebSocketUrl = (path) => {
  const baseUrl =
    import.meta.env.VITE_WS_URL ||
    "wss://coastal-seven-backend.onrender.com";

  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const separator = path.includes("?") ? "&" : "?";
  return token ? `${baseUrl}${path}${separator}token=${encodeURIComponent(token)}` : `${baseUrl}${path}`;
};
