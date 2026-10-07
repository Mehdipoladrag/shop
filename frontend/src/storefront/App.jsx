import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import { NotFound } from "./components/States";
import HomePage from "./pages/HomePage";
import ShopPage from "./pages/ShopPage";
import ProductPage from "./pages/ProductPage";
import CartPage from "./pages/CartPage";
import { BlogDetailPage, BlogListPage } from "./pages/BlogPages";
import { AboutPage, ContactPage } from "./pages/InfoPages";
import RequireAuth from "./auth/RequireAuth";
import LoginPage from "./pages/account/LoginPage";
import RegisterPage from "./pages/account/RegisterPage";
import AccountLayout from "./pages/account/AccountLayout";
import ProfilePage from "./pages/account/ProfilePage";
import ProfileEditPage from "./pages/account/ProfileEditPage";
import PasswordPage from "./pages/account/PasswordPage";
import AddressPage from "./pages/account/AddressPage";
import OrdersPage from "./pages/account/OrdersPage";
import OrderStatusPage from "./pages/account/OrderStatusPage";
import CheckoutPage from "./pages/CheckoutPage";
import OrderSuccessPage from "./pages/OrderSuccessPage";

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
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
        <Route element={<RequireAuth />}>
          <Route path="checkout" element={<CheckoutPage />} />
          <Route path="checkout/success/:id" element={<OrderSuccessPage />} />
          <Route path="account" element={<AccountLayout />}>
            <Route index element={<ProfilePage />} />
            <Route path="edit" element={<ProfileEditPage />} />
            <Route path="password" element={<PasswordPage />} />
            <Route path="address" element={<AddressPage />} />
            <Route path="orders" element={<OrdersPage />} />
            <Route path="orders/:id" element={<OrderStatusPage />} />
          </Route>
        </Route>
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
