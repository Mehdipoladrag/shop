import { dashboardApi, orderApi } from "../api/endpoints";
import { useApi } from "../hooks/useApi";
import { AsyncContent } from "../components/Feedback";
import PageHeader from "../components/PageHeader";
import StatCard from "../components/StatCard";
import DataTable from "../components/DataTable";
import { formatNumber, toPersianDigits } from "../utils/format";

const LATEST_ORDERS_LIMIT = 5;

async function loadDashboard() {
  const [users, orders, products, orderList] = await Promise.all([
    dashboardApi.userCounts(),
    dashboardApi.orderCount(),
    dashboardApi.productCount(),
    orderApi.list(),
  ]);
  return { users, orders, products, latestOrders: orderList.slice(0, LATEST_ORDERS_LIMIT) };
}

const ORDER_COLUMNS = [
  { key: "customer", header: "مشتری" },
  { key: "order_persian_date", header: "تاریخ", render: (order) => toPersianDigits(order.order_persian_date) },
  { key: "total_cost", header: "مبلغ کل", render: (order) => `${toPersianDigits(order.total_cost)} تومان` },
];

export default function DashboardPage() {
  const state = useApi(loadDashboard);

  return (
    <>
      <PageHeader title="داشبورد" />
      <AsyncContent state={state}>
        {({ users, orders, products, latestOrders }) => (
          <>
            <section className="stats-grid" aria-label="آمار کلی">
              <StatCard tone="info" label="سفارش‌ها" value={formatNumber(orders.order_count)} />
              <StatCard tone="success" label="محصولات" value={formatNumber(products.product_count)} />
              <StatCard tone="warning" label="کاربران" value={formatNumber(users.counter)} />
              <StatCard tone="danger" label="مدیران" value={formatNumber(users.super_users)} />
            </section>

            <section className="panel">
              <h2>آخرین سفارش‌ها</h2>
              <DataTable
                columns={ORDER_COLUMNS}
                rows={latestOrders}
                getRowKey={(order) => `${order.customer}-${order.order_date}`}
                emptyText="هنوز سفارشی ثبت نشده است."
              />
            </section>
          </>
        )}
      </AsyncContent>
    </>
  );
}
