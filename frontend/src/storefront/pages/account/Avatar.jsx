import { useState } from "react";
import { toRelativeUrl } from "../../format";

/** First letter of the customer's first name (or of the username, without the "@"). */
function initialOf(profile) {
  const source = (profile.first_name || profile.username || "").replace(/^@/, "").trim();
  return source ? [...source][0] : "?";
}

/**
 * Profile picture, or a circle with the initial when there is no picture.
 * `src` overrides the saved picture (the live preview of an upload).
 */
export default function Avatar({ profile, src, size = "md", testId }) {
  const [failedUrl, setFailedUrl] = useState("");
  const url = src ?? (profile.customer_image ? toRelativeUrl(profile.customer_image) : "");
  const showPicture = url && url !== failedUrl;

  return (
    <span className={`account-avatar account-avatar--${size}`} data-testid={testId}>
      {showPicture ? (
        <img src={url} alt="" width="96" height="96" onError={() => setFailedUrl(url)} />
      ) : (
        <span aria-hidden="true">{initialOf(profile)}</span>
      )}
    </span>
  );
}
