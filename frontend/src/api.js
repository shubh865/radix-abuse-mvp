// src/api.js
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
});

// small test call
export async function pingHealth() {
  const { data } = await api.get("/health");
  return data; // { status: "ok" }
}

export default api;
