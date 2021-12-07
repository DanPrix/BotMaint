from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLineEdit, QLabel,
                             QPushButton, QHBoxLayout,
                             QTabWidget, QAbstractScrollArea,
                             QTableWidgetItem, QMessageBox,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox)
import sys
import psycopg2


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Shedule")

        self.ConnectToDb()

        self.tabs = QTabWidget()

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.tabs)

        self.CreateSheduleTabs()

    def ConnectToDb(self):
        self.conn = psycopg2.connect(database="raspisanie",
                                user="postgres",
                                password="4ds97n1JfdlnLDAlz",
                                host="localhost",
                                port="5432")
        self.cursor = self.conn.cursor()

    def CreateSheduleTabs(self):
        self.SheduleTab = QWidget()
        self.tabs.addTab(self.SheduleTab, "Расписание")

        self.MondayGbox = QGroupBox("Понедельник")
        self.TuesdayGbox = QGroupBox("Вторник")
        self.WednesdayGbox = QGroupBox("Среда")
        self.ThursdayGbox = QGroupBox("Четверг")
        self.FridayGbox = QGroupBox("Пятница")

        self.svbox = QVBoxLayout()
        self.shboxMon = QHBoxLayout()
        self.shboxTue = QHBoxLayout()
        self.shboxWed = QHBoxLayout()
        self.shboxThu = QHBoxLayout()
        self.shboxFri = QHBoxLayout()
        self.shboxU = QHBoxLayout()

        self.svbox.addLayout(self.shboxMon)
        self.svbox.addLayout(self.shboxTue)
        self.svbox.addLayout(self.shboxWed)
        self.svbox.addLayout(self.shboxThu)
        self.svbox.addLayout(self.shboxFri)
        self.svbox.addLayout(self.shboxU)


        self.shboxMon.addWidget(self.MondayGbox)
        self.shboxTue.addWidget(self.TuesdayGbox)
        self.shboxWed.addWidget(self.WednesdayGbox)
        self.shboxThu.addWidget(self.ThursdayGbox)
        self.shboxFri.addWidget(self.FridayGbox)

        self.CreateMondayTable()
        self.CreateTuesdayTable()
        self.CreateWednesdayTable()
        self.CreateThursdayTable()
        self.CreateFridayTable()

        self.UpdateSheduleButton = QPushButton("Update")
        self.shboxU.addWidget(self.UpdateSheduleButton)
        self.UpdateSheduleButton.clicked.connect(self.UpdateShedule)

        self.SheduleTab.setLayout(self.svbox)

    def CreateMondayTable(self):
        self.MondayTable = QTableWidget()

        self.MondayTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.MondayTable.setColumnCount(7)
        self.MondayTable.setHorizontalHeaderLabels(["Предмет", "Неделя", "Время", "Кабинет", "", "", ""])
        self.MondayTable.setColumnHidden(6, True)

        self.UpdateMondayTable()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.MondayTable)
        self.MondayGbox.setLayout(self.mvbox)

    def UpdateMondayTable(self):
        self.cursor.execute("SELECT * FROM timetable WHERE day='Понедельник' ORDER BY start;")
        records = list(self.cursor.fetchall())

        self.MondayTable.setRowCount(len(records)+1)

        for i, r in enumerate(records):
            r = list(r)
            self.MondayTable.setItem(i, 6, QTableWidgetItem(str(r[0])))
            self.MondayTable.setItem(i, 0, QTableWidgetItem(str(r[3])))
            self.MondayTable.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.MondayTable.setItem(i, 2, QTableWidgetItem(str(r[5])))
            self.MondayTable.setItem(i, 3, QTableWidgetItem(str(r[4])))
            joinButton = QPushButton("Изменить")
            delButton = QPushButton("Удалить")
            addButton = QPushButton("Добавить")
            self.MondayTable.setCellWidget(i, 4, joinButton)
            self.MondayTable.setCellWidget(i, 5, delButton)
            self.MondayTable.setCellWidget(len(records), 4, addButton)
            joinButton.clicked.connect(lambda ch, num=i: self.ChangeDayFromTable(num, 'Mon'))
            delButton.clicked.connect(lambda ch, id=records[i][0]: self.DelFromTable(id))
            addButton.clicked.connect(lambda ch, num=i: self.AddToTable(num, 'Mon'))

        self.MondayTable.resizeRowsToContents()

    def CreateTuesdayTable(self):
        self.TuesdayTable = QTableWidget()

        self.TuesdayTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.TuesdayTable.setColumnCount(7)
        self.TuesdayTable.setHorizontalHeaderLabels(["Предмет", "Неделя", "Время", "Кабинет", "", "", ""])
        self.TuesdayTable.setColumnHidden(6, True)

        self.UpdateTuesdayTable()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.TuesdayTable)
        self.TuesdayGbox.setLayout(self.mvbox)

    def UpdateTuesdayTable(self):
        self.cursor.execute("SELECT * FROM timetable WHERE day='Вторник' ORDER BY start;")
        records = list(self.cursor.fetchall())

        self.TuesdayTable.setRowCount(len(records)+1)

        for i, r in enumerate(records):
            r = list(r)
            self.TuesdayTable.setItem(i, 6, QTableWidgetItem(str(r[0])))
            self.TuesdayTable.setItem(i, 0, QTableWidgetItem(str(r[3])))
            self.TuesdayTable.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.TuesdayTable.setItem(i, 2, QTableWidgetItem(str(r[5])))
            self.TuesdayTable.setItem(i, 3, QTableWidgetItem(str(r[4])))
            joinButton = QPushButton("Изменить")
            delButton = QPushButton("Удалить")
            addButton = QPushButton("Добавить")
            self.TuesdayTable.setCellWidget(i, 4, joinButton)
            self.TuesdayTable.setCellWidget(i, 5, delButton)
            self.TuesdayTable.setCellWidget(len(records), 4, addButton)
            joinButton.clicked.connect(lambda ch, num=i: self.ChangeDayFromTable(num, 'Tue'))

        self.TuesdayTable.resizeRowsToContents()

    def CreateWednesdayTable(self):
        self.WednesdayTable = QTableWidget()

        self.WednesdayTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.WednesdayTable.setColumnCount(7)
        self.WednesdayTable.setHorizontalHeaderLabels(["Предмет", "Неделя", "Время", "Кабинет", "", "", ""])
        self.WednesdayTable.setColumnHidden(6, True)

        self.UpdateWednesdayTable()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.WednesdayTable)
        self.WednesdayGbox.setLayout(self.mvbox)

    def UpdateWednesdayTable(self):
        self.cursor.execute("SELECT * FROM timetable WHERE day='Среда' ORDER BY start;")
        records = list(self.cursor.fetchall())

        self.WednesdayTable.setRowCount(len(records)+1)

        for i, r in enumerate(records):
            r = list(r)
            self.WednesdayTable.setItem(i, 6, QTableWidgetItem(str(r[0])))
            self.WednesdayTable.setItem(i, 0, QTableWidgetItem(str(r[3])))
            self.WednesdayTable.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.WednesdayTable.setItem(i, 2, QTableWidgetItem(str(r[5])))
            self.WednesdayTable.setItem(i, 3, QTableWidgetItem(str(r[4])))
            joinButton = QPushButton("Изменить")
            delButton = QPushButton("Удалить")
            addButton = QPushButton("Добавить")
            self.WednesdayTable.setCellWidget(i, 4, joinButton)
            self.WednesdayTable.setCellWidget(i, 5, delButton)
            self.WednesdayTable.setCellWidget(len(records), 4, addButton)
            joinButton.clicked.connect(lambda ch, num=i: self.ChangeDayFromTable(num, 'Wed'))

        self.WednesdayTable.resizeRowsToContents()

    def CreateThursdayTable(self):
        self.ThursdayTable = QTableWidget()

        self.ThursdayTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.ThursdayTable.setColumnCount(7)
        self.ThursdayTable.setHorizontalHeaderLabels(["Предмет", "Неделя", "Время", "Кабинет", "", "", ""])
        self.ThursdayTable.setColumnHidden(6, True)

        self.UpdateThursdayTable()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.ThursdayTable)
        self.ThursdayGbox.setLayout(self.mvbox)

    def UpdateThursdayTable(self):
        self.cursor.execute("SELECT * FROM timetable WHERE day='Четверг' ORDER BY start;")
        records = list(self.cursor.fetchall())

        self.ThursdayTable.setRowCount(len(records)+1)

        for i, r in enumerate(records):
            r = list(r)
            self.ThursdayTable.setItem(i, 6, QTableWidgetItem(str(r[0])))
            self.ThursdayTable.setItem(i, 0, QTableWidgetItem(str(r[3])))
            self.ThursdayTable.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.ThursdayTable.setItem(i, 2, QTableWidgetItem(str(r[5])))
            self.ThursdayTable.setItem(i, 3, QTableWidgetItem(str(r[4])))
            joinButton  = QPushButton("Изменить")
            delButton = QPushButton("Удалить")
            addButton = QPushButton("Добавить")
            self.ThursdayTable.setCellWidget(i, 4, joinButton)
            self.ThursdayTable.setCellWidget(i, 5, delButton)
            self.ThursdayTable.setCellWidget(len(records), 4, addButton)
            joinButton.clicked.connect(lambda ch, num=i: self.ChangeDayFromTable(num, 'Thu'))

        self.ThursdayTable.resizeRowsToContents()

    def CreateFridayTable(self):
        self.FridayTable = QTableWidget()

        self.FridayTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.FridayTable.setColumnCount(7)
        self.FridayTable.setHorizontalHeaderLabels(["Предмет", "Неделя", "Время", "Кабинет", "", "", ""])
        self.FridayTable.setColumnHidden(6, True)

        self.UpdateFridayTable()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.FridayTable)
        self.FridayGbox.setLayout(self.mvbox)

    def UpdateFridayTable(self):
        self.cursor.execute("SELECT * FROM timetable WHERE day='Пятница' ORDER BY start;")
        records = list(self.cursor.fetchall())

        self.FridayTable.setRowCount(len(records)+1)

        for i, r in enumerate(records):
            r = list(r)
            self.FridayTable.setItem(i, 6, QTableWidgetItem(str(r[0])))
            self.FridayTable.setItem(i, 0, QTableWidgetItem(str(r[3])))
            self.FridayTable.setItem(i, 1, QTableWidgetItem(str(r[2])))
            self.FridayTable.setItem(i, 2, QTableWidgetItem(str(r[5])))
            self.FridayTable.setItem(i, 3, QTableWidgetItem(str(r[4])))
            joinButton  = QPushButton("Изменить")
            delButton = QPushButton("Удалить")
            addButton = QPushButton("Добавить")
            self.FridayTable.setCellWidget(i, 4, joinButton)
            self.FridayTable.setCellWidget(i, 5, delButton)
            self.FridayTable.setCellWidget(len(records), 4, addButton)
            joinButton.clicked.connect(lambda ch, num=i: self.ChangeDayFromTable(num, 'Fri'))

        self.FridayTable.resizeRowsToContents()

    def ChangeDayFromTable(self, rowNumb, day):
        row = list()

        print(self.WDayChoose(day, self.MondayTable.rowCount(),1))
        for i in range(self.WDayColumnCount(day)):
            try:
                row.append(self.WDayChoose(day, rowNumb, i)())
            except:
                row.append(None)
        print(self.WDayColumnCount(day))
        try:
            self.cursor.execute(f"UPDATE timetable SET subject='{str(row[0])}', pos='{str(row[1])}', "
                                f"start='{str(row[2])}', room='{str(row[3])}' WHERE id='{str(row[6])}';")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields.")
        else:
            self.UpdateShedule()

    def DelFromTable(self, id):
        try:
            self.cursor.execute(f"DELETE from timetable WHERE id='{id}';")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Error")
        else:
            self.UpdateShedule()

    def AddToTable(self, num, day):
        wDay = {
            'Mon': 'Понедельник',
            'Tue': 'Вторник',
            'Wed': 'Среда',
            'Thu': 'Четверг',
            'Fri': 'Пятница'
        }
        try:
            self.cursor.execute(f"INSERT INTO timetable(day, subject, pos, start, room) values('{wDay[day]}',"
                                f"'{self.WDayChoose(day, num, 0)}', '{self.WDayChoose(day, num, 1)}',"
                                f"'{self.WDayChoose(day, num, 2)}','{self.WDayChoose(day, num, 3)}',"
                                f"'{self.WDayChoose(day, num, 4)}');")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Error")
        else:
            self.UpdateShedule()

    def WDayChoose(self, day, i, j):
        if day == 'Mon':
            return self.MondayTable.item(i, j).text
        if day == 'Tue':
            return self.TuesdayTable.item(i, j).text
        if day == 'Wed':
            return self.WednesdayTable.item(i, j).text
        if day == 'Thu':
            return self.ThursdayTable.item(i, j).text
        if day == 'Fri':
            return self.FridayTable.item(i, j).text

    def WDayColumnCount(self, day):
        if day == 'Mon':
            return self.MondayTable.columnCount()
        if day == 'Tue':
            return self.TuesdayTable.columnCount()
        if day == 'Wed':
            return self.WednesdayTable.columnCount()
        if day == 'Thu':
            return self.ThursdayTable.columnCount()
        if day == 'Fri':
            return self.FridayTable.columnCount()

    def UpdateShedule(self):
        self.UpdateMondayTable()
        self.UpdateTuesdayTable()
        self.UpdateWednesdayTable()
        self.UpdateThursdayTable()
        self.UpdateFridayTable()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
