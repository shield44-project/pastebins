import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Online Code Runner - C, C++, Python",
  description: "Compile and run C, C++, and Python code online with intelligent compilation and zero warnings",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
