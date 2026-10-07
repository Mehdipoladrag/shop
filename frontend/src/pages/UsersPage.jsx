import { useEffect, useState } from "react";
import { userApi } from "../api/endpoints";
import { useApi } from "../hooks/useApi";
import { AsyncContent } from "../components/Feedback";
import PageHeader from "../components/PageHeader";
import DataTable from "../components/DataTable";
import { formatDate, formatNumber } from "../utils/format";

const SEARCH_DEBOUNCE_MS = 350;

const COLUMNS = [
  { key: "username", header: "نام کاربری", render: (user) => <span dir="ltr">{user.username}</span> },
  { key: "email", header: "ایمیل", render: (user) => <span dir="ltr">{user.email || "—"}</span> },
  { key: "date_joined", header: "تاریخ عضویت", render: (user) => formatDate(user.date_joined) },
  {
    key: "role",
    header: "نقش",
    render: (user) => <span className={`badge ${user.is_superuser ? "badge--accent" : ""}`}>{user.is_superuser ? "مدیر کل" : user.is_staff ? "کارمند" : "کاربر"}</span>,
  },
  {
    key: "is_active",
    header: "وضعیت",
    render: (user) => <span className={`badge ${user.is_active ? "badge--ok" : "badge--off"}`}>{user.is_active ? "فعال" : "غیرفعال"}</span>,
  },
];

export default function UsersPage() {
  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  // Debounce typing so the API is not called on every keystroke.
  useEffect(() => {
    const timer = setTimeout(() => {
      setSearch(searchInput.trim());
      setPage(1);
    }, SEARCH_DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [searchInput]);

  const state = useApi(() => userApi.list({ search, page }), [search, page]);

  return (
    <>
      <PageHeader title="کاربران">
        <input
          type="search"
          className="search-input"
          placeholder="جست‌وجوی کاربر…"
          aria-label="جست‌وجوی کاربران"
          value={searchInput}
          onChange={(event) => setSearchInput(event.target.value)}
        />
      </PageHeader>

      <AsyncContent state={state}>
        {({ results, count, next, previous }) => (
          <>
            <DataTable columns={COLUMNS} rows={results} getRowKey={(user) => user.id} emptyText="کاربری پیدا نشد." />
            <nav className="pagination" aria-label="صفحه‌بندی">
              <button type="button" className="btn btn--ghost" disabled={!previous} onClick={() => setPage(page - 1)}>
                صفحه‌ی قبل
              </button>
              <span>
                صفحه <bdi>{formatNumber(page)}</bdi> · <bdi>{formatNumber(count)}</bdi> کاربر
              </span>
              <button type="button" className="btn btn--ghost" disabled={!next} onClick={() => setPage(page + 1)}>
                صفحه‌ی بعد
              </button>
            </nav>
          </>
        )}
      </AsyncContent>
    </>
  );
}
