import { useCallback, useEffect, useState } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { catalogApi } from "../api/endpoints";
import { useAuth } from "../auth/AuthContext";
import { useApi } from "../../shared/useApi";
import { useFlash } from "./Flash";
import Footer from "./Footer";
import Header from "./Header";
import MobileDrawer from "./MobileDrawer";

/** Page frame shared by every storefront route: header, drawer, content and footer. */
export default function Layout() {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  const { logout } = useAuth();
  const flash = useFlash();
  const categories = useApi(catalogApi.categories);

  const closeMenu = useCallback(() => setMenuOpen(false), []);

  // A new page starts at the top and closes the mobile menu.
  useEffect(() => {
    window.scrollTo(0, 0);
    setMenuOpen(false);
  }, [pathname]);

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
      <a href="#content" className="skip-link">
        پرش به محتوای صفحه
      </a>
      <Header onSearch={handleSearch} onLogout={handleLogout} onOpenMenu={() => setMenuOpen(true)} />
      <MobileDrawer open={menuOpen} categories={categories.data ?? []} onClose={closeMenu} onLogout={handleLogout} />
      <div id="content">
        <Outlet />
      </div>
      <Footer />
    </>
  );
}
