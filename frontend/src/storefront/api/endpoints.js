import { request } from "./client";

const API = "/shop/api/v1/public";

export const catalogApi = {
  categories: () => request(`${API}/categories/`),
  brands: () => request(`${API}/brands/`),
  products: (params) => request(`${API}/products/`, { params }),
  productFilters: () => request(`${API}/products/filters/`),
  product: (slug) => request(`${API}/products/${encodeURIComponent(slug)}/`),
};

export const cartApi = {
  get: () => request(`${API}/cart/`),
  add: (productId, productCount) =>
    request(`${API}/cart/`, { method: "POST", body: { product_id: productId, product_count: productCount } }),
  setCount: (productId, productCount) =>
    request(`${API}/cart/`, {
      method: "POST",
      body: { product_id: productId, product_count: productCount, update: true },
    }),
  remove: (productId) => request(`${API}/cart/${productId}/`, { method: "DELETE" }),
};

export const blogApi = {
  posts: (params) => request(`${API}/blog/`, { params }),
  post: (slug) => request(`${API}/blog/${encodeURIComponent(slug)}/`),
  categories: () => request(`${API}/blog/categories/`),
};

export const contactApi = {
  send: (message) => request(`${API}/contact/`, { method: "POST", body: message }),
};

const CUSTOMER = "/accounts/api/v1/customer";

export const customerApi = {
  register: (values) => request(`${CUSTOMER}/register/`, { method: "POST", body: values }),
  login: (username, password) => request(`${CUSTOMER}/login/`, { method: "POST", body: { username, password } }),
  logout: () => request(`${CUSTOMER}/logout/`, { method: "POST" }),
  // `FormData` so the profile picture can be uploaded together with the fields.
  profile: () => request(`${CUSTOMER}/profile/`),
  updateProfile: (formData) => request(`${CUSTOMER}/profile/`, { method: "PATCH", body: formData }),
  changePassword: (values) => request(`${CUSTOMER}/password/`, { method: "POST", body: values }),
  address: () => request(`${CUSTOMER}/address/`),
  updateAddress: (values) => request(`${CUSTOMER}/address/`, { method: "PUT", body: values }),
  orders: (page) => request(`${CUSTOMER}/orders/`, { params: { page } }),
  order: (id) => request(`${CUSTOMER}/orders/${id}/`),
  latestOrder: () => request(`${CUSTOMER}/orders/latest/`),
};

export const checkoutApi = {
  summary: () => request(`${API}/checkout/`),
  placeOrder: () => request(`${API}/checkout/`, { method: "POST" }),
};

export const sessionApi = {
  // Lightweight login state; the profile has its own endpoint.
  current: () => request(`${API}/session/`),
};
