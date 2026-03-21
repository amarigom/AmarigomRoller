/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: { ignoreBuildErrors: true },
  eslint: { ignoreDuringBuilds: true },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        // Si estamos en Vercel, usa la URL del backend. Si no, usa localhost.
        destination: process.env.NODE_ENV === 'production' 
          ? 'https://amarigom-roller.vercel.app/api/:path*' 
          : 'http://localhost:5000/api/:path*',
      },
    ];
  },
};

export default nextConfig;