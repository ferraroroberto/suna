#!/bin/bash
set -e

echo "📁 Copying Chrome profile to /tmp/profile..."
rm -rf /tmp/profile
cp -r /chrome_profile_src /tmp/profile

echo "✅ Launching Chromium headless on 127.0.0.1:9222"
/ms-playwright/chromium-*/chrome-linux/chrome \
  --headless \
  --no-sandbox \
  --disable-dev-shm-usage \
  --disable-gpu \
  --user-data-dir=/tmp/profile \
  --remote-debugging-port=9222 \
  about:blank
