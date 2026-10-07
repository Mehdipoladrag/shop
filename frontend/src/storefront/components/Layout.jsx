import { useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { MobileHeader, PcHeader, TopBanner } from "./Header";
import Footer from "./Footer";

/** Page frame shared by every storefront route: banner, headers, content, footer. */
export default function Layout() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  // The slide-in mobile menu is driven by a class on <html>, as in the original theme.
  useEffect(() => {
    document.documentElement.classList.toggle("nav-open", menuOpen);
    return () => document.documentElement.classList.remove("nav-open");
  }, [menuOpen]);

  // A new page starts at the top and closes the mobile menu.
  useEffect(() => {
    window.scrollTo(0, 0);
    setMenuOpen(false);
  }, [pathname]);

  const closeMenu = () => setMenuOpen(false);

  function handleSearch(query) {
    closeMenu();
    if (query) navigate(`/search?q=${encodeURIComponent(query)}`);
  }

  return (
    <>
      <TopBanner />
      <MobileHeader
        menuOpen={menuOpen}
        onToggleMenu={() => setMenuOpen(!menuOpen)}
        onNavigate={closeMenu}
        onSearch={handleSearch}
      />
      {menuOpen && <div id="bodyClick" onClick={closeMenu} />}
      <div className="wrapper default">
        <PcHeader onSearch={handleSearch} />
        <Outlet />
        <Footer />
      </div>
    </>
  );
}
