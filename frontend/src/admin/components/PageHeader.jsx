export default function PageHeader({ title, children }) {
  return (
    <div className="page-header">
      <h1>{title}</h1>
      {children && <div className="page-header__actions">{children}</div>}
    </div>
  );
}
