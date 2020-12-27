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
# form_class = uic.loadUiType("UI_main.ui")[0]

# IS_TEST = 0 # 실제작업
# IS_TEST = 1 # 테스트
# IS_TEST = 2 # 테스트크롤링
IS_TEST = 0
UNREGISTERD_BLOG_COUNT = 2
UNREGISTERD_KEYWORD_COUNT = 10
DELAY_TIME = 10

DUEDATE = 20210632



class WindowClass(QMainWindow, UI_main.Ui_mainWindow):
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
        self.duedate = (int(datetime.today().strftime("%Y%m%d"))<DUEDATE)
        self.validate = self.checkValidate()

        self.setupUi(self)
        self.dbCreate()
        self.refresh_init()

        if self.duedate and self.validate:
            self.Button_start.clicked.connect(self.crawling_start)
            self.Button_stop.clicked.connect(self.crawling_stop)
            self.pushButton_addurl.clicked.connect(self.addUrl)
            self.pushButton_saveurl.clicked.connect(self.saveUrl)
            self.pushButton_addkeyword.clicked.connect(self.addKeyword)
            self.pushButton_savekeyword.clicked.connect(self.saveKeyword)
            self.pushButton_register.clicked.connect(self.saveRegist)
        else : 
            self.disableAll()

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
        conn = sqlite3.connect("KMDEssential.cfg")
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
        conn = sqlite3.connect("KMDEssential.cfg")
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
        conn = sqlite3.connect("KMDEssential.cfg")
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
        conn = sqlite3.connect("KMDEssential.cfg")
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
            conn = sqlite3.connect('KMDEssential.cfg')
            c = conn.cursor()
            with conn:  
                c.execute("INSERT OR REPLACE INTO config(name,content) VALUES(?,?)", ('ispc',self.config['ispc']))
                conn.commit()   
        if 'serial' in cfg_list:
            conn = sqlite3.connect('KMDEssential.cfg')
            c = conn.cursor()
            with conn:  
                c.execute("INSERT OR REPLACE INTO config(name,content) VALUES(?,?)", ('serial',self.config['serial']))
                conn.commit()   
        if 'regdate' in cfg_list:
            conn = sqlite3.connect('KMDEssential.cfg')
            c = conn.cursor()
            with conn:  
                c.execute("INSERT OR REPLACE INTO config(name,content) VALUES(?,?)", ('regdate',self.config['regdate']))
                conn.commit()   
        if 'pathserial' in cfg_list:
            conn = sqlite3.connect('KMDEssential.cfg')
            c = conn.cursor()
            with conn:  
                c.execute("INSERT OR REPLACE INTO config(name,content) VALUES(?,?)", ('pathserial',self.config['pathserial']))
                conn.commit()   
        if 'validate' in cfg_list:
            conn = sqlite3.connect('KMDEssential.cfg')
            c = conn.cursor()
            with conn:  
                c.execute("INSERT OR REPLACE INTO config(name,content) VALUES(?,?)", ('validate',self.config['validate']))
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
        if not self.duedate:
            label_regist.setText('이 프로그램의 사용기한이 만료되었습니다.')
        if not self.validate:
            label_regist.setText('이 프로그램의 사용권한이 중단되었습니다.')
        
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

    def checkValidate(self):
        server = getserver.getServer()
        validate = server.getValidate(VERSION)
        return validate

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