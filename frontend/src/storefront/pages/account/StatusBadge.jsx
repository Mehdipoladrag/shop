import { CircleCheck, CircleX, Clock } from "lucide-react";
import "./shared.css";

const ICONS = { pending: Clock, completed: CircleCheck, failed: CircleX };

/** Order status chip; the colors come from the kit's status-badge--* classes. */
export default function StatusBadge({ order, testId }) {
  const Icon = ICONS[order.status] ?? Clock;
  return (
    <span className={`status-badge status-badge--${order.status} account-status`} data-testid={testId}>
      <Icon size={14} aria-hidden="true" />
      {order.status_label}
    </span>
  );
}
