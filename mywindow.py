from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QInputDialog

from mycanvas import *
from mymodel import *

class MyWindow(QMainWindow):
  def __init__(self):
    super(MyWindow, self).__init__()
    self.setGeometry(100, 100, 600, 400)
    self.setWindowTitle("Trabalho P2 - Programação Científica - Daniel Lessa")
    self.canvas = MyCanvas()
    self.setCentralWidget(self.canvas)
    # create a model object and pass to canvas
    self.model = MyModel()
    self.canvas.setModel(self.model)
    # create a Toolbar
    tb = self.addToolBar("File")
    fit = QAction(QIcon("icons/button_menu.png"), "fit", self)
    tb.addAction(fit)
    tb.actionTriggered[QAction].connect(self.tbpressed)
    grade = QAction(QIcon("icons/button_grade.png"), "grade", self)
    tb.addAction(grade)
    tb.actionTriggered[QAction].connect(self.tbpressed)

  def tbpressed(self, a):
    if a.text() == "fit":
      self.canvas.fitWorldToViewport()
      
    if a.text() == "grade":
      espaco, valid = QInputDialog.getInt(self, 'Grade de Pontos', 'Digite o espaço entre os pontos:')
      if valid:
        self.canvas.pointGrid(int(espaco))
