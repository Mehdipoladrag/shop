import { Link, useParams, useSearchParams } from "react-router-dom";
import { ArrowRight, CalendarDays, Clock, FileText, User } from "lucide-react";
import { blogApi } from "../api/endpoints";
import { ApiError } from "../api/client";
import { useApi } from "../../shared/useApi";
import { BRAND } from "../../shared/brand";
import { formatJalaliDate, toRelativeUrl } from "../format";
import Breadcrumb from "../components/Breadcrumb";
import Pagination from "../components/Pagination";
import SectionHeader from "../components/SectionHeader";
import { AsyncContent, EmptyState, NotFound } from "../components/States";
import { useDocumentTitle } from "../components/useDocumentTitle";
import PostCard from "./content/PostCard";
import "./content.css";

const BLOG_PAGE_SIZE = 6;
const RELATED_POSTS = 3;
const WORDS_PER_MINUTE = 180;

function CategoryChips({ active }) {
  const categories = useApi(blogApi.categories);
  return (
    <nav className="chips" aria-label="دسته‌بندی مطالب" data-testid="blog-categories" data-allow-overflow>
      <Link to="/blog" className="chip" aria-current={active ? undefined : "page"} data-testid="blog-category-all">
        همه مطالب
      </Link>
      {(categories.data ?? []).map((category) => (
        <Link
          key={category.id}
          to={`/blog?category=${category.slug}`}
          className="chip"
          aria-current={active === category.slug ? "page" : undefined}
          data-testid="blog-category-chip"
        >
          {category.name}
        </Link>
      ))}
    </nav>
  );
}

export function BlogListPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const page = Number(searchParams.get("page")) || 1;
  const category = searchParams.get("category") ?? "";
  useDocumentTitle("وبلاگ");

  const posts = useApi(() => blogApi.posts({ page, category }), [page, category]);

  function changePage(target) {
    const next = new URLSearchParams(searchParams);
    next.set("page", String(target));
    setSearchParams(next);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <main className="page" data-testid="blog-page">
      <div className="container">
        <Breadcrumb items={[{ label: "وبلاگ" }]} />
        <header className="blog-header">
          <h1>وبلاگ {BRAND.name}</h1>
          <p>راهنمای خرید، مقایسه و نکته‌های کاربردی درباره‌ی گوشی، تبلت و لوازم دیجیتال</p>
        </header>
        <CategoryChips active={category} />

        <AsyncContent state={posts} variant="grid">
          {({ results, count }) =>
            results.length === 0 ? (
              <EmptyState icon={FileText} title="وبلاگی وجود ندارد" text="هنوز مطلبی در این دسته منتشر نشده است.">
                <Link to="/blog" className="btn btn--primary">
                  همه مطالب
                </Link>
              </EmptyState>
            ) : (
              <>
                <div className="post-grid">
                  {results.map((post) => (
                    <PostCard post={post} key={post.id} />
                  ))}
                </div>
                <Pagination page={page} pageCount={Math.ceil(count / BLOG_PAGE_SIZE)} onChange={changePage} />
              </>
            )
          }
        </AsyncContent>
      </div>
    </main>
  );
}

function RelatedPosts({ currentSlug }) {
  const latest = useApi(() => blogApi.posts({}));
  const related = (latest.data?.results ?? []).filter((post) => post.slug !== currentSlug).slice(0, RELATED_POSTS);
  if (related.length === 0) return null;

  return (
    <section className="section">
      <SectionHeader title="مطالب مرتبط" to="/blog" linkLabel="همه مطالب" />
      <div className="post-grid">
        {related.map((post) => (
          <PostCard post={post} key={post.id} headingLevel={3} />
        ))}
      </div>
    </section>
  );
}

const readingMinutes = (text) => Math.max(1, Math.ceil(String(text).split(/\s+/).filter(Boolean).length / WORDS_PER_MINUTE));

function PostArticle({ post }) {
  const paragraphs = String(post.blog_description).split(/\n{2,}/).filter((paragraph) => paragraph.trim());

  return (
    <>
      <Breadcrumb
        items={[
          { label: "وبلاگ", to: "/blog" },
          { label: post.category, to: `/blog?category=${post.category_slug}` },
          { label: post.blog_name },
        ]}
      />
      <article className="blog-post" data-testid="blog-post-page">
        <header className="blog-post__header">
          <Link to={`/blog?category=${post.category_slug}`} className="badge">
            {post.category}
          </Link>
          <h1>{post.blog_name}</h1>
          <div className="blog-post__meta">
            <span>
              <User size={16} aria-hidden="true" /> ارسال شده توسط <bdi>{post.author}</bdi>
            </span>
            <span>
              <CalendarDays size={16} aria-hidden="true" /> {formatJalaliDate(post.create_date)}
            </span>
            <span>
              <Clock size={16} aria-hidden="true" /> زمان مطالعه: {readingMinutes(post.blog_description)} دقیقه
            </span>
          </div>
        </header>

        <figure className="blog-post__cover">
          <img src={toRelativeUrl(post.blog_image)} alt={post.blog_name} width="1200" height="640" />
        </figure>

        <div className="prose blog-post__body">
          {paragraphs.map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </div>

        <Link to="/blog" className="btn btn--secondary blog-post__back">
          <ArrowRight size={18} aria-hidden="true" /> بازگشت به وبلاگ
        </Link>
      </article>
      <RelatedPosts currentSlug={post.slug} />
    </>
  );
}

export function BlogDetailPage() {
  const { slug } = useParams();
  const state = useApi(() => blogApi.post(slug), [slug]);
  useDocumentTitle(state.data?.blog_name);

  if (state.error instanceof ApiError && state.error.status === 404) return <NotFound />;

  return (
    <main className="page">
      <div className="container">
        <AsyncContent state={state}>{(post) => <PostArticle post={post} />}</AsyncContent>
      </div>
    </main>
  );
}
