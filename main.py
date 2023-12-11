import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QInputDialog, QLabel, QGridLayout
import graph  # Import your graph module
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.G = graph.create_graph()  # Create the graph once
        self.path = None  # Store the current path
        self.pos = nx.spring_layout(self.G)  # Store the positions of the nodes

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.btn = QPushButton('Find shortest path', self)
        self.btn.clicked.connect(self.showDialog)
        grid.addWidget(self.btn, 0, 0)

        self.label = QLabel(self)
        grid.addWidget(self.label, 1, 0)

        self.figure = plt.figure(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)
        grid.addWidget(self.canvas, 0, 1, 2, 1)

        self.setWindowTitle('Shortest Path Finder')
        self.setGeometry(300, 300, 700, 300)
        self.show()

        # Draw the graph once
        self.draw_graph()

    def draw_graph(self):
        self.figure.clear()

        # Draw all edges in black
        nx.draw_networkx_edges(self.G, self.pos, ax=self.figure.add_subplot(111))

        # Draw all nodes in black
        nx.draw_networkx_nodes(self.G, self.pos, node_color='black', ax=self.figure.gca())
        nx.draw_networkx_labels(self.G, self.pos, ax=self.figure.gca())  # Add node labels

        # Add labels with edge parameters
        edge_labels = {(u, v): f'[{d["length"]}, {d["speed_limit"]}, {d["congestion1"]}, {d["congestion2"]}]'
                       for u, v, d in self.G.edges(data=True)}
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.figure.gca())

        # If there's a path, highlight it
        if self.path is not None:
            nx.draw_networkx_edges(self.G, self.pos, edgelist=self.path, edge_color='r', ax=self.figure.gca())
            nx.draw_networkx_nodes(self.G, self.pos, nodelist=[node for edge in self.path for node in edge], node_color='r', ax=self.figure.gca())

        self.canvas.draw()

    def showDialog(self):
        start_node, ok1 = QInputDialog.getInt(self, 'Input Dialog', 'Enter start node:')
        end_node, ok2 = QInputDialog.getInt(self, 'Input Dialog', 'Enter end node:')

        if ok1 and ok2:
            path, time = graph.a_star(self.G, start_node, end_node)
            self.label.setText(f'Shortest path: {" -> ".join(map(str, path))}\nTime: {time} minutes')

            # Store the path as a list of edges
            self.path = list(zip(path, path[1:]))

            # Redraw the graph with the new path
            self.draw_graph()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
