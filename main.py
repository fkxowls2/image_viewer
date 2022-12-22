from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt
import sys, time



#화면을 띄우는데 사용되는 Class 선언
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.build_ui()
        self.showMaximized()

        self.pathBtn.clicked.connect(self.path_btn_func)
        self.listWidget.itemClicked.connect(self.list_widget_func)

        self.imgJob = QPixmap()
        self.img_width = None
        self.control = False
        self.mouse_right = False
    
    def build_ui(self):
        '''그리드 레이아웃'''
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)
        '''파일 불러오기 버튼'''
        self.pathBtn = QPushButton('파일 불러오기', self)
        self.pathBtn.setMinimumSize(200, 50)
        self.pathBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.gridLayout.addWidget(self.pathBtn, 0, 0)
        '''기능 설명 라벨'''
        self.label = QLabel('확대(Ctrl+마우스휠), 이동(마우스 오른쪽 버튼+이동)', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label, 0, 1)
        '''파일 리스트 위젯'''
        self.listWidget = QListWidget()
        self.listWidget.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        self.gridLayout.addWidget(self.listWidget, 1, 0)
        '''이미지 뷰어 라벨'''
        self.labelView = QLabel()
        '''이미지 뷰어 스크롤'''
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.labelView)
        self.scrollArea.setWidgetResizable(True)
        self.gridLayout.addWidget(self.scrollArea, 1, 1)
        
        self.setWindowTitle('Image Viewer')
        self.show()
        
    def path_btn_func(self):
        self.file_paths = QFileDialog.getOpenFileNames(self)[0]
        self.listWidget.clear()
        for f in self.file_paths:
            self.listWidget.addItem(f.split('/')[-1])
            
    def list_widget_func(self):
        label_width = self.labelView.size().width()
        self.imgJob.load(self.file_paths[self.listWidget.currentRow()])
        if self.img_width is None:
            self.img_width = self.imgJob.size().width()
        if self.img_width > label_width:
            self.img_width = label_width
        self.imgJob = self.imgJob.scaledToWidth(self.img_width)
        self.labelView.setPixmap(self.imgJob)
        
    def wheelEvent(self, e):
        if self.control:
            zoom = e.angleDelta()
            self.img_width += zoom.y()
            if self.img_width <= 0:
                self.img_width = 0
            self.imgJob.load(self.file_paths[self.listWidget.currentRow()])
            self.imgJob = self.imgJob.scaledToWidth(self.img_width)
            self.labelView.setPixmap(self.imgJob)
        
    def keyPressEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            self.control = True
            
    def keyReleaseEvent(self, e):
        self.control = False
            
    def mouseMoveEvent(self, e):
        if self.mouse_right:
            self.scrollArea.ensureVisible(e.x()*10, e.y()*10)
            
    def mousePressEvent(self, e):
        if e.buttons() & Qt.RightButton:
            # self.scrollArea.ensureVisible(e.x(), e.y())
            self.mouse_right = True
    
    def mouseReleaseEvent(self, e):
        self.mouse_right = False
        

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 
    #WindowClass의 인스턴스 생성
    myWindow = Main() 
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()