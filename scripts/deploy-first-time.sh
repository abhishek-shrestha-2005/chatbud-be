#!/bin/bash
# First deploy — gets SSL cert, starts everything
# Run from /opt/embedchat-be as root

set -e

cd /opt/embedchat-be

echo "=== Step 1: Start with HTTP-only nginx ==="
cp nginx/nginx.init.conf nginx/nginx.conf.bak
cp nginx/nginx.init.conf nginx/nginx.conf

docker compose -f docker-compose.prod.yml up -d postgres app nginx

echo "=== Waiting for services... ==="
sleep 10

echo "=== Step 2: Get SSL certificate ==="
docker run --rm \
  -v embedchat-be_certbot_data:/etc/letsencrypt \
  -v embedchat-be_certbot_www:/var/www/certbot \
  certbot/certbot certonly \
  --webroot --webroot-path=/var/www/certbot \
  --email your-email@example.com \
  --agree-tos --no-eff-email \
  -d chat.obuseklearns.dev

echo "=== Step 3: Switch to HTTPS nginx config ==="
# Restore the SSL nginx config
git checkout nginx/nginx.conf

docker compose -f docker-compose.prod.yml restart nginx

echo "=== Step 4: Run migrations ==="
docker compose -f docker-compose.prod.yml exec app uv run python -m alembic upgrade head

echo "=== Done! ==="
echo "Backend live at https://chat.obuseklearns.dev"
echo "Health check: https://chat.obuseklearns.dev/health"
