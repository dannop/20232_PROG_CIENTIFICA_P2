class MyPoint:
    def __init__(self):
        self.m_x = 0
        self.m_y = 0

    def __init__(self,_x,_y):
        self.m_x = _x
        self.m_y = _y
    
    def setX(self,_x):
        self.m_x = _x

    def setY(self,_y):
        self.m_y = _y

    def getX(self):
        return self.m_x

    def getY(self):
        return self.m_y

class MyCurve:
    def __init__(self,_p1=None,_p2=None):
        self.m_p1 = _p1
        self.m_p2 = _p2
    
    def setP1(self,_p1):
        self.m_p1 = _p1
    
    def setP2(self,_p2):
        self.m_p2 = _p2
    
    def getP1(self):
        return self.m_p1
    
    def getP2(self):
        return self.m_p2

class MyModel:
    def __init__(self):
        self.m_verts = []
        self.m_coords = []
        self.m_connections = []
        self.m_restrictions = []
        self.m_forces = []
        self.m_temperatures = []

    def addVert(self, _vert):
        self.m_verts.append(_vert)

    def getVerts(self):
        return self.m_verts

    # def clearConnections(self):
    #     self.m_connections = []
        
    # def addConnection(self, _connection):
    #     self.m_connections.append(_connection)

    def getConnections(self):
        return self.m_connections
    
    def getRestrictions(self):
        return self.m_restrictions

    def setRestrictions(self, m_restrictions):
        self.m_restrictions = m_restrictions

    def getForces(self):
        return self.m_forces

    def setForces(self, m_forces):
        self.m_forces = m_forces
    
    def isEmpty(self):
        return (len(self.m_verts) == 0)
    
    def getBoundBox(self):
        if (len(self.m_verts) < 1):
            return 0.0,10.0,0.0,10.0
        if len(self.m_verts) > 0:
            xmin = self.m_verts[0]['x']
            xmax = xmin
            ymin = self.m_verts[0]['y']
            ymax = ymin
            for i in range(1,len(self.m_verts)):
                if self.m_verts[i]['x'] < xmin:
                    xmin = self.m_verts[i]['x']
                if self.m_verts[i]['x'] > xmax:
                    xmax = self.m_verts[i]['x']
                if self.m_verts[i]['y'] < ymin:
                    ymin = self.m_verts[i]['y']
                if self.m_verts[i]['y'] > ymax:
                    ymax = self.m_verts[i]['y']
        return xmin,xmax,ymin,ymax
    
    def clearAll(self):
        self.m_verts = []
        self.m_connections = []
        self.m_restrictions = []
        self.m_forces = []
        self.m_temperatures = []

    def getCoords(self):
        return self.m_coords
    
    def getConnections(self):
        return self.m_connections
    
    def getForces(self):
        return self.m_forces
    
    def getRestrictions(self):
        return self.m_restrictions
    
    def getTemperatures(self):
        return self.m_temperatures

    def setJSONData(self, space):
        self.m_coords = []
        self.m_connections = []
        self.m_forces = []
        self.m_restrictions = []
        self.m_temperatures = []
        for i in range(len(self.m_verts)):
            vert = self.m_verts[i]
            print(vert)
            count = 0
            i_left = 0
            i_right = 0
            i_up = 0
            i_down = 0
            
            for vert2 in self.m_verts:
                # Verificando se tem vertice a esquerda do vertice atual
                if vert['x'] == vert2['x'] - space and vert['y'] == vert2['y']:
                    count += 1
                    i_left = vert2['i']
                # Verificando se tem vertice a direita do vertice atual
                if vert['x'] == vert2['x'] + space and vert['y'] == vert2['y']:
                    count += 1
                    i_right = vert2['i']
                # Verificando se tem vertice acima do vertice atual
                if vert['x'] == vert2['x'] and vert['y'] == vert2['y'] + space:
                    count += 1
                    i_up = vert2['i']
                # Verificando se tem vertice abaixo do vertice atual
                if vert['x'] == vert2['x'] and vert['y'] == vert2['y'] - space:
                    count += 1
                    i_down = vert2['i']
            
            if count > 0:
                self.m_coords.append([vert['x'], vert['y']])
                values = [count, i_left, i_right, i_up, i_down]
                # Jogando todos os zeros pro final
                values.sort(key=lambda n:n==0)
                self.m_connections.append(values)
                self.m_temperatures.append(vert['temp'])
                self.m_forces.append(vert['force'])
                self.m_restrictions.append(vert['restric'])