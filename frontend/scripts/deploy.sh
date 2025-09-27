#!/bin/bash

# Add WhatsApp environment variables
echo "🔧 Configuring WhatsApp environment..."
cat > .env.production << EOF
REACT_APP_API_URL=https://api.synthai.co.za
REACT_APP_STRIPE_PUBLISHABLE_KEY=${REACT_APP_STRIPE_PUBLISHABLE_KEY}
REACT_APP_WHATSAPP_NUMBER=+27721423215
REACT_APP_WHATSAPP_MESSAGE=Hi%20SynthAI%2C%20I%20would%20like%20to%20get%20more%20information%20about%20your%20services.
REACT_APP_VERSION=${VERSION}
REACT_APP_ENVIRONMENT=${ENVIRONMENT}
EOF

# Rest of the deployment script remains the same...
# SynthAI Frontend Deployment Script
# Usage: ./scripts/deploy.sh [environment] [version]

set -e

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}
S3_BUCKET="synthai-frontend-${ENVIRONMENT}"
CLOUDFRONT_DISTRIBUTION=${CLOUDFRONT_DISTRIBUTION:-}

echo "🚀 Deploying SynthAI Frontend to $ENVIRONMENT"
echo "📦 Version: $VERSION"

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(development|staging|production)$ ]]; then
    echo "❌ Invalid environment: $ENVIRONMENT"
    exit 1
fi

# Check AWS CLI availability
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed"
    exit 1
fi

# Check if build exists
BUILD_DIR="build_${ENVIRONMENT}_*"
LATEST_BUILD=$(ls -td $BUILD_DIR | head -1)

if [ -z "$LATEST_BUILD" ]; then
    echo "❌ No build found for environment $ENVIRONMENT"
    echo "💡 Run ./scripts/build.sh $ENVIRONMENT first"
    exit 1
fi

echo "📁 Using build: $LATEST_BUILD"

# Sync to S3
echo "☁️  Uploading to S3 bucket: $S3_BUCKET"
aws s3 sync $LATEST_BUILD s3://$S3_BUCKET/ \
    --delete \
    --cache-control "public, max-age=31536000" \
    --exclude "index.html" \
    --exclude "static/*"

# Upload HTML with different cache settings
aws s3 sync $LATEST_BUILD s3://$S3_BUCKET/ \
    --include "index.html" \
    --cache-control "public, max-age=0, must-revalidate"

# Upload static files with long cache
aws s3 sync $LATEST_BUILD s3://$S3_BUCKET/ \
    --include "static/*" \
    --cache-control "public, max-age=31536000, immutable"

# Invalidate CloudFront cache if distribution is specified
if [ -n "$CLOUDFRONT_DISTRIBUTION" ]; then
    echo "🔄 Invalidating CloudFront cache..."
    INVALIDATION_ID=$(aws cloudfront create-invalidation \
        --distribution-id $CLOUDFRONT_DISTRIBUTION \
        --paths "/*" \
        --query 'Invalidation.Id' \
        --output text)
    
    echo "⏳ Waiting for invalidation to complete..."
    aws cloudfront wait invalidation-completed \
        --distribution-id $CLOUDFRONT_DISTRIBUTION \
        --id $INVALIDATION_ID
fi

# Update deployment tracking
DEPLOYMENT_INFO=$(cat << EOF
{
    "environment": "$ENVIRONMENT",
    "version": "$VERSION",
    "build": "$(basename $LATEST_BUILD)",
    "deployedAt": "$(date -Iseconds)",
    "deployedBy": "$(whoami)",
    "gitCommit": "$(git rev-parse --short HEAD)"
}
EOF
)

echo $DEPLOYMENT_INFO > deployment-info.json
aws s3 cp deployment-info.json s3://$S3_BUCKET/deployment-info.json

echo "✅ Deployment completed successfully!"
echo "🌐 Application URL: https://$(aws s3api get-bucket-location --bucket $S3_BUCKET --query 'LocationConstraint' --output text).s3.amazonaws.com/index.html"

# Send deployment notification
if [ -n "$SLACK_WEBHOOK_URL" ]; then
    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"✅ SynthAI Frontend deployed to $ENVIRONMENT\n• Version: $VERSION\n• Build: $(basename $LATEST_BUILD)\n• Commit: $(git rev-parse --short HEAD)\"}" \
        $SLACK_WEBHOOK_URL
fi

echo "🎉 Deployment process completed!"
