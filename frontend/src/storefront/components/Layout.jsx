import { useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { useFlash } from "./Flash";
import { MobileHeader, PcHeader, TopBanner } from "./Header";
import Footer from "./Footer";

/** Page frame shared by every storefront route: banner, headers, content, footer. */
export default function Layout() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const { logout } = useAuth();
  const flash = useFlash();

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

  async function handleLogout() {
    closeMenu();
    try {
      await logout();
    } catch (error) {
      flash.show(`خروج انجام نشد. ${error.message}`, "error");
      return;
    }
    flash.show("از حساب کاربری خارج شدید");
    navigate("/");
  }

  return (
    <>
      <TopBanner />
      <MobileHeader
        menuOpen={menuOpen}
        onToggleMenu={() => setMenuOpen(!menuOpen)}
        onNavigate={closeMenu}
        onSearch={handleSearch}
        onLogout={handleLogout}
      />
      {menuOpen && <div id="bodyClick" onClick={closeMenu} />}
      <div className="wrapper default">
        <PcHeader onSearch={handleSearch} onLogout={handleLogout} />
        <Outlet />
        <Footer />
      </div>
    </>
  );
}
