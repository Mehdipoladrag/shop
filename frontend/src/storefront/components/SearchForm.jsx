import { useState } from "react";
import { Search } from "lucide-react";

/** Pill-shaped product search; `onSearch(query)` receives the trimmed text. */
export default function SearchForm({ onSearch, className = "" }) {
  const [query, setQuery] = useState("");

  function handleSubmit(event) {
    event.preventDefault();
    onSearch(query.trim());
  }

  return (
    <form className={`site-search ${className}`} role="search" onSubmit={handleSubmit}>
      <input
        type="search"
        name="q"
        className="site-search__input"
        placeholder="جستجوی محصول، برند یا دسته‌بندی …"
        aria-label="جستجو"
        autoComplete="off"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
      />
      <button type="submit" className="site-search__button" aria-label="جستجو">
        <Search size={20} aria-hidden="true" />
      </button>
    </form>
  );
}
