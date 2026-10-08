import { Link } from "react-router-dom";
import { CalendarDays, UserRound } from "lucide-react";
import { BRAND } from "../../../shared/brand";
import Carousel from "../../components/Carousel";
import SectionHeader from "../../components/SectionHeader";
import { formatJalaliDate, toRelativeUrl } from "../../format";
import { RowSkeleton, SectionError } from "./SectionStates";

function PostCard({ post }) {
  const url = `/blog/${post.slug}`;
  return (
    <article className="home-post" data-testid="home-post-card">
      <Link to={url} className="home-post__media" tabIndex={-1} aria-hidden="true">
        {post.blog_image && <img src={toRelativeUrl(post.blog_image)} alt="" width="640" height="400" loading="lazy" decoding="async" />}
        {post.category && <span className="badge home-post__badge">{post.category}</span>}
      </Link>
      <div className="home-post__body">
        <h3 className="home-post__title">
          <Link to={url}>{post.blog_name}</Link>
        </h3>
        <div className="home-post__meta">
          <span>
            <UserRound size={16} aria-hidden="true" />
            {post.author}
          </span>
          <span>
            <CalendarDays size={16} aria-hidden="true" />
            {formatJalaliDate(post.create_date)}
          </span>
        </div>
      </div>
    </article>
  );
}

/** Latest blog posts as a carousel of cards. */
export default function BlogSection({ state }) {
  const posts = state.data?.results ?? [];
  const loading = state.loading && !state.data;
  if (!loading && !state.error && posts.length === 0) return null;

  let content;
  if (state.error) {
    content = <SectionError error={state.error} onRetry={state.reload} testId="home-blog-error" />;
  } else if (loading) {
    content = <RowSkeleton variant="posts" count={4} itemClassName="home-skeleton__post" />;
  } else {
    content = (
      <Carousel variant="posts" label="مطالب وبلاگ">
        {posts.map((post) => (
          <PostCard post={post} key={post.id} />
        ))}
      </Carousel>
    );
  }

  return (
    <section className="section" data-testid="home-blog">
      <SectionHeader title={`${BRAND.name} مگ`} to="/blog" linkLabel="مشاهده همه مطالب" />
      {content}
    </section>
  );
}
