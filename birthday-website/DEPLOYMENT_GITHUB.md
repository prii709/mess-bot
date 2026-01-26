# 🚀 GitHub Pages Deployment Guide

This guide will help you deploy your birthday website to GitHub Pages for FREE!

## Prerequisites
- GitHub account (create one at [github.com](https://github.com) if you don't have)
- Git installed on your computer ([download here](https://git-scm.com/downloads))

## Step-by-Step Deployment

### Step 1: Initialize Git Repository

Open PowerShell/Terminal in the `birthday-website` folder and run:

```bash
git init
git add .
git commit -m "Initial commit - Beautiful birthday website"
```

### Step 2: Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click the **"+"** icon (top right) → **"New repository"**
3. **Repository name**: `birthday-surprise` (or any name you like)
4. **Description**: "A special birthday website for my best friend 🎉"
5. Keep it **Public** (or Private if you want)
6. **DO NOT** check "Initialize with README"
7. Click **"Create repository"**

### Step 3: Push Your Code

Copy the commands from GitHub (they'll look like this):

```bash
git remote add origin https://github.com/YOUR_USERNAME/birthday-surprise.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username and run these commands.

### Step 4: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **"Settings"** (top menu)
3. Click **"Pages"** (left sidebar)
4. Under **"Source"**, select:
   - Branch: **main**
   - Folder: **/ (root)**
5. Click **"Save"**

### Step 5: Get Your Website URL

After 1-2 minutes, your site will be live at:

```
https://YOUR_USERNAME.github.io/birthday-surprise/
```

You'll see a success message with the URL at the top of the Pages settings.

## 🎉 Congratulations!

Your website is now live and accessible to anyone with the link!

## 📱 Sharing the Website

### Create a Short Link (Optional)
1. Copy your GitHub Pages URL
2. Go to [bit.ly](https://bitly.com) or [tinyurl.com](https://tinyurl.com)
3. Create a custom short link like: `bit.ly/sarah-birthday`
4. Share this link with your friend!

### Share via QR Code (Creative!)
1. Go to [qr-code-generator.com](https://www.qr-code-generator.com)
2. Paste your GitHub Pages URL
3. Download the QR code
4. Print it on a card or send digitally!

## 🔄 Updating the Website

If you want to make changes after deployment:

```bash
# Make your changes to the files
git add .
git commit -m "Updated birthday message"
git push
```

Your site will automatically update in 1-2 minutes!

## 🔒 Making Repository Private

If you want to keep the code private (but website still public):

1. Go to **Settings** → **General**
2. Scroll to **"Danger Zone"**
3. Click **"Change visibility"** → **"Make private"**

Note: The website will still be publicly accessible at the URL.

## ⚡ Alternative: Using GitHub Desktop (Easier)

If you prefer a visual tool instead of command line:

1. Download [GitHub Desktop](https://desktop.github.com)
2. Install and sign in
3. Click **"Add"** → **"Add existing repository"**
4. Select your `birthday-website` folder
5. Click **"Publish repository"**
6. Go to repository settings on GitHub.com to enable Pages

## 🐛 Troubleshooting

### Images Not Showing
- Make sure all image paths use relative paths: `images/photo.jpg` (not `d:\mess\...`)
- Check that image filenames in HTML match exactly (case-sensitive)

### 404 Error
- Wait 2-3 minutes after enabling Pages
- Make sure `index.html` is in the root folder
- Check branch is set to `main` in Pages settings

### Website Not Updating
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Wait a few minutes for GitHub to rebuild
- Check commit was successful: `git log`

### CSS/JS Not Loading
- Verify all files are in the repository
- Check paths in HTML are relative, not absolute

## 📊 Checking Website Stats (Optional)

To see how many people visit:

1. Add [Google Analytics](https://analytics.google.com) (free)
2. Or use [Goat Counter](https://www.goatcounter.com) (simpler, privacy-friendly)

## 🎁 Pro Tips

1. **Custom Domain**: You can use a custom domain (like `happybirthday-sarah.com`) - see [GitHub Docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

2. **Password Protection**: GitHub Pages doesn't support passwords, but you can:
   - Use [Netlify](https://www.netlify.com) instead (offers password protection)
   - Share via private link only

3. **Scheduled Release**: If you want to hide the site until birthday:
   - Keep repository private until the day
   - Or deploy on her birthday morning

4. **Analytics**: Add a visitor counter to see when she views it!

## 🆘 Need Help?

- GitHub Pages Docs: [docs.github.com/pages](https://docs.github.com/en/pages)
- Git Basics: [git-scm.com/doc](https://git-scm.com/doc)
- Video Tutorial: Search "GitHub Pages tutorial" on YouTube

---

## Quick Command Reference

```bash
# Check current status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Your message here"

# Push to GitHub
git push

# View commit history
git log --oneline

# Create a new branch (for testing)
git checkout -b test-changes
```

---

**🎉 Happy Deploying! Your friend will love this! 💖**
