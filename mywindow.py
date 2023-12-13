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
    
    tb = self.addToolBar("File")
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
    delete = QAction(QIcon("icons/button_delete.png"), "Delete", self)
    tb.addAction(delete)
    pvc = QAction(QIcon("icons/button_download.png"), "Apply Force", self)
    tb.addAction(pvc)
    pvi = QAction(QIcon("icons/button_arrow.png"), "Apply Restriction", self)
    tb.addAction(pvi)
    pvc = QAction(QIcon("icons/button_termo.png"), "PVC", self)
    tb.addAction(pvc)
    pvi = QAction(QIcon("icons/button_task.png"), "PVI", self)
    tb.addAction(pvi)
    tb.actionTriggered[QAction].connect(self.tbpressed)
    undo = QAction(QIcon("icons/button_undo.png"), "Undo", self)
    tb.addAction(undo)
    redo = QAction(QIcon("icons/button_redo.png"), "Redo", self)
    tb.addAction(redo)

  def tbpressed(self, action):
    if action.text() == "Fit View":
      self.canvas.fitWorldToViewport()
      self.canvas.update()
    elif action.text() == "Add Line":
      self.canvas.setState("Collect", "Line")
    elif action.text() == "Add 3 pt Bezier":
      self.canvas.setState("Collect", "Bezier2")
    if action.text() == "Set Mesh":
      value, valid = QInputDialog.getInt(self, 'Mesh', 'Digite o espaço entre os pontos:')
      if valid:
        self.canvas.createMesh(int(value))
    elif action.text() == "Select":
      self.canvas.setState("Select")
    elif action.text() == "Delete":
      action.delSelectedEntities()
      self.canvas.update()
    elif action.text() == "Apply Force":
      self.canvas.updateForce()
    elif action.text() == "Apply Restriction":
      self.canvas.updateRestriction()
    elif action.text() == "PVC":
      action.undo()
      self.canvas.update()
    elif action.text() == "PVI":
      action.redo()
      self.canvas.update()
    elif action.text() == "Undo":
      action.undo()
      self.canvas.update()
    elif action.text() == "Redo":
      action.redo()
      self.canvas.update()
