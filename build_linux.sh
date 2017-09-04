# Shell script to build the Tetris Linux executable.
# The resulting "tetris_linux" script will be available in the "dist" directory.

pyinstaller \
    --clean --noconfirm --onefile \
    --log-level=WARN \
    --name="tetris_linux" \
    --add-data="resources:resources" \
    run.py