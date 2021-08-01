# front end, back end and main in one file to be able to create only one .exe program

##### FRONT END #####
import sys
import optparse
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QTimer, QRect, QTime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox, \
    QDateTimeEdit, QTimeEdit)
from PyQt5.QtGui import QIcon
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
        self.setWindowIcon(QIcon('Bot-a.png'))
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
        self.passwordButton.setCheckable(True)
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

        self.authorLabel = QLabel('Creado por F. Estelle', self)
        self.authorLabel.setGeometry((400-100)/2, 425, 100, 20)

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
        if self.passwordButton.isChecked():
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



#####  BACK END  #####
from selenium import webdriver
import time
import datetime
import functools
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QTimer, QThread
from webdriver_manager.chrome import ChromeDriverManager
import threading

class main_window_logic(QObject):
    backEnd_signal = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.backEnd_signal.connect(self.index)
        self.frontEnd_signal = None
        self.user = None
        self.password = None
        self.NRC1 = None
        self.NRC2 = None
        self.NRC3 = None
        self.start_time = None
    
    def index(self, data):
        #El primer elemento de la lista es la orden de lo que hay que hacer
        order = data[0]
        if order == 'start_process':
            self.start_process(data)

    def start_process(self, data):

        # Se guarda la data entregada
        self.user, self.password, self.NRC1 = data[1], data[2], data[3]
        self.NRC2, self.NRC3, self.start_time = data[4], data[5], data[6]
        # Se crea una instancia de driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # Se prepara la cuenta
        self.prepare_account(driver)
        # Con la cuenta preparada se toman los ramos
        self.take_classes(driver)


    def prepare_account(self, driver):

        ####    PASOS PARA INGRESAR A PORTAL UC, NO ES NECESARIO ####

        # driver.get('https://sso.uc.cl/cas/login?service=https%3A%2F%2Fportal.uc.cl%2Fc%2Fportal%2Flogin')
        # #Se ingresa la información de la cuenta y se inicia sesión
        # userBox = driver.find_element_by_id("username")
        # userBox.click()
        # userBox.send_keys(user)
        # passBox = driver.find_element_by_id("password")
        # passBox.click()
        # passBox.send_keys(password)
        # submitButton = driver.find_element_by_name("submit")
        # submitButton.click()

        #Se mueve hasta la sección de agregar y eliminar ramos
        driver.get('https://ssb.uc.cl/ERPUC/twbkwbis.P_WWWLogin')

        #Se vuelve a ingresar
        userBox = driver.find_element_by_id("UserID")
        userBox.click()
        userBox.send_keys(self.user)

        passBox = driver.find_element_by_name("PIN")
        passBox.click()
        passBox.send_keys(self.password)

        submitButton = driver.find_element_by_xpath("/html/body/div[3]/form/p/input")
        submitButton.click()
        time.sleep(1)
        botonAgregarClases = driver.find_element_by_link_text("Agregar o Eliminar Clases")
        botonAgregarClases.click()

        
        #Se espera que sea la hora correcta para empezar la toma de ramos
        now = str(datetime.datetime.now())[0:16]
        start_datetime = str(datetime.datetime.now())[0:11] + self.start_time
        while now != start_datetime:
            now = str(datetime.datetime.now())[0:16]
        
 
        

    def take_classes(self, driver):
        #Una vez que es la hora, se mide el tiempo que se demora
        initial_time = time.clock()
        #Se selecciona el periodo de inscripción actual, se puede modificar para dar opción
        submitButton = driver.find_element_by_xpath("/html/body/div[3]/form/input")
        submitButton.click()

        #Se selecciona el plan de estudio
        planMenu = driver.find_element_by_id("st_path_id")
        #SOLO FUNCIONA PARA APRETAR LA SEGUNDA OPCION QUE APARECE EN EL MENU
        ####    REVISAR SI FUNCIONA PARA SEGUNDO SEMETRE    ####
        planMenu.find_element_by_xpath("/html/body/div[3]/form/table/tbody/tr[2]/td/select/option[2]").click()


        sendButton = driver.find_element_by_xpath("/html/body/div[3]/form/input[19]")
        sendButton.click()

        #Se ingresan los ramos a tomar
        inputClass1 = driver.find_element_by_id("crn_id1")
        inputClass1.send_keys(self.NRC1)

        inputClass2 = driver.find_element_by_id("crn_id2")
        inputClass2.send_keys(self.NRC2)

        inputClass3 = driver.find_element_by_id("crn_id3")
        inputClass3.send_keys(self.NRC3)

        #Se aprieta el botón de enviar cambios
        sendButton = driver.find_element_by_xpath('/html/body/div[3]/form/input[19]')
        sendButton.click()

        #Se calcula e imprime tiempo demorado en toma
        final_time = time.clock() - initial_time
        print('Tiempo demorado en tomar los ramos:', final_time)
###### main.py ###### 
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication([])
    
    #Se crean las instancias de mainWindow
    mainWindow = main_window()
    mainWindowLogic = main_window_logic()

    #Se crean y conectan las señales de mainWindow
    mainWindow.backEnd_signal = mainWindowLogic.backEnd_signal
    mainWindowLogic.frontEnd_signal = mainWindow.frontEnd_signal

    #Se abre la ventana principal
    mainWindow.show()
    sys.exit(app.exec_())