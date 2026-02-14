import { createBrowserRouter } from "react-router-dom";
import { LoginPage } from "./pages/LoginPage";
import { CareerSetupPage } from "./pages/CareerSetupPage";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: LoginPage,
  },
  {
    path: "/setup",
    Component: CareerSetupPage,
  },
]);
