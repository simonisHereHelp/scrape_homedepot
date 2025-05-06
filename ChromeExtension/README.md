# 🛠️ Capture Home Depot Page — Chrome Extension

This Chrome Extension adds a **"Capture Page"** button that, when clicked, captures the **current page's title and URL**, then downloads a `title_array.txt` file with the entry formatted as:

"title","https://www.homedepot.com/..."

captureHomeDepotExtension/
│
├── manifest.json
├── popup.html
├── captureHomeDepot.js
├── icon16.png
├── icon48.png
├── icon128.png
└── README.md



---

## 🔧 How to Install

1. Open Google Chrome
2. Go to `chrome://extensions/`
3. Enable **Developer Mode** (top right)
4. Click **“Load unpacked”**
5. Select this folder (`captureHomeDepotExtension/`)
6. The extension icon will appear in your toolbar

---

## 🚀 How to Use

1. Navigate to a **Home Depot article page**
2. Click the 🧩 **extension icon**
3. Click the **"Add to title_array.txt"** button
4. A file named `title_array.txt` will be downloaded
   - It contains the current tab’s title and URL in CSV format

Example:

```txt
"How to Remove Wallpaper","https://www.homedepot.com/c/ah/how-to-remove-wallpaper/9ba683603be9fa5395fab90baa35578"
