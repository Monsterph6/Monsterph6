import { App as AntApp, ConfigProvider } from "antd";
import viVN from "antd/locale/vi_VN";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App";
import { AuthProvider } from "./auth/AuthContext";
import { QueryProvider } from "./api/QueryProvider";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ConfigProvider locale={viVN}>
      <AntApp>
        <QueryProvider>
          <BrowserRouter>
            <AuthProvider>
              <App />
            </AuthProvider>
          </BrowserRouter>
        </QueryProvider>
      </AntApp>
    </ConfigProvider>
  </StrictMode>,
);
