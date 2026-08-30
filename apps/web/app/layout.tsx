import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Travel Scanner｜完整旅程比價",
  description: "同時比較機票、住宿、交通與活動，找出真正適合你的旅程。",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh-Hant">
      <body>{children}</body>
    </html>
  );
}

