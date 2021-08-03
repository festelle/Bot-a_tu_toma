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
        self.NRC2, self.NRC3, self.start_time, self.start_time_obj = data[4], data[5], data[6], data[7]
        # Se crea una instancia de driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # Se prepara la cuenta
        prepare = self.prepare_account(driver)
        if prepare != 'error':
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

        # Se comienza el proceso 3 minutos antes de que comience la hora de la toma de ramos
        
        
        time_start = datetime.datetime.combine(datetime.date.today(), self.start_time_obj) - datetime.timedelta(minutes=3)
        now = datetime.datetime.now()
        if (time_start-now).total_seconds() > 0:
            userBox = driver.find_element_by_id("UserID")
            userBox.click()
            userBox.send_keys(f'Proceso comenzará a las {time_start.time().hour}:{time_start.time().minute}')
            time.sleep((time_start-now).total_seconds())

        #Se vuelve a ingresar
        userBox = driver.find_element_by_id("UserID")
        userBox.click()
        userBox.clear()
        userBox.send_keys(self.user)

        passBox = driver.find_element_by_name("PIN")
        passBox.click()
        passBox.send_keys(self.password)

        submitButton = driver.find_element_by_xpath("/html/body/div[3]/form/p/input")
        submitButton.click()
        time.sleep(1)
        try:
            botonAgregarClases = driver.find_element_by_link_text("Agregar o Eliminar Clases")
            botonAgregarClases.click()
        except:
            print('\n\n USUARIO O CLAVE UC INCORRECTA \n\n')
            return 'error'

        
        #Se espera que sea la hora correcta para empezar la toma de ramos
        time_start = datetime.datetime.combine(datetime.date.today(), self.start_time_obj)
        now = datetime.datetime.now()
        if (time_start-now).total_seconds() > 0:
            time.sleep((time_start-now).total_seconds())

        
 
        

    def take_classes(self, driver):
        #Una vez que es la hora, se mide el tiempo que se demora
        initial_time = time.clock()
        #Se selecciona el periodo de inscripción actual, se puede modificar para dar opción
        submitButton = driver.find_element_by_xpath("/html/body/div[3]/form/input")
        submitButton.click()

        try: 
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

        except:
            print('\n\n OCURRIÓ UN ERROR (ES LA HORA CORRECTA?) \n\n')