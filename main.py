import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu
from PyQt5.QtCore import  QTimer, QDate, QTime,QEvent, Qt
from PyQt5.QtGui import QIcon

from PyQt5.uic import loadUi

import urllib.request
import json
from random import randint

from threading import *


class main(QMainWindow):

    def __init__(self):
        super(main, self).__init__()
        loadUi('main.ui', self)

        #Título de la ventana
        self.setWindowTitle("Postulante para ROBOTILSA S.A") 

        #Se obtiene fecha para QLabel con el formato requerido
        fechaActual = QDate.currentDate()
        self.fecha.setText(fechaActual.toString('dd/MM/yyyy'))

        #Se define el logo y la función del botón al clickear
        self.btRequest.setIcon(QIcon('logo.png')) 
        self.btRequest.clicked.connect(self.request)

        #Se define el click derecho para el QListWidget
        self.listNames.installEventFilter(self)
                
        #Se define la hora para QLabel con el formato requerido
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)
        
    #Función para mostrar la hora actual en QLabel
    def displayTime(self):
        currentTime = QTime.currentTime()
        displayText = currentTime.toString('hh:mm:ss')
        self.hora.setText(displayText)
        
    #Función para el request al api
    def request(self):

        #Se encera el QListWidget y la lista de jsons
        self.listNames.clear()       
        self.listJsons = []

        #Se itera 10 veces para obtener los items que se agregan en el QListWidget
        for i in range(10):
            
            id = randint(1, 83)
            
            url = "https://swapi.dev/api/people/"+str(id)
            

            try:
                #Request para el api
                response = urllib.request.urlopen(url)
                data =response.read()
                encoding = response.info().get_content_charset('utf-8')
                jsonData = json.loads(data.decode(encoding))
                self.listJsons.append(jsonData)
                
                self.listNames.addItem(jsonData["name"])
                
            except:
                print("Error obteniendo id: "+str(id))

            
    #Función para el click derecho del QListWidget
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.listNames:
            menu = QMenu()
            menu.addAction('Información del personaje')

            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())

                for data in self.listJsons:

                    if(data['name'] == item.text()):

                        #Se muestra la segunda ventana
                        
                        self.window = QMainWindow()
                        loadUi('details.ui', self.window)
                        self.window.show()

                        self.window.height.setText(data["height"])
                        self.window.mass.setText(data["mass"])
                        self.window.hair.setText(data["hair_color"])
                        self.window.skin.setText(data["skin_color"])
                        self.window.eye.setText(data["eye_color"])
                        self.window.birth.setText(data["birth_year"])
                        self.window.gender.setText(data["gender"])
                        

            return True
        return super().eventFilter(source, event)

    
app = QApplication(sys.argv)
main = main()
main.show()
sys.exit(app.exec_())









