#!/usr/bin/env python3
"""
Cross-platform Playwright test:
- On Windows: use your real Chrome profile directly
- On Linux/Docker: connect via CDP to a headless Chromium container
"""

import sys, os, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# Detect environment
IS_LINUX = sys.platform.startswith("linux")
IS_WINDOWS = sys.platform.startswith("win")

# Config
DEFAULT_PROFILE = r"E:\onedrive\Documentos\Roberto\projects\automation\suna\suna\profile"
CDP_ENDPOINT = "http://browser:9222"
TEST_PAGE = "https://www.linkedin.com/"

# Get Chrome profile path
PROFILE_DIR = (
    sys.argv[1]
    if len(sys.argv) > 1
    else os.getenv("PROFILE_DIR", DEFAULT_PROFILE)
)

if IS_WINDOWS and not Path(PROFILE_DIR).is_dir():
    sys.exit(f"❌ Chrome profile not found at: {PROFILE_DIR}")

# ───────────────────────────────────────────────────────────────
async def main():
    async with async_playwright() as p:
        # ░░ Windows: local browser launch with profile
        if IS_WINDOWS:
            print(f"🪟 Windows mode: launching with profile {PROFILE_DIR}")
            browser_context = await p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                headless=False,
                args=["--start-maximized"]
            )

        # ░░ Linux/Docker: connect to remote Chromium via CDP
        else:
            print(f"🐧 Docker/Linux mode: connecting to {CDP_ENDPOINT}")
            for attempt in range(10):
                try:
                    browser = await p.chromium.connect_over_cdp(CDP_ENDPOINT)
                    break
                except Exception:
                    print(f"⏳ Browser not ready (attempt {attempt+1}), retrying...")
                    await asyncio.sleep(3)
            else:
                raise RuntimeError("❌ Failed to connect to remote browser after 10 attempts")

            browser_context = browser.contexts[0] if browser.contexts else await browser.new_context()

        # ░░ Run page
        page = browser_context.pages[0] if browser_context.pages else await browser_context.new_page()
        print(f"🌐 Navigating to: {TEST_PAGE}")
        await page.goto(TEST_PAGE, timeout=60_000)

        # ░░ Output status
        print("✅ Page title:", await page.title())
        print("✅ Cookies loaded:", len(await browser_context.cookies()))

        # ░░ Wait for inspection or user exit
        if IS_WINDOWS:
            input("🔎 Press ENTER to close browser...")
        else:
            print("🕒 Waiting 30s before closing...")
            await asyncio.sleep(30)

        await browser_context.close()
        print("👋 Browser closed cleanly.")

# ───────────────────────────────────────────────────────────────
asyncio.run(main())
