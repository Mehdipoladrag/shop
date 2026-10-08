import { useState } from "react";
import { Mail, Search } from "lucide-react";
import { catalogApi } from "../api/endpoints";
import { useApi } from "../../shared/useApi";
import Breadcrumb from "../components/Breadcrumb";
import Carousel from "../components/Carousel";
import Countdown from "../components/Countdown";
import FormField, { FormError } from "../components/FormField";
import Pagination from "../components/Pagination";
import ProductCard from "../components/ProductCard";
import QuantityStepper from "../components/QuantityStepper";
import SectionHeader from "../components/SectionHeader";
import { AsyncContent, EmptyState } from "../components/States";
import { useFlash } from "../components/Flash";

/** Living style guide of the storefront kit; only routed in development (see App.jsx). */
export default function DesignKit() {
  const products = useApi(() => catalogApi.products({ page_size: 10 }));
  const [quantity, setQuantity] = useState(2);
  const [page, setPage] = useState(3);
  const flash = useFlash();

  return (
    <main className="page">
      <div className="container">
        <Breadcrumb items={[{ label: "فروشگاه", to: "/products" }, { label: "کیت طراحی" }]} />
        <h1 className="page-title">کیت طراحی مَسای</h1>

        <section className="section card card--pad">
          <h2 className="card__title">دکمه‌ها و نشان‌ها</h2>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 12, alignItems: "center" }}>
            <button className="btn btn--primary">اصلی</button>
            <button className="btn btn--accent">خرید</button>
            <button className="btn btn--secondary">ثانویه</button>
            <button className="btn btn--ghost">شفاف</button>
            <button className="btn btn--danger">حذف</button>
            <button className="btn btn--primary" disabled>غیرفعال</button>
            <button className="btn btn--primary btn--sm">کوچک</button>
            <button className="btn btn--primary btn--lg">بزرگ</button>
            <span className="badge">پیش‌فرض</span>
            <span className="badge badge--discount">۱۲%</span>
            <span className="badge badge--success">موفق</span>
            <span className="badge badge--warning">در انتظار</span>
            <span className="badge badge--danger">ناموفق</span>
            <button className="btn btn--secondary" onClick={() => flash.show("پیام موفقیت")}>پیام موفق</button>
            <button className="btn btn--secondary" onClick={() => flash.show("پیام خطا", "error")}>پیام خطا</button>
          </div>
        </section>

        <section className="section card card--pad">
          <h2 className="card__title">فرم‌ها</h2>
          <div style={{ display: "grid", gap: 16, gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))" }}>
            <FormField label="نام کاربری" name="u" placeholder="@name" icon={<Mail size={18} />} required />
            <FormField label="با خطا" name="e" error="این فیلد الزامی است" defaultValue="مقدار" />
            <FormField label="با راهنما" name="h" hint="راهنمای کوتاه فیلد" />
            <FormField label="لیست">
              {(aria) => (
                <select className="select" {...aria}>
                  <option>مرد</option>
                  <option>زن</option>
                </select>
              )}
            </FormField>
            <FormField label="توضیحات">{(aria) => <textarea className="textarea" {...aria} />}</FormField>
            <div>
              <p className="field__label" style={{ marginBottom: 8 }}>تعداد و شمارش معکوس</p>
              <QuantityStepper value={quantity} max={5} onChange={setQuantity} />
              <div style={{ marginTop: 12 }}><Countdown /></div>
              <div style={{ marginTop: 12, padding: 12, background: "var(--navy-800)", borderRadius: 12 }}><Countdown tone="light" /></div>
            </div>
          </div>
          <FormError message="خطای کلی فرم نمونه" />
        </section>

        <section className="section">
          <SectionHeader title="پیشنهاد شگفت‌انگیز" subtitle="تخفیف‌های امروز" to="/products">
            <Countdown />
          </SectionHeader>
          <AsyncContent state={products} variant="grid">
            {(data) => (
              <Carousel variant="cards" label="محصولات">
                {data.results.map((product) => (
                  <ProductCard product={product} key={product.id} />
                ))}
              </Carousel>
            )}
          </AsyncContent>
        </section>

        <section className="section">
          <SectionHeader title="شبکه محصولات" />
          <AsyncContent state={products} variant="grid">
            {(data) => (
              <div className="product-grid">
                {data.results.slice(0, 8).map((product) => (
                  <ProductCard product={product} key={product.id} />
                ))}
              </div>
            )}
          </AsyncContent>
          <Pagination page={page} pageCount={9} onChange={setPage} />
        </section>

        <EmptyState icon={Search} title="نتیجه‌ای پیدا نشد" text="عبارت دیگری را جستجو کنید یا فیلترها را پاک کنید.">
          <button className="btn btn--primary">پاک کردن فیلترها</button>
        </EmptyState>
      </div>
    </main>
  );
}
