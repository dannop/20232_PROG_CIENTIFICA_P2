import json
from PyQt5 import QtOpenGL, QtCore
from OpenGL.GL import *
from hetool.compgeom.compgeom import CompGeom
from hetool.he.hecontroller import HeController
from hetool.he.hemodel import HeModel
from hetool.geometry.segments.line import Point
from hetool.geometry.point import Point
from hetool.compgeom.tesselation import Tesselation
from mycollector import *
from pvc_mdf.main import PVC
from pvi_med.main import PVI
class MyCanvas(QtOpenGL.QGLWidget):
    def __init__(self, m_model):
        super(MyCanvas, self).__init__()
        self.m_model = m_model
        self.m_w = 0
        self.m_h = 0
        self.m_L = -1000.0
        self.m_R = 1000.0
        self.m_B = -1000.0
        self.m_T = 1000.0
        self.space = 0

        self.m_collector = MyCollector()
        self.m_state = "View"
        self.m_mousePt = QtCore.QPointF(0.0, 0.0)
        self.m_heTol = 10.0

        self.m_hmodel = HeModel()
        self.m_controller = HeController(self.m_hmodel)

    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        
    def resizeGL(self, _width, _height):
        self.m_w = _width
        self.m_h = _height

        if self.m_model.isEmpty():
            self.scaleWorldWindow(1.0)
        else:
            self.fitWorldToViewport()

        glViewport(0, 0, _width, _height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glShadeModel(GL_SMOOTH)

        patches = self.m_hmodel.getPatches()
        for patch in patches:
            if patch.isDeleted:
                glColor3f(0.0, 0.0, 0.0)
            elif patch.isSelected():
                glColor3f(1.00, 0.75, 0.75)
            else:
                glColor3f(0.75, 0.75, 0.75)
            
            triangs = Tesselation.tessellate(patch.getPoints())
            for triangle in triangs:
                glBegin(GL_TRIANGLES)
                for point in triangle:
                    glVertex2d(point.getX(), point.getY())
                glEnd()

        segments = self.m_hmodel.getSegments()
        for segment in segments:
            if segment.isSelected():
                glColor3f(1.00, 0.75, 0.75)
            else:
                glColor(0.0, 1.0, 1.0)
            
            points = segment.getPointsToDraw()
            glBegin(GL_LINE_STRIP)
            for point in points:
                glVertex2f(point.getX(), point.getY())
            glEnd()

        points = self.m_hmodel.getPoints()
        for point in points:
            if point.isSelected():
                glColor3f(1.00, 0.75, 0.75)
            else:
                for vert in self.m_model.getVerts():
                    if vert['x'] == point.getX() and vert['y'] == point.getY():
                        if vert['force'] != [0, 0]:
                            glColor3f(0.0, 1.0, 0.5)
                        elif vert['restric'] != [0, 0]:
                            glColor3f(0.0, 0.0, 0.0)
                        elif vert['temp'] != [0, 0]:
                            glColor3f(1.0, 0.0, 0.0)
                        else:
                            glColor3f(0.7, 0.0, 1.0)
                        break
                    else:
                        glColor3f(0.7, 0.0, 1.0)

            glPointSize(3)
            glBegin(GL_POINTS)
            glVertex2f(point.getX(), point.getY())
            glEnd()
        
        if self.m_collector.isActive():
            currentCurve = self.m_collector.getCurveToDraw()
            if len(currentCurve) > 0:
                glColor3f(1.0, 0.0, 1.0)
                glBegin(GL_LINE_STRIP)
                for point in currentCurve:
                    glVertex2f(point[0], point[1])
                glEnd()

    def fitWorldToViewport(self):
        if self.m_model.isEmpty():
            return

        self.m_L, self.m_R, self.m_B, self.m_T = self.m_model.getBoundBox()
        self.scaleWorldWindow(1.1)
        self.update()

    def scaleWorldWindow(self, _scaleFactor):
        cx = 0.5*(self.m_L + self.m_R)
        cy = 0.5*(self.m_B + self.m_T)
        dx = (self.m_R - self.m_L)*_scaleFactor
        dy = (self.m_T - self.m_B)*_scaleFactor

        ratioVP = self.m_h/self.m_w
        if dy > dx*ratioVP:
            dx = dy/ratioVP
        else:
            dy = dx*ratioVP

        self.m_L = cx - 0.5*dx
        self.m_R = cx + 0.5*dx
        self.m_B = cy - 0.5*dy
        self.m_T = cy + 0.5*dy

        self.m_heTol = 0.005*(dx+dy)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def setState(self, state="View", varg="default"):
        self.m_state = state
        
        if state == "View":
            self.m_collector.deactivateCollector()
            self.m_controller.unSelectAll()
        elif state == "Collect":
            self.m_collector.activateCollector(varg)
        else:
            self.m_collector.deactivateCollector()

    def mouseMoveEvent(self, event):
        point = event.pos()
        self.m_mousePt = point
        if self.m_collector.isActive():
            point = self.convertPtCoordsToUniverse(point)
            self.m_collector.update(point.x(), point.y())
            self.update()

    def mouseReleaseEvent(self, event):
        point = event.pos()
        point_univ = self.convertPtCoordsToUniverse(point)
        if self.m_collector.isActive():
            snaped, xs, ys = self.m_hmodel.snapToPoint(point_univ.x(), point_univ.y(), self.m_heTol)
            if snaped:
                isComplete = self.m_collector.collectPoint(xs, ys)
            else:
                snaped, xs, ys = self.m_hmodel.snapToSegment(point_univ.x(), point_univ.y(), self.m_heTol)
                if snaped:
                    isComplete = self.m_collector.collectPoint(xs, ys)
                else:
                    isComplete = self.m_collector.collectPoint(point_univ.x(), point_univ.y())

            if isComplete:
                self.setMouseTracking(False)
                curve = self.m_collector.getCurve()
                heSegment = []
                for point in curve:
                    heSegment.append(point[0])
                    heSegment.append(point[1])
                self.m_controller.insertSegment(heSegment, 0.01)
                self.update()
                self.repaint()
            else:
                self.setMouseTracking(True)

        if self.m_state == "Select":
            self.m_controller.selectPick(point_univ.x(), point_univ.y(), self.m_heTol, False)
            self.update()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scaleWorldWindow(0.9)
        else:
            self.scaleWorldWindow(1.1)
        self.update()

    def convertPtCoordsToUniverse(self, _pt):
        dX = self.m_R - self.m_L
        dY = self.m_T - self.m_B
        mX = _pt.x() * dX / self.m_w
        mY = (self.m_h - _pt.y()) * dY / self.m_h
        x = self.m_L + mX
        y = self.m_B + mY
        return QtCore.QPointF(x, y)

    def clearData(self):
        self.m_model.clearAll()
        self.m_hmodel.clearAll()
        self.update()
    
    def updatePointTags(self, kind, if_value, else_value):
        points = self.m_hmodel.getPoints()
        for point in points:
            if point.isSelected():
                for vert in self.m_model.getVerts():
                    if vert['x'] == point.getX() and vert['y'] == point.getY():
                        vert[kind] = if_value if vert[kind] == else_value else else_value
                        break
        self.update()
        self.m_model.setJSONData(self.space)

    def runPVC(self):
        json_data = {
            "connections": self.m_model.getConnections(), 
            "temperatures": self.m_model.getTemperatures(),
        }
        json_object = json.dumps(json_data)
        with open("pvc_mdf/input.json", "w") as outfile:
            outfile.write(json_object)
        pvc = PVC()
        pvc.run()

    def runPVI(self):
        json_data = {
            "coords": self.m_model.getCoords(), 
            "connections": self.m_model.getConnections(), 
            "restrictions": self.m_model.getRestrictions(), 
            "forces": self.m_model.getForces()
        }
        json_object = json.dumps(json_data)
        with open("pvi_med/input.json", "w") as outfile:
            outfile.write(json_object)
        pvi = PVI()
        pvi.run()

    def createMesh(self, space):
        self.space = space
        if space > 0:
            xmax = self.m_hmodel.getBoundBox()[1]
            xmin = self.m_hmodel.getBoundBox()[0]
            x_quant = int((xmax - xmin) / space)

            ymax = self.m_hmodel.getBoundBox()[3]
            ymin = self.m_hmodel.getBoundBox()[2]
            y_quant = int((ymax - ymin) / space)

            points = []
            for i in range(x_quant):
                for j in range(y_quant):
                    posx = xmin + space*i
                    posy = ymin + space*j
                    point = Point(posx, posy)
                    patches = self.m_hmodel.getPatches()
                    for pacth in patches:
                        if CompGeom.isPointInPolygon(pacth.getPoints(), point):
                            self.m_controller.insertPoint([point.getX(), point.getY()], 0.01)
                            points.append(point)
            self.update()

            for i in range(len(points)):
                point = points[i]
                self.m_model.addVert({
                    'i': i+1, 
                    'x': point.getX(), 
                    'y': point.getY(),
                    'force': [0, 0],
                    'restric': [0, 0],
                    'temp': [0, 0]
                })
            self.m_model.setJSONData(space)
