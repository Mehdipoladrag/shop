import { useState } from "react";
import { ChevronLeft, ChevronRight, ImageOff } from "lucide-react";
import { toRelativeUrl } from "../../format";

const PICTURE_SIZE = 640;
const THUMB_SIZE = 96;

/** Large picture on a tinted tile, with clickable thumbnails when the product has more than one picture. */
export default function Gallery({ product }) {
  const [active, setActive] = useState(0);
  const sources = product.images?.length ? product.images : [product.pic];
  const images = sources.filter(Boolean).map(toRelativeUrl);
  const count = images.length;
  const current = Math.min(active, Math.max(count - 1, 0));
  const step = (offset) => setActive((current + offset + count) % count);

  return (
    <div className="product-media" data-testid="product-gallery">
      <div className="product-media__stage" data-testid="product-gallery-main">
        {count === 0 ? (
          <span className="product-media__empty">
            <ImageOff size={48} aria-hidden="true" />
            <span>تصویری برای این محصول ثبت نشده است.</span>
          </span>
        ) : (
          <img
            key={images[current]}
            className="product-media__image"
            src={images[current]}
            alt={product.product_name}
            width={PICTURE_SIZE}
            height={PICTURE_SIZE}
            decoding="async"
            fetchpriority="high"
          />
        )}

        {count > 1 && (
          <>
            <button type="button" className="product-media__arrow product-media__arrow--prev" aria-label="تصویر قبلی" onClick={() => step(-1)} data-testid="product-gallery-prev">
              <ChevronRight size={22} aria-hidden="true" />
            </button>
            <button type="button" className="product-media__arrow product-media__arrow--next" aria-label="تصویر بعدی" onClick={() => step(1)} data-testid="product-gallery-next">
              <ChevronLeft size={22} aria-hidden="true" />
            </button>
          </>
        )}
      </div>

      {count > 1 && (
        <>
          <p className="visually-hidden" role="status">
            تصویر {current + 1} از {count}
          </p>
          <ul className="product-media__thumbs" aria-label="تصاویر محصول" data-testid="product-gallery-thumbs">
            {images.map((image, position) => (
              <li key={image}>
                <button
                  type="button"
                  className={`product-media__thumb${position === current ? " is-active" : ""}`}
                  aria-label={`نمایش تصویر ${position + 1} از ${count}`}
                  aria-current={position === current ? "true" : undefined}
                  onClick={() => setActive(position)}
                  data-testid={`product-thumb-${position}`}
                >
                  <img src={image} alt="" width={THUMB_SIZE} height={THUMB_SIZE} loading="lazy" decoding="async" />
                </button>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
