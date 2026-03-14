/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://amarigom-roller-e02bak03n-andreas-projects-71d69b69.vercel.app/api/:path*',
      },
    ];
  },
};

export default nextConfig;