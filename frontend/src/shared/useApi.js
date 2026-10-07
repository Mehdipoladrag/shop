import { useCallback, useEffect, useRef, useState } from "react";

/**
 * Loads data from an API function and exposes loading and error state.
 * `reload` refetches; the latest request always wins so stale responses
 * (for example from a fast-typed search) never overwrite newer data.
 */
export function useApi(fetcher, deps = []) {
  const [state, setState] = useState({ data: null, error: null, loading: true });
  const requestId = useRef(0);

  const load = useCallback(() => {
    const currentId = ++requestId.current;
    setState((previous) => ({ ...previous, loading: true, error: null }));

    return fetcher()
      .then((data) => {
        if (currentId === requestId.current) setState({ data, error: null, loading: false });
      })
      .catch((error) => {
        if (currentId === requestId.current) setState({ data: null, error, loading: false });
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    load();
  }, [load]);

  return { ...state, reload: load };
}
