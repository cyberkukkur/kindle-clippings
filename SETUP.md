# My Clippings — Setup Guide

Your app URL: https://cyberkukkur.github.io/kindle-clippings

---

## One-time Setup (~10 minutes)

### Step 1: Install Git
Download and install Git from https://git-scm.com/downloads
(On Mac it may already be installed — open Terminal and type `git --version` to check)

### Step 2: Create the GitHub repository
1. Go to https://github.com/new
2. Set Repository name to: `kindle-clippings`
3. Set visibility to **Public**
4. Do NOT tick any "initialise" options — leave them all blank
5. Click **Create repository**

### Step 3: Upload these files
Open Terminal (Mac/Linux) or Command Prompt (Windows) in this folder and run:

```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/cyberkukkur/kindle-clippings.git
git push -u origin main
```

If asked for a password, GitHub now uses tokens instead.
Create one at: https://github.com/settings/tokens
(Select "repo" scope, set no expiry)
Use the token as your password when prompted.

### Step 4: Enable GitHub Pages
1. Go to https://github.com/cyberkukkur/kindle-clippings/settings/pages
2. Under "Source", select **Deploy from a branch**
3. Branch: **main**, folder: **/ (root)**
4. Click **Save**

Wait 1–2 minutes, then visit: https://cyberkukkur.github.io/kindle-clippings

### Step 5: Install as an app on Android
1. Open Chrome on your Android phone
2. Go to https://cyberkukkur.github.io/kindle-clippings
3. Tap the three-dot menu (⋮) → **Add to Home screen**
4. Tap **Add**

It will appear on your home screen like a real app. Tap it — it opens fullscreen
with no browser chrome.

---

## Updating your clippings

Whenever you want to update with new highlights from your Kindle:

1. Connect your Kindle via USB
2. Copy `My Clippings.txt` from your Kindle into this folder
3. Run: `python update.py`
4. Wait ~30 seconds, then pull down to refresh the app on your phone

---

## Troubleshooting

**"git push" asks for a password**
Use a personal access token, not your GitHub password.
Create one at: https://github.com/settings/tokens

**App not updating after push**
GitHub Pages can take up to 2 minutes to deploy. 
Also try a hard refresh: hold Shift and tap the refresh button.

**App works on desktop but not phone**
Make sure you visited the GitHub Pages URL (not a local file) before installing.
