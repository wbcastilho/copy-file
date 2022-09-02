# CopyFile
Software utilizado para copiar um arquivo selecionado para uma determinada pasta em um momento especificado do dia.

## Comando para gerar o instalador pelo pyinstaller
pyinstaller --noconsole --name="CopyFile" --add-data="assets\;.\assets" --icon=assets\favicon.ico --collect-all ttkbootstrap main.py