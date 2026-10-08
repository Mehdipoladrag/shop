import { Link } from "react-router-dom";
import { CalendarDays, User } from "lucide-react";
import { formatJalaliDate, toRelativeUrl } from "../../format";

/** Blog post tile: picture with the category on it, title and author/date line. */
export default function PostCard({ post, headingLevel = 2 }) {
  const url = `/blog/${post.slug}`;
  const Heading = `h${headingLevel}`;

  return (
    <article className="post-card" data-testid="post-card">
      <Link to={url} className="post-card__media" tabIndex={-1} aria-hidden="true">
        <img src={toRelativeUrl(post.blog_image)} alt="" loading="lazy" decoding="async" width="640" height="400" />
        <span className="badge post-card__badge">{post.category}</span>
      </Link>
      <div className="post-card__body">
        <Heading className="post-card__title">
          <Link to={url}>{post.blog_name}</Link>
        </Heading>
        <div className="post-card__meta">
          <span>
            <User size={15} aria-hidden="true" /> <bdi>{post.author}</bdi>
          </span>
          <span>
            <CalendarDays size={15} aria-hidden="true" /> {formatJalaliDate(post.create_date)}
          </span>
        </div>
      </div>
    </article>
  );
}
