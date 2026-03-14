/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://amarigomroller-backend-test.onrender.com/api/:path*',
      },
    ];
  },
};

export default nextConfig;