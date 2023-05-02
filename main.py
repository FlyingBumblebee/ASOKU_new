from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QWidget, QVBoxLayout, QLabel, \
    QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QComboBox, QSizePolicy, QFormLayout, QDateTimeEdit, QToolBar
import sys
import  mysql.connector
from PySide6.QtCore import Qt, QDateTime




class AuthenticationWindow(QWidget):
    def __init__(self):
        super(AuthenticationWindow, self).__init__()

        self.setWindowTitle("АСОКУ")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.authenticate)

        self.setLayout(layout)
    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Connect to MySQL database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="06032003",
                database="ASU"
            )
            cursor = conn.cursor()

            # Perform authentication query
            query = "SELECT * FROM users WHERE Login = %s AND Password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                # Check if the user is an admin
                if result[6] == 'True': # Assuming the role is stored in the third column of the 'users' table
                    self.close()
                    app.admin_window.show()
                else:
                    self.close()
                    app.non_admin_window.show()
            else:
                QMessageBox.warning(self, "Authentication Failed", "Invalid username or password")

            cursor.close()
            conn.close()

        except mysql.connector.Error as e:
            print("Error connecting to MySQL database:", e)

class TableWidget(QTableWidget):
    def __init__(self):
        super(TableWidget, self).__init__()

        # Set table properties
        self.setColumnCount(10)  # Number of columns in the table
        self.setHorizontalHeaderLabels([ "Назва", "Область", "Відповідальний орган", "Статус", "Дата відновлення", "Тип інфраструктури","Тип ураження","Рівень ураження","Кількість постраждалих","Дата ураження"])

        self.resizeColumnsToContents()
        self.resizeRowsToContents()
    def display_data(self, data):
        # Clear existing data from the table
        self.clearContents()
        self.setRowCount(0)

        # Populate the table with data
        for row in data:
            row_position = self.rowCount()
            self.insertRow(row_position)
            for col, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.setItem(row_position, col, item)

        # Resize the columns to fit the contents
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Graph Window")
        self.setGeometry(100, 100, 800, 600)



