import { useEffect, useState } from "react";
import "./Countdown.css";

const SECOND_MS = 1000;
const MINUTE_S = 60;
const HOUR_S = 3600;
const DAY_S = 86400;

function secondsUntil(target) {
  return Math.max(0, Math.floor((target.getTime() - Date.now()) / SECOND_MS));
}

function endOfToday() {
  const end = new Date();
  end.setHours(23, 59, 59, 999);
  return end;
}

const pad = (value) => String(value).padStart(2, "0");

/** Countdown timer; `target` is a Date and defaults to the end of today. `tone="light"` is for dark backgrounds. */
export default function Countdown({ target, tone = "dark" }) {
  const [deadline] = useState(() => target ?? endOfToday());
  const [remaining, setRemaining] = useState(() => secondsUntil(deadline));

  useEffect(() => {
    const timer = setInterval(() => setRemaining(secondsUntil(deadline)), SECOND_MS);
    return () => clearInterval(timer);
  }, [deadline]);

  const units = [
    [Math.floor(remaining / DAY_S), "روز"],
    [Math.floor((remaining % DAY_S) / HOUR_S), "ساعت"],
    [Math.floor((remaining % HOUR_S) / MINUTE_S), "دقیقه"],
    [remaining % MINUTE_S, "ثانیه"],
  ];

  return (
    <div className={`countdown countdown--${tone}`} role="timer" aria-label="زمان باقی‌مانده">
      {units.map(([value, label]) => (
        <div className="countdown__unit" key={label}>
          <strong>{pad(value)}</strong>
          <span>{label}</span>
        </div>
      ))}
    </div>
  );
}
