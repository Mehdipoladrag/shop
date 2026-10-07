import { request } from "./client";

const SHOP_API = "/shop/api/v1";
const ACCOUNTS_API = "/accounts/api/v1";
const DASHBOARD_API = "/admin-panel/api/v2";

export const authApi = {
  login: (username, password) =>
    request(`${ACCOUNTS_API}/login/`, { method: "POST", body: { username, password }, auth: false }),
};

export const dashboardApi = {
  userCounts: () => request(`${DASHBOARD_API}/user-count/`),
  orderCount: () => request(`${DASHBOARD_API}/new-order/`),
  productCount: () => request(`${DASHBOARD_API}/product-count/`),
};

export const categoryApi = {
  list: () => request(`${SHOP_API}/category-list/`),
  create: (formData) => request(`${SHOP_API}/category-create/`, { method: "POST", body: formData }),
  update: (id, formData) => request(`${SHOP_API}/category-data/${id}/`, { method: "PUT", body: formData }),
  remove: (id) => request(`${SHOP_API}/category-data/${id}/`, { method: "DELETE" }),
};

export const productApi = {
  list: () => request(`${SHOP_API}/product-list/`),
  remove: (id) => request(`${SHOP_API}/product-data/${id}/`, { method: "DELETE" }),
};

export const orderApi = {
  list: () => request(`${SHOP_API}/order-list/`),
};

export const userApi = {
  // Users are paginated; `search` matches username, email and names.
  list: ({ search = "", page = 1 } = {}) => {
    const params = new URLSearchParams({ page });
    if (search) params.set("search", search);
    return request(`${ACCOUNTS_API}/users-list/?${params}`);
  },
};
