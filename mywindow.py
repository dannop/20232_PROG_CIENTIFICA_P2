from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QInputDialog

from mycanvas import *
from mymodel import *

class MyWindow(QMainWindow):
  def __init__(self):
    super(MyWindow, self).__init__()
    self.setGeometry(100, 100, 800, 600)
    self.setWindowTitle("Programação Científica - P2 - Daniel Lessa")
    self.model = MyModel()
    self.canvas = MyCanvas(self.model)
    self.setCentralWidget(self.canvas)
    self.setActions()
    
  def setActions(self):
    tb = self.addToolBar("File")
    delete = QAction(QIcon("icons/button_delete.png"), "Delete", self)
    tb.addAction(delete)
    fit = QAction(QIcon("icons/button_fit.png"), "Fit View", self)
    tb.addAction(fit)
    addLine = QAction(QIcon("icons/button_line.png"), "Add Line", self)
    tb.addAction(addLine)
    addBezier = QAction(QIcon("icons/button_points.png"), "Add 3 pt Bezier", self)
    tb.addAction(addBezier)
    grade = QAction(QIcon("icons/button_grade.png"), "Set Mesh", self)
    tb.addAction(grade)
    select = QAction(QIcon("icons/button_select.png"), "Select", self)
    tb.addAction(select)
    pvi = QAction("PVI", self)
    tb.addAction(pvi)
    force = QAction(QIcon("icons/button_download.png"), "Apply Force", self)
    tb.addAction(force)
    restriction = QAction(QIcon("icons/button_disable.png"), "Apply Restriction", self)
    tb.addAction(restriction)
    pvc = QAction("PVC", self)
    tb.addAction(pvc)
    temperature = QAction(QIcon("icons/button_termo.png"), "Apply Temperature", self)
    tb.addAction(temperature)
    tb.actionTriggered[QAction].connect(self.tbpressed)

  def tbpressed(self, action):
    if action.text() == "Delete":
      self.canvas.clearData()
    elif action.text() == "Fit View":
      self.canvas.fitWorldToViewport()
      self.canvas.update()
    elif action.text() == "Add Line":
      self.canvas.setState("Collect", "Line")
    elif action.text() == "Add 3 pt Bezier":
      self.canvas.setState("Collect", "Bezier2")
    elif action.text() == "Set Mesh":
      value, valid = QInputDialog.getInt(self, 'Mesh', 'Digite o espaço entre os pontos:')
      if valid:
        self.canvas.createMesh(int(value))
    elif action.text() == "Select":
      self.canvas.setState("Select")
    elif action.text() == "PVI":
      self.canvas.runPVI()
    elif action.text() == "Apply Force":
      self.canvas.updatePointTags('force', [1000, 0], [0, 0])
    elif action.text() == "Apply Restriction":
      self.canvas.updatePointTags('restric', 1, 0)
    elif action.text() == "PVC":
      self.canvas.runPVC()
    elif action.text() == "Apply Temperature":
      self.canvas.updatePointTags('temp', 1, 0)