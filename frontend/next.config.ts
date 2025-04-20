import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: 'standalone',
  // Specify trusted hosts to allow API requests (when needed)
  images: {
    domains: ['localhost'],
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
