#!/bin/bash

# Ecommerce Analytics Dashboard - Setup and Launch Script

echo "Ecommerce Analytics Dashboard"
echo "=================================="

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Initialize database if needed
if [ ! -f "db/ecommerce.db" ]; then
    echo "🗄️  Initializing database..."
    python3 init_db.py
else
    echo "✅ Database already initialized"
fi

# Start the app
echo ""
echo "🎯 Starting dashboard..."
echo "📍 Dashboard will be available at: http://localhost:8050"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python3 app.py
