import json
from PyQt5 import QtOpenGL, QtCore
from OpenGL.GL import *
from hetool.compgeom.compgeom import CompGeom
from hetool.he.hecontroller import HeController
from hetool.he.hemodel import HeModel
from hetool.geometry.segments.line import Point, Line
from hetool.geometry.point import Point
from hetool.compgeom.tesselation import Tesselation

class MyCanvas(QtOpenGL.QGLWidget):
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.m_model = None
        self.m_w = 0
        self.m_h = 0
        self.m_L = -1000.0
        self.m_R = 1000.0
        self.m_B = -1000.0
        self.m_T = 1000.0
        self.list = None

        self.m_buttonPressed = False
        self.m_pt0 = QtCore.QPoint(0, 0)
        self.m_pt1 = QtCore.QPoint(0, 0)

        self.m_hmodel = HeModel()
        self.m_controller = HeController(self.m_hmodel)

    def initializeGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
        self.list = glGenLists(1)

    def resizeGL(self, _width, _height):
        self.m_w = _width
        self.m_h = _height
        self.m_h = _height
        if (self.m_model is None) or (self.m_model.isEmpty()):
            self.scaleWorldWindow(1.0)
        else:
            self.m_L, self.m_R, self.m_B, self.m_T = self.m_model.getBoundBox()
            self.scaleWorldWindow(1.1)

        glViewport(0, 0, self.m_w, self.m_h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        if not (self.m_hmodel.isEmpty()):
            patches = self.m_hmodel.getPatches()

            for pat in patches:
                print(len(patches))
                pts = pat.getPoints()
                print(len(pts))
                triangs = Tesselation.tessellate(pts)
                for j in range(len(triangs)):
                    glColor(1.0, 0.0, 1.0)
                    glBegin(GL_TRIANGLES)
                    for i in range(3):
                        glVertex2d(triangs[j][i].getX(), triangs[j][i].getY())
                    glEnd()
            segments = self.m_hmodel.getSegments()
            for curv in segments:
                ptc = curv.getPointsToDraw()
                glColor(0.0, 1.0, 1.0)
                glBegin(GL_LINES)
                for i in range(2):
                    glVertex2f(ptc[i].getX(), ptc[i].getY())
                # glVertex2f(ptc[1].getX(), ptc[1].getY())
                glEnd()

    def setModel(self, _model):
        self.m_model = _model

    def fitWorldToViewport(self):
        print("fitWorldToViewport")

        if self.m_model is None:
            return

        self.m_L, self.m_R, self.m_B, self.m_T = self.m_model.getBoundBox()
        self.scaleWorldWindow(1.10)
        self.update()

    def scaleWorldWindow(self, _scaleFac):
        vpr = self.m_h / self.m_w
        cx = (self.m_L + self.m_R) / 2.0
        cy = (self.m_B + self.m_T) / 2.0
        sizex = (self.m_R - self.m_L) * _scaleFac
        sizey = (self.m_T - self.m_B) * _scaleFac
        if sizey > (vpr * sizex):
            sizex = sizey / vpr
        else:
            sizey = sizex * vpr
        self.m_L = cx - (sizex * 0.5)
        self.m_R = cx + (sizex * 0.5)
        self.m_B = cy - (sizey * 0.5)
        self.m_T = cy + (sizey * 0.5)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)

    def panWorldWindow(self, _panFacX, _panFacY):
        panX = (self.m_R - self.m_L) * _panFacX
        panY = (self.m_T - self.m_B) * _panFacY
        self.m_L += panX
        self.m_R += panX
        self.m_B += panY
        self.m_T += panY
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)

    def convertPtCoordsToUniverse(self, _pt):
        dX = self.m_R - self.m_L
        dY = self.m_T - self.m_B
        mX = _pt.x() * dX / self.m_w
        mY = (self.m_h - _pt.y()) * dY / self.m_h
        x = self.m_L + mX
        y = self.m_B + mY
        return QtCore.QPointF(x, y)

    def mousePressEvent(self, event):
        self.m_buttonPressed = True

        self.m_pt0 = event.pos()

    def mouseMoveEvent(self, event):
        if self.m_buttonPressed:
            self.m_pt1 = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)

        # self.m_model.setCurve(pt0_U.x(), pt0_U.y(), pt1_U.x(), pt1_U.y())
        # self.m_model.setCurve(self.m_pt0.x(), self.m_pt0.y(), self.m_pt1.x(), self.m_pt1.y())
        self.m_buttonPressed = False
        self.m_pt0.setX(0)
        self.m_pt0.setY(0)
        self.m_pt1.setX(0)
        self.m_pt1.setY(0)

        p0 = Point(pt0_U.x(), pt0_U.y())
        p1 = Point(pt1_U.x(), pt1_U.y())
        segment = Line(p0, p1)

        self.m_controller.insertSegment(segment, 0.01)
        self.update()
        self.repaint()

    def pointGrid(self, space):
        self.space = space
        if self.space > 0:
            xmax = self.m_hmodel.getBoundBox()[1]
            xmin = self.m_hmodel.getBoundBox()[0]
            x_quant = int((xmax - xmin) / self.space)
            ymax = self.m_hmodel.getBoundBox()[3]
            ymin = self.m_hmodel.getBoundBox()[2]
            y_quant = int((ymax - ymin) / self.space)
            glNewList(self.list, GL_COMPILE)
            json_data = {"points": [] }
            for i in range(x_quant):
                for j in range(y_quant):
                    posx = xmin + self.space*i
                    posy = ymin + self.space*j
                    point = Point(posx, posy)
                    if CompGeom.isPointInPolygon(self.m_hmodel.getPoints(), point):
                        glColor4f(1.0, 1.0, 1.0, 1.0)
                        glPointSize(4)
                        glBegin(GL_POINTS)
                        glVertex2f(point.getX(), point.getY())
                        glEnd()
                        json_data["points"].append([point.getX(), point.getY()])
            glEndList()

            json_object = json.dumps(json_data)
            with open("input.json", "w") as outfile:
                outfile.write(json_object)