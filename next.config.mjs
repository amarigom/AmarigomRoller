/** @type {import('next').NextConfig} */
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Desactivamos el modo estricto de React para evitar doble render en dev si querés
  reactStrictMode: false,
  
  async rewrites() {
    return {
      beforeFiles: [
        {
          source: '/api/:path*',
          destination: 'http://127.0.0.1:5000/api/:path*',
        },
      ],
    }
  },
}

export default nextConfig
