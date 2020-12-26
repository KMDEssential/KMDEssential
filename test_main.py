import sys
import io
import csv
import random
import threading
import sqlite3
from datetime import datetime

from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets


import time
import random

import worker
import manageserial
import getserver
import UI_main

VERSION = "0.1.0"

form_class = uic.loadUiType("UI_main.ui")[0]
# form_class = UI_main.Ui_mainWindow()

# IS_TEST = False
# IS_TEST = 0 # 실제작업
# IS_TEST = 1 # 테스트
# IS_TEST = 2 # 테스트크롤링
IS_TEST = 1
UNREGISTERD_BLOG_COUNT = 1
UNREGISTERD_KEYWORD_COUNT = 2
DELAY_TIME = 5

DUEDATE = 20210632

class WindowClass(QMainWindow, form_class):
# class WindowClass(QMainWindow, UI_main.Ui_mainWindow):    
    def __init__(self):
        super().__init__()

        self.config = dict()
        self.blogurl_list = list()
        self.blogtitle_list = list()
        self.keyword_list = list()        
        self.cfg_list = list()
        self.m = 0 
        self._running = True
        self.checkregist = False
        self.checkpath = False
        self.regist = False
        self.delaytime_min = DELAY_TIME
        self.delaytime_max = DELAY_TIME*2
        if IS_TEST == 1 : 
            self.delaytime_min = 1
            self.delaytime_max = 2
        self.validate = (int(datetime.today().strftime("%Y%m%d"))<DUEDATE)

        self.setupUi(self)
        self.dbCreate()
        self.refresh_init()

        if self.validate:
            self.Button_start.clicked.connect(self.crawling_start)
            self.Button_stop.clicked.connect(self.crawling_stop)
            self.pushButton_addurl.clicked.connect(self.addUrl)
            self.pushButton_saveurl.clicked.connect(self.saveUrl)
            self.pushButton_addkeyword.clicked.connect(self.addKeyword)
            self.pushButton_savekeyword.clicked.connect(self.saveKeyword)
            self.pushButton_register.clicked.connect(self.saveRegist)
        else : 
            self.disableAll()

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(600, 600)
        mainWindow.setMinimumSize(QtCore.QSize(600, 600))
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(10)
        mainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setMinimumSize(QtCore.QSize(231, 61))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.Button_start = QtWidgets.QPushButton(self.groupBox)
        self.Button_start.setGeometry(QtCore.QRect(140, 10, 100, 40))
        self.Button_start.setObjectName("Button_start")
        self.radioButton1 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton1.setGeometry(QtCore.QRect(10, 10, 120, 16))
        self.radioButton1.setObjectName("radioButton1")
        self.radioButton2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton2.setGeometry(QtCore.QRect(10, 30, 120, 16))
        self.radioButton2.setObjectName("radioButton2")
        self.Button_stop = QtWidgets.QPushButton(self.groupBox)
        self.Button_stop.setGeometry(QtCore.QRect(240, 10, 100, 40))
        self.Button_stop.setObjectName("Button_stop")
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget_result = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_result.setObjectName("tableWidget_result")
        self.tableWidget_result.setColumnCount(0)
        self.tableWidget_result.setRowCount(0)
        self.gridLayout_3.addWidget(self.tableWidget_result, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.pushButton_saveurl = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_saveurl.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_saveurl.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_saveurl.setObjectName("pushButton_saveurl")
        self.gridLayout_8.addWidget(self.pushButton_saveurl, 0, 2, 1, 1)
        self.pushButton_addkeyword = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_addkeyword.setMinimumSize(QtCore.QSize(130, 0))
        self.pushButton_addkeyword.setMaximumSize(QtCore.QSize(130, 16777215))
        self.pushButton_addkeyword.setObjectName("pushButton_addkeyword")
        self.gridLayout_8.addWidget(self.pushButton_addkeyword, 0, 4, 1, 1)
        self.pushButton_savekeyword = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_savekeyword.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_savekeyword.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_savekeyword.setObjectName("pushButton_savekeyword")
        self.gridLayout_8.addWidget(self.pushButton_savekeyword, 0, 5, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem, 0, 0, 1, 1)
        self.pushButton_addurl = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_addurl.setMinimumSize(QtCore.QSize(130, 0))
        self.pushButton_addurl.setMaximumSize(QtCore.QSize(130, 16777215))
        self.pushButton_addurl.setObjectName("pushButton_addurl")
        self.gridLayout_8.addWidget(self.pushButton_addurl, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem1, 0, 3, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_8, 0, 0, 1, 1)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.tableWidget_blogurl = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_blogurl.setObjectName("tableWidget_blogurl")
        self.tableWidget_blogurl.setColumnCount(0)
        self.tableWidget_blogurl.setRowCount(0)
        self.gridLayout_9.addWidget(self.tableWidget_blogurl, 0, 0, 1, 1)
        self.tableWidget_keyword = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_keyword.setObjectName("tableWidget_keyword")
        self.tableWidget_keyword.setColumnCount(0)
        self.tableWidget_keyword.setRowCount(0)
        self.gridLayout_9.addWidget(self.tableWidget_keyword, 0, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_9, 1, 0, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 10, 551, 501))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_regist = QtWidgets.QLabel(self.groupBox_3)
        self.label_regist.setGeometry(QtCore.QRect(10, 20, 521, 20))
        self.label_regist.setAlignment(QtCore.Qt.AlignCenter)
        self.label_regist.setObjectName("label_regist")
        self.pushButton_register = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_register.setGeometry(QtCore.QRect(450, 180, 93, 28))
        self.pushButton_register.setObjectName("pushButton_register")
        self.lineEdit_serial = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_serial.setGeometry(QtCore.QRect(60, 180, 381, 28))
        self.lineEdit_serial.setObjectName("lineEdit_serial")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(10, 180, 64, 28))
        self.label_3.setObjectName("label_3")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.groupBox_3)
        self.textBrowser_3.setGeometry(QtCore.QRect(10, 50, 531, 81))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser.setGeometry(QtCore.QRect(10, 280, 531, 131))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser_2.setGeometry(QtCore.QRect(10, 150, 531, 121))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 5, 531, 20))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_version = QtWidgets.QLabel(self.groupBox_2)
        self.label_version.setGeometry(QtCore.QRect(10, 30, 531, 20))
        self.label_version.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.setObjectName("label_version")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser_4.setGeometry(QtCore.QRect(10, 420, 531, 71))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.textBrowser_msg = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser_msg.setGeometry(QtCore.QRect(10, 70, 531, 71))
        self.textBrowser_msg.setObjectName("textBrowser_msg")
        self.gridLayout_13.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.action_config = QtWidgets.QAction(mainWindow)
        self.action_config.setObjectName("action_config")
        self.action_exit = QtWidgets.QAction(mainWindow)
        self.action_exit.setObjectName("action_exit")

        self.retranslateUi(mainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "KMD Essential"))
        self.Button_start.setText(_translate("mainWindow", "체크시작"))
        self.radioButton1.setText(_translate("mainWindow", "PC순위"))
        self.radioButton2.setText(_translate("mainWindow", "Mobile 순위"))
        self.Button_stop.setText(_translate("mainWindow", "정지"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("mainWindow", "블로그순위"))
        self.pushButton_saveurl.setText(_translate("mainWindow", "저장"))
        self.pushButton_addkeyword.setText(_translate("mainWindow", "키워드 추가"))
        self.pushButton_savekeyword.setText(_translate("mainWindow", "저장"))
        self.pushButton_addurl.setText(_translate("mainWindow", "블로그주소 추가"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("mainWindow", "키워드설정"))
        self.label_regist.setText(_translate("mainWindow", "등록문구"))
        self.pushButton_register.setText(_translate("mainWindow", "등록"))
        self.label_3.setText(_translate("mainWindow", "Serial : "))
        self.textBrowser_3.setHtml(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'굴림\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">KMD Essential은 등록없이도 사용가능합니다.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">등록없이 사용시 URL 2개, 키워드 10개까지 사용가능합니다</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">등록이 필요한 경우에는 Contact us 를 참고해주세요.</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("mainWindow", "Register"))
        self.textBrowser.setHtml(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'굴림\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji\'; font-size:9pt; color:#24292e; background-color:#ffffff;\">면책 조항</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji\'; font-size:9pt; color:#24292e; background-color:#ffffff;\">본 소프트웨어는 저작권 소유자 및 기여자에 의해 있는 그대로 제공되며, 상품성, 특정 목적에의 적합성에 대한 묵시적 보증 포함 (이에 한정되지는 않음) 명시적 또는 묵시적 보증을 배제한다. 어떠한 경우에도 저작권 소유자 또는 기여자는 계약, 엄격 책임 또는 (과실 및 기타 사유 포함) 불법 행위 등 사유 및 책임 이론에 관계없이, (대체 제품 또는 서비스 조달; 사용, 데이터 또는 이익 상실; 사업 중단 포함; 이에 한정되지는 않음) 본 소프트웨어 사용 관련 직접, 간접, 파생적, 특별, 징벌적 또는 결과적 손해에 대해 책임을 지지 않는다. 이러한 손해 가능성을 사전에 알고 있은 경우도 마찬가지이다.</span></p></body></html>"))
        self.textBrowser_2.setHtml(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'굴림\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">저작권의 범위</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">이 프로그램은 KMD licence를 보유한자만이 사용할 수 있습니다.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">KMD licence 를 보유하지 않은 자의 복제, 전파, 사용을 금지합니다.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">이 프로그램의 소스를 사용하여 수정하여 사용하는 것을 허용합니다.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">이 프로그램의 소스와 이 소스 부분 또는 전부를 이용하여 만든 프로그램을 </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">배포하는 것을 허용하지 않습니다.</span></p></body></html>"))
        self.label.setText(_translate("mainWindow", "KMD Essential"))
        self.label_version.setText(_translate("mainWindow", "v 0.0.1"))
        self.textBrowser_4.setHtml(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'굴림\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">contact us : kmdessential@gmail.com</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">https://github.com/KMDEssential/KMDEssential</p></body></html>"))
        self.textBrowser_msg.setHtml(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'굴림\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">현재 버전은 v 0.0.1 입니다.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">최신 버전은 v 0.0.1 입니다.</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("mainWindow", "About.."))
        self.action_config.setText(_translate("mainWindow", "환경설정"))
        self.action_config.setShortcut(_translate("mainWindow", "Ctrl+F"))
        self.action_exit.setText(_translate("mainWindow", "종료"))
        self.action_exit.setShortcut(_translate("mainWindow", "Ctrl+Q"))


    def crawling_start(self):
        self._running = True
        cfg_list = list()
        cfg_list.append('ispc')
        self.dbSaveconfig(cfg_list)
        self.disable_button()
        is_PC = self.radioButton1.isChecked()
        self.t1 = threading.Thread(target=self.startthread, args=(is_PC,))
        self.t1.start()

    def crawling_stop(self):
        self._running = False

    def dbCreate(self):
        conn = sqlite3.connect("KMDessential.cfg")
        with conn:
            c = conn.cursor()
            c.execute("CREATE TABLE IF NOT EXISTS blogurl \
                (seq integer PRIMARY KEY AUTOINCREMENT, url text)")

            c.execute("CREATE TABLE IF NOT EXISTS keyword \
                (seq integer PRIMARY KEY AUTOINCREMENT, keyword text)")

            c.execute("CREATE TABLE IF NOT EXISTS config \
                (seq integer PRIMARY KEY AUTOINCREMENT, name text UNIQUE, content text)")

            conn.commit()

    def dbOpen(self):
        conn = sqlite3.connect("KMDessential.cfg")
        with conn:
            c = conn.cursor()
            c.execute("select name,content from config")
            rows = c.fetchall()
            for row in rows:
                self.config[row[0]]= row[1]

            c.execute("select url from blogurl")
            rows = c.fetchall()
            self.blogurl_list = list()
            for row in rows:
                self.blogurl_list.append(str(row[0]))

            c.execute("select keyword from keyword")
            rows = c.fetchall()
            self.keyword_list = list()
            for row in rows:
                self.keyword_list.append(str(row[0]))

        self.blogtitle_list = list()
        for key in self.blogurl_list:
            if 'blog.naver.com/' in key:
                self.blogtitle_list.append(key.split('blog.naver.com')[1].split('/')[1])

    def dbSaveurl(self):
        conn = sqlite3.connect("KMDessential.cfg")
        with conn:
            c = conn.cursor()
            c.execute("DELETE FROM blogurl")
            conn.commit()
        with conn:
            c = conn.cursor()
            for item in self.blogurl_list :
                c.execute("INSERT INTO blogurl(url) VALUES(?)", (item,))
            conn.commit()

    def dbSavekeyword(self):
        conn = sqlite3.connect("KMDessential.cfg")
        with conn:
            c = conn.cursor()
            c.execute("DELETE FROM keyword")
            conn.commit()
        with conn:
            c = conn.cursor()
            for item in self.keyword_list :
                c.execute("INSERT INTO keyword(keyword) VALUES(?)", (item,))
            conn.commit()

    def dbSaveconfig(self, cfg_list):
        if 'ispc' in cfg_list:
            if self.radioButton1.isChecked() : self.config['ispc'] = '1'
            elif self.radioButton2.isChecked() : self.config['ispc'] = '0'
            print(self.config['ispc'])
            conn = sqlite3.connect('KMDessential.cfg')
            c = conn.cursor()
            with conn:  
                c.execute("INSERT OR REPLACE INTO config(name,content) VALUES(?,?)", ('ispc',self.config['ispc']))
                conn.commit()   
        if 'serial' in cfg_list:
            conn = sqlite3.connect('KMDessential.cfg')
            c = conn.cursor()
            with conn:  
                c.execute("INSERT OR REPLACE INTO config(name,content) VALUES(?,?)", ('serial',self.config['serial']))
                conn.commit()   
        if 'regdate' in cfg_list:
            conn = sqlite3.connect('KMDessential.cfg')
            c = conn.cursor()
            with conn:  
                c.execute("INSERT OR REPLACE INTO config(name,content) VALUES(?,?)", ('regdate',self.config['regdate']))
                conn.commit()   
        if 'pathserial' in cfg_list:
            conn = sqlite3.connect('KMDessential.cfg')
            c = conn.cursor()
            with conn:  
                c.execute("INSERT OR REPLACE INTO config(name,content) VALUES(?,?)", ('pathserial',self.config['pathserial']))
                conn.commit()   

    def trim_url(self, url):
        url=url.replace("//","/")
        url=url.replace("..",".")
        result =''
        if 'blog.naver.com/' in url:
            result = 'blog.naver.com/'+url.split('blog.naver.com')[1].split('/')[1]
        return result

    def refresh_init(self):
        self.dbOpen()
        self.setup_main()
        self.setup_config_blogurl()
        self.setup_config_keyword()
        self.setup_regist()

    def refresh_blogurl(self):
        self.dbOpen()
        self.setup_main()
        self.setup_config_blogurl()

    def refresh_keyword(self):
        self.dbOpen()
        self.setup_main()
        self.setup_config_keyword()

    def setup_main(self):
        table_result = self.tableWidget_result
        if len(self.blogtitle_list) > 0 : table_result.setColumnCount(len(self.blogtitle_list))
        else : table_result.setColumnCount(1)
        if len(self.keyword_list) > 0 : table_result.setRowCount(len(self.keyword_list))
        else : table_result.setRowCount(1)
        table_result.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for m in range(0, len(self.blogtitle_list)):
            table_result.setColumnWidth(m,100)
        table_result.setSelectionMode(QAbstractItemView.ExtendedSelection)
        if len(self.keyword_list) > 0 : table_result.setVerticalHeaderLabels(self.keyword_list)
        if len(self.blogtitle_list) > 0 : table_result.setHorizontalHeaderLabels(self.blogtitle_list)
        if  not self.config.get('ispc') : self.config['ispc'] = '2'
        if self.config['ispc'] == '1' : self.radioButton1.setChecked(True)
        else : self.radioButton2.setChecked(True)

        table_blog_url = self.tableWidget_blogurl
        table_blog_url.setSelectionMode(QAbstractItemView.ExtendedSelection)
        table_blog_url.setColumnWidth(0,250)

    def setup_config_blogurl(self):
        table_blogurl = self.tableWidget_blogurl
        table_blogurl.setColumnCount(1)
        if len(self.blogurl_list) > 0 : table_blogurl.setRowCount(len(self.blogurl_list))
        else : table_blogurl.setRowCount(1)
        table_blogurl.verticalHeader().setVisible(False)
        table_blogurl.horizontalHeader().setVisible(False)
        table_blogurl.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        try:
            for n, item in enumerate(self.blogurl_list):
                if(item==0):
                    item = ' '        
                newitem = QTableWidgetItem(str(item))
                newitem.setTextAlignment(Qt.AlignVCenter)
                table_blogurl.setItem(0, n, newitem)
        except:
            pass
        table_blogurl.setEditTriggers(QAbstractItemView.AllEditTriggers)

    def setup_config_keyword(self):
        table_keyword = self.tableWidget_keyword
        table_keyword.setColumnCount(1)
        if len(self.keyword_list) > 0 : table_keyword.setRowCount(len(self.keyword_list))
        else : table_keyword.setRowCount(1)
        table_keyword.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table_keyword.verticalHeader().setVisible(False)
        table_keyword.horizontalHeader().setVisible(False)
        table_keyword.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        try:
            for n, item in enumerate(self.keyword_list):
                if(item==0):
                    item = ' '        
                newitem = QTableWidgetItem(str(item))
                newitem.setTextAlignment(Qt.AlignVCenter)
                table_keyword.setItem(0, n, newitem)
        except:
            pass
        table_keyword.setEditTriggers(QAbstractItemView.AllEditTriggers)

    def setup_regist(self):
        label_regist = self.label_regist
        self.label_version.setText("v "+VERSION)
        self.checkregist = self.checkRegist()
        self.checkpath = self.checkPath()
        if self.checkregist and self.checkpath:
            self.regist = True
            self.lineEdit_serial.setEnabled(False)
            self.pushButton_register.setEnabled(False)
            label_regist.setText('이 프로그램은 정상 등록되었습니다.')
        if not self.checkpath :
            label_regist.setText('이 프로그램의 경로가 변경되었습니다.')
        if not self.checkregist :
            label_regist.setText('이 프로그램은 등록되지 않았습니다.')
        if not self.validate:
            label_regist.setText('이 프로그램의 사용기한이 만료되었습니다.')
        
        server = getserver.getServer()
        server.version = VERSION
        msg = server.getmsg()
        self.textBrowser_msg.setPlainText(msg)
        version_latest = server.getversion()

    def addUrl(self):
        table = self.tableWidget_blogurl
        row_count = table.rowCount()
        if self.regist == False and row_count >= UNREGISTERD_BLOG_COUNT:
            QMessageBox.about(self, "블로그 추가 제한", "블로그 개수는 "+ str(UNREGISTERD_BLOG_COUNT)  +"개까지 가능합니다.")
        else : 
            table.setRowCount(row_count+1)   # row 추가        

    def saveUrl(self):
        table = self.tableWidget_blogurl
        row_count = table.rowCount()
        self.blogurl_list = list()
        for n in range(row_count):
            if table.item(n,0) != None : 
                url = self.trim_url(table.item(n,0).text())
                if url != '':
                    self.blogurl_list.append(url)
                    print(url)
        self.dbSaveurl()
        self.refresh_blogurl()

    def addKeyword(self):
        table = self.tableWidget_keyword
        row_count = table.rowCount()
        if self.regist == False and row_count >= UNREGISTERD_KEYWORD_COUNT:
            QMessageBox.about(self, "키워드 추가 제한", "키워드 갯수는 "+ str(UNREGISTERD_KEYWORD_COUNT)+"개까지 가능합니다.")
        else : 
            table.setRowCount(row_count+1)   # row 추가        

    def saveKeyword(self):
        table = self.tableWidget_keyword
        row_count = table.rowCount()
        self.keyword_list = list()
        for n in range(row_count):
            if table.item(n,0) != None : 
                keyword = table.item(n,0).text()
                if keyword != '':
                    self.keyword_list.append(keyword)
                    print(keyword)
        self.dbSavekeyword()
        self.refresh_keyword()

    def saveRegist(self):
        cfg_list = list()
        serial = self.lineEdit_serial.text()
        serialclass = manageserial.manageSerial()
        regdate = datetime.today().strftime("%Y%m%d")
        self.checkregist = serialclass.checkSerial(serial,regdate)
        if self.checkregist:
            self.config['serial'] = serial
            self.config['regdate'] = regdate
            self.config['pathserial'] = serialclass.makePathserial(serial)
            
            cfg_list.append('serial')
            cfg_list.append('regdate')
            cfg_list.append('pathserial')
            self.dbSaveconfig(cfg_list)
            self.setup_regist()
        if self.checkregist : 
            QMessageBox.about(self, "Register", "등록이 완료되었습니다.")
            self.lineEdit_serial.setText("")
            self.lineEdit_serial.setEnabled(False)
            self.pushButton_register.setEnabled(False)
        else:
            QMessageBox.about(self, "Register", "등록을 실패했습니다.")

    def checkRegist(self):
        result = False
        clsserial = manageserial.manageSerial()
        is_serial = self.config.get('serial')
        is_regdate = self.config.get('regdate')
        if is_serial and is_regdate:
            serial = self.config['serial']
            regdate = self.config['regdate']
            result = clsserial.checkSerial(serial, regdate)
        return result

    def checkPath(self):
        result = False
        clsserial = manageserial.manageSerial()
        is_serial = self.config.get('serial')
        is_pathserial = self.config.get('pathserial')
        if is_serial and is_pathserial:
            serial = self.config['serial']
            pathserial = self.config['pathserial']
            result = clsserial.checkPathserial(serial, pathserial)
        return result

    def disable_button(self):
        self.radioButton1.setEnabled(False)
        self.radioButton2.setEnabled(False)
        self.Button_start.setEnabled(False)

    def enable_button(self):
        self.radioButton1.setEnabled(True)
        self.radioButton2.setEnabled(True)
        self.Button_start.setEnabled(True)

    def disableAll(self):
        self.Button_start.setEnabled(False)
        self.Button_stop.setEnabled(False)
        self.pushButton_addurl.setEnabled(False)
        self.pushButton_saveurl.setEnabled(False)
        self.pushButton_addkeyword.setEnabled(False)
        self.pushButton_savekeyword.setEnabled(False)
        self.pushButton_register.setEnabled(False)
        self.tableWidget_result.setEnabled(False)
        self.tableWidget_blogurl.setEnabled(False)
        self.tableWidget_keyword.setEnabled(False)
        self.radioButton1.setEnabled(False)
        self.radioButton2.setEnabled(False)        

    def startthread(self, is_PC):
        try:
            for m, key in enumerate(self.keyword_list):
                if self._running == False : break
                if self.regist == False and m >= UNREGISTERD_KEYWORD_COUNT : break
                self.worker = worker.Worker()
                self.worker.is_test = IS_TEST
                self.worker.is_PC = is_PC
                self.worker.keyword = key
                self.worker.blog_url_list = self.blogurl_list
                self.m_row = m
                self.worker.finished.connect(self.update_table_widget)
                self.worker.start()
                time.sleep(random.randrange(self.delaytime_min,self.delaytime_max))
        except IndexError as e:
            print(e)
        self.enable_button()

    @pyqtSlot(list)
    def update_table_widget(self, list):
        table_result = self.tableWidget_result
        try:
            for n, item in enumerate(list):
                if(item==0):
                    item = ' '        
                newitem = QTableWidgetItem(str(item))
                newitem.setTextAlignment(Qt.AlignHCenter)
                newitem.setTextAlignment(Qt.AlignVCenter)
                newitem.setTextAlignment(Qt.AlignCenter)
                table_result.setItem(self.m_row, n, newitem)
        except:
            pass

    def keyPressEvent(self, ev):
        if (ev.key() == Qt.Key_C) and (ev.modifiers() & Qt.ControlModifier): 
            self.copySelection()

    def copySelection(self): #헤더빼고 복사
        selection = self.tableWidget_result.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream).writerows(table)
            QApplication.clipboard().setText(stream.getvalue().replace(",","\t"))

    def copySelection_temp(self): #해더포함복사
        selected = self.tableWidget_result.selectedRanges()

        s = '\t'+"\t".join([str(self.tableWidget_result.horizontalHeaderItem(i).text()) for i in range(selected[0].leftColumn(), selected[0].rightColumn()+1)])
        s = s + '\n'

        for r in range(selected[0].topRow(), selected[0].bottomRow()+1):
            s += self.tableWidget_result.verticalHeaderItem(r).text() + '\t'
            for c in range(selected[0].leftColumn(), selected[0].rightColumn()+1):
                try:
                    s += str(self.tableWidget_result.item(r,c).text()) + "\t"
                except AttributeError:
                    s += "\t"
            s = s[:-1] + "\n" #eliminate last '\t'
        QApplication.clipboard().setText(s)

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = WindowClass()
    mywindow.show()
    app.exec_()