##### FRONT END #####
import sys
import optparse
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QTimer, QRect, QTime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox, \
    QDateTimeEdit, QTimeEdit)
import random
import time
import datetime

class main_window(QWidget):
    frontEnd_signal = pyqtSignal(list)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.init_gui()
        self.backEnd_signal = None
        self.frontEnd_signal.connect(self.index)

    
    def init_gui(self):
        #Se crea la ventana inicial
        self.setWindowTitle('Bot-a tu toma')
        self.setGeometry(100, 100, 400, 450)

        col1 = 25
        col2 = 100
        col3 = 205
        self.userLabel = QLabel('Usuario:', self)
        self.userLabel.move(col1, 50)
        self.userEdit = QLineEdit('', self)
        self.userEdit.setGeometry(col2, 50, 100, 20)
        self.userLabelInstruccions = QLabel('(Solo usuario, no mail UC)', self)
        self.userLabelInstruccions.move(col3, 50)

        self.passwordLabel = QLabel('Contraseña:', self)
        self.passwordLabel.move(col1, 90)
        self.passwordEdit = QLineEdit('', self)
        self.passwordEdit.setGeometry(col2, 90, 100, 20)
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.passwordButton = QPushButton('ver', self)
        self.passwordButton.clicked.connect(self.view_password)
        self.passwordButton.setGeometry( col3, 90, 45, 20)

        self.labelNRC1 = QLabel('Ramo 1 (NRC):', self)
        self.labelNRC1.move(col1, 170)
        self.editNRC1 = QLineEdit('', self)
        self.editNRC1.setGeometry(col2, 170, 100, 20)

        self.labelNRC2 = QLabel('Ramo 2 (NRC):', self)
        self.labelNRC2.move(col1, 210)
        self.editNRC2 = QLineEdit('', self)
        self.editNRC2.setGeometry(col2, 210, 100, 20)

        self.labelNRC3 = QLabel('Ramo 3 (NRC):', self)
        self.labelNRC3.move(col1, 250)
        self.editNRC3 = QLineEdit('', self)
        self.editNRC3.setGeometry(col2, 250, 100, 20)

        self.startTimeLabel = QLabel('Hora de toma:', self)
        self.startTimeLabel.move(col1, 290)
        self.startTimeEdit = QTimeEdit(self)
        time = QTime()
        time.setHMS(8,30,0)
        self.startTimeEdit.setTime(time)
        self.startTimeEdit.setGeometry(col2, 290, 100, 20)
        self.startTimeInstruccions = QLabel('(Formato 24 horas. Ej: 2 pm -> 14:00)', self)
        self.startTimeInstruccions.move(col3, 290)

        self.startButton = QPushButton('&Empezar', self)
        self.startButton.resize(self.startButton.sizeHint())
        self.startButton.clicked.connect(self.button_click)
        self.startButton.setGeometry( col2, 340, 100, 40)

        self.countdownLabel = QLabel('', self)
        self.countdownLabel.move(75, 400)

    def index (self, data):
        #se interpreta la orden que la señal manda
        pass

    def button_click(self):
        #No se permiten cambiar los datos
        self.deactivate()
        #Se esconde la ventana (para poder mostrar la ventana, hay que hacer el siguiente paso con threading)
        self.hide()

        #Se mandan los datos en un thread y se espera a que se inicie el proceso
        data = ['start_process', self.userEdit.text(), self.passwordEdit.text(), self.editNRC1.text(), \
            self.editNRC2.text(), self.editNRC3.text(), self.startTimeEdit.text()]
        self.backEnd_signal.emit(data)

    
    def view_password(self):
        if self.passwordButton.text() == 'ver':
            self.passwordButton.setText('ocultar')
            self.passwordEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.passwordButton.setText('ver')
            self.passwordEdit.setEchoMode(QLineEdit.Password)
    def deactivate(self):
        self.userEdit.setDisabled(True)
        self.passwordEdit.setDisabled(True)
        self.editNRC1.setDisabled(True)
        self.editNRC2.setDisabled(True)
        self.editNRC3.setDisabled(True)
        self.startTimeEdit.setDisabled(True)
        self.startButton.setDisabled(True)

