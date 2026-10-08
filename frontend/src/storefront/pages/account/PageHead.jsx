/** Title row of an account page: the page's single h1 and optional actions. */
export default function PageHead({ title, children }) {
  return (
    <header className="account-head">
      <h1 className="account-head__title">{title}</h1>
      {children && <div className="account-head__actions">{children}</div>}
    </header>
  );
}
