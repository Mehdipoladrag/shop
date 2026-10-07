import { orderApi } from "../api/endpoints";
import { useApi } from "../../shared/useApi";
import { AsyncContent } from "../components/Feedback";
import PageHeader from "../components/PageHeader";
import DataTable from "../components/DataTable";
import { toPersianDigits } from "../../shared/format";

const COLUMNS = [
  { key: "customer", header: "مشتری" },
  { key: "order_persian_date", header: "تاریخ سفارش", render: (order) => toPersianDigits(order.order_persian_date) },
  { key: "total_cost", header: "مبلغ کل", render: (order) => `${toPersianDigits(order.total_cost)} تومان` },
];

export default function OrdersPage() {
  const state = useApi(orderApi.list);

  return (
    <>
      <PageHeader title="سفارش‌ها" />
      <AsyncContent state={state}>
        {(orders) => (
          <DataTable
            columns={COLUMNS}
            rows={orders}
            getRowKey={(order) => `${order.customer}-${order.order_date}`}
            emptyText="هنوز سفارشی ثبت نشده است."
          />
        )}
      </AsyncContent>
    </>
  );
}
