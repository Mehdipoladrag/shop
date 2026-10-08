import { Children, useCallback, useEffect, useRef, useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import "./Carousel.css";

const AUTOPLAY_MS = 6000;
const EDGE_TOLERANCE_PX = 4;
const PAGE_RATIO = 0.9;

const prefersReducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/**
 * Horizontal carousel built on CSS scroll snapping: touch swipe, mouse wheel
 * and keyboard scrolling work natively, buttons and dots only call scrollTo.
 *
 * `variant` sets how many items fit per screen width (see Carousel.css):
 * "cards" (products), "posts" (blog cards), "brands" and "hero" (one slide).
 */
export default function Carousel({ children, variant = "cards", label, autoplay = false, dots = false, arrows = true, className = "" }) {
  const trackRef = useRef(null);
  const [edge, setEdge] = useState({ atStart: true, atEnd: true });
  const [active, setActive] = useState(0);
  const [paused, setPaused] = useState(false);
  const items = Children.toArray(children);

  // In right-to-left layout the scroll offset runs into negative numbers.
  const direction = () => (getComputedStyle(trackRef.current).direction === "rtl" ? -1 : 1);

  const itemStep = useCallback(() => {
    const track = trackRef.current;
    const first = track?.firstElementChild;
    if (!first) return track?.clientWidth ?? 0;
    const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    return first.getBoundingClientRect().width + gap;
  }, []);

  const measure = useCallback(() => {
    const track = trackRef.current;
    if (!track) return;
    const offset = Math.abs(track.scrollLeft);
    const maxOffset = track.scrollWidth - track.clientWidth;
    setEdge({ atStart: offset <= EDGE_TOLERANCE_PX, atEnd: offset >= maxOffset - EDGE_TOLERANCE_PX });
    setActive(Math.round(offset / (itemStep() || 1)));
  }, [itemStep]);

  useEffect(() => {
    measure();
    const track = trackRef.current;
    const observer = new ResizeObserver(measure);
    observer.observe(track);
    return () => observer.disconnect();
  }, [measure, items.length]);

  const scrollToOffset = (offset) => trackRef.current.scrollTo({ left: direction() * offset, behavior: "smooth" });

  const scrollByPage = (sign) => {
    const track = trackRef.current;
    const page = variant === "hero" ? itemStep() : Math.max(itemStep(), track.clientWidth * PAGE_RATIO);
    track.scrollBy({ left: direction() * sign * page, behavior: "smooth" });
  };

  const goTo = (index) => scrollToOffset(index * itemStep());

  // Autoplay advances one item and starts over at the end.
  useEffect(() => {
    if (!autoplay || paused || items.length < 2 || prefersReducedMotion()) return undefined;
    const timer = setInterval(() => {
      if (document.hidden) return;
      const track = trackRef.current;
      const offset = Math.abs(track.scrollLeft);
      const atEnd = offset >= track.scrollWidth - track.clientWidth - EDGE_TOLERANCE_PX;
      if (atEnd) scrollToOffset(0);
      else scrollByPage(1);
    }, AUTOPLAY_MS);
    return () => clearInterval(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [autoplay, paused, items.length]);

  const scrollable = !(edge.atStart && edge.atEnd);

  return (
    <section
      className={`carousel carousel--${variant} ${className}`}
      aria-roledescription="carousel"
      aria-label={label}
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
      onFocus={() => setPaused(true)}
      onBlur={() => setPaused(false)}
      onTouchStart={() => setPaused(true)}
    >
      <div className="carousel__track" ref={trackRef} onScroll={measure} tabIndex={0}>
        {items.map((child, position) => (
          <div
            className="carousel__item"
            key={child.key ?? position}
            role="group"
            aria-roledescription="slide"
            aria-label={`${position + 1} از ${items.length}`}
          >
            {child}
          </div>
        ))}
      </div>

      {arrows && scrollable && (
        <>
          <button type="button" className="carousel__arrow carousel__arrow--prev" aria-label="قبلی" disabled={edge.atStart} onClick={() => scrollByPage(-1)}>
            <ChevronRight size={22} aria-hidden="true" />
          </button>
          <button type="button" className="carousel__arrow carousel__arrow--next" aria-label="بعدی" disabled={edge.atEnd} onClick={() => scrollByPage(1)}>
            <ChevronLeft size={22} aria-hidden="true" />
          </button>
        </>
      )}

      {dots && items.length > 1 && (
        <div className="carousel__dots">
          {items.map((child, position) => (
            <button
              key={child.key ?? position}
              type="button"
              aria-label={`اسلاید ${position + 1}`}
              aria-current={position === active ? "true" : undefined}
              className={`carousel__dot${position === active ? " is-active" : ""}`}
              onClick={() => goTo(position)}
            />
          ))}
        </div>
      )}
    </section>
  );
}
