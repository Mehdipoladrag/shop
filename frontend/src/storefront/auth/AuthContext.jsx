import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { SESSION_EXPIRED_EVENT } from "../api/client";
import { customerApi, sessionApi } from "../api/endpoints";

const ANONYMOUS = { is_authenticated: false, username: "" };

const AuthContext = createContext(null);

/**
 * Login state of the visitor, taken from the Django session cookie.
 *
 * `sessionVersion` changes whenever the session changes (login, logout), so
 * data tied to the session, such as the cart, knows to reload.
 */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(ANONYMOUS);
  const [loading, setLoading] = useState(true);
  const [sessionVersion, setSessionVersion] = useState(0);

  useEffect(() => {
    sessionApi
      .current()
      .then(setUser)
      .catch(() => setUser(ANONYMOUS))
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (username, password) => {
    const loggedIn = await customerApi.login(username, password);
    setUser(loggedIn);
    setSessionVersion((version) => version + 1);
    return loggedIn;
  }, []);

  // If the request fails the server session is still alive, so the UI must not
  // pretend to be logged out; the error goes to the caller.
  const logout = useCallback(async () => {
    await customerApi.logout();
    setUser(ANONYMOUS);
    setSessionVersion((version) => version + 1);
  }, []);

  // The API client reports when the server stopped recognising the customer.
  useEffect(() => {
    const handleExpired = () => {
      setUser(ANONYMOUS);
      setSessionVersion((version) => version + 1);
    };
    window.addEventListener(SESSION_EXPIRED_EVENT, handleExpired);
    return () => window.removeEventListener(SESSION_EXPIRED_EVENT, handleExpired);
  }, []);

  const value = useMemo(
    () => ({ user, loading, isAuthenticated: user.is_authenticated, sessionVersion, login, logout }),
    [user, loading, sessionVersion, login, logout]
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used inside AuthProvider");
  return context;
}
