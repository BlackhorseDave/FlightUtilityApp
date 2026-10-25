/* 01 */ const fs = require("node:fs");
/* 02 */ const path = require("node:path");
/* 03 */
/* 04 */ const files = [
/* 05 */   "index.html",
/* 06 */   "styles.css",
/* 07 */   "app.js",
/* 08 */   "manifest.webmanifest",
/* 09 */   "sw.js",
/* 10 */   "lib/mgrs.js",
/* 10 */   "THIRD-PARTY-NOTICES.md",
/* 11 */   "icons/icon-192.svg",
/* 12 */   "icons/icon-512.svg",
/* 13 */];
/* 14 */
/* 15 */ for (const file of files) {
/* 16 */   const source = path.join(__dirname, file);
/* 17 */   const destination = path.join(__dirname, "www", file);
/* 18 */   fs.mkdirSync(path.dirname(destination), { recursive: true });
/* 19 */   fs.copyFileSync(source, destination);
    /* 20 */
}
/* 21 */
/* 22 */ console.log(`Copied ${files.length} web files into www.`);