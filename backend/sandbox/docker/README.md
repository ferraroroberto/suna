# Sandbox

## Chrome Profile Mounting for Playwright

To use your local Chrome profile for realistic browser automation, you **must mount your Chrome user profile directory into the container**. This enables Playwright to launch Chrome with your real browsing data, cookies, and extensions.

**Example Docker run (macOS/Linux):**

```
docker run -v /Users/me/Library/Application\ Support/Google/Chrome/Default:/chrome-profile:ro ...
```

**Example Docker run (Windows):**

```
docker run -v "C:/Users/rober/AppData/Local/Google/Chrome/User Data/Default/Default_suna:/chrome-profile:ro" ...
```

- The container expects the profile at `/chrome-profile` by default, or you can override with the `CHROME_PROFILE_PATH` environment variable.
- The profile should be mounted **read-only** (`:ro`) for safety.
- If you want to use a different Chrome profile, mount the appropriate folder and set `CHROME_PROFILE_PATH` accordingly.

**Why?**
- This enables Playwright to launch Chrome with your real user data, bypassing many anti-bot checks and preserving your browsing state.
- The code uses `launch_persistent_context` with the mounted profile and disables Playwright's automation fingerprint.

---
