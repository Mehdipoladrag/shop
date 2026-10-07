import { Link, useParams, useSearchParams } from "react-router-dom";
import { blogApi } from "../api/endpoints";
import { useApi } from "../../shared/useApi";
import { formatJalaliDate, toRelativeUrl } from "../format";
import Pagination from "../components/Pagination";
import { AsyncContent, NotFound } from "../components/States";
import { ApiError } from "../api/client";

const BLOG_PAGE_SIZE = 6;
const LATEST_POSTS_LIMIT = 6;

function Breadcrumb({ items }) {
  return (
    <div className="col-12">
      <nav>
        <ul className="breadcrumb">
          <Link to="/">
            <li>
              <i className="fa fa-home" aria-hidden="true" />
            </li>
          </Link>
          {items.map((item) => (
            <li key={item}>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}

function Sidebar() {
  const categories = useApi(blogApi.categories);
  const latest = useApi(() => blogApi.posts({ page_size: LATEST_POSTS_LIMIT }));

  return (
    <div className="col-12 col-lg-3">
      <div className="sidebar_blog">
        <div className="widget_blog">
          <div className="widget_blog_headbox">
            <h3>دسته بندی ها</h3>
          </div>
          <div className="blog_list_widget_blog">
            <div className="widget_blog_groups">
              {(categories.data ?? []).map((category) => (
                <ul className="widget_blog_posts" key={category.id}>
                  <li>
                    <Link className="widget_blog_title_link" to={`/blog?category=${category.slug}`}>
                      {category.name}
                    </Link>
                  </li>
                </ul>
              ))}
            </div>
          </div>
        </div>
        <div className="widget_blog marg_top20">
          <div className="widget_blog_headbox">
            <h3>آخرین مقالات</h3>
          </div>
          <div className="blog_list_widget_blog">
            <div className="widget_blog_groups">
              <ul className="widget_blog_posts">
                {(latest.data?.results ?? []).map((post) => (
                  <li key={post.id}>
                    <Link className="widget_blog_title_link" to={`/blog/${post.slug}`}>
                      {post.blog_name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export function BlogListPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const page = Number(searchParams.get("page")) || 1;
  const category = searchParams.get("category") ?? "";

  const posts = useApi(() => blogApi.posts({ page, category }), [page, category]);

  function changePage(target) {
    const next = new URLSearchParams(searchParams);
    next.set("page", String(target));
    setSearchParams(next);
  }

  return (
    <main className="category-blog default space-top-30">
      <div className="container">
        <div className="row">
          <Breadcrumb items={["وبلاگ", "اخبار روز تکنولوژی"]} />
          <div className="single_blog_content cat_blog_content col-12 col-lg-9 mx-auto order-1 order-sm-1">
            <AsyncContent state={posts}>
              {({ results, count }) => (
                <div className="row listing-items Blog-category">
                  {results.map((post) => (
                    <div className="col-xl-6 col-lg-6 col-md-6 col-12" key={post.id}>
                      <div className="blog_tag">
                        <Link to={`/blog/${post.slug}`}>
                          <img src={toRelativeUrl(post.blog_image)} className="img-fluid" alt={post.blog_name} />
                        </Link>
                        <Link to={`/blog/${post.slug}`}>
                          <h2 className="Blog_title">{post.blog_name}</h2>
                        </Link>
                        <div className="Blog_list">
                          <span className="Blog_author">
                            <i className="fa fa-user" /> {post.author}
                          </span>
                          <span className="Blog_Date">
                            <i className="fa fa-calendar" /> {formatJalaliDate(post.create_date, { withTime: true })}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                  {results.length === 0 && <h3 style={{ color: "var(--color-primary)", padding: 120 }}>وبلاگی وجود ندارد</h3>}
                  <div className="row">
                    <div className="col-sm-9 padding-right">
                      <Pagination page={page} pageCount={Math.ceil(count / BLOG_PAGE_SIZE)} onChange={changePage} />
                    </div>
                  </div>
                </div>
              )}
            </AsyncContent>
          </div>
          <Sidebar />
        </div>
      </div>
    </main>
  );
}

export function BlogDetailPage() {
  const { slug } = useParams();
  const state = useApi(() => blogApi.post(slug), [slug]);

  if (state.error instanceof ApiError && state.error.status === 404) return <NotFound />;

  return (
    <main className="cart-page default">
      <div className="container">
        <div className="row">
          <div className="single_blog_content col-12 col-lg-9 mx-auto order-1 order-sm-1">
            <AsyncContent state={state}>
              {(post) => (
                <>
                  <header className="card-header">
                    <h3 className="card-title">
                      <span>{post.blog_name}</span>
                    </h3>
                  </header>
                  <div className="single_blog_page">
                    <div className="single_blog_box_content">
                      <div className="form-account">
                        <div className="row">
                          <div className="col-md-12 col-sm-12">
                            <img src={toRelativeUrl(post.blog_image)} alt={post.blog_name} />
                            <div className="data_det">
                              <span className="publish_date">
                                <i className="fa fa-clock" /> {formatJalaliDate(post.create_date, { withTime: true })}
                              </span>
                              <span className="author">
                                <i className="fa fa-user-alt" /> ارسال شده توسط {post.author}
                              </span>
                              <span className="categoey">
                                <i className="fa fa-folder" /> {post.category}
                              </span>
                            </div>
                            <p style={{ whiteSpace: "pre-line" }}>{post.blog_description}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </AsyncContent>
          </div>
          <Sidebar />
        </div>
      </div>
    </main>
  );
}
