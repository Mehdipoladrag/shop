export default function StatCard({ label, value, tone }) {
  return (
    <article className={`stat-card stat-card--${tone}`}>
      <span className="stat-card__value">{value}</span>
      <span className="stat-card__label">{label}</span>
    </article>
  );
}
