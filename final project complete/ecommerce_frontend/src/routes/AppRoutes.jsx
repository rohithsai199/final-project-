import { Component, lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from "../components/layout/MainLayout";
import ProtectedRoute from "./ProtectedRoute";
import AdminRoute from "./AdminRoute";

function lazyWithRetry(factory) {
  return lazy(async () => {
    try {
      return await factory();
    } catch (err) {
      const msg = String(err?.message || "");
      if (
        msg.includes("Failed to fetch dynamically imported module") ||
        msg.includes("Importing a module script failed") ||
        msg.includes("text/html")
      ) {
        const retryKey = "chunk_preload_retried";
        if (typeof window !== "undefined" && !sessionStorage.getItem(retryKey)) {
          sessionStorage.setItem(retryKey, "true");
          window.location.reload();
          return new Promise(() => {});
        }
      }
      throw err;
    }
  });
}

class AppErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div
          style={{
            minHeight: "100vh",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            padding: "24px",
            fontFamily: "inherit",
            textAlign: "center",
          }}
        >
          <h2 style={{ fontSize: "22px", fontWeight: "700", marginBottom: "8px" }}>
            New Store Update Ready
          </h2>
          <p style={{ color: "#666", marginBottom: "20px", maxWidth: "420px", fontSize: "14px", lineHeight: "1.5" }}>
            A new version of ARISE was just published. Click the button below to load the latest release.
          </p>
          <button
            onClick={() => {
              sessionStorage.removeItem("chunk_preload_retried");
              window.location.reload();
            }}
            style={{
              padding: "12px 28px",
              background: "#111",
              color: "#fff",
              borderRadius: "9999px",
              border: "none",
              cursor: "pointer",
              fontWeight: "600",
              fontSize: "14px",
            }}
          >
            Reload Store
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// Code splitting / lazy loading routes for optimal Lighthouse performance
const Home = lazyWithRetry(() => import("../pages/Home/Home"));
const Products = lazyWithRetry(() => import("../pages/Products/Products"));
const ProductDetails = lazyWithRetry(() =>
  import("../pages/ProductDetails/ProductDetails")
);
const Cart = lazyWithRetry(() => import("../pages/Cart/Cart"));
const Checkout = lazyWithRetry(() => import("../pages/Checkout/Checkout"));
const Orders = lazyWithRetry(() => import("../pages/Orders/Orders"));
const OrderDetails = lazyWithRetry(() => import("../pages/Orders/OrderDetails"));
const Login = lazyWithRetry(() => import("../pages/Login/Login"));
const Register = lazyWithRetry(() => import("../pages/Register/Register"));
const Admin = lazyWithRetry(() => import("../pages/Admin/Admin"));

function RouteLoadingFallback() {
  return (
    <div
      style={{
        minHeight: "50vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div className="modern-spinner"></div>
    </div>
  );
}

function AppRoutes() {
  return (
    <AppErrorBoundary>
      <BrowserRouter>
        <Suspense fallback={<RouteLoadingFallback />}>
        <Routes>
          <Route element={<MainLayout />}>
            {/* Public pages */}
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<Products />} />
            <Route
              path="/products/:productId"
              element={<ProductDetails />}
            />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected pages */}
            <Route element={<ProtectedRoute />}>
              <Route path="/cart" element={<Cart />} />
              <Route path="/checkout" element={<Checkout />} />
              <Route path="/orders" element={<Orders />} />
              <Route
                path="/orders/:orderId"
                element={<OrderDetails />}
              />

              {/* Admin-only pages */}
              <Route element={<AdminRoute />}>
                <Route path="/admin" element={<Admin />} />
              </Route>
            </Route>
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  </AppErrorBoundary>
);
}

export default AppRoutes;
