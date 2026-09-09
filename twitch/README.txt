Twitch channel art for twitch.tv/adwarehackclub, made 9 Sep 2026.

profile-picture.png    800x800    favicon.svg mark on the tiled ADWARE backdrop. Twitch crops to a circle.
profile-banner.png     1200x480   channel header background.
offline-screen.png     1920x1080  video player banner, shown when the channel is offline.
panel-how-it-works.png 320x100    header image for the "How it works" channel panel.
panel-rate-card.png    320x150    header image for the "Rate card" channel panel.

Each PNG is a headless Chrome screenshot of the .html file beside it, which pulls
the real SVG assets from the repo root. To re-render one, from the repo root:

  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
    --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --user-data-dir=/tmp/adware-render --window-size=1200,480 \
    --screenshot=twitch/profile-banner.png "file://$PWD/twitch/banner.html"

Window size must match the body size set in each file. This folder is in
.vercelignore, so nothing here ships with the site.
