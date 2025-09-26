#!/bin/bash

# SynthAI Frontend Build Script
# Usage: ./scripts/build.sh [environment]

set -e

ENVIRONMENT=${1:-production}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
VERSION=${VERSION:-1.0.0}

echo "🏗️  Building SynthAI Frontend for $ENVIRONMENT environment"
echo "📦 Version: $VERSION"
echo "⏰ Timestamp: $TIMESTAMP"

# Create build directory
BUILD_DIR="build_${ENVIRONMENT}_${TIMESTAMP}"
echo "📁 Creating build directory: $BUILD_DIR"

# Install dependencies
echo "📦 Installing dependencies..."
npm ci --silent

# Create environment file
echo "🔧 Creating environment configuration..."
cat > .env.${ENVIRONMENT} << EOF
REACT_APP_API_URL=${REACT_APP_API_URL:-http://localhost:8000}
REACT_APP_STRIPE_PUBLISHABLE_KEY=${REACT_APP_STRIPE_PUBLISHABLE_KEY}
REACT_APP_VERSION=${VERSION}
REACT_APP_ENVIRONMENT=${ENVIRONMENT}
REACT_APP_BUILD_TIMESTAMP=${TIMESTAMP}
EOF

# Build the application
echo "🔨 Building application..."
npm run build

# Move build to versioned directory
mv build $BUILD_DIR

# Create build info file
cat > ${BUILD_DIR}/build-info.json << EOF
{
  "version": "${VERSION}",
  "environment": "${ENVIRONMENT}",
  "timestamp": "${TIMESTAMP}",
  "gitCommit": "$(git rev-parse --short HEAD)",
  "buildTime": "$(date -Iseconds)"
}
EOF

# Create deployment package
echo "📦 Creating deployment package..."
tar -czf synthai-frontend-${ENVIRONMENT}-${VERSION}.tar.gz -C ${BUILD_DIR} .

# Generate checksum
echo "🔍 Generating checksum..."
sha256sum synthai-frontend-${ENVIRONMENT}-${VERSION}.tar.gz > synthai-frontend-${ENVIRONMENT}-${VERSION}.tar.gz.sha256

echo "✅ Build completed successfully!"
echo "📁 Build output: $BUILD_DIR"
echo "📦 Package: synthai-frontend-${ENVIRONMENT}-${VERSION}.tar.gz"
echo "🔍 Checksum: synthai-frontend-${ENVIRONMENT}-${VERSION}.tar.gz.sha256"

# Cleanup old builds (keep last 5)
echo "🧹 Cleaning up old builds..."
ls -td build_* | tail -n +6 | xargs rm -rf

echo "🎉 Build process completed!"
