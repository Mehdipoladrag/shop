import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { CircleAlert, CircleCheck } from "lucide-react";
import "./Flash.css";

const FLASH_DURATION_MS = 4000;

const FlashContext = createContext(null);

/** Short-lived success and error messages at the bottom of the screen. */
export function FlashProvider({ children }) {
  const [message, setMessage] = useState(null);

  useEffect(() => {
    if (!message) return undefined;
    const timer = setTimeout(() => setMessage(null), FLASH_DURATION_MS);
    return () => clearTimeout(timer);
  }, [message]);

  const show = useCallback((text, type = "success") => setMessage({ text, type, id: Date.now() }), []);
  const value = useMemo(() => ({ show }), [show]);
  const Icon = message?.type === "error" ? CircleAlert : CircleCheck;

  return (
    <FlashContext.Provider value={value}>
      {children}
      {message && (
        <div className={`flash flash--${message.type}`} role={message.type === "error" ? "alert" : "status"} key={message.id}>
          <Icon size={20} aria-hidden="true" />
          <span>{message.text}</span>
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
