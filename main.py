from PyQt5.QtWidgets import (QApplication, QWidget,
                             QPushButton, QTabWidget, QAbstractScrollArea,
                             QTableWidgetItem, QMessageBox,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox, QStyledItemDelegate)
import sys
import psycopg2

class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return

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

        self.updateSheduleButton = QPushButton("Update")
        self.shboxU.addWidget(self.updateSheduleButton)
        self.updateSheduleButton.clicked.connect(self.UpdateShedule)

        self.SheduleTab.setLayout(self.svbox)

        self.SubjectTab = QWidget()
        self.tabs.addTab(self.SubjectTab, "Предметы")

        self.SubGbox = QGroupBox("")

        self.svboxSub = QVBoxLayout()
        self.shboxSub = QHBoxLayout()
        self.shboxSubU = QHBoxLayout()

        self.svboxSub.addLayout(self.shboxSub)
        self.svboxSub.addLayout(self.shboxSubU)

        self.shboxSub.addWidget(self.SubGbox)

        self.CreateSubTable()

        self.updateSubButton = QPushButton("Update")
        self.shboxSubU.addWidget(self.updateSubButton)
        self.updateSubButton.clicked.connect(self.UpdateSubTable)

        self.SubjectTab.setLayout(self.svboxSub)

        self.TeacherTab = QWidget()
        self.tabs.addTab(self.TeacherTab, "Преподаватели")

        self.TeaGbox = QGroupBox("")

        self.svboxTea = QVBoxLayout()
        self.shboxTea = QHBoxLayout()
        self.shboxTeaU = QHBoxLayout()

        self.svboxTea.addLayout(self.shboxTea)
        self.svboxTea.addLayout(self.shboxTeaU)

        self.shboxTea.addWidget(self.TeaGbox)

        self.CreateTeaTable()

        self.updateTeaButton = QPushButton("Update")
        self.shboxTeaU.addWidget(self.updateTeaButton)
        self.updateTeaButton.clicked.connect(self.UpdateTea)

        self.TeacherTab.setLayout(self.svboxTea)

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
            addButton.clicked.connect(lambda ch, num=len(records): self.AddToTable(num, 'Mon'))

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
            delButton.clicked.connect(lambda ch, id=records[i][0]: self.DelFromTable(id))
            addButton.clicked.connect(lambda ch, num=len(records): self.AddToTable(num, 'Tue'))

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
            delButton.clicked.connect(lambda ch, id=records[i][0]: self.DelFromTable(id))
            addButton.clicked.connect(lambda ch, num=len(records): self.AddToTable(num, 'Wed'))

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
            delButton.clicked.connect(lambda ch, id=records[i][0]: self.DelFromTable(id))
            addButton.clicked.connect(lambda ch, num=len(records): self.AddToTable(num, 'Thu'))

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
            delButton.clicked.connect(lambda ch, id=records[i][0]: self.DelFromTable(id))
            addButton.clicked.connect(lambda ch, num=len(records): self.AddToTable(num, 'Fri'))

        self.FridayTable.resizeRowsToContents()

    def ChangeDayFromTable(self, rowNumb, day):
        row = list()

        for i in range(self.WDayColumnCount(day)):
            try:
                row.append(self.WDayChoose(day, rowNumb, i)())
            except:
                row.append(None)
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

    def AddToTable(self, rowNumb, day):
        row = list()
        wDay = {
            'Mon': 'Понедельник',
            'Tue': 'Вторник',
            'Wed': 'Среда',
            'Thu': 'Четверг',
            'Fri': 'Пятница'
        }

        for i in range(self.WDayColumnCount(day)):
            try:
                row.append(self.WDayChoose(day, rowNumb, i)())
            except:
                row.append(None)

        try:
            self.cursor.execute(f"INSERT INTO timetable(day, subject, pos, start, room) values('{wDay[day]}',"
                                f"'{str(row[0])}', '{str(row[1])}','{str(row[2])}','{str(row[3])}');")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter fields correctly.")
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

    def WDaySet(self, data, day, i, j):
        if day == 'Mon':
            return self.MondayTable.setItem(i, j, QTableWidgetItem(str(data)))
        if day == 'Tue':
            return self.TuesdayTable.setItem(i, j, QTableWidgetItem(str(data)))
        if day == 'Wed':
            return self.WednesdayTable.setItem(i, j, QTableWidgetItem(str(data)))
        if day == 'Thu':
            return self.ThursdayTable.setItem(i, j, QTableWidgetItem(str(data)))
        if day == 'Fri':
            return self.FridayTable.setItem(i, j, QTableWidgetItem(str(data)))

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

    def WDayRowCount(self, day):
        if day == 'Mon':
            return self.MondayTable.rowCount()
        if day == 'Tue':
            return self.TuesdayTable.rowCount()
        if day == 'Wed':
            return self.WednesdayTable.rowCount()
        if day == 'Thu':
            return self.ThursdayTable.rowCount()
        if day == 'Fri':
            return self.FridayTable.rowCount()

    def ClearLastRow(self):
        try:
            self.MondayTable.removeRow(self.WDayRowCount('Mon')-1)
            self.TuesdayTable.removeRow(self.WDayRowCount('Tue') - 1)
            self.WednesdayTable.removeRow(self.WDayRowCount('Wed') - 1)
            self.ThursdayTable.removeRow(self.WDayRowCount('Thu') - 1)
            self.FridayTable.removeRow(self.WDayRowCount('Fri') - 1)
        except:
            QMessageBox.about(self, "Error", "Enter fields correctly.")

    def UpdateShedule(self):
        self.ClearLastRow()
        self.UpdateMondayTable()
        self.UpdateTuesdayTable()
        self.UpdateWednesdayTable()
        self.UpdateThursdayTable()
        self.UpdateFridayTable()

    def CreateSubTable(self):
        self.SubTable = QTableWidget()

        self.SubTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.SubTable.setColumnCount(4)
        self.SubTable.setHorizontalHeaderLabels(["Предмет", "", "", ""])
        self.SubTable.setColumnHidden(3, True)

        self.UpdateSubTable()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.SubTable)
        self.SubGbox.setLayout(self.mvbox)

    def UpdateSubTable(self):
        self.cursor.execute("SELECT * FROM subject ORDER BY name;")
        records = list(self.cursor.fetchall())

        self.SubTable.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            self.SubTable.setItem(i, 3, QTableWidgetItem(str(r[0])))
            self.SubTable.setItem(i, 0, QTableWidgetItem(str(r[1])))
            joinButton = QPushButton("Изменить")
            delButton = QPushButton("Удалить")
            addButton = QPushButton("Добавить")
            self.SubTable.setCellWidget(i, 1, joinButton)
            self.SubTable.setCellWidget(i, 2, delButton)
            self.SubTable.setCellWidget(len(records), 1, addButton)
            joinButton.clicked.connect(lambda ch, num=i: self.ChangeSubFromTable(num))
            delButton.clicked.connect(lambda ch, id=records[i][0]: self.DelSubFromTable(id))
            addButton.clicked.connect(lambda ch, num=len(records): self.AddSubToTable(num))

        self.SubTable.resizeRowsToContents()

    def ChangeSubFromTable(self, rowNumb):
        row = list()

        for i in range(self.SubTable.columnCount()):
            try:
                row.append(str(self.SubTable.item(rowNumb, i).text()))
            except:
                row.append(None)
        try:
            self.cursor.execute(f"UPDATE subject SET name='{str(row[0])}' WHERE id='{str(row[4])}';")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields.")
        else:
            self.UpdateShedule()

    def DelSubFromTable(self, id):
        try:
            self.cursor.execute(f"DELETE from subject WHERE id='{id}';")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Error")
        else:
            self.UpdateSub()

    def AddSubToTable(self, rowNumb):
        row = list()
        print(self.SubTable.item(rowNumb, 0).text())
        for i in range(self.SubTable.columnCount()):
            try:
                row.append(self.SubTable.item(rowNumb, i).text())
            except:
                row.append(None)

        try:
            self.cursor.execute(f"INSERT INTO subject(name, teacher) values('{str(row[0])}','unknown');")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter fields correctly.")
        else:
            self.UpdateSub()

    def ClearSubLastRow(self):
        try:
            self.SubTable.removeRow(self.SubTable.columnCount()-1)
        except:
            QMessageBox.about(self, "Error", "Enter fields correctly.")

    def UpdateSub(self):
        self.ClearSubLastRow()
        self.UpdateSubTable()

    def CreateTeaTable(self):
        self.TeaTable = QTableWidget()

        self.TeaTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.TeaTable.setColumnCount(4)
        self.TeaTable.setHorizontalHeaderLabels(["Предмет", "Преподователь", "", "", ""])
        self.TeaTable.setColumnHidden(3, True)
        delegate = ReadOnlyDelegate(self)
        self.TeaTable.setItemDelegateForColumn(0, delegate)

        self.UpdateTeaTable()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.TeaTable)
        self.TeaGbox.setLayout(self.mvbox)

    def UpdateTeaTable(self):
        self.cursor.execute("SELECT * FROM subject ORDER BY name;")
        records = list(self.cursor.fetchall())

        self.TeaTable.setRowCount(len(records))

        for i, r in enumerate(records):
            r = list(r)
            self.TeaTable.setItem(i, 4, QTableWidgetItem(str(r[0])))
            self.TeaTable.setItem(i, 0, QTableWidgetItem(str(r[1])))
            self.TeaTable.setItem(i, 1, QTableWidgetItem(str(r[2])))
            joinButton = QPushButton("Изменить")
            self.TeaTable.setCellWidget(i, 2, joinButton)
            joinButton.clicked.connect(lambda ch, num=i: self.ChangeTeaFromTable(num))
        self.TeaTable.resizeRowsToContents()

    def ChangeTeaFromTable(self, rowNumb):
        row = list()

        for i in range(self.TeaTable.columnCount()):
            try:
                row.append(str(self.TeaTable.item(rowNumb, i).text()))
            except:
                row.append(None)
        try:
            self.cursor.execute(f"UPDATE subject SET teacher='{str(row[1])}' WHERE id='{str(row[5])}';")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields.")
        else:
            self.UpdateTea()

    def DelTeaFromTable(self, id):
        try:
            self.cursor.execute(f"DELETE from subject WHERE id='{id}';")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Error")
        else:
            self.UpdateTea()

    def AddTeaToTable(self, rowNumb):
        row = list()
        print(self.TeaTable.item(rowNumb, 0).text())
        for i in range(self.TeaTable.columnCount()):
            try:
                row.append(self.TeaTable.item(rowNumb, i).text())
            except:
                row.append(None)

        try:
            self.cursor.execute(f"INSERT INTO subject(teacher) values('{str(row[1])}');")
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter fields correctly.")
        else:
            self.UpdateTea()

    def ClearTeaLastRow(self):
        try:
            self.TeaTable.removeRow(self.TeaTable.columnCount()-1)
        except:
            QMessageBox.about(self, "Error", "Enter fields correctly.")

    def UpdateTea(self):
        self.ClearTeaLastRow()
        self.UpdateTeaTable()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
