#!/bin/sh

# This assumes poetry, gets where poetry stores its dependencies
# VIRTUAL_ENV_PATH=`poetry show -v 2> /dev/null | head -n1 | cut -d ' ' -f 3`
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Clean up anything just in case
rm -rf dist
rm -rf build

# And go...
pyinstaller \
--windowed \
--onefile \
-n chessgame \
--add-data "${SCRIPT_DIR}/chess/assets/bishop.png:assets" \
--add-data "${SCRIPT_DIR}/chess/assets/boo.mp3:assets" \
--add-data "${SCRIPT_DIR}/chess/assets/clack.mp3:assets" \
--add-data "${SCRIPT_DIR}/chess/assets/correct.wav:assets" \
--add-data "${SCRIPT_DIR}/chess/assets/gameDefinitions.json:assets" \
--add-data "${SCRIPT_DIR}/chess/assets/Hide.png:assets" \
--add-data "${SCRIPT_DIR}/chess/assets/LoginButtonImage.png:assets" \
--add-data "${SCRIPT_DIR}/chess/assets/queen.png:assets" \
--add-data "${SCRIPT_DIR}/chess/assets/rook.png:assets" \
--add-data "${SCRIPT_DIR}/chess/assets/Show.png:assets" \
${SCRIPT_DIR}/entry_point.py