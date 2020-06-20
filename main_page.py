import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow,QLabel
from mainpage_form import Ui_MainWindow
from register_form import Ui_RegisterWindow
from PyQt5.QtGui import QPixmap,QIcon
from PyQt5.QtCore import QDate, QTime, QDateTime
from PyQt5.QtWidgets import QMessageBox
import register
import pymongo
from bson.objectid import ObjectId
from signin_form import Ui_SigninWindow
from research_form import Ui_ResearchWindow
from connectiondb import connection   
import numpy as np 
from research_form import Ui_ResearchWindow
from messagebx import messagebx
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

class MainForm(QMainWindow):
    def __init__(self):
        super(MainForm,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet("QWidget#MainWindow {background-image: url(mainimage.png)}")
        self.setWindowTitle("Advice Movie")
        self.setWindowIcon(QIcon("video-camera.png"))
        self.ui.btnAdmin.clicked.connect(self.RegisterWindow)
        self.ui.btnUser.clicked.connect(self.SigninWindow)
        self.main_window()

    def main_window(self):
        self.show()

    def RegisterWindow(self):
        self.w=RegisterWindow()
        self.w.show()
        self.hide()

    def SigninWindow(self):
        self.w=SigninWindow()
        self.w.show()
        self.hide()

class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow,self).__init__()
        self.uiRegister = Ui_RegisterWindow()
        self.uiRegister.setupUi(self)
        self.setStyleSheet("QWidget#RegisterWindow {background-image: url(registerimage.png)}")
        countries = register.countries()
        self.uiRegister.comboBox.addItems(countries)
        self.uiRegister.comboBox.setCurrentIndex(194)
        self.uiRegister.pushButton.clicked.connect(self.createaccount)
        self.uiRegister.txtMail.setText("")
    def createaccount(self):
        Name = self.uiRegister.txtName.text()
        Surname = self.uiRegister.txtSurname.text()
        Mail = self.uiRegister.txtMail.text()
        Password = self.uiRegister.txtPassword.text()
        Country = self.uiRegister.comboBox.currentText()
        Birthdate = self.uiRegister.dateEdit.date()
        Year = Birthdate.year()
        Month = Birthdate.month()
        Day = Birthdate.day()
        self.mycollection = connection("Register")
        result = self.mycollection.find({},{"Mail"})
        k=0
        for i in result:
            if (Mail =="") | (Mail==i["Mail"]):
                messagebx("This mail address already exists...")
                k=1
                break

        if k==0:
            self.RegisterSignin(Name,Surname,Country,Year,Month,Day,Mail,Password)
                
    def RegisterSignin(self,Name,Surname,Country,Year,Month,Day,Mail,Password):
        mycollection = connection("Register")
        register = {"Name": Name,"Surname": Surname,"Country": Country,"Birthdate":[Year,Month,Day],"Mail":Mail,"Password":Password}
        mycollection.insert_one(register)
        self.messagebx()

    def messagebx(self):

        msg = QMessageBox()
        msg.setWindowTitle("Create Account")
        msg.setText("Registration is Successful")
        msg.setIconPixmap(QPixmap("profile.png"))
        msg.setWindowIcon(QIcon("tick.png"))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.changepage)
        msg.exec_()
               
    def changepage(self):
        self.w=MainForm()
        self.w.show()
        self.hide()

class SigninWindow(QMainWindow):
    def __init__(self):
        super(SigninWindow,self).__init__()
        self.uiSignin = Ui_SigninWindow()
        self.uiSignin.setupUi(self)
        self.setStyleSheet("QWidget#SigninWindow {background-image: url(signinpage.png)}")
        self.setWindowTitle("Sign in")
        self.setWindowIcon(QIcon("video-camera.png"))
        self.mycollection = connection("Register")
        self.list=[]
        result = self.mycollection.find({},{"Mail"})
        for i in result:
            self.list.append(i["Mail"])

        self.uiSignin.pushButton.clicked.connect(self.accept)

    def accept(self):
        self.mail = self.uiSignin.lineEdit.text()
        self.password = self.uiSignin.lineEdit_2.text()
        k=1
        m=0
        for i in self.list:
            
            if i == self.mail:
                result = self.mycollection.find({"$or":[{"Mail":self.mail}]})
                m=1
                for i in result:
                    if i["Password"] == self.password:
                        self.changewindow()
                    else:
                        message = "Incorrect Password...\nTry Again..."
                        messagebx(message)                       
                        break    
            elif (k==len(self.list)) & (m==0):
                message = "Incorrect Name or Mail...\nTry Again..."
                messagebx(message)
            k=k+1

        # result = self.mycollection.find({"$and":[{"$or":[{"Name":self.name},{"Mail":self.name}]},{"Password":self.password}]})
        # print(result[0]["Name"])
        # print(result[0]["Password"])
    def changewindow(self):
        self.w=ResearchWindow()
        self.w.show()
        self.hide()
       
