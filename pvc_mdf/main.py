import json
import numpy as np
import matplotlib.pyplot as plt

class PVC():
    def __init__(self):
        super(PVC, self).__init__()
        self.file_path = "input.json"
        
    def read_connections(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            if 'connections' in data:
                ne_connections = len(data['connections'])
                connections = np.array(data['connections'])
                return ne_connections, connections

    def read_temperatures(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            if 'temperatures' in data:
                ne_temperatures = len(data['temperatures'])
                is_fixed = np.array([int(point[0]) for point in data['temperatures']])
                temperatures = np.array([float(point[1]) for point in data['temperatures']])
                return ne_temperatures, is_fixed, temperatures

    def output_res(self, result):
        output_dict = {"result": result}
        with open("output.json", "w") as f:
            json.dump(output_dict, f)

    def run(self):
        ne_connections, connections = self.read_connections()
        ne_temperatures, is_fixed, temperatures = self.read_temperatures()

        if ne_connections != ne_temperatures:
            return "Error: number of connections and temperatures are different"
        
        A = np.zeros((ne_connections, ne_connections))
        b = np.zeros(ne_connections)

        for i in range(ne_connections):
            if is_fixed[i] == 1:
                A[i, i] = 1
            else:
                A[i, i] = connections[i][0]
                for j in connections[i][1:]:
                    if j == 0:
                        continue
                    j -= 1
                    A[i, j] = -1
            b[i] = temperatures[i]
        
        x = np.linalg.solve(A, b)

        self.output_res({"x": x.tolist()})
        plt.plot(x)
        plt.show()