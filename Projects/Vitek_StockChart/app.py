import sys
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QStyle,
    QSizePolicy,
    QMessageBox,
    QSpinBox
)
from PyQt6.QtGui import QIcon, QFont, QFontDatabase, QPalette, QColor, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtCharts import QCandlestickSeries, QChart, QChartView, QCandlestickSet, QValueAxis, QBarCategoryAxis, QBarSeries, QBarSet, QCategoryAxis, QAbstractAxis, QLineSeries




class Window(QWidget):
    def change_stock_ticker(self, ticker: str) -> None:
        self.stock_ticker = ticker
        
    def update_stock(self) -> None:
        self.downloadData()
        self.series.clear()
        self.axisX.clear()
        self.processData()
        self.set_boundaries()
    
    def change_market_days(self, days: int) -> None:
        self.market_days_shown = days
        self.series.clear()
        self.axisX.clear()
        self.processData()
        self.set_boundaries()

    stock_ticker = 'BA'    
    tm = []  # stores str type data
    market_days_shown = 20

    def downloadData(self):
        # api key 9FTHOZM5TKJCTYXL
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&datatype=csv&symbol='+self.stock_ticker+'&outputsize=compact&apikey=9FTHOZM5TKJCTYXL'
        try:
            self.df = pd.read_csv(url)
        except:
            print("Nepodařilo se stáhnout data")
        else:
            print("Downloaded")
    
    def create_series(self):
        self.series = QCandlestickSeries()
        self.series.setDecreasingColor(QColor(255,0,0))
        self.series.setIncreasingColor(QColor(0,255,0))
    
    def create_rest(self):
        self.chart = QChart()
        self.chart.addSeries(self.series)  # candles
        #self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.legend().hide()

        self.axisX = QBarCategoryAxis()
        self.axisX.setLabelsAngle(-90)
        self.axisX.append(self.tm)

        self.axisX.show()
        self.chart.addAxis(self.axisX, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axisX)

        self.axisY = QValueAxis()   # axis Y
        self.axisY.show()
        self.chart.addAxis(self.axisY, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axisY)

        self.axisY.setMax(self.y_max)
        self.axisY.setMin(self.y_min)
        

        self.chart.show()

    def processData(self):
        self.tm=[]
        self.y_min, self.y_max = (
            float("inf"),
            -float("inf"),
        )
        try:
            for index, row in self.df.iterrows():
                self.series.insert(0,QCandlestickSet(row['open'], row['high'], row['low'], row['close']))
                timestamp = str(int(row['timestamp'][8:10]))+'.'+str(row['timestamp'][5:7])+'.'
                self.tm.insert(0,timestamp)
                self.y_min = min(self.y_min, row['open'], row['high'], row['low'], row['close'])
                self.y_max = max(self.y_max, row['open'], row['high'], row['low'], row['close'])
                if index == self.market_days_shown-1: break
        except KeyError:
            print("Pravděpodobně je zadaný neplatný ticker")
            return
        
        
    def set_boundaries(self):
        self.axisX.append(self.tm)
        self.axisY.setMax(self.y_max)
        self.axisY.setMin(self.y_min)
        self.axisY.setRange(self.y_min, self.y_max)
        self.axisY.show()


    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("StockChart v1")

        self.scroll_area = QScrollArea()
        self.vbox = QVBoxLayout()

        # STOCK BUTTON AND LINE EDIT
        self.stock_symbol_container = QWidget()
        self.stock_symbol_container.setLayout(QHBoxLayout())

        btn = QPushButton("Aktualizovat")
        btn.clicked.connect(self.update_stock)
        self.stock_symbol_container.layout().addWidget(btn)
        line_edit = QLineEdit(self.stock_ticker)
        line_edit.textChanged.connect(self.change_stock_ticker)
        self.stock_symbol_container.layout().addWidget(line_edit)

        spinbox = QSpinBox()
        spinbox.setRange(15,100) # number of market days shown allowed
        spinbox.setValue(20) # set initial value
        spinbox.valueChanged.connect(self.change_market_days)
        self.stock_symbol_container.layout().addWidget(spinbox)

        self.vbox.addWidget(self.stock_symbol_container)

        self.downloadData()
        self.create_series()
        self.processData()
        self.create_rest()

        # VARIABLE GRID
        self.chartview = QChartView(self.chart)
        self.chartview.setObjectName("chartview")
        self.vbox.addWidget(self.chartview)

        # MAIN LAYOUT
        self.vbox.addWidget(QLabel("Vytvořil Lukáš Vítek, 2022"))
        self.setLayout(self.vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.resize(800, 600)
    window.move(300, 100)
    sys.exit(app.exec())