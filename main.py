import sys
import backEnd
import frontEnd
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication([])
    
    #Se crean las instancias de mainWindow
    mainWindow = frontEnd.main_window()
    mainWindowLogic = backEnd.main_window_logic()

    #Se crean y conectan las señales de mainWindow
    mainWindow.backend_signal = mainWindowLogic.backend_signal
    mainWindowLogic.frontEnd_signal = mainWindow.frontEnd_signal

    #Se abre la ventana principal
    mainWindow.show()
    sys.exit(app.exec_())