import { createRoot } from "react-dom/client";
import { createBrowserRouter, Outlet } from "react-router";
import { RouterProvider } from "react-router";

// Page Components
import App from "../App.jsx";
import Books from "../pages/Books.jsx";
import Profile from "../pages/Profile.jsx";
import MainLayout from "../pages/MainLayout.jsx";

export let router = createBrowserRouter([
  {
    path: "",
    element: <App />,
    children: [
      {
        index: true,
        path: "",
        element: <MainLayout />,
      },
      {
        path: "profile",
        element: <Profile />,
      },
      {
        path: "books",
        element: <Books />,
      },
    ],
  },
]);
