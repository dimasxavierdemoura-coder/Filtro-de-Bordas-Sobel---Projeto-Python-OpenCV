@echo off
REM Start script para executar o modo HARD do filtro Sobel

python sobel_edge_detection.py dataset --output dataset_sobel --ksize 5 --blur 5 --blur-sigma 1.0 --equalize --bilateral --morph gradient --morph-ksize 5 --canny --canny-th1 50 --canny-th2 150 --threshold 100 --show

if %ERRORLEVEL% neq 0 (
    echo.
    echo Erro ao executar o script. Verifique se o Python e as dependencias estao instalados.
) else (
    echo.
    echo Execucao concluida com sucesso.
)

pause
