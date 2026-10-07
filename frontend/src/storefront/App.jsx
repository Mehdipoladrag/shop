import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import { NotFound } from "./components/States";
import HomePage from "./pages/HomePage";
import ShopPage from "./pages/ShopPage";
import ProductPage from "./pages/ProductPage";
import CartPage from "./pages/CartPage";
import { BlogDetailPage, BlogListPage } from "./pages/BlogPages";
import { AboutPage, ContactPage } from "./pages/InfoPages";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="products" element={<ShopPage mode="all" />} />
        <Route path="categories" element={<ShopPage mode="all" />} />
        <Route path="category/:slug" element={<ShopPage mode="category" />} />
        <Route path="search" element={<ShopPage mode="search" />} />
        <Route path="products/:slug" element={<ProductPage />} />
        <Route path="cart" element={<CartPage />} />
        <Route path="blog" element={<BlogListPage />} />
        <Route path="blog/:slug" element={<BlogDetailPage />} />
        <Route path="about" element={<AboutPage />} />
        <Route path="contact" element={<ContactPage />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
