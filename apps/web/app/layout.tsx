import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000"),
  title: "Travel Scanner｜完整旅程比價",
  description: "同時比較機票、住宿、交通與活動，找出真正適合你的旅程。",
  openGraph: {
    title: "Travel Scanner｜完整旅程比價與最佳化",
    description: "一次比較機票、住宿、交通與活動，找出真正適合你的完整旅程。",
    images: [{ url: "/og.png", width: 1200, height: 630, alt: "Travel Scanner 完整旅程比價與最佳化" }],
    locale: "zh_TW",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Travel Scanner｜完整旅程比價與最佳化",
    description: "一次比較機票、住宿、交通與活動。",
    images: ["/og.png"],
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh-Hant">
      <body>{children}</body>
    </html>
  );
}
