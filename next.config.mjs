// next.config.mjs
/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        // Cuando el frontend pida /api/inventario, 
        // Next.js lo redirige al servidor de Flask
        source: '/api/:path*',
        destination: 'http://127.0.0.1:5000/api/:path*', 
      },
    ];
  },
};

export default nextConfig;