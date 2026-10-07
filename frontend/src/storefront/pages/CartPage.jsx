import { useState } from "react";
import { Link } from "react-router-dom";
import { useCart } from "../cart/CartContext";
import { staticUrl } from "../config";
import { formatPrice, toRelativeUrl } from "../format";

const QUANTITY_OPTIONS = Array.from({ length: 9 }, (_, index) => index + 1);

function EmptyCart() {
  return (
    <main className="cart default">
      <div className="container text-center cart_empty">
        <img src={staticUrl("img/empty-cart.png")} alt="" />
        <h6>سبد خرید شما در حال حاضر خالی است.</h6>
        <Link to="/" className="btn btn-main-masai">
          صفحه نخست
        </Link>
      </div>
    </main>
  );
}

function CartRow({ item, onChangeCount, onRemove }) {
  const { product } = item;
  const hasOffer = Boolean(product.offer);

  return (
    <tr className="cart_item">
      <td>
        <img src={toRelativeUrl(product.pic)} alt={product.product_name} />
        <a
          href="#remove"
          aria-label={`حذف ${product.product_name} از سبد`}
          onClick={(event) => {
            event.preventDefault();
            onRemove(product.id);
          }}
        >
          <i className="fa fa-times" aria-hidden="true" />
        </a>
      </td>
      <td>
        <h3 className="cart_title">
          <Link to={`/products/${product.slug}`}>{product.product_name}</Link>
        </h3>
        <div className="cart_content">
          <div>
            <span>برند </span>
            <span className="item_property">{product.brand}</span>
          </div>
          <span className="cart_divider" />
          <div>
            <span>رنگ </span>
            <span className="item_property">{item.product_color}</span>
          </div>
        </div>
      </td>
      <td>
        <div className="cart_price">
          {hasOffer && (
            <del>
              <span>
                {formatPrice(product.price)}
                <span>تومان</span>
              </span>
            </del>
          )}
          {hasOffer ? (
            <ins>
              <span>
                {formatPrice(item.unit_price)}
                <span>تومان</span>
              </span>
            </ins>
          ) : (
            <>
              {formatPrice(item.unit_price)} <span>تومان</span>
            </>
          )}
        </div>
      </td>
      <td>
        <select
          value={item.product_count}
          aria-label={`تعداد ${product.product_name}`}
          onChange={(event) => onChangeCount(product.id, Number(event.target.value))}
        >
          {QUANTITY_OPTIONS.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </td>
      <td className="price_alltd">
        {formatPrice(item.total_price)} <span>تومان</span>
      </td>
    </tr>
  );
}

export default function CartPage() {
  const { cart, loaded, setItemCount, removeItem } = useCart();
  const [error, setError] = useState("");

  async function run(action) {
    setError("");
    try {
      await action();
    } catch {
      setError("به‌روزرسانی سبد خرید انجام نشد. دوباره تلاش کنید.");
    }
  }

  if (!loaded) return null;
  if (cart.items.length === 0) return <EmptyCart />;

  return (
    <main className="cart-page default space-top-30">
      <div className="container">
        <div className="row">
          <div className="col-12 text-center">
            <ul className="order-steps">
              <li>
                <a href="/cart" className="active" onClick={(event) => event.preventDefault()}>
                  <span>سبدخرید</span>
                </a>
              </li>
              <li>
                <a href="/cart" onClick={(event) => event.preventDefault()}>
                  <span>پرداخت</span>
                </a>
              </li>
              <li>
                <a href="/cart" onClick={(event) => event.preventDefault()}>
                  <span>اتمام خرید و ارسال</span>
                </a>
              </li>
            </ul>
          </div>

          <div className="cart_content col-xl-12 col-lg-12 col-md-12">
            <header className="card-header">
              <h3 className="card-title">
                <span>سبد خرید شما</span>
              </h3>
            </header>
            {error && (
              <p className="txt_note" role="alert">
                {error}
              </p>
            )}
            <div className="table-responsive default">
              <table className="table">
                <thead>
                  <tr>
                    <th scope="col">محصول</th>
                    <th scope="col">سبد خرید شما</th>
                    <th scope="col">قیمت واحد</th>
                    <th scope="col">تعداد</th>
                    <th scope="col">قیمت نهایی</th>
                  </tr>
                </thead>
                <tbody>
                  {cart.items.map((item) => (
                    <CartRow
                      key={item.product.id}
                      item={item}
                      onChangeCount={(id, count) => run(() => setItemCount(id, count))}
                      onRemove={(id) => run(() => removeItem(id))}
                    />
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="cart-page-content col-xl-12 col-lg-12 col-md-12">
            <div className="row cart_details">
              <div className="cart-page-content col-xl-8 col-lg-7 col-md-7">
                <div className="text_details">
                  <p>ارسال رایگان برای سفارش‌های بالای 1 میلیون و 400 هزار تومان</p>
                  <p>
                    افزودن کالا به سبد خرید به معنی رزرو آن نیست با توجه به محدودیت موجودی سبد خود را ثبت و خرید را
                    نهایی کنید.
                  </p>
                </div>
              </div>
              <div className="cart-page-aside col-xl-4 col-lg-5 col-md-5 divider_details">
                <table className="table table_details">
                  <tbody>
                    <tr>
                      <td>تعداد کالا:</td>
                      <td>{cart.total_count}</td>
                    </tr>
                    <tr>
                      <td>بسته‌بندی و ارسال:</td>
                      <td>وابسته به نوع ارسال</td>
                    </tr>
                    <tr className="all">
                      <td>قیمت قابل پرداخت:</td>
                      <td>
                        {formatPrice(cart.total_price)} <span>تومان</span>
                      </td>
                    </tr>
                    <tr>
                      <td colSpan="2">
                        <Link to="/checkout" className="btn big_btn btn-main-masai">
                          گام بعدی
                        </Link>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
