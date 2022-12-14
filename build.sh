#!/bin/sh

# This assumes poetry, gets where poetry stores its dependencies
VIRTUAL_ENV_PATH=`poetry show -v 2> /dev/null | head -n1 | cut -d ' ' -f 3`

# Clean up anything just in case
rm -rf dist
rm -rf build

# And go...
pyinstaller \
--paths "$VIRTUAL_ENV_PATH/lib/python3.9/site-packages" \
--windowed \
--onefile \
-n chessgame \
--clean \
--add-data "chess/assets/bishop.png:assets" \
--add-data "chess/assets/boo.mp3:assets" \
--add-data "chess/assets/clack.mp3:assets" \
--add-data "chess/assets/correct.wav:assets" \
--add-data "chess/assets/gameDefinitions.json:assets" \
--add-data "chess/assets/Hide.png:assets" \
--add-data "chess/assets/LoginButtonImage.png:assets" \
--add-data "chess/assets/queen.png:assets" \
--add-data "chess/assets/rook.png:assets" \
--add-data "chess/assets/Show.png:assets" \
entry_point.py