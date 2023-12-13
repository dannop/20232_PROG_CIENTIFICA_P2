import json
import numpy as np
# import matplotlib.pyplot as plt

class PVI():
    def __init__(self):
        super(PVI, self).__init__()
        self.file_path = "pvi_med/input.json"

    def read_coords(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            if 'coords' in data:
                ne_coords = len(data['coords'])
                x_coords = np.array([float(point[0]) for point in data['coords']])
                y_coords = np.array([float(point[1]) for point in data['coords']])
                return ne_coords, x_coords, y_coords

    def read_connections(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            if 'connections' in data:
                ne_connections = len(data['connections'])
                connections = np.array(data['connections'])
                return ne_connections, connections

    def read_restrictions(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            if 'restrictions' in data:
                ne_restrictions = len(data['restrictions'])
                restrictions = np.array(data['restrictions'])
                return ne_restrictions, restrictions

    def read_forces(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            if 'forces' in data:
                ne_forces = len(data['forces'])
                x_forces = np.array([float(point[0]) for point in data['forces']])
                y_forces = np.array([float(point[1]) for point in data['forces']])
                return ne_forces, x_forces, y_forces
            
    def output_res(self, key, ux, uy, vx, vy, ax, ay):
        print(key)
        output_dict = {key: {
            "ux": ux.tolist(),
            "uy": uy.tolist(),
            "vx": vx.tolist(),
            "vy": vy.tolist(),
            "ax": ax.tolist(),
            "ay": ay.tolist()
        }}
        
        with open("output.json", "w") as f:
            json.dump(output_dict, f)

    def run(self):
        T = 1
        num_steps = 1
        dt = T/num_steps
        
        radius = 0.1
        mass = 1
        kf = 1

        ne_coords, x_coords, y_coords = self.read_coords()
        
        ne_connections, connections = self.read_connections()
        if ne_coords != ne_connections:
            print("Error: number of coordinates and connections are different", ne_coords, ne_connections)
            return "Error: number of coordinates and connections are different"
        
        ne_restrictions, restrictions = self.read_restrictions()
        if ne_coords != ne_restrictions:
            print("Error: number of coordinates and restrictions are different", ne_coords, ne_restrictions)
            return "Error: number of coordinates and restrictions are different"

        ne_forces, x_forces, y_forces = self.read_forces()
        if ne_coords != ne_forces:
            print("Error: number of coordinates and forces are different", ne_coords, ne_forces)
            return "Error: number of coordinates and forces are different"

        ux = np.zeros(ne_coords)
        uy = np.zeros(ne_coords)
        vx = np.zeros(ne_coords)
        vy = np.zeros(ne_coords)
        ax = np.zeros(ne_coords)
        ay = np.zeros(ne_coords)
        fix = np.zeros(ne_coords)
        fiy = np.zeros(ne_coords)
        
        for i in range(num_steps):
            print("PVI", i)
            ax = (x_forces - fix)/mass
            ay = (y_forces - fiy)/mass
            vx = vx + ax*dt
            vy = vy + ay*dt
            ux = ux + vx*dt + ax*dt*dt/2
            uy = uy + vy*dt + ay*dt*dt/2

            fix = np.zeros(ne_coords)
            fiy = np.zeros(ne_coords)
            for j in range(ne_coords):
                if restrictions[j][0] == 1:
                    ux[j] = 0

                if restrictions[j][1] == 1:
                    uy[j] = 0

                x = x_coords[j]+ux[j]
                y = y_coords[j]+uy[j]
                
                for k in connections[j][1:]:
                    if k == 0:
                        continue
                    k = k-1
                    xk = x_coords[k]+ux[k]
                    yk = y_coords[k]+uy[k]
                    dx = xk-x
                    dy = yk-y
                    dl = np.sqrt(dx*dx+dy*dy)
                    dc = dl - 2*radius 
                    dx = dx * dc/dl
                    dy = dy * dc/dl
                    fix[j] = fix[j] + dx * kf
                    fiy[j] = fiy[j] + dy * kf
                    
            self.output_res("Result_"+str(i), ux, uy, vx, vy, ax, ay)