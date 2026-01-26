# 🎨 Quick Customization Guide

This guide will help you personalize the birthday website for your friend!

## ✏️ Essential Customizations

### 1. Change Your Friend's Name (IMPORTANT!)

**File**: `index.html`

**Line 30**: Change the hero name
```html
<!-- Find this line -->
<h2 class="hero-name">Beautiful Soul</h2>

<!-- Change to -->
<h2 class="hero-name">Sarah</h2>  <!-- Use your friend's name -->
```

### 2. Customize the Typing Messages

**File**: `js/script.js`

**Lines 3-7**: Update the typing text phrases
```javascript
const phrases = [
    "Here's to another year of amazing adventures! 🌟",
    "You make the world brighter just by being in it ✨",
    "Wishing you endless happiness today and always 💖"
];
```

Replace with your own sweet messages!

### 3. Update the Birthday Message

**File**: `index.html`

**Lines 189-211**: Edit the heartfelt message section
```html
<p class="message-paragraph">
    To my dearest friend, on this special day...
    <!-- Replace with your personal message -->
</p>
```

### 4. Customize "Things I Love About You"

**File**: `index.html`

**Lines 219-226**: Update the list items
```html
<li>🌟 Your contagious laughter that lights up every room</li>
<li>🎨 The way you see beauty in everything</li>
<!-- Add your own unique points -->
```

### 5. Change the Surprise Messages

**File**: `index.html`

**Lines 235-239**: Edit the fun messages
```html
<p>🎉 Fun Fact: You're not getting older, you're leveling up! 🎮</p>
<!-- Add your own funny birthday jokes -->
```

## 🎵 Adding Background Music

### Step 1: Get Your Music File
- Download an MP3 file (romantic, soft instrumental music works best)
- Popular free sources: YouTube Audio Library, Free Music Archive
- Keep file size under 5MB for faster loading

### Step 2: Add to Project
```
birthday-website/
└── audio/
    └── birthday-song.mp3  ← Place your MP3 here
```

### Step 3: Update HTML
**File**: `index.html`, **Line 17**
```html
<!-- Find this -->
<audio id="bgMusic" loop>
    <!-- You can add a music file here -->
</audio>

<!-- Change to -->
<audio id="bgMusic" loop>
    <source src="audio/birthday-song.mp3" type="audio/mpeg">
</audio>
```

## 📸 Managing Photos

### Using Different Photos

**Option A: Replace existing images**
1. Keep the same filenames (easier)
2. Just replace the files in `images/` folder
3. No code changes needed!

**Option B: Use new filenames**
1. Add your photos to `images/` folder
2. Update `index.html`:

**Hero Image** (Line 31):
```html
<img src="images/YOUR_BEST_PHOTO.jpg" alt="Hero">
```

**Gallery Items** (Lines 43-104):
```html
<div class="gallery-item" data-image="images/YOUR_PHOTO_1.jpg">
    <img src="images/YOUR_PHOTO_1.jpg" alt="Memory 1">
    ...
</div>
```

**Slideshow** (Lines 116-160):
```html
<div class="slide active">
    <img src="images/YOUR_PHOTO_1.jpg" alt="Description">
    <p class="slide-caption">Your Caption Here</p>
</div>
```

### Adding More Photos to Gallery

Copy this block and paste after the last gallery item:
```html
<div class="gallery-item" data-image="images/NEW_PHOTO.jpg">
    <img src="images/NEW_PHOTO.jpg" alt="Memory 10">
    <div class="gallery-overlay">
        <span class="zoom-icon">🔍</span>
    </div>
</div>
```

## 🎨 Changing Colors

**File**: `css/style.css`, **Lines 11-18**

```css
:root {
    --pastel-pink: #FFD1DC;      /* Change to your favorite pastel pink */
    --pastel-lavender: #E6E6FA;  /* Change to your favorite lavender */
    --pastel-mint: #B5EAD7;      /* Change to your favorite mint */
    /* ... and so on */
}
```

Use [Coolors.co](https://coolors.co) to find perfect color palettes!

## 🎯 Quick Checklist Before Sharing

- [ ] Changed friend's name in hero section
- [ ] Updated birthday message with personal content
- [ ] Customized "Things I Love About You" list
- [ ] Replaced or verified all photos work
- [ ] Added custom typing messages
- [ ] (Optional) Added background music
- [ ] (Optional) Updated colors to match her favorites
- [ ] Tested on mobile phone
- [ ] Tested in browser (Chrome, Safari, Firefox)

## 🚀 Deployment Quick Start

### Easiest: Share as Folder
1. Zip the entire `birthday-website` folder
2. Share via Google Drive / Dropbox / email
3. Friend can extract and open `index.html`

### Best: GitHub Pages (Free Hosting)
1. Create GitHub account (if needed)
2. Create new repository called `birthday-[name]`
3. Upload all files
4. Go to Settings > Pages
5. Enable Pages from `main` branch
6. Share the URL: `https://[username].github.io/birthday-[name]/`

### Alternative: Netlify (Easiest Hosting)
1. Go to [netlify.com](https://www.netlify.com)
2. Sign up (free)
3. Drag & drop the `birthday-website` folder
4. Get instant URL to share!

## 💡 Pro Tips

1. **Photo Quality**: Use high-quality but compressed images (500-800KB each)
2. **Testing**: Open in incognito mode to see fresh version
3. **Mobile**: Test on your phone before sharing
4. **Timing**: Share on midnight of her birthday for surprise effect! 🎉
5. **Backup**: Keep a copy of original before customizing

## ❓ Common Questions

**Q: Can I add more sections?**
A: Yes! Copy any section structure and modify it. Follow the existing HTML pattern.

**Q: How do I change fonts?**
A: Visit [Google Fonts](https://fonts.google.com), pick a font, and update the `<link>` in HTML line 8.

**Q: Can I remove the floating hearts?**
A: In `js/script.js`, remove or comment out lines 24-36 (the `createHeart` function and interval).

**Q: Website not loading on phone?**
A: Make sure images aren't too large (compress them). Use a proper hosting service instead of opening locally.

**Q: Can I add videos?**
A: Yes! Add a `<video>` tag in HTML. Example:
```html
<video controls style="width: 100%; border-radius: 20px; margin: 20px 0;">
    <source src="videos/birthday-video.mp4" type="video/mp4">
</video>
```

## 🎁 Final Touch

Add a personal message in the browser console! Edit `js/script.js` (bottom):
```javascript
console.log('%c🎉 Happy Birthday Sarah! 🎂', 'font-size: 30px; color: #FFB3BA; font-weight: bold;');
console.log('%cMade with 💖 by [Your Name]', 'font-size: 16px; color: #D4B5FF;');
```

---

**Have fun customizing! Your friend will love this! 💖✨**

Need help? Check the README.md for more details.
