import json
import numpy as np
import matplotlib.pyplot as plt

def read_coords(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        if 'coords' in data:
            ne_coords = len(data['coords'])
            x_coords = np.array([float(point[0]) for point in data['coords']])
            y_coords = np.array([float(point[1]) for point in data['coords']])
            return ne_coords, x_coords, y_coords

def read_connections(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        if 'connections' in data:
            ne_connections = len(data['connections'])
            connections = np.array(data['connections'])
            return ne_connections, connections

def read_restrictions(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        if 'restrictions' in data:
            ne_restrictions = len(data['restrictions'])
            restrictions = np.array(data['restrictions'])
            return ne_restrictions, restrictions

def read_forces(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        if 'forces' in data:
            ne_forces = len(data['forces'])
            x_forces = np.array([float(point[0]) for point in data['forces']])
            y_forces = np.array([float(point[1]) for point in data['forces']])
            return ne_forces, x_forces, y_forces
        
def output_res(key, ux, uy, vx, vy, ax, ay):
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

def run(file_path):
    T = 1
    num_steps = 100
    dt = T/num_steps
    
    radius = 0.1
    mass = 1
    kf = 1

    ne_coords, x_coords, y_coords = read_coords(file_path)
    
    ne_connections, connections = read_connections(file_path)
    if ne_coords != ne_connections:
        return "Error: number of coordinates and connections are different"
    
    ne_restrictions, restrictions = read_restrictions(file_path)
    if ne_coords != ne_restrictions:
        return "Error: number of coordinates and restrictions are different"

    ne_forces, x_forces, y_forces = read_forces(file_path)
    if ne_coords != ne_forces:
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

            for k in connections[j]:
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
                
        output_res("Result_"+str(i), ux, uy, vx, vy, ax, ay)