#!/bin/bash
# Run once on fresh DigitalOcean droplet as root
# Usage: bash server-setup.sh

set -e

echo "=== Installing Docker ==="
curl -fsSL https://get.docker.com | sh

echo "=== Cloning repo ==="
# Replace with your actual repo URL
git clone https://github.com/YOUR_USERNAME/embedchat-be.git /opt/embedchat-be
cd /opt/embedchat-be

echo "=== Create .env.prod ==="
echo "Create /opt/embedchat-be/.env.prod with these values:"
cat <<'TEMPLATE'

APP_ENV=production
DATABASE_URL=postgresql+psycopg://embedchat:CHANGE_ME_STRONG_PASSWORD@postgres:5432/embedchat
POSTGRES_USER=embedchat
POSTGRES_PASSWORD=CHANGE_ME_STRONG_PASSWORD
POSTGRES_DB=embedchat
FIREBASE_SERVICE_ACCOUNT_PATH=/app/firebase-sa.json
GEMINI_API_KEY=your-gemini-api-key

TEMPLATE

echo ""
echo "=== Next steps ==="
echo "1. Edit /opt/embedchat-be/.env.prod with real values"
echo "2. Copy firebase service account JSON to /opt/embedchat-be/firebase-sa.json"
echo "3. Point DNS: chat.obuseklearns.dev → $(curl -s ifconfig.me)"
echo "4. Run: cd /opt/embedchat-be && bash scripts/deploy-first-time.sh"
