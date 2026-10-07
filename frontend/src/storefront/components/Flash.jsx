import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

const FLASH_DURATION_MS = 4000;

const FlashContext = createContext(null);

/** Short-lived success and error messages in the corner of the screen. */
export function FlashProvider({ children }) {
  const [message, setMessage] = useState(null);

  useEffect(() => {
    if (!message) return undefined;
    const timer = setTimeout(() => setMessage(null), FLASH_DURATION_MS);
    return () => clearTimeout(timer);
  }, [message]);

  const show = useCallback((text, type = "success") => setMessage({ text, type, id: Date.now() }), []);
  const value = useMemo(() => ({ show }), [show]);

  return (
    <FlashContext.Provider value={value}>
      {children}
      {message && (
        <div className={`flash flash--${message.type}`} role={message.type === "error" ? "alert" : "status"} key={message.id}>
          <i className={`fa ${message.type === "error" ? "fa-times-circle" : "fa-check-circle"}`} aria-hidden="true" /> {message.text}
        </div>
      )}
    </FlashContext.Provider>
  );
}

export function useFlash() {
  const context = useContext(FlashContext);
  if (!context) throw new Error("useFlash must be used inside FlashProvider");
  return context;
}
