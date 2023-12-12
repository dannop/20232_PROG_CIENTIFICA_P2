import json
import numpy as np
import matplotlib.pyplot as plt

def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        if 'coords' in data:
            ne = len(data['coords'])
            x0 = np.array([float(point[0]) for point in data['coords']])
            y0 = np.array([float(point[1]) for point in data['coords']])
            return ne, x0, y0

def output_res(result):
    output_dict = {"result": result}
    with open("output.json", "w") as f:
        json.dump(output_dict, f)

def run(file_path):
    N = 600
    h = 0.00004
    ne, x0, y0 = read_json(file_path)
    ndofs = 2 * ne
    raio = 1.0
    mass = 7850.0
    kspr = 210000000000.0
    conect = np.array([
        [2, 2, 4, 0, 0],
        [3, 1, 3, 5, 0],
        # ... (remaining array elements)
    ])

    F = np.array([
        [0.0, 0.0],
        # ... (remaining array elements)
    ])

    restrs = np.array([
        [1, 1],
        # ... (remaining array elements)
    ])

    F = F.T.reshape((ndofs, 1))
    restrs = restrs.T.reshape((ndofs, 1))

    u = np.zeros((ndofs, 1))
    v = np.zeros((ndofs, 1))
    a = np.zeros((ndofs, 1))
    res = np.zeros((N,))

    fi = np.zeros((ndofs, 1))

    a[:] = (F - fi) / mass

    for i in range(N):
        print("Novo I")
        v += a * (0.5 * h)
        u += v * h

        # contato
        fi.fill(0.0)

        for j in range(ne):
            print("Novo J")
            if restrs[2*j, 0] == 1:
                u[2*j, 0] = 0.0
            if restrs[2*j + 1, 0] == 1:
                u[2*j + 1, 0] = 0.0

            xj = x0[j] + u[2*j, 0]
            yj = y0[j] + u[2*j + 1, 0]

            for index in range(1, conect[j, 0] + 1):
                k = conect[j, index]
                xk = x0[k] + u[2*k, 0]
                yk = y0[k] + u[2*k + 1, 0]
                dX = xj - xk
                dY = yj - yk
                di = np.sqrt(dX**2 + dY**2)
                d2 = (di - 2 * raio)
                dx = d2 * dX / di
                dy = d2 * dY / di
                fi[2*j, 0] += kspr * dx
                fi[2*j + 1, 0] += kspr * dy

        a[:] = (F - fi) / mass
        v += a * (0.5 * h)
        # plot
        res[i] = u[32, 0]

    output_res(res)
    x = np.arange(1, N + 1)
    plt.plot(x, res)
    plt.show()