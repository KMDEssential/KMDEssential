# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\UI_main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(600, 600)
        mainWindow.setMinimumSize(QtCore.QSize(600, 600))
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(10)
        mainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(16, 16))
        self.tabWidget.setMovable(True)
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
        self.Button_start.setGeometry(QtCore.QRect(0, 10, 100, 40))
        self.Button_start.setObjectName("Button_start")
        self.radioButton1 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton1.setGeometry(QtCore.QRect(220, 12, 120, 16))
        self.radioButton1.setObjectName("radioButton1")
        self.radioButton2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton2.setGeometry(QtCore.QRect(220, 35, 120, 16))
        self.radioButton2.setObjectName("radioButton2")
        self.Button_stop = QtWidgets.QPushButton(self.groupBox)
        self.Button_stop.setGeometry(QtCore.QRect(100, 10, 100, 40))
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
        self.pushButton_saveurl.setMinimumSize(QtCore.QSize(70, 30))
        self.pushButton_saveurl.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_saveurl.setObjectName("pushButton_saveurl")
        self.gridLayout_8.addWidget(self.pushButton_saveurl, 0, 2, 1, 1)
        self.pushButton_addkeyword = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_addkeyword.setMinimumSize(QtCore.QSize(150, 30))
        self.pushButton_addkeyword.setMaximumSize(QtCore.QSize(130, 16777215))
        self.pushButton_addkeyword.setObjectName("pushButton_addkeyword")
        self.gridLayout_8.addWidget(self.pushButton_addkeyword, 0, 4, 1, 1)
        self.pushButton_savekeyword = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_savekeyword.setMinimumSize(QtCore.QSize(70, 30))
        self.pushButton_savekeyword.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pushButton_savekeyword.setObjectName("pushButton_savekeyword")
        self.gridLayout_8.addWidget(self.pushButton_savekeyword, 0, 5, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem, 0, 0, 1, 1)
        self.pushButton_addurl = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_addurl.setMinimumSize(QtCore.QSize(150, 30))
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
        self.pushButton_register.setGeometry(QtCore.QRect(450, 210, 93, 28))
        self.pushButton_register.setObjectName("pushButton_register")
        self.lineEdit_serial = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_serial.setGeometry(QtCore.QRect(10, 210, 431, 28))
        self.lineEdit_serial.setObjectName("lineEdit_serial")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(20, 180, 64, 28))
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
        self.label.setGeometry(QtCore.QRect(10, 15, 531, 20))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_version = QtWidgets.QLabel(self.groupBox_2)
        self.label_version.setGeometry(QtCore.QRect(10, 40, 531, 20))
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
        self.label_regist.setText(_translate("mainWindow", "Register"))
        self.pushButton_register.setText(_translate("mainWindow", "등록"))
        self.label_3.setText(_translate("mainWindow", "Serial"))
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
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji\'; color:#24292e; background-color:#ffffff;\">면책 조항</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji\'; color:#24292e; background-color:#ffffff;\">본 소프트웨어는 저작권 소유자 및 기여자에 의해 있는 그대로 제공되며, 상품성, 특정 목적에의 적합성에 대한 묵시적 보증 포함 (이에 한정되지는 않음) 명시적 또는 묵시적 보증을 배제한다. 어떠한 경우에도 저작권 소유자 또는 기여자는 계약, 엄격 책임 또는 (과실 및 기타 사유 포함) 불법 행위 등 사유 및 책임 이론에 관계없이, (대체 제품 또는 서비스 조달; 사용, 데이터 또는 이익 상실; 사업 중단 포함; 이에 한정되지는 않음) 본 소프트웨어 사용 관련 직접, 간접, 파생적, 특별, 징벌적 또는 결과적 손해에 대해 책임을 지지 않는다. 이러한 손해 가능성을 사전에 알고 있은 경우도 마찬가지이다.</span></p></body></html>"))
        self.textBrowser_2.setHtml(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'굴림\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">저작권의 범위</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">이 프로그램은 KMD licence를 보유한자만이 사용할 수 있습니다.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">KMD licence 를 보유하지 않은 자의 복제, 전파, 사용을 금지합니다.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">이 프로그램의 소스를 사용하여 수정하여 사용하는 것을 허용합니다.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">이 프로그램의 소스와 이 소스 부분 또는 전부를 이용하여 만든 프로그램을 </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">배포하는 것을 허용하지 않습니다.</p></body></html>"))
        self.label.setText(_translate("mainWindow", "KMD Essential"))
        self.label_version.setText(_translate("mainWindow", "v 0.1.0"))
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

