import { useEffect, useState } from "react";

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

/** Countdown timer styled like the one of the Django site. Defaults to the end of today. */
export default function Countdown({ target }) {
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
    <div className="countdown-timer">
      {units.map(([value, label]) => (
        <ul className="text_countdown" key={label}>
          <li className="number_countdown">{value}</li>
          <li>{label}</li>
        </ul>
      ))}
    </div>
  );
}
