@ECHO off
REM Batch script to build the Tetris Windows executable.
REM The resulting "tetris_windows.exe" executable will be available in the "dist" directory.

pyinstaller ^
    --clean --noconfirm --onefile --windowed ^
    --log-level=WARN ^
    --name="tetris_windows" ^
    --icon="resources/images/icon.ico" ^
    --add-data="resources;resources" ^
    run.py