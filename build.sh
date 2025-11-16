#!/bin/bash
# Build script for Vercel deployment

echo "🚀 Starting build process..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Generate static data from stored_codes
echo "📦 Generating static code data..."
python3 generate_static_data.py

if [ $? -eq 0 ]; then
    echo "✅ Static data generated successfully"
else
    echo "❌ Failed to generate static data"
    exit 1
fi

echo "✅ Build complete!"
