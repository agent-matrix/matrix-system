/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  poweredByHeader: false,
  compress: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://api.matrixhub.io',
    NEXT_PUBLIC_MATRIX_AI_URL: process.env.NEXT_PUBLIC_MATRIX_AI_URL || 'https://huggingface.co/spaces/agent-matrix/matrix-ai',
    NEXT_PUBLIC_GUARDIAN_URL: process.env.NEXT_PUBLIC_GUARDIAN_URL || 'http://localhost:8080',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'https://api.matrixhub.io'}/:path*`,
      },
    ];
  },
};

export default nextConfig;
