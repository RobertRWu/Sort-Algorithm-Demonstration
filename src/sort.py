# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QListView,QMessageBox
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QApplication
import PyQt5.uic
from PyQt5 import QtCore
import numpy as np
import math
import random
import operator
import copy


DATA_NUM_MAX = 20
BLOCK_HEIGHT = 12
BLOCK_WIDTH = 24
DELAY_TIME = 100

SORT_ALGORITMS = ["Straight Insertion", "Binary", "Shell", "Bubble", "Quick", "Selection", "Merge", "Heap"]


class Sort(QObject):
    data_changed_signal = pyqtSignal(int)

    def __init__(self, data=[], algorithm="", order="", parent=None):
        '''
        Args:
            oringin_data: unsorted data
            algorithm: the chosen algorithm
        '''
        super(Sort, self).__init__(parent)
        self.data = data
        self.algorithm = algorithm 
        self.arr_len = 0
        self.order = order


    def solve(self):
        if(self.algorithm == "Straight Insertion Sort"):
            self.insertion_sort()
        elif(self.algorithm == "Binary Sort"):
            self.binary_sort()
        elif(self.algorithm == "Shell Sort"):
            self.shell_sort()
        elif(self.algorithm == "Bubble Sort"):
            self.bubble_sort()
        elif(self.algorithm == "Quick Sort"):
            self.quick_sort()
        elif(self.algorithm == "Selection Sort"):
            self.selections_sort()
        elif(self.algorithm == "Merge Sort"):
            self.merge_sort(0, len(self.data) - 1)
        elif(self.algorithm == "Heap Sort"):
            self.heap_sort()


    def compare(self, data1, data2):
        if self.order == 'Ascending':
            return data1 < data2
        else:
            return data1 > data2


    def insertion_sort(self):
        for i in range(1, len(self.data), 1):
            pre_index = i - 1
            current = self.data[i]
            while pre_index >= 0 and self.compare(current, self.data[pre_index]):
                self.data[pre_index + 1] = self.data[pre_index]
                pre_index -= 1
                self.data_changed_signal.emit(pre_index + 1)
                QThread.msleep(DELAY_TIME)
            self.data[pre_index + 1] = current
            self.data_changed_signal.emit(pre_index + 1)
            QThread.msleep(DELAY_TIME)


    def binary_sort(self):
        for i in range(1, len(self.data), 1):
            tmp = self.data[i]
            low = 0
            high = i - 1
            while low <= high:
                m = (low + high) // 2
                if self.compare(tmp, self.data[m]):
                    high = m - 1
                else:
                    low = m + 1
            for j in range(i - 1, high, -1):
                self.data[j + 1] = self.data[j]
                self.data_changed_signal.emit(j + 1)
                QThread.msleep(DELAY_TIME)
            self.data[high + 1] = tmp 
            self.data_changed_signal.emit(high + 1)
            QThread.msleep(DELAY_TIME)


    def shell_sort(self):
        gap = 1
        while(gap < len(self.data)/3):
            gap = gap*3 + 1
        while gap > 0:
            for i in range(gap, len(self.data)):
                temp = self.data[i]
                j = i - gap
                while j >= 0 and self.compare(temp, self.data[j]):
                    self.data[j + gap] = self.data[j]
                    self.data_changed_signal.emit(j + gap)
                    QThread.msleep(DELAY_TIME)
                    j -= gap
                self.data[j + gap] = temp
                self.data_changed_signal.emit(j + gap)
                QThread.msleep(DELAY_TIME)
            gap = math.floor(gap/3)
        

    def bubble_sort(self):
        flag = False
        for i in range(1, len(self.data)):
            if flag == True:
                break
            flag = True
            for j in range(0, len(self.data) - i):
                if self.compare(self.data[j + 1], self.data[j]):
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    flag = False
                self.data_changed_signal.emit(j)
                QThread.msleep(DELAY_TIME)


    def quick_sort(self, left=None, right=None):
        left = 0 if not isinstance(left,(int, float)) else left
        right = len(self.data) - 1 if not isinstance(right,(int, float)) else right
        if left < right:
            partitionIndex = self.partition(left, right)
            self.quick_sort(left, partitionIndex-1)
            self.quick_sort(partitionIndex+1, right)
        return self.data
    

    def partition(self, left, right):
        pivot = left
        index = pivot + 1
        i = index
        while  i <= right:
            if self.compare(self.data[i], self.data[pivot]):
                self.swap(i, index)
                index += 1
            i += 1
        self.swap(pivot, index-1)
        return index - 1
    

    def swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self.data_changed_signal.emit(i)
        QThread.msleep(DELAY_TIME)


    def selections_sort(self):
        for i in range(len(self.data) - 1):
            min_index = i
            for j in range(i + 1, len(self.data)):
                if self.compare(self.data[j], self.data[min_index]):
                    min_index = j
            if i != min_index:
                self.swap(i, min_index)


    def merge_sort(self, start, end):
        if start < end:
           middle = start + (end - start) // 2
           self.merge_sort(start, middle)
           self.merge_sort(middle + 1, end)
           self.merge(start, middle, end)
        
        
    def merge(self, start, middle, end):
        n1 = middle - start + 1
        n2 = end - middle
        L = []
        R = []
        for i in range(n1):
            L.append(self.data[start + i])
        for i in range(n2):
            R.append(self.data[middle + 1 + i])
        k = start
        i = 0
        j = 0
        while i < n1 and j < n2:
            if self.compare(L[i], R[j]):
                self.data[k] = L[i]
                i = i + 1
            else:
                self.data[k] = R[j]
                j = j + 1
            k = k + 1
            self.data_changed_signal.emit(k)
            QThread.msleep(DELAY_TIME)
        while i < n1:
            self.data[k] = L[i]
            i = i + 1
            k = k + 1
            self.data_changed_signal.emit(k)
            QThread.msleep(DELAY_TIME)
        while j < n2:
            self.data[k] = R[j]
            j = j + 1
            k = k + 1
            self.data_changed_signal.emit(k)
            QThread.msleep(DELAY_TIME)

        
    def build_max_heap(self):
        for i in range(math.floor(len(self.data) / 2), -1, -1):
            self.heapify(i)
    
    
    def heapify(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        if left < self.arr_len and self.compare(self.data[largest], self.data[left]):
            largest = left
        if right < self.arr_len and self.compare(self.data[largest], self.data[right]):
            largest = right
    
        if largest != i:
            self.swap(i, largest)
            self.heapify(largest)

    
    def heap_sort(self):
        self.arr_len = len(self.data)
        self.build_max_heap()
        for i in range(len(self.data) - 1, 0, -1):
            self.swap(0, i)
            self.arr_len -= 1
            self.heapify(0)


# address of the ui file
ui_file_main = r"./sort_main.ui"

# analysis the ui file, get ui class and its basic class
(class_ui_main, class_basic_class_main) = PyQt5.uic.loadUiType(ui_file_main)


class MainWindow(class_basic_class_main, class_ui_main):
    '''
    GUI 界面
    '''
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # generate data set
        self.data = [i for i in range(1, 21, 1)]
        random.shuffle(self.data)
        self.data_validator = QIntValidator(self)
        self.lineEdit_data.setValidator(self.data_validator)
        
        self.initUI()
        self.initSignal()
        self.show() 


    def initUI(self):
        '''
        初始化GUI 界面
        '''
        self.listWidget_data.addItems([str(self.data[i]) for i in range(len(self.data))])
        self.comboBox_sort.addItems([i + " Sort" for i in SORT_ALGORITMS])


    def initSignal(self): 
        '''
        连接QT各组件间信号
        '''
        self.pushButton_add.clicked.connect(self.pushButton_add_clicked)
        self.pushButton_delete.clicked.connect(self.pushButton_delete_clicked)
        self.pushButton_StartSort.clicked.connect(self.pushButton_StartSort_clicked)


    def pushButton_add_clicked(self):
        if len(self.data) == DATA_NUM_MAX:
            QMessageBox.critical(self, "Warning", "The amount of data should be no more than " + str(DATA_NUM_MAX))
        else:
            tmp = self.lineEdit_data.text()
            self.data.append(int(self.lineEdit_data.text()))
            self.listWidget_data.addItem(tmp)


    def pushButton_delete_clicked(self):
        i = self.listWidget_data.currentRow()
        self.data.remove(int(self.listWidget_data.item(i).text()))
        self.listWidget_data.takeItem(i)
        self.listWidget_data.removeItemWidget(self.listWidget_data.item(i))
        

    def pushButton_StartSort_clicked(self):
        sort_data = copy.deepcopy(self.data)
        algorithm_name = self.comboBox_sort.currentText()
        if self.radioButton_de.isChecked():
            order = 'Descending'
        else:
            order = 'Ascending'
        self.sort_anime = SortAnime(algorithm_name, sort_data, len(sort_data), order)
        self.sort_anime.show()



# address of the ui file
ui_file_sort = r"./sort.ui"

# analysis the ui file, get ui class and its basic class
(class_ui_sort, class_basic_class_sort) = PyQt5.uic.loadUiType(ui_file_sort)


class SortAnime(class_basic_class_sort, class_ui_sort):
    '''
    GUI 界面
    '''
    def __init__(self, algorithm, data, num, order):
        super(SortAnime, self).__init__()
        self.title = algorithm
        self.algorithm = algorithm
        self.num = num
        self.data = data
        self.order = order
        self.oringin_data = copy.deepcopy(data)
        self.maximum = max(self.data)
        self.cur = 0
        self.setupUi(self)


        self.s = Sort(self.data, self.algorithm, self.order)
        self.thread = QThread(self)
        self.s.moveToThread(self.thread)
        self.initSignal()
        self.thread.start()
        self.initUI()
        self.color = [QColor('blue'), QColor('tomato'), QColor('gold'), QColor('orange'), QColor('deeppink'),
                      QColor('hotpink'), QColor('forestgreen'), QColor('violet')]


    def __del__(self):
        self.thread.quit()
        self.thread.wait()
        del self.thread

    def initUI(self):
        self.setWindowTitle(self.title)
        self.show()


    def initSignal(self): 
        '''
        连接QT各组件间信号
        '''
        self.s.data_changed_signal.connect(self.deal)
        self.thread.started.connect(self.s.solve)


    def paintEvent(self, event):
        q = QFont("黑体", 10)
        repeat_data = []
        counter = []
        for i in self.oringin_data:
            if self.oringin_data.count(i) > 1 and i not in repeat_data:
                counter.append(self.oringin_data.count(i))
                repeat_data.append(i)

        painter = QPainter()
        if(self.num == 0):
            return
        painter.begin(self)
        for i in range(self.num):
            rect = QRect(i*BLOCK_WIDTH + (i - 1) * 8 + 15, QWidget.height(self) - self.data[i]*BLOCK_HEIGHT/self.maximum*30 - 40, 
                         BLOCK_WIDTH - 1, self.data[i]*BLOCK_HEIGHT/self.maximum*30)
            if i == self.cur:
                painter.setBrush(QColor('red'))
            else:
                if self.data[i] in repeat_data:
                    tmp = repeat_data.index(self.data[i])
                    painter.setBrush(self.color[counter[tmp]])
                    counter[tmp] = counter[tmp] - 1
                else:
                    painter.setBrush(QColor('black'))
            painter.setFont(q)
            painter.drawText(i*BLOCK_WIDTH + (i - 1) * 8 + 20, QWidget.height(self) - 10, str(self.data[i]))
            painter.drawRect(rect)
        painter.end()


    def deal(self, c):
        self.cur = c
        self.repaint()


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_()) 


if __name__ == '__main__':
    main()
