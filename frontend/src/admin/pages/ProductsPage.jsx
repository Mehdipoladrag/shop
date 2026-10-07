import { useState } from "react";
import { productApi } from "../api/endpoints";
import { useApi } from "../../shared/useApi";
import { AsyncContent } from "../components/Feedback";
import PageHeader from "../components/PageHeader";
import DataTable from "../components/DataTable";
import ConfirmDialog from "../components/ConfirmDialog";
import { formatNumber, formatPrice, toPersianDigits } from "../../shared/format";
import { toRelativeMediaUrl } from "../../shared/media";

const COLUMNS = [
  {
    key: "pic",
    header: "تصویر",
    render: (product) => <img className="thumb" src={toRelativeMediaUrl(product.pic)} alt={product.product_name} loading="lazy" />,
  },
  { key: "product_name", header: "نام محصول" },
  { key: "product_category", header: "دسته‌بندی" },
  { key: "product_brand", header: "برند" },
  { key: "price", header: "قیمت", render: (product) => formatPrice(product.price) },
  { key: "product_number", header: "موجودی", render: (product) => formatNumber(product.product_number) },
  { key: "product_rate", header: "امتیاز", render: (product) => toPersianDigits(product.product_rate) },
];

export default function ProductsPage() {
  const state = useApi(productApi.list);
  const [productToDelete, setProductToDelete] = useState(null);

  async function handleDelete() {
    await productApi.remove(productToDelete.id);
    setProductToDelete(null);
    state.reload();
  }

  return (
    <>
      <PageHeader title="محصولات" />
      <AsyncContent state={state}>
        {(products) => (
          <DataTable
            columns={COLUMNS}
            rows={products}
            getRowKey={(product) => product.id}
            emptyText="هنوز محصولی ثبت نشده است."
            renderActions={(product) => (
              <button type="button" className="btn btn--danger-ghost" onClick={() => setProductToDelete(product)}>
                حذف
              </button>
            )}
          />
        )}
      </AsyncContent>

      {productToDelete && (
        <ConfirmDialog
          title="حذف محصول"
          message={`محصول «${productToDelete.product_name}» حذف شود؟ این کار قابل بازگشت نیست.`}
          onConfirm={handleDelete}
          onCancel={() => setProductToDelete(null)}
        />
      )}
    </>
  );
}
