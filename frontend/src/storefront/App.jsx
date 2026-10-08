import { lazy, Suspense } from "react";
import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import { Loading, NotFound } from "./components/States";
import RequireAuth from "./auth/RequireAuth";

// Every page is its own chunk, loaded when its route is first visited.
const lazyPage = (load, exportName = "default") => lazy(() => load().then((module) => ({ default: module[exportName] })));

const HomePage = lazyPage(() => import("./pages/HomePage"));
const ShopPage = lazyPage(() => import("./pages/ShopPage"));
const ProductPage = lazyPage(() => import("./pages/ProductPage"));
const CartPage = lazyPage(() => import("./pages/CartPage"));
const BlogListPage = lazyPage(() => import("./pages/BlogPages"), "BlogListPage");
const BlogDetailPage = lazyPage(() => import("./pages/BlogPages"), "BlogDetailPage");
const AboutPage = lazyPage(() => import("./pages/InfoPages"), "AboutPage");
const ContactPage = lazyPage(() => import("./pages/InfoPages"), "ContactPage");
const LoginPage = lazyPage(() => import("./pages/account/LoginPage"));
const RegisterPage = lazyPage(() => import("./pages/account/RegisterPage"));
const AccountLayout = lazyPage(() => import("./pages/account/AccountLayout"));
const ProfilePage = lazyPage(() => import("./pages/account/ProfilePage"));
const ProfileEditPage = lazyPage(() => import("./pages/account/ProfileEditPage"));
const PasswordPage = lazyPage(() => import("./pages/account/PasswordPage"));
const AddressPage = lazyPage(() => import("./pages/account/AddressPage"));
const OrdersPage = lazyPage(() => import("./pages/account/OrdersPage"));
const OrderStatusPage = lazyPage(() => import("./pages/account/OrderStatusPage"));
const CheckoutPage = lazyPage(() => import("./pages/CheckoutPage"));
const OrderSuccessPage = lazyPage(() => import("./pages/OrderSuccessPage"));
const DesignKit = import.meta.env.DEV ? lazyPage(() => import("./pages/DesignKit")) : null;

export default function App() {
  return (
    <Suspense fallback={<Loading />}>
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
          {DesignKit && <Route path="design-kit" element={<DesignKit />} />}
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </Suspense>
  );
}