class ResearchWindow(QMainWindow):
    def __init__(self):
        super(ResearchWindow,self).__init__()
        self.uiResearch = Ui_ResearchWindow() 
        self.uiResearch.setupUi(self)
        self.setStyleSheet("QWidget#ResearchWindow {background-image: url(research.png)}")
        self.setWindowTitle("Advice Movie")
        self.setWindowIcon(QIcon("video-camera.png"))
        actors = register.actors()
        self.uiResearch.comboActor.addItems(actors)
        self.mycollection = connection("Movies")
        result = self.mycollection.find({},{"genre"})
        _genre = [""]
        for i in result:
            _genre.append(i["genre"])
        Seri = pd.Series(_genre)
        self.genre = Seri.unique()
        self.uiResearch.comboGenre.addItems(self.genre)
        self.uiResearch.pushButton.clicked.connect(self.filter)
        self.uiResearch.comboChoose.currentIndexChanged[str].connect(self.moviefeature)
        self.uiResearch.commandLinkButton.clicked.connect(self.searchgoogle)
    def filter(self):
        Genre = self.uiResearch.comboGenre.currentText()
        Actor = self.uiResearch.comboActor.currentText()
        MinImdb = self.uiResearch.doubleSpinBox.value()
        Duration = self.uiResearch.doubleSpinBox_2.value()

        self.mycollection = connection("Movies")
        
        self.uiResearch.comboChoose.clear()
        if (Actor=="") & (Genre==""):
            result = self.mycollection.find({ "$and": [ { "star_rating": { "$gte": MinImdb } }, { "duration": { "$lte": Duration} }] } )
            for i in result:
                self.uiResearch.comboChoose.addItem(i["title"])
            if self.uiResearch.comboChoose.currentText() =="":
                self.uiResearch.comboChoose.addItem("Not Found")
        elif Actor=="":
        
            result = self.mycollection.find({ "$and": [ { "star_rating": { "$gte": MinImdb } }, { "duration": { "$lte": Duration} },{"genre":Genre}] } )
            for i in result:
                self.uiResearch.comboChoose.addItem(i["title"])
            if self.uiResearch.comboChoose.currentText() =="":
                self.uiResearch.comboChoose.addItem("Not Found")
        elif Genre=="":

            result = self.mycollection.find({ "$and": [ { "star_rating": { "$gte": MinImdb } }, { "duration": { "$lte": Duration} },{"actors_list":{"$regex":Actor}}] } )
            for i in result:
                self.uiResearch.comboChoose.addItem(i["title"])
            if self.uiResearch.comboChoose.currentText() =="":
                self.uiResearch.comboChoose.addItem("Not Found")
        elif (Actor!="") & (Genre!=""):
            result = self.mycollection.find({ "$and": [ { "star_rating": { "$gte": MinImdb } }, { "duration": { "$lte": Duration} },{"actors_list":{"$regex":Actor}},{"genre":Genre}] } )
            for i in result:
                self.uiResearch.comboChoose.addItem(i["title"])
            if self.uiResearch.comboChoose.currentText() =="":
                self.uiResearch.comboChoose.addItem("Not Found")
        else:
            self.uiResearch.comboChoose.addItem("Not Found")
    def moviefeature(self,movie):
        self.mycollection = connection("Movies")
        result = self.mycollection.find({ "title":movie})
        for i in result:
            self.uiResearch.txtImdb.setText(str(i["star_rating"]))
            self.uiResearch.txtGenre.setText(i["genre"])
            self.uiResearch.txtMovie.setText(i["title"])
            self.uiResearch.txtActor.setText(i["actors_list"].strip("[']").replace("', '",","))
            self.uiResearch.lineEdit_5.setText(str(i["duration"]))

    def searchgoogle(self):
        search = self.uiResearch.comboChoose.currentText()
        self.browser=webdriver.Chrome()
        self.browser.get("https://www.google.com.tr/")
        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(search)
        time.sleep(2)
        search = self.browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[2]/div[2]/div[2]/center/input[1]')
        search.send_keys(Keys.ENTER)
def app():
    app = QApplication(sys.argv)
    win = MainForm()
    sys.exit(app.exec_())

app()