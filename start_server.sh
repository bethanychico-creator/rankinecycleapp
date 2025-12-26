#!/bin/bash
# Rankine Cycle Practice App - Startup Script

echo "Starting Rankine Cycle Calculator Server..."
echo "================================================"
echo ""
echo "Make sure CoolProp is installed:"
echo "  pip install --break-system-packages CoolProp"
echo ""
echo "Starting server on http://localhost:8888"
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python3 rankine_server.py
