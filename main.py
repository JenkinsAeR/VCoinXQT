import sys, os

from configUI import *
from PyQt5 import QtCore, QtGui, QtWidgets

          
file_path = os.getcwd() + '\\config.js'     


config_dict= {'TOKEN': "", #сам токен доступа
            'DONEURL': '""', #ссылка на приложение
            'BOT_NAME': "#БОТ", #Имя отображаемое в консоли
            'TSUM': 0, #сумма автоперевода
            'TI': 300, #интервал автоперевода
            'TPERC': 50, #автоперевод в процентах
            'TO': 1234, #ID для автоперевода
            'AUTOBUY': 'false', #автопокупка
            'SMARTBUY': 'false',#умная покупка
            'SHOW_STATUS': 'true', #показывать количество коинов и место в топе
            'SHOW_T_IN': 'true', #показывать автопереводы от этого бота
            'SHOW_T_OUT': 'true', #показывать полученные переводы
            'SHOW_BUY': 'true' #показывать сообщения об автопокупке умной покупке
        } 

def wrapper_dictionary(func):
    def wrapper():
        return '        {\n'+ func() + '        },\n'
    return wrapper


def wrapper_generator(func):
    def wrapper():
        return '''module.exports = {
    BOTS: [\n''' + func() + '''\n    ]\n};'''
    return wrapper


@wrapper_dictionary
def create_kwargs():
    text = ''
    for key, val in config_dict.items():
        if key == "TOKEN" or key == 'BOT_NAME':
            line = str('            ' + key) + ': ' + '"' + str(val)+'",\n'
            text += line
        else:
            line = str('            ' + key) + ': ' + str(val)+',\n'
            text += line
    return text


@wrapper_generator
def reader_file():
    with open(file_path, 'r', encoding='utf-8') as file:
        whole_file = file.read()
    return whole_file


def output_file():
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(create_kwargs())





class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.counter = 0
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.pushButton.clicked.connect(self.AddAccount)
        self.ui.pushButton_2.clicked.connect(self.generator)
        self.ui.pushButton_3.clicked.connect(self.cleaner)
        

    def AddAccount(self):
        #lcd дисплей
        self.counter += 1
        self.ui.lcdNumber.display(self.counter)
        #заполнение словоря из полей
        config_dict['TOKEN'] = self.ui.lineEdit.text()
        config_dict['BOT_NAME'] = self.ui.lineEdit_2.text()
        if self.ui.lineEdit_3.text():
            config_dict['TO'] = self.ui.lineEdit_3.text()
        if not self.ui.lineEdit_3.text():
            config_dict['TO'] = 0

        if self.ui.lineEdit_4.text() and self.ui.checkBox.checkState() == 2:
            config_dict['TI'] = self.ui.lineEdit_4.text()#автоперевод в процентах
        else:config_dict['TI'] = 0

        if self.ui.lineEdit_6.text() and self.ui.checkBox_2.checkState() == 2:
            config_dict['TPERC'] = self.ui.lineEdit_6.text()#автоперевод в процентах  
        else:config_dict['TPERC'] = 0

        if self.ui.lineEdit_5.text() and self.ui.checkBox_3.checkState() == 2:
            config_dict['TSUM'] = self.ui.lineEdit_5.text() #интервал автоперевода
        else:config_dict['TSUM'] = 0
        
        if self.ui.checkBox_5.checkState() == 2:
            config_dict['AUTOBUY'] = 'true'
        else:config_dict['AUTOBUY'] = 'false'

        if self.ui.checkBox_6.checkState() == 2:
            config_dict['SHOW_T_IN'] = 'true'
        else:config_dict['SHOW_T_IN'] = 'false'

        if self.ui.checkBox_4.checkState() == 2:
            config_dict['SHOW_T_OUT'] = 'true'
        else:config_dict['SHOW_T_OUT'] = 'false'

        if self.ui.checkBox_7.checkState() == 2:
            config_dict['SHOW_STATUS'] = 'true'
        else:config_dict['SHOW_STATUS'] = 'false'
            
        #Скроллинг в конец textBrowser-а при нажатии кнопки "Добавить..."
        self.ui.verticalScrollBar.setValue(self.ui.verticalScrollBar.maximum()) 
        #Вывод информации о добавленных пользователях
        self.ui.textBrowser.append(f"<p>{config_dict['BOT_NAME']}</p>")
        self.ui.textBrowser.append(f"<b>Аккаунт №{self.counter} ДОБАВЛЕН!</b>")
        self.ui.textBrowser.append(f"-" * 20)
        output_file()
    
    def generator(self):
        '''Метод обёртывания всех блоков в общую шаблонную форму 
        необходимую для использования + принт об успешном завершении'''
        output = reader_file()
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(output)
        self.ui.textBrowser.append(f"<b>Файл сгенерирован!</b>")

    def cleaner(self):
        '''Метод очистки файла, textBrowser блока и сброса каунтера LCD'''
        self.counter = 0
        with open(file_path,'w'): pass
        self.ui.textBrowser.clear()

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())