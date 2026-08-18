import { createContext, useContext, useEffect, useState } from 'react';
import { authApi } from '../api/authApi';

const AuthContext = createContext(null);
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); const [loading, setLoading] = useState(Boolean(localStorage.getItem('access_token')));
  const refreshUser = async () => { const { data } = await authApi.me(); setUser(data); return data; };
  useEffect(() => { if (loading) refreshUser().catch(() => localStorage.clear()).finally(() => setLoading(false)); }, []);
  const login = async (credentials) => { const { data } = await authApi.login(credentials); localStorage.setItem('access_token', data.access); localStorage.setItem('refresh_token', data.refresh); await refreshUser(); };
  const logout = () => { localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token'); setUser(null); };
  return <AuthContext.Provider value={{ user, loading, login, logout, refreshUser }}>{children}</AuthContext.Provider>;
}
export const useAuth = () => useContext(AuthContext);
