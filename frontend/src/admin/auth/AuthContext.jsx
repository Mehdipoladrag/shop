import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { authApi } from "../api/endpoints";
import { AUTH_EXPIRED_EVENT } from "../api/client";
import { tokenStorage } from "../api/tokenStorage";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(() => Boolean(tokenStorage.getAccess()));

  const login = useCallback(async (username, password) => {
    const tokens = await authApi.login(username, password);
    tokenStorage.setTokens(tokens);
    setIsAuthenticated(true);
  }, []);

  const logout = useCallback(() => {
    tokenStorage.clear();
    setIsAuthenticated(false);
  }, []);

  // The API client emits this event when a token can no longer be refreshed.
  useEffect(() => {
    window.addEventListener(AUTH_EXPIRED_EVENT, logout);
    return () => window.removeEventListener(AUTH_EXPIRED_EVENT, logout);
  }, [logout]);

  const value = useMemo(() => ({ isAuthenticated, login, logout }), [isAuthenticated, login, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}
