# 🎵 Background Music Recommendations

Adding the right background music can make your birthday website even more special! Here are some tips and recommendations.

## 🎼 Music Style Recommendations

### Soft & Romantic
Perfect for emotional, heartfelt birthdays:
- Acoustic guitar instrumentals
- Piano melodies
- Soft jazz
- Classical pieces

### Upbeat & Happy
Great for fun, energetic vibes:
- Ukulele songs
- Light pop instrumentals
- Indie folk
- Happy acoustic

### Ambient & Dreamy
For a magical, ethereal feel:
- Lofi beats
- Chillhop
- Ambient soundscapes
- Nature sounds with music

## 📥 Where to Find Free Music

### 1. YouTube Audio Library
- URL: [studio.youtube.com/channel/UC.../music](https://studio.youtube.com)
- 100% free, no copyright
- Large variety
- Download as MP3

**Recommended tracks to search:**
- "Happy Birthday" (instrumental)
- "Acoustic Guitar Happy"
- "Soft Piano Romantic"
- "Lofi Birthday"

### 2. Free Music Archive
- URL: [freemusicarchive.org](https://freemusicarchive.org)
- Search: "birthday", "celebration", "happy"
- Filter by license (CC0 or Attribution)

### 3. Pixabay Music
- URL: [pixabay.com/music](https://pixabay.com/music)
- Completely free
- No attribution required
- Good selection of upbeat music

### 4. Bensound
- URL: [bensound.com](https://www.bensound.com)
- High-quality tracks
- Free with attribution
- Search: "ukulele", "happiness", "birthday"

### 5. Incompetech
- URL: [incompetech.com](https://incompetech.com)
- Huge library by Kevin MacLeod
- Free with attribution
- Search: "happy", "celebration"

## 🎯 Specific Track Recommendations

### Soft & Emotional
- "Acoustic Breeze" - Bensound
- "Dawn" - Sappheiros
- "To You" - Telecasted
- "Your Journey" - Artificial.Music

### Happy & Upbeat
- "Ukulele Happy" - YouTube Audio Library
- "Happy Birthday to You (Instrumental)"
- "Sunny" - Bensound
- "Good Mood" - Bensound

### Lofi & Chill
- "Coffee Shop" - Lukrembo
- "Lofi Study" - FASSounds
- "Chill Day" - Lakey Inspired

## 💾 How to Add Music to Your Website

### Step 1: Download Music
1. Choose a track from above sources
2. Download as MP3 format
3. Keep file size under 5MB (compress if needed)

### Step 2: Add to Project
```
birthday-website/
└── audio/
    └── birthday-song.mp3  ← Place file here
```

### Step 3: Update HTML
Open `index.html` and find line ~17:

```html
<!-- Change this -->
<audio id="bgMusic" loop>
    <!-- You can add a music file here -->
</audio>

<!-- To this -->
<audio id="bgMusic" loop>
    <source src="audio/birthday-song.mp3" type="audio/mpeg">
</audio>
```

### Step 4: Test
- Open website in browser
- Click the 🎵 button (top right)
- Music should play!

## 🔧 Music Compression (If File Too Large)

If your MP3 is larger than 5MB, compress it:

### Online Tools:
1. **MP3Smaller**: [mp3smaller.com](https://www.mp3smaller.com)
2. **YouCompress**: [youcompress.com](https://www.youcompress.com)
3. **FreeConvert**: [freeconvert.com/mp3-compressor](https://www.freeconvert.com/mp3-compressor)

Target: 128kbps or 192kbps bitrate (good quality, smaller size)

## ⚙️ Music Settings

### Adjusting Volume
In `js/script.js`, add after line 30:

```javascript
bgMusic.volume = 0.3; // 30% volume (adjust 0.0 to 1.0)
```

### Change Loop Behavior
Remove `loop` from HTML if you want music to play once:

```html
<audio id="bgMusic">  <!-- Removed 'loop' -->
```

### Auto-play (with mute)
In `index.html`:

```html
<audio id="bgMusic" loop autoplay muted>
```

User can click button to unmute. (Browsers block autoplay with sound)

## 🎼 Copyright & Attribution

### If Using Free Music with Attribution:
Add credit to your footer in `index.html`:

```html
<footer class="footer">
    <p>Made with 💖 and lots of love</p>
    <p class="footer-note">
        Music: "Track Name" by Artist | 
        <a href="LICENSE_URL">License</a>
    </p>
</footer>
```

### CC0 / Public Domain:
No attribution needed! Use freely.

## 🎵 Personal Touch Ideas

### Option 1: Record Your Own
- Record yourself singing "Happy Birthday"
- Add a personal voice message
- Use your phone's voice recorder
- Convert to MP3

### Option 2: Her Favorite Song
- Use an instrumental version of her favorite song
- Make sure you have rights (personal use usually OK)
- Find on YouTube → download instrumental version

### Option 3: Voice Message
Instead of music, add a birthday voice message:
- Record: "Happy birthday! Click around to see your surprise!"
- Place in `audio/` folder
- Update HTML same way

## 🐛 Troubleshooting

**Music not playing:**
- ✅ Check file is in `audio/` folder
- ✅ Check filename matches HTML exactly (case-sensitive)
- ✅ Try different browser
- ✅ Check browser console for errors (F12)

**Music too quiet/loud:**
- Adjust volume in `js/script.js` (see settings above)

**File too large / slow loading:**
- Compress MP3 to 128kbps
- Or use a shorter clip (30-60 seconds that loops)

**Browser blocks autoplay:**
- This is normal! Users must interact first
- Keep the music button - it's the solution

## 💡 Pro Tips

1. **Length**: 30-90 seconds is perfect (will loop)
2. **No Vocals**: Instrumental works best (less distracting)
3. **Volume**: Keep it subtle - around 30-40% volume
4. **Testing**: Test with headphones and speakers
5. **Mobile**: Test on phone - music might not work on some mobile browsers

## 🎁 Recommended Final Tracks

My top 3 picks for birthday websites:

1. **"Ukulele Happy" (YouTube Audio Library)**
   - Perfect upbeat vibe
   - Loops well
   - Free, no attribution

2. **"Acoustic Breeze" (Bensound)**
   - Soft and emotional
   - Beautiful guitar
   - Free with attribution

3. **"Love" (Bensound)**
   - Romantic piano
   - Perfect for heartfelt messages
   - Free with attribution

---

**🎵 Choose music that matches your friend's personality!**

**Questions?** Check the main README.md or CUSTOMIZATION_GUIDE.md!
