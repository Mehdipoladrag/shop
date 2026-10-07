import { Navigate, Outlet, useLocation } from "react-router-dom";
import { Loading } from "../components/States";
import { useAuth } from "./AuthContext";

/** Sends visitors who are not logged in to the login page, then back here. */
export default function RequireAuth() {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) return <Loading />;
  if (!isAuthenticated) return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  return <Outlet />;
}
