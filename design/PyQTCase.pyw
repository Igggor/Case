# -*- coding: utf-8 -*-
from array import array
from words_count import counts_info_words, get_meta
from Bd import get_all, get_link, add_link_to_bd, find_link, is_link_in_bd, clear_bd
from Neron_for_case import get_state
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QRunnable, QThreadPool, QUrl, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import imp
import time
import os
import sys
import webbrowser
import csv
FiltersFrameFlag = False
a = []
threadpool = QThreadPool()

class workerlabel(QRunnable):
    def __init__(self):
        super(workerlabel, self).__init__()
    def run(self):
        ui.ActionStatusLabel.show()
        time.sleep(2.7)
        ui.ActionStatusLabel.hide()

class Ui_MainWindow(object):
    global threadpool
    def open (self):
        self.ActionStatusLabel.setText("Подождите, анализируем полученный список...")
        self.ActionStatusLabel.adjustSize()
        self.ActionStatusLabel.move(795-self.ActionStatusLabel.width(), 95)
        self.ActionStatusLabel.show()
        c = 0
        filepath = QFileDialog.getOpenFileName(self.CentralWidget, 'Загрузить список ссылок для анализа', '/Users', 'CSV File (*.csv)')
        try:
            with open(filepath[0], encoding='utf-8') as r_file:
                file_reader = csv.reader(r_file, delimiter = ",")
                for row in file_reader:
                    print(row[0])
                    a = get_meta(link=row[0])
                    a = counts_info_words(a)
                    if (a != "Can't connect"):
                        f = get_state(a)
                        ss = add_link_to_bd(link=row[0], type=f, info="None")
                        if ss == "New line added":
                            c += 1
            self.ActionStatusLabel.hide()
            self.loadData()
            self.ActionStatusLabel.setText(f"Ссылок из файла успешно загружено: {c}")
            self.ActionStatusLabel.adjustSize()
            self.ActionStatusLabel.move(795-self.ActionStatusLabel.width(), 95)
            self.label_show()
        except Exception as ex:
            print(ex)
            self.ActionStatusLabel.hide()
    def deleteDB(self):
        clear_bd()
        self.loadData()
        self.ActionStatusLabel.setText("Список ссылок успешно удалён")
        self.ActionStatusLabel.adjustSize()
        self.ActionStatusLabel.move(795-self.ActionStatusLabel.width(), 95)
        self.label_show()
    def keyPressEvent(self, e):
        if e.key()  == Qt.Key_Return :
            self.search_link_by_type()
        elif e.key() == Qt.Key_Enter :   
            self.search_link_by_type()
    def mousePressEvent(self, event):
        global FiltersFrameFlag
        if event.button() == Qt.LeftButton:
            if not self.FiltersFrame.isHidden():
                self.FiltersFrame.hide()
                FiltersFrameFlag = not FiltersFrameFlag
    def buttonIndividual(self):
        global a
        sender = MainWindow.sender()
        webbrowser.open_new_tab(a[int(sender.objectName())][0])
    def deleteIndividual(self):
        global a
        sender = MainWindow.sender()
        clear_bd(a[int(sender.objectName())][0])
        self.loadData()
        self.ActionStatusLabel.setText("Ссылка успешно удалена")
        self.ActionStatusLabel.adjustSize()
        self.ActionStatusLabel.move(795-self.ActionStatusLabel.width(), 95)
        self.label_show()
    def loadData(self):
        global a
        self.BDView.clear()
        types = ["mes", "games", "shop", "news", "video", "else"]
        a = []
        for el in types:
            n = find_link(type=el)
            if (n != "No links whis this type"):
                for i in n:
                    k = [i, el]
                    a.append(k)
        for i in range(len(a)):
            type = ""
            if(a[i][1] == "mes"): type = "Мессенджер"
            if(a[i][1] == "news"): type = "Новости"
            if(a[i][1] == "shop"): type = "Магазин"
            if(a[i][1] == "games"): type = "Игры"
            if(a[i][1] == "video"): type = "Видеохостинг"
            if(a[i][1] == "else"): type = "Другое"
            s = str(a[i][0])
            if len(s)>46:
                s = f'{i+1}) ' + s[0:46] + "...   -   " + type
            else:
                s = f'{i+1}) ' + s + "   -   " + type
            item = QListWidgetItem()
            item_widget = QWidget()
            line_text = QLabel(s)
            line_push_button = QPushButton("")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            line_push_button.setSizePolicy(sizePolicy)
            line_push_button.setObjectName(str(i))
            line_push_button.clicked.connect(self.buttonIndividual)
            line_delete_button = QPushButton("")
            line_delete_button.setSizePolicy(sizePolicy)
            line_delete_button.setObjectName(str(i))
            line_delete_button.clicked.connect(self.deleteIndividual)
            item_layout = QHBoxLayout()
            line_text.setStyleSheet("font-size: 17px;\n"
            "font-weight: 400;\n"
            "margin-top: 4px;\n")
            line_delete_button.setStyleSheet("QPushButton {\n"
            "margin-top: 6px;\n"
            "padding: 1px;"
            "font-size: 14px;\n"
            "background-color: whitesmoke;\n"
            "border: 0px;\n"
            "border-radius: 0px;\n"
            "border-radius: 7px\n"
            "}\n"
            "QPushButton:hover {\n"
            "background-color: rgb(120, 200, 255);\n"
            "}\n")
            line_push_button.setStyleSheet("QPushButton {\n"
            "margin-top: 6px;\n"
            "padding: 1px;"
            "font-size: 14px;\n"
            "background-color: whitesmoke;\n"
            "border: 0px;\n"
            "border-radius: 0px;\n"
            "border-radius: 7px\n"
            "}\n"
            "QPushButton:hover {\n"
            "background-color: rgb(120, 200, 255);\n"
            "}\n")
            plg_dir = os.path.dirname(__file__)
            icon_path = plg_dir + '/images/delete.png'
            icon = QtGui.QIcon(icon_path)
            line_delete_button.setIcon(icon)
            line_delete_button.setIconSize(QtCore.QSize(22, 20))
            icon_path1 = plg_dir + '/images/goto.png'
            icon1 = QtGui.QIcon(icon_path1)
            line_push_button.setIcon(icon1)
            line_push_button.setIconSize(QtCore.QSize(22, 20))
            item_widget.setStyleSheet("background-color: whitesmoke;\n")
            item_layout.addWidget(line_text)
            item_layout.addWidget(line_push_button)
            item_layout.addWidget(line_delete_button)
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(3)
            item_layout.addStretch(1)
            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self.BDView.addItem(item)
            self.BDView.setItemWidget(item, item_widget)
    def label_show(self):
        self.obj = workerlabel()
        threadpool.start(self.obj)

    def check_link(self):
        global FiltersFrameFlag
        if not self.FiltersFrame.isHidden():
            self.FiltersFrame.hide()
            FiltersFrameFlag = not FiltersFrameFlag
        link = self.SearchBar.text()
        self.SearchBar.clear()
        try:
            a = get_meta(link=link)
            if a != "Can't connect": a = counts_info_words(a)
            if (a != "Can't connect"):
                type_of_link = get_state(a)
                f = add_link_to_bd(link=link, type=type_of_link, info="")
                if (f == "Link is already in bd"):
                    self.ActionStatusLabel.setText("Ссылка уже содержится в базе данных")
                    self.ActionStatusLabel.adjustSize()
                    self.ActionStatusLabel.move(795-self.ActionStatusLabel.width(), 95)
                    self.label_show()
                    self.SearchBar.setText("")
                else:
                    with open("links.csv", mode="a", encoding='utf-8') as w_file:
                        file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
                        file_writer.writerow([link, type_of_link])
                    self.ActionStatusLabel.setText("Ссылка успешно добавлена")
                    self.ActionStatusLabel.adjustSize()
                    self.ActionStatusLabel.move(795-self.ActionStatusLabel.width(), 95)
                    self.label_show()
            else:
                self.ActionStatusLabel.setText("Ошибка! Не удалось подключиться к сайту")
                self.ActionStatusLabel.adjustSize()
                self.ActionStatusLabel.move(795-self.ActionStatusLabel.width(), 95)
                self.label_show()
        except:
            self.ActionStatusLabel.setText("Ошибка! Не удалось подключиться к сайту")
            self.ActionStatusLabel.adjustSize()
            self.ActionStatusLabel.move(795-self.ActionStatusLabel.width(), 95)
            self.label_show()
        self.loadData()
        print("check_link func successfully worked")


    def search_link_by_type(self):
        global a, FiltersFrameFlag
        if not self.FiltersFrame.isHidden():
            self.FiltersFrame.hide()
            FiltersFrameFlag = not FiltersFrameFlag
        textFilter = self.SearchBar.text()
        types = []
        if self.CheckBoxMessengers.isChecked():
            types.append("mes")
        if self.CheckBoxGames.isChecked():
            types.append("games")
        if self.CheckBoxShops.isChecked():
            types.append("shop")
        if self.CheckBoxNews.isChecked():
            types.append("news")
        if self.CheckBoxVideo.isChecked():
            types.append("video")
        if self.CheckBoxOther.isChecked():
            types.append("else")
        if types == []:
            types = ["mes", "games", "shop", "news", "video", "else"]
        a = []
        for el in types:
            n = find_link(type=el)
            if (n != "No links whis this type"):
                for i in n:
                    k = [i, el]
                    if textFilter != "":
                        if k[0].count(textFilter):
                            a.append(k)
                    else:
                        a.append(k)

        self.BDView.clear()
        if a == []:
            self.ActionStatusLabel.setText("Поиск по указанным фильтрам не дал результатов")
            self.ActionStatusLabel.adjustSize()
            self.ActionStatusLabel.move(795-self.ActionStatusLabel.width(), 95)
            self.label_show()
        else:
            for i in range(len(a)):
                type = ""
                if(a[i][1] == "mes"): type = "Мессенджер"
                if(a[i][1] == "news"): type = "Новости"
                if(a[i][1] == "shop"): type = "Магазин"
                if(a[i][1] == "games"): type = "Игры"
                if(a[i][1] == "video"): type = "Видеохостинг"
                if(a[i][1] == "else"): type = "Другое"
                s = str(a[i][0])
                if len(s)>46:
                    s = f'{i+1}) ' + s[0:46] + "...   -   " + type
                else:
                    s = f'{i+1}) ' + s + "   -   " + type
                item = QListWidgetItem()
                item_widget = QWidget()
                line_text = QLabel(s)
                line_push_button = QPushButton("")
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                line_push_button.setSizePolicy(sizePolicy)
                line_push_button.setObjectName(str(i))
                line_push_button.clicked.connect(self.buttonIndividual)
                line_delete_button = QPushButton("")
                line_delete_button.setSizePolicy(sizePolicy)
                line_delete_button.setObjectName(str(i))
                line_delete_button.clicked.connect(self.deleteIndividual)
                item_layout = QHBoxLayout()
                line_text.setStyleSheet("font-size: 17px;\n"
                "font-weight: 400;\n"
                "margin-top: 4px;\n")
                line_delete_button.setStyleSheet("QPushButton {\n"
                "margin-top: 6px;\n"
                "padding: 1px;"
                "font-size: 14px;\n"
                "background-color: whitesmoke;\n"
                "border: 0px;\n"
                "border-radius: 0px;\n"
                "border-radius: 7px\n"
                "}\n"
                "QPushButton:hover {\n"
                "background-color: rgb(120, 200, 255);\n"
                "}\n")
                line_push_button.setStyleSheet("QPushButton {\n"
                "margin-top: 6px;\n"
                "padding: 1px;"
                "font-size: 14px;\n"
                "background-color: whitesmoke;\n"
                "border: 0px;\n"
                "border-radius: 0px;\n"
                "border-radius: 7px\n"
                "}\n"
                "QPushButton:hover {\n"
                "background-color: rgb(120, 200, 255);\n"
                "}\n")
                plg_dir = os.path.dirname(__file__)
                icon_path = plg_dir + '/images/delete.png'
                icon = QtGui.QIcon(icon_path)
                line_delete_button.setIcon(icon)
                line_delete_button.setIconSize(QtCore.QSize(22, 20))
                icon_path1 = plg_dir + '/images/goto.png'
                icon1 = QtGui.QIcon(icon_path1)
                line_push_button.setIcon(icon1)
                line_push_button.setIconSize(QtCore.QSize(22, 20))
                item_widget.setStyleSheet("background-color: whitesmoke;\n")
                item_layout.addWidget(line_text)
                item_layout.addWidget(line_push_button)
                item_layout.addWidget(line_delete_button)
                item_layout.setContentsMargins(0, 0, 0, 0)
                item_layout.setSpacing(3)
                item_layout.addStretch(1)
                item_widget.setLayout(item_layout)
                item.setSizeHint(item_widget.sizeHint())
                self.BDView.addItem(item)
                self.BDView.setItemWidget(item, item_widget)
            self.ActionStatusLabel.setText(f"Количество результатов: {len(a)}")
            self.ActionStatusLabel.adjustSize()
            self.ActionStatusLabel.move(795-self.ActionStatusLabel.width(), 95)
            self.label_show()

    def FiltersFrameVisibilityStatus(self):
            global FiltersFrameFlag
            FiltersFrameFlag = not FiltersFrameFlag
            if FiltersFrameFlag:
                self.FiltersFrame.show()
            else:
                self.FiltersFrame.hide()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(810, 640)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        plg_dir = os.path.dirname(__file__)
        icon_path = plg_dir + '/images/DesktopIcon.png'
        icon = QtGui.QIcon(icon_path)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow {\n"
"}\n"
"QScrollBar:vertical {\n"
"background-color: rgb(107, 107, 107);\n"
"width: 17px;\n"
"margin: 15px 0 15px 0;\n"
"border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"background-color: rgb(0, 200, 255);\n"
"min-height: 30px;\n"
"border-radius: 7px;\n"
"}\n"
"QScrollBar::handle:vertical:hover {\n"
"background-color: rgb(120, 200, 255);\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"border: none;\n"
"background-color: rgb(0, 200, 255);\n"
"height: 15px;\n"
"border-top-right-radius: 7px;\n"
"subcontrol-position: top;\n"
"subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical:hover {\n"
"background-color: rgb(120, 200, 255);\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"border: none;\n"
"background-color: rgb(0, 200, 255);\n"
"height: 15px;\n"
"border-bottom-right-radius: 7px;\n"
"subcontrol-position: bottom;\n"
"subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:vertical:hover {\n"
"background-color: rgb(120, 200, 255);\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"background-color: rgb(107, 107, 107);\n"
"}")
        MainWindow.setIconSize(QtCore.QSize(30, 30))
        self.CentralWidget = QtWidgets.QWidget(MainWindow)
        self.CentralWidget.setMouseTracking(True)
        self.CentralWidget.setStyleSheet("QWidget {\n"
"background-color: rgb(85, 76, 76);\n"
"}")
        self.CentralWidget.setObjectName("CentralWidget")
        self.CentralWidget.keyPressEvent = self.keyPressEvent
        self.CentralWidget.mousePressEvent = self.mousePressEvent
        self.DownloadDBButton = QtWidgets.QToolButton(self.CentralWidget)
        self.DownloadDBButton.setGeometry(QtCore.QRect(734, 490, 50, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DownloadDBButton.sizePolicy().hasHeightForWidth())
        self.DownloadDBButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.DownloadDBButton.setFont(font)
        self.DownloadDBButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.DownloadDBButton.setFocusPolicy(QtCore.Qt.TabFocus)
        self.DownloadDBButton.setStyleSheet("QToolButton {\n"
"background-color: rgb(0, 200, 255);\n"
"border: 1px solid black;\n"
"border-radius: 7px;\n"
"}\n"
"QToolButton:hover {\n"
"background-color: rgb(120, 200, 255);\n"
"}")
        self.DownloadDBButton.setText("")
        icon_path2 = plg_dir + '/images/download.png'
        icon2 = QtGui.QIcon(icon_path2)
        self.DownloadDBButton.setIcon(icon2)
        self.DownloadDBButton.setIconSize(QtCore.QSize(30, 30))
        self.DownloadDBButton.setArrowType(QtCore.Qt.NoArrow)
        self.DownloadDBButton.setObjectName("DownloadDBButton")
        self.DownloadDBButton.clicked.connect(self.open)
        self.label = QtWidgets.QLabel(self.CentralWidget)
        self.label.setGeometry(QtCore.QRect(711, 470, 100, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(7)
        self.label.setFont(font)
        self.label.setStyleSheet("border: none;\n"
"")
        self.label.setObjectName("label")
        self.DeleteDBButton = QtWidgets.QToolButton(self.CentralWidget)
        self.DeleteDBButton.setGeometry(QtCore.QRect(734, 570, 50, 50))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DeleteDBButton.sizePolicy().hasHeightForWidth())
        self.DeleteDBButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.DeleteDBButton.setFont(font)
        self.DeleteDBButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.DeleteDBButton.setFocusPolicy(QtCore.Qt.TabFocus)
        self.DeleteDBButton.setStyleSheet("QToolButton {\n"
"background-color: rgb(0, 200, 255);\n"
"border: 1px solid black;\n"
"border-radius: 7px;\n"
"}\n"
"QToolButton:hover {\n"
"background-color: rgb(120, 200, 255);\n"
"}")
        self.DeleteDBButton.setText("")
        icon_path5 = plg_dir + '/images/delete.png'
        icon5 = QtGui.QIcon(icon_path5)
        self.DeleteDBButton.setIcon(icon5)
        self.DeleteDBButton.setIconSize(QtCore.QSize(30, 30))
        self.DeleteDBButton.setArrowType(QtCore.Qt.NoArrow)
        self.DeleteDBButton.setObjectName("DownloadDBButton")
        self.DeleteDBButton.clicked.connect(self.deleteDB)
        self.deletelabel = QtWidgets.QLabel(self.CentralWidget)
        self.deletelabel.setGeometry(QtCore.QRect(715, 550, 100, 20))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(7)
        self.deletelabel.setFont(font)
        self.deletelabel.setStyleSheet("border: none;\n"
"")
        self.deletelabel.setObjectName("label")
        self.deletelabel.setText("Удалить список")
        self.SearchBox = QtWidgets.QGroupBox(self.CentralWidget)
        self.SearchBox.setGeometry(QtCore.QRect(10, 10, 790, 70))
        self.SearchBox.setStyleSheet("border-radius: 20px;\n"
"background-color: rgb(107, 107, 107);\n"
"border: 3px solid rgb(0, 200, 255);\n"
"border-style: outset;")
        self.SearchBox.setTitle("")
        self.SearchBox.setObjectName("SearchBox")
        self.SearchBar = QtWidgets.QLineEdit(self.SearchBox)
        self.SearchBar.setGeometry(QtCore.QRect(52, 20, 610, 30))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.SearchBar.setFont(font)
        self.SearchBar.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.SearchBar.setToolTipDuration(-1)
        self.SearchBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.SearchBar.setAutoFillBackground(False)
        self.SearchBar.setStyleSheet("background-color: whitesmoke;\n"
"border: 1px solid black;\n"
"border-radius: 0px;\n"
"color: #000000;\n"
"padding-left: 5px;")
        self.SearchBar.setText("")
        self.SearchBar.setMaxLength(32767)
        self.SearchBar.setFrame(True)
        self.SearchBar.setCursorPosition(0)
        self.SearchBar.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SearchBar.setDragEnabled(False)
        self.SearchBar.setObjectName("SearchBar")
        self.SearchButton = QtWidgets.QPushButton(self.SearchBox)
        self.SearchButton.setEnabled(True)
        self.SearchButton.setGeometry(QtCore.QRect(13, 20, 40, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchButton.sizePolicy().hasHeightForWidth())
        self.SearchButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(8)
        self.SearchButton.setFont(font)
        self.SearchButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SearchButton.setFocusPolicy(QtCore.Qt.TabFocus)
        self.SearchButton.setStyleSheet("QPushButton {\n"
"background-color: rgb(0, 200, 255);\n"
"border: 1px solid black;\n"
"border-radius: 0px;\n"
"border-top-left-radius: 7px 7px;\n"
"border-bottom-left-radius: 7px 7px;\n"
"}\n"
"QPushButton:hover {\n"
"background-color: rgb(120, 200, 255);\n"
"}\n"
"")
        self.SearchButton.setText("")
        icon_path1 = plg_dir + '/images/SearchIcon.png'
        icon1 = QtGui.QIcon(icon_path1)
        self.SearchButton.setIcon(icon1)
        self.SearchButton.setCheckable(False)
        self.SearchButton.setObjectName("SearchButton")
        self.SearchButton.clicked.connect(self.search_link_by_type)
        self.SearchFiltersButton = QtWidgets.QToolButton(self.SearchBox)
        self.SearchFiltersButton.setGeometry(QtCore.QRect(697, 20, 80, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchFiltersButton.sizePolicy().hasHeightForWidth())
        self.SearchFiltersButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.SearchFiltersButton.setFont(font)
        self.SearchFiltersButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SearchFiltersButton.setFocusPolicy(QtCore.Qt.TabFocus)
        self.SearchFiltersButton.setStyleSheet("QToolButton {\n"
"background-color: rgb(0, 200, 255);\n"
"border: 1px solid black;\n"
"border-radius: 0px;\n"
"border-top-right-radius: 7px 7px;\n"
"border-bottom-right-radius: 7px 7px;\n"
"}\n"
"QToolButton:hover {\n"
"background-color: rgb(120, 200, 255);\n"
"}")
        self.SearchFiltersButton.setArrowType(QtCore.Qt.NoArrow)
        self.SearchFiltersButton.setObjectName("SearchFiltersButton")
        self.SearchFiltersButton.clicked.connect(lambda: self.FiltersFrameVisibilityStatus())
        self.AddLinkButton = QtWidgets.QPushButton(self.SearchBox)
        self.AddLinkButton.setGeometry(QtCore.QRect(660, 20, 38, 30))
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(30)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.AddLinkButton.setFont(font)
        self.AddLinkButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddLinkButton.setStyleSheet("QPushButton {\n"
"background-color: rgb(0, 200, 255);\n"
"border: 1px solid black;\n"
"border-radius: 0px;\n"
"}\n"
"QPushButton:hover {\n"
"background-color: rgb(120, 200, 255);\n"
"}\n"
"")
        self.AddLinkButton.setObjectName("AddLinkButton")
        self.AddLinkButton.clicked.connect(self.check_link)
        icon_path4 = plg_dir + '/images/DesktopIconBlack.png'
        icon4 = QtGui.QIcon(icon_path4)
        self.AddLinkButton.setIcon(icon4)
        self.BDView = QtWidgets.QListWidget(self.CentralWidget)
        self.BDView.mousePressEvent = self.mousePressEvent
        self.BDView.setGeometry(QtCore.QRect(24, 90, 683, 530))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        self.BDView.setFont(font)
        self.BDView.setStyleSheet("QListWidget {\n"
"    background-color: whitesmoke;\n"
"    border: none;\n"
"    border-top-left-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-top-right-radius: 10px;\n"
"    border-bottom-right-radius: 10px;\n"
"    font-size: 18px;\n"
"    font-weight: 500;\n"
"    padding-left: 5px;\n"
"}")
        self.BDView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.BDView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.BDView.setObjectName("BDView")
        self.FiltersFrame = QtWidgets.QFrame(self.CentralWidget)
        self.FiltersFrame.setEnabled(True)
        self.FiltersFrame.setGeometry(QtCore.QRect(645, 60, 141, 191))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.FiltersFrame.setFont(font)
        self.FiltersFrame.setStyleSheet("QFrame {\n"
"    background-color: whitesmoke;\n"
"    padding: 0px;\n"
"    border-radius: 7px;\n"
"    border: 3px solid rgb(0, 200, 255);\n"
"    border-style: outset;\n"
"}\n"
"QCheckBox {\n"
"    background-color: whitesmoke;\n"
"}")
        self.FiltersFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.FiltersFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.FiltersFrame.setObjectName("FiltersFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.FiltersFrame)
        self.verticalLayout.setContentsMargins(6, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.CheckBoxMessengers = QtWidgets.QCheckBox(self.FiltersFrame)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.CheckBoxMessengers.setFont(font)
        self.CheckBoxMessengers.setObjectName("CheckBoxMessengers")
        self.verticalLayout.addWidget(self.CheckBoxMessengers)
        self.CheckBoxGames = QtWidgets.QCheckBox(self.FiltersFrame)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.CheckBoxGames.setFont(font)
        self.CheckBoxGames.setObjectName("CheckBoxGames")
        self.verticalLayout.addWidget(self.CheckBoxGames)
        self.CheckBoxShops = QtWidgets.QCheckBox(self.FiltersFrame)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.CheckBoxShops.setFont(font)
        self.CheckBoxShops.setObjectName("CheckBoxShops")
        self.verticalLayout.addWidget(self.CheckBoxShops)
        self.CheckBoxNews = QtWidgets.QCheckBox(self.FiltersFrame)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.CheckBoxNews.setFont(font)
        self.CheckBoxNews.setObjectName("CheckBoxNews")
        self.verticalLayout.addWidget(self.CheckBoxNews)
        self.CheckBoxVideo = QtWidgets.QCheckBox(self.FiltersFrame)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.CheckBoxVideo.setFont(font)
        self.CheckBoxVideo.setObjectName("CheckBoxVideo")
        self.verticalLayout.addWidget(self.CheckBoxVideo)
        self.CheckBoxOther = QtWidgets.QCheckBox(self.FiltersFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CheckBoxOther.sizePolicy().hasHeightForWidth())
        self.CheckBoxOther.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.CheckBoxOther.setFont(font)
        self.CheckBoxOther.setObjectName("CheckBoxOther")
        self.verticalLayout.addWidget(self.CheckBoxOther)
        self.ActionStatusLabel = QtWidgets.QLabel(self.CentralWidget)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(9)
        self.ActionStatusLabel.setFont(font)
        self.ActionStatusLabel.setStyleSheet("    background-color: whitesmoke;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    border-radius: 7px;\n"
"    border: 3px solid rgb(0, 200, 255);\n"
"    border-style: outset;")
        self.ActionStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ActionStatusLabel.setObjectName("ActionStatusLabel")
        MainWindow.setCentralWidget(self.CentralWidget)
        self.MenuBar = QtWidgets.QMenuBar(MainWindow)
        self.MenuBar.setEnabled(True)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 960, 26))
        self.MenuBar.setDefaultUp(False)
        self.MenuBar.setObjectName("MenuBar")
        MainWindow.setMenuBar(self.MenuBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LinkAnalyzer"))
        self.SearchBar.setPlaceholderText(_translate("MainWindow", "<- Поиск ссылки / Добавление ссылки ->"))
        self.SearchFiltersButton.setText(_translate("MainWindow", "Фильтры"))
        self.CheckBoxMessengers.setText(_translate("MainWindow", "Мессенджеры"))
        self.CheckBoxGames.setText(_translate("MainWindow", "Игры"))
        self.CheckBoxShops.setText(_translate("MainWindow", "Магазины"))
        self.CheckBoxNews.setText(_translate("MainWindow", "Новости"))
        self.CheckBoxVideo.setText(_translate("MainWindow", "Видеохостинг"))
        self.CheckBoxOther.setText(_translate("MainWindow", "Другое"))
        self.label.setText(_translate("MainWindow", "Загрузить ссылки"))
        self.ActionStatusLabel.setText(_translate("MainWindow", "system text"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.loadData()
    ui.ActionStatusLabel.hide()
    ui.FiltersFrame.hide()
    sys.exit(app.exec_())
