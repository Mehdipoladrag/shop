import { createContext, useContext, useEffect, useState } from "react";
import { sessionApi } from "../api/endpoints";

const ANONYMOUS = { is_authenticated: false, username: "" };

const SessionContext = createContext(ANONYMOUS);

/** Login state of the visitor, taken from the Django session cookie. */
export function SessionProvider({ children }) {
  const [session, setSession] = useState(ANONYMOUS);

  useEffect(() => {
    sessionApi.current().then(setSession).catch(() => setSession(ANONYMOUS));
  }, []);

  return <SessionContext.Provider value={session}>{children}</SessionContext.Provider>;
}

export const useSession = () => useContext(SessionContext);
