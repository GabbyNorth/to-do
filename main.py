import os
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton, QMessageBox

class window(QWidget):
    def __init__(self, parent = None):
        super(window, self).__init__(parent)

        if os.stat('tasks.txt').st_size != 0:
            file = open('tasks.txt', 'r')
            contents = file.read()
            self.tasks = contents.split(', ')
            file.close()
            while ('' in self.tasks):
                self.tasks.remove('')
        else:
            self.tasks = []

        self.setWindowTitle('To-Do List')
        layout = QVBoxLayout(self)

        # widgets
        self.app_title = QLabel(self)
        self.app_title.setText('TO-DO App')
        self.app_title.setFont(QFont('Arial', 25))
        layout.addWidget(self.app_title)

        # label
        self.label = QLabel()
        self.label.setText('Organize your world.')
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(16)
        self.label.setFont(font)
        layout.addWidget(self.label)

        # list
        self.list = QListWidget(self)
        layout.addWidget(self.list)
        if (self.tasks):
            for i in self.tasks:
                if (i != ''):
                    self.list.addItem(i)

        # Task entry
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText('Enter your task here')
        self.task_input.returnPressed.connect(self.add)
        layout.addWidget(self.task_input)

        # buttons
        self.add_button = QPushButton('Add Task')
        self.add_button.clicked.connect(self.add)
        layout.addWidget(self.add_button)

        self.delete_button = QPushButton('Delete Task')
        self.delete_button.clicked.connect(self.delete)
        layout.addWidget(self.delete_button)

        self.undo_button = QPushButton('Undo')
        self.undo_button.clicked.connect(self.undo)
        layout.addWidget(self.undo_button)

        self.advanced_button = QPushButton('Advanced Options')
        self.advanced_button.setCheckable(True)
        self.advanced_button.clicked.connect(self.advanced)
        layout.addWidget(self.advanced_button)

    def add(self):
        string = self.task_input.text()
        self.tasks.append(string)
        self.list.addItem(string)
        self.update_data()
        self.task_input.clear()

    def delete(self):
        delete_warning = QMessageBox(self)
        delete_warning.setWindowTitle('You are deleting a task.')
        delete_warning.setText('You are deleting a task. Are you sure you would like to proceed?')
        delete_warning.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        delete_warning.setIcon(QMessageBox.Question)
        button = delete_warning.exec()

        if button == QMessageBox.Yes:
            row = self.list.currentRow()
            self.tasks.remove(self.list.currentItem().text())
            self.update_data()
            self.list.takeItem(row)
        else:
            pass

    def undo(self):
        print('undo clicked')

    def advanced(self):
        print('advanced options clicked')

    def update_data (self):
        with open('tasks.txt', 'w') as txt_file:
            for item in self.tasks:
                txt_file.write(item + ', ')

    def welcome_message(self):
        welcome_msg = QMessageBox()
        welcome_msg.setIcon(QMessageBox.Information)
        welcome_text = 'Increase your productivity by organizing your tasks with the TODO App!\n\n' \
                       'You can add your tasks to your to-do list by typing them into ' \
                       'the textbox and clicking \"Add Task\"'
        welcome_msg.setText(welcome_text)
        welcome_msg.setStandardButtons(QMessageBox.Ok)
        welcome_msg.exec()

def main():
   app = QApplication([])
   win = window()
   win.welcome_message()
   win.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
