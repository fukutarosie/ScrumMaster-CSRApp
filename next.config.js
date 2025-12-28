/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
  },
  // Disable static page generation for dynamic pages
  // This prevents build errors when pages try to fetch data during build time
  experimental: {
    missingSuspenseWithCSRBailout: false,
  },
}

module.exports = nextConfig