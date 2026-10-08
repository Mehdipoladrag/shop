import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { ShoppingCart } from "lucide-react";
import { checkoutApi, customerApi } from "../api/endpoints";
import { useApi } from "../../shared/useApi";
import { useCart } from "../cart/CartContext";
import { useFlash } from "../components/Flash";
import { EmptyState, LoadError } from "../components/States";
import { useDocumentTitle } from "../components/useDocumentTitle";
import AddressCard from "./checkout/AddressCard";
import CheckoutSkeleton from "./checkout/CheckoutSkeleton";
import CheckoutSteps from "./checkout/CheckoutSteps";
import OrderItems from "./checkout/OrderItems";
import TotalCard from "./checkout/TotalCard";
import "./checkout.css";

function EmptyCheckout() {
  return (
    <main className="page checkout-page" data-testid="checkout-empty">
      <EmptyState level={1} icon={ShoppingCart} title="سبد خرید شما در حال حاضر خالی است." text="کالاهای مورد نظر را به سبد خرید اضافه کنید و دوباره برگردید.">
        <Link to="/" className="btn btn--primary">
          صفحه نخست
        </Link>
        <Link to="/products" className="btn btn--secondary">
          مشاهده محصولات
        </Link>
      </EmptyState>
    </main>
  );
}

function CheckoutContent({ summary, profile }) {
  const navigate = useNavigate();
  const flash = useFlash();
  const { reload: reloadCart } = useCart();
  const [placing, setPlacing] = useState(false);
  const [error, setError] = useState("");
  const { cart, address_complete: addressComplete } = summary;

  async function handlePay(event) {
    event.preventDefault();
    setPlacing(true);
    setError("");
    try {
      const order = await checkoutApi.placeOrder();
      await reloadCart();
      navigate(`/checkout/success/${order.id}`, { replace: true });
    } catch (placeError) {
      flash.show(placeError.message, "error");
      setError(placeError.message);
      setPlacing(false);
    }
  }

  if (cart.items.length === 0) return <EmptyCheckout />;

  return (
    <main className="page checkout-page" data-testid="checkout-page">
      <div className="container">
        <CheckoutSteps step={2} />
        <h1 className="checkout-title">بررسی و ثبت سفارش</h1>
        <div className="checkout-layout">
          <div className="checkout-main">
            <AddressCard complete={addressComplete} profile={profile.data} loading={profile.loading} />
            <OrderItems items={cart.items} totalCount={cart.total_count} />
          </div>
          <aside className="checkout-aside">
            <TotalCard cart={cart} placing={placing} error={error} onPlace={handlePay} />
          </aside>
        </div>
      </div>
    </main>
  );
}

export default function CheckoutPage() {
  useDocumentTitle("ثبت سفارش");
  const state = useApi(checkoutApi.summary);
  // The saved address is only shown; if it cannot be loaded the order can still be placed.
  const profile = useApi(customerApi.profile);

  if (state.loading && !state.data) return <CheckoutSkeleton />;
  if (state.error) {
    return (
      <main className="page checkout-page">
        <LoadError error={state.error} onRetry={state.reload} />
      </main>
    );
  }
  return <CheckoutContent summary={state.data} profile={profile} />;
}
