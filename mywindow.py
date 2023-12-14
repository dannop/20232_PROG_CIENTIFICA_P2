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
    restriction = QAction(QIcon("icons/button_disable.png"), "Apply Restriction", self)
    tb.addAction(restriction)
    left_force = QAction(QIcon("icons/button_arrow_left.png"), "Apply Left Force", self)
    tb.addAction(left_force)
    right_force = QAction(QIcon("icons/button_arrow_right.png"), "Apply Right Force", self)
    tb.addAction(right_force)
    up_force = QAction(QIcon("icons/button_arrow_up.png"), "Apply Up Force", self)
    tb.addAction(up_force)
    down_force = QAction(QIcon("icons/button_arrow_down.png"), "Apply Down Force", self)
    tb.addAction(down_force)
    pvc = QAction("PVC", self)
    tb.addAction(pvc)
    temperature = QAction(QIcon("icons/button_termo1.png"), "Apply Temperature 100", self)
    tb.addAction(temperature)
    temperature = QAction(QIcon("icons/button_termo2.png"), "Apply Temperature 50", self)
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
        self.canvas.createMesh(float(value))
    elif action.text() == "Select":
      self.canvas.setState("Select")
    elif action.text() == "PVI":
      self.canvas.runPVI()
    elif action.text() == "Apply Restriction":
      self.canvas.updatePointTags('restric', [1, 1], [0, 0])
    elif action.text() == "Apply Left Force":
      self.canvas.updatePointTags('force', [1000, 0], [0, 0])
    elif action.text() == "Apply Right Force":
      self.canvas.updatePointTags('force', [-1000, 0], [0, 0])
    elif action.text() == "Apply Up Force":
      self.canvas.updatePointTags('force', [0, 1000], [0, 0])
    elif action.text() == "Apply Down Force":
      self.canvas.updatePointTags('force', [0, -1000], [0, 0])
    elif action.text() == "PVC":
      self.canvas.runPVC()
    elif action.text() == "Apply Temperature 100":
      self.canvas.updatePointTags('temp', [1, 100], [0, 0])
    elif action.text() == "Apply Temperature 50":
      self.canvas.updatePointTags('temp', [1, 50], [0, 0])