class WorkingWindow(QMainWindow):
    def __init__(self, window_type):
        super(WorkingWindow, self).__init__()


        self.setWindowTitle("АСОКУ")

        if window_type == 'admin':
            self.setFixedSize(1300, 600)
            self.welcome_label = QLabel("Welcome Admin!")
        else:
            self.setFixedSize(1300, 600)
            self.welcome_label = QLabel("Welcome!")

        self.welcome_label.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)



        left_layout = QVBoxLayout()

        side_layout = QVBoxLayout()
        self.graph_button = QPushButton("Графіки")
        self.graph_button.clicked.connect(self.open_graph_window)
        side_layout.addWidget(self.graph_button)
        layout.addLayout(side_layout)
        form_layout = QFormLayout()
        #Створення віджитів для фільтрації
        self.select_name_label = QLabel("Назва інфраструктури:")
        self.select_name_edit = QLineEdit()

        self.select_oblast_label = QLabel("Область:")
        self.select_oblast_dropdown = QComboBox()
        self.select_oblast_dropdown.addItems([" ","АР Крим","Вінницька","Волинська","Дніпропетровська","Донецька","Житомирська","Закарпатська","Запорізька","Івано-Франківська","Ки\u0457вська","Кіровоградська","Луганська","Львівська","Микола\u0457вська","Одеська","Полтавська","Рівненська","\u0425\u0430\u0440\u043a\u0456\u0432\u0441\u044c\u043a\u0430","Херсонська","Хмельницька","Черкаська","Чернівецька","Чернігівська","Не визначено"])

        self.select_organ_label = QLabel("Відповідальний орган:")
        self.select_organ_dropdown = QComboBox()
        self.select_organ_dropdown.addItems([" ", "МВС", "МО","МНС","ДСНС","МЕЗД"])

        self.select_status_label = QLabel("Статус:")
        self.select_status_dropdown = QComboBox()
        self.select_status_dropdown.addItems([" ", "Ведуться роботи", "Відновлення", "Завершено", "Відкладено"])

        self.select_type_label = QLabel("Тип інфраструктури:")
        self.select_type_dropdown = QComboBox()
        self.select_type_dropdown.addItems([" ", "Енергетика", "Газопровідна інфраструктура"])

        self.select_damage_type_label = QLabel("Тип ураження:")
        self.select_damage_type_dropdown = QComboBox()
        self.select_damage_type_dropdown.addItems([" ", "Природні катаклізми", "Техногенні катастрофи","Кібератаки","Терористичні акти","Військові конфлікти"])

        self.select_damage_level_label = QLabel("Рівень ураження:")
        self.select_damage_level_dropdown = QComboBox()
        self.select_damage_level_dropdown.addItems([" ", "1", "2", "3"])

        self.select_casualties_label = QLabel("Кількість постраждалих:")
        self.select_casualties_edit = QLineEdit()

        self.select_time1_label1 = QLabel("Дата та час ураження від:")
        self.select_time1_val1 = QDateTimeEdit()
        default_time = QDateTime(2023, 1,1,0,0,0)
        self.select_time1_val1.setDateTime(default_time)
        self.select_time1_label2 = QLabel("до:")
        self.select_time1_val2 = QDateTimeEdit()
        self.select_time1_val2.setDateTime(default_time)

        self.apply_button = QPushButton("Пошук")
        self.apply_button.clicked.connect(self.load_data)

        self.remove_button = QPushButton("Скинути фільтр")
        self.remove_button.clicked.connect(self.reset_data)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.remove_button)

        form_layout.addRow(self.select_name_label, self.select_name_edit)
        form_layout.addRow(self.select_oblast_label, self.select_oblast_dropdown)
        form_layout.addRow(self.select_organ_label, self.select_organ_dropdown)
        form_layout.addRow(self.select_status_label, self.select_status_dropdown)
        form_layout.addRow(self.select_type_label, self.select_type_dropdown)
        form_layout.addRow(self.select_damage_type_label, self.select_damage_type_dropdown)
        form_layout.addRow(self.select_damage_level_label, self.select_damage_level_dropdown)
        form_layout.addRow(self.select_casualties_label, self.select_casualties_edit)
        form_layout.addRow(self.select_time1_label1, self.select_time1_val1)
        form_layout.addRow(self.select_time1_label2,self.select_time1_val2)
        form_layout.addRow("",button_layout)
        left_layout.addLayout(form_layout)


        left_layout.addStretch()

        layout.addLayout(left_layout)

        self.table_widget = TableWidget()
        layout.addWidget(self.table_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.select_name_edit.setFixedWidth(200)
        self.select_oblast_dropdown.setFixedWidth(200)
        self.select_organ_dropdown.setFixedWidth(200)
        self.select_status_dropdown.setFixedWidth(200)
        self.select_type_dropdown.setFixedWidth(200)
        self.select_damage_type_dropdown.setFixedWidth(200)
        self.select_damage_level_dropdown.setFixedWidth(200)
        self.select_casualties_edit.setFixedWidth(200)
        self.select_time1_val1.setFixedWidth(200)
        self.select_time1_val2.setFixedWidth(200)
        self.apply_button.setFixedWidth(98)
        self.remove_button.setFixedWidth(98)

        self.select_name_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.select_oblast_dropdown.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.select_organ_dropdown.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.select_status_dropdown.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.select_type_dropdown.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.select_damage_type_dropdown.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.select_damage_level_dropdown.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.select_casualties_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.select_time1_val1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.select_time1_val2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.apply_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.remove_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.select_name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.select_oblast_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.select_organ_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.select_status_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.select_type_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.select_damage_type_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.select_damage_level_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.select_casualties_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.select_time1_label1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.select_time1_label2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


        self.select_name_label.setFixedWidth(200)
        self.select_oblast_label.setFixedWidth(200)
        self.select_organ_label.setFixedWidth(200)
        self.select_status_label.setFixedWidth(200)
        self.select_type_label.setFixedWidth(200)
        self.select_damage_type_label.setFixedWidth(200)
        self.select_damage_level_label.setFixedWidth(200)
        self.select_casualties_label.setFixedWidth(200)
        self.select_time1_label1.setFixedWidth(200)
        self.select_time1_label2.setFixedWidth(200)

        self.select_name_edit.setGeometry(100, 100, 200, 30)
        self.select_oblast_dropdown.setGeometry(100, 100, 200, 30)
        self.select_organ_dropdown.setGeometry(100, 100, 200, 30)
        self.select_status_dropdown.setGeometry(100, 100, 200, 30)
        self.select_type_dropdown.setGeometry(100, 100, 200, 30)
        self.select_damage_type_dropdown.setGeometry(100, 100, 200, 30)
        self.select_damage_level_dropdown.setGeometry(100, 100, 200, 30)
        self.select_casualties_edit.setGeometry(100, 100, 200, 30)
        self.select_time1_val1.setGeometry(100, 100, 200, 30)
        self.select_time1_val2.setGeometry(100, 100, 200, 30)
        self.apply_button.setGeometry(100, 100, 100, 30)
        self.remove_button.setGeometry(100,100,100,30)
        self.load_data()

    def open_graph_window(self):
        self.graph_window = GraphWindow()
        self.graph_window.show()
        self.close()
    def reset_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="06032003",
                database="ASU"
            )
            cursor = conn.cursor()

            # Clear line edits and dropdowns
            self.select_name_edit.setText("")
            self.select_oblast_dropdown.setCurrentIndex(0)
            self.select_organ_dropdown.setCurrentIndex(0)
            self.select_status_dropdown.setCurrentIndex(0)
            self.select_type_dropdown.setCurrentIndex(0)
            self.select_damage_type_dropdown.setCurrentIndex(0)
            self.select_casualties_edit.setText("")
            self.select_damage_level_dropdown.setCurrentIndex(0)
            # Reset datetime
            default_time = QDateTime(2023, 1, 1, 0, 0, 0)
            self.select_time1_val1.setDateTime(default_time)
            self.select_time1_val2.setDateTime(default_time)

            damage_time1 = '1000-01-01 00:00:00'
            damage_time2 = '9999-12-31 23:59:59'
            query = f"""
                           SELECT infrastructure.Name, infrastructure.Oblast, infrastructure.Organ, 
                                   infrastructure.Status, infrastructure.AproxRecover, infrastructure.Type,
                                   damage.Type, damage.DamageLevel, damage.NumCasualties, damage.Date
                           FROM infrastructure
                           JOIN damage ON infrastructure.Damage_ID = damage.DamageID
                           WHERE infrastructure.Type LIKE '%' AND damage.DamageLevel LIKE '%' AND infrastructure.Name LIKE '%' AND infrastructure.Oblast LIKE '%' AND infrastructure.Organ LIKE '%' AND infrastructure.Status LIKE '%' AND damage.Type LIKE '%' AND damage.NumCasualties LIKE '%' AND damage.Date BETWEEN STR_TO_DATE('{damage_time1}','%Y-%m-%d %H:%i:%s') AND STR_TO_DATE('{damage_time2}','%Y-%m-%d %H:%i:%s')
                           """

            cursor.execute(query)
            result = cursor.fetchall()

            self.table_widget.display_data(result)

            # Resize columns to fit the contents
            self.table_widget.resizeColumnsToContents()
            cursor.close()
            conn.close()

        except Exception as e:
            print(e)
    def load_data(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="06032003",
                database="ASU"
            )
            cursor = conn.cursor()

            # Get the selected value from the dropdown list
            selected_name = self.select_name_edit.text()
            selected_oblast = self.select_oblast_dropdown.currentText()
            selected_organ = self.select_organ_dropdown.currentText()
            selected_status = self.select_status_dropdown.currentText()
            selected_type = self.select_type_dropdown.currentText()
            selected_damage_type = self.select_damage_type_dropdown.currentText()
            damage_level = self.select_damage_level_dropdown.currentText()
            selected_casualties = self.select_casualties_edit.text()

            damage_time1 = self.select_time1_val1.dateTime()
            damage_time2 = self.select_time1_val2.dateTime()

            # Use the selected value in the MySQL query
            if selected_type == " ":
                selected_type = "%"
            if damage_level == " ":
                damage_level = "%"
            if selected_name == "":
                selected_name = "%"
            if selected_oblast == " ":
                selected_oblast = "%"
            if selected_organ == " ":
                selected_organ = "%"
            if selected_status == " ":
                selected_status = "%"
            if selected_damage_type == " ":
                selected_damage_type = "%"
            if selected_casualties == "":
                selected_casualties = "%"
            default_time = QDateTime(2023, 1, 1, 0, 0, 0)
            damage_time12 = damage_time1.toString("yyyy-MM-dd HH:mm:ss")
            damage_time22 = damage_time2.toString("yyyy-MM-dd HH:mm:ss")
            default_time = default_time.toString("yyyy-MM-dd HH:mm:ss")
            if damage_time12 == default_time:
                damage_time1 = '1000-01-01 00:00:00'
            else:
                damage_time1 = damage_time1.toString("yyyy-MM-dd HH:mm:ss")
            if damage_time22 == default_time:
                damage_time2 = '9999-12-31 23:59:59'
            else:
                damage_time2 = damage_time2.toString("yyyy-MM-dd HH:mm:ss")

            query = f"""
                SELECT infrastructure.Name, infrastructure.Oblast, infrastructure.Organ, 
                        infrastructure.Status, infrastructure.AproxRecover, infrastructure.Type,
                        damage.Type, damage.DamageLevel, damage.NumCasualties, damage.Date
                FROM infrastructure
                JOIN damage ON infrastructure.Damage_ID = damage.DamageID
                WHERE infrastructure.Type LIKE '{selected_type}' AND damage.DamageLevel LIKE '{damage_level}' AND infrastructure.Name LIKE '%{selected_name}%' AND infrastructure.Oblast LIKE '{selected_oblast}' AND infrastructure.Organ LIKE '{selected_organ}' AND infrastructure.Status LIKE '{selected_status}' AND damage.Type LIKE '{selected_damage_type}' AND damage.NumCasualties LIKE '{selected_casualties}' AND damage.Date BETWEEN STR_TO_DATE('{damage_time1}','%Y-%m-%d %H:%i:%s') AND STR_TO_DATE('{damage_time2}','%Y-%m-%d %H:%i:%s')
                """

            cursor.execute(query)
            result = cursor.fetchall()

            self.table_widget.display_data(result)

            # Resize columns to fit the contents
            self.table_widget.resizeColumnsToContents()

            cursor.close()
            conn.close()

        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    auth_window = AuthenticationWindow()
    app.admin_window = WorkingWindow('admin')
    app.non_admin_window = WorkingWindow('non-admin')

    auth_window.show()

    sys.exit(app.exec())