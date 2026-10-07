import { useCallback, useEffect, useRef, useState } from "react";

const SWIPE_THRESHOLD_PX = 40;

/** Number of items shown at the given screen width, from a `{minWidth: items}` map. */
function itemsForWidth(responsive, screenWidth) {
  const matching = Object.keys(responsive)
    .map(Number)
    .filter((minWidth) => minWidth <= screenWidth)
    .sort((a, b) => b - a);
  return responsive[matching[0] ?? 0] ?? { items: 1 };
}

/**
 * Right-to-left carousel that renders the same markup as Owl Carousel, so the
 * existing Owl stylesheet (`owl-theme`, `owl-nav`, `owl-dots`) styles it.
 *
 * `responsive` maps a minimum screen width to `{items, slideBy?, dots?}`.
 */
export default function Carousel({
  children,
  className = "",
  responsive = { 0: { items: 1 } },
  margin = 0,
  nav = false,
  navText,
  dots = false,
  loop = false,
  autoplay = false,
  autoplayTimeout = 5000,
}) {
  const slides = Array.isArray(children) ? children : [children];
  const outerRef = useRef(null);
  const [width, setWidth] = useState(0);
  const [screenWidth, setScreenWidth] = useState(window.innerWidth);
  const [index, setIndex] = useState(0);
  const [paused, setPaused] = useState(false);
  const swipeStart = useRef(null);

  useEffect(() => {
    const element = outerRef.current;
    const update = () => {
      setWidth(element.clientWidth);
      setScreenWidth(window.innerWidth);
    };
    update();
    const observer = new ResizeObserver(update);
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  const { items, slideBy = 1, dots: showDotsHere = dots } = itemsForWidth(responsive, screenWidth);
  const maxIndex = Math.max(0, slides.length - items);
  const currentIndex = Math.min(index, maxIndex);

  const goTo = useCallback(
    (target) => {
      if (target > maxIndex) setIndex(loop ? 0 : maxIndex);
      else if (target < 0) setIndex(loop ? maxIndex : 0);
      else setIndex(target);
    },
    [maxIndex, loop]
  );

  useEffect(() => {
    if (!autoplay || paused || maxIndex === 0) return undefined;
    const timer = setInterval(() => goTo(currentIndex + slideBy), autoplayTimeout);
    return () => clearInterval(timer);
  }, [autoplay, paused, maxIndex, currentIndex, slideBy, autoplayTimeout, goTo]);

  const itemWidth = width / items - margin;
  const step = itemWidth + margin;
  const dotCount = maxIndex + 1;

  const handlePointerDown = (event) => {
    swipeStart.current = event.clientX;
  };
  const handlePointerUp = (event) => {
    if (swipeStart.current === null) return;
    const distance = event.clientX - swipeStart.current;
    swipeStart.current = null;
    // In right-to-left layout, dragging right reveals the next items.
    if (Math.abs(distance) > SWIPE_THRESHOLD_PX) goTo(currentIndex + (distance > 0 ? slideBy : -slideBy));
  };

  const [prevText, nextText] = navText ?? [
    <i key="prev" className="now-ui-icons arrows-1_minimal-right" />,
    <i key="next" className="now-ui-icons arrows-1_minimal-left" />,
  ];

  return (
    <div
      className={`owl-carousel owl-theme owl-loaded owl-rtl owl-drag ${className}`}
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
    >
      <div className="owl-stage-outer" ref={outerRef} onPointerDown={handlePointerDown} onPointerUp={handlePointerUp}>
        <div
          className="owl-stage"
          style={{
            transform: `translate3d(${currentIndex * step}px, 0px, 0px)`,
            transition: "all 0.4s ease",
            width: step * slides.length,
          }}
        >
          {slides.map((slide, position) => (
            <div
              key={slide.key ?? position}
              className={`owl-item${position >= currentIndex && position < currentIndex + items ? " active" : ""}`}
              style={{ width: itemWidth, marginLeft: margin }}
            >
              {slide}
            </div>
          ))}
        </div>
      </div>

      {nav && maxIndex > 0 && (
        <div className="owl-nav">
          <button type="button" className="owl-prev" aria-label="قبلی" onClick={() => goTo(currentIndex - slideBy)}>
            {prevText}
          </button>
          <button type="button" className="owl-next" aria-label="بعدی" onClick={() => goTo(currentIndex + slideBy)}>
            {nextText}
          </button>
        </div>
      )}

      {showDotsHere && dotCount > 1 && (
        <div className="owl-dots">
          {Array.from({ length: dotCount }, (_, position) => (
            <button
              key={position}
              type="button"
              aria-label={`اسلاید ${position + 1}`}
              className={`owl-dot${position === currentIndex ? " active" : ""}`}
              onClick={() => goTo(position)}
            >
              <span />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
