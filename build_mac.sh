# Shell script to build the Tetris Mac OS executable.
# The resulting "tetris_mac.app" executable and "tetris_mac" script will be available in the "dist" directory.

pyinstaller \
    --clean --noconfirm --onefile --windowed \
    --log-level=WARN \
    --name="tetris_mac" \
    --icon="resources/images/icon.icns" \
    --add-data="resources:resources" \
    --osx-bundle-identifier="fr.epoc.python.games.tetris" \
    run.py