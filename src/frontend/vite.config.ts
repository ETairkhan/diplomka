/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// Frontend tests live in the repository folder tests/frontend.
// Packages are installed here, in src/frontend/node_modules.
const modules = path.resolve(__dirname, "node_modules");
const testsDir = path.resolve(__dirname, "../../tests/frontend");

export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        fs: { allow: [path.resolve(__dirname, "../..")] },
    },
    resolve: {
        alias: {
            "@testing-library": path.join(modules, "@testing-library"),
            "react-router-dom": path.join(modules, "react-router-dom"),
            "react-dom": path.join(modules, "react-dom"),
            "react": path.join(modules, "react"),
        },
    },
    test: {
        environment: "jsdom",
        dir: testsDir,
        include: ["**/*.test.tsx"],
        setupFiles: [path.join(testsDir, "setup.ts")],
    },
});
