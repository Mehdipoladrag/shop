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

export const sessionApi = {
  // Login happens on the Django site; this only reports its state.
  current: () => request(`${API}/session/`),
};
