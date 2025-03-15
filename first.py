from collections import deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices  
        self.graph = [[0] * vertices for _ in range(vertices)]  
        self.flow = [[0] * vertices for _ in range(vertices)]  
    
    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity

    def bfs(self, source, sink, parent):
        visited = [False] * self.V
        queue = deque([source])
        visited[source] = True
        
        while queue:
            u = queue.popleft()

            for v in range(self.V):
                if not visited[v] and self.graph[u][v] > 0: 
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u

                    if v == sink:
                        return True
        return False
    
    def edmonds_karp(self, source, sink):
        parent = [-1] * self.V  
        max_flow = 0
        
        while self.bfs(source, sink, parent):
            path_flow = float('Inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                self.flow[u][v] += path_flow  
                v = parent[v]
            
            max_flow += path_flow
        
        return max_flow
    
    def get_flows(self):
        return self.flow

if __name__ == "__main__":
    vertices = 20 + 2
    source = 0
    sink = vertices - 1

    graph = Graph(vertices)

    graph.add_edge(source, 1, 25)
    graph.add_edge(source, 2, 20)
    graph.add_edge(source, 3, 15)
    graph.add_edge(source, 4, 15)
    graph.add_edge(source, 5, 30)
    graph.add_edge(source, 2, 10)

    graph.add_edge(1, 6, 15)
    graph.add_edge(1, 7, 10)
    graph.add_edge(1, 8, 20)
    graph.add_edge(2, 9, 15)
    graph.add_edge(2, 10, 10)
    graph.add_edge(2, 11, 25)
    graph.add_edge(3, 12, 20)
    graph.add_edge(3, 13, 15)
    graph.add_edge(3, 14, 10)
    graph.add_edge(4, 15, 20)
    graph.add_edge(4, 16, 10)
    graph.add_edge(4, 17, 15)
    graph.add_edge(4, 18, 5)
    graph.add_edge(4, 19, 10)

    graph.add_edge(6, sink, 15)
    graph.add_edge(7, sink, 10)
    graph.add_edge(8, sink, 20)
    graph.add_edge(9, sink, 15)
    graph.add_edge(10, sink, 10)
    graph.add_edge(11, sink, 25)
    graph.add_edge(12, sink, 20)
    graph.add_edge(13, sink, 15)
    graph.add_edge(14, sink, 10)
    graph.add_edge(15, sink, 20)
    graph.add_edge(16, sink, 10)
    graph.add_edge(17, sink, 15)
    graph.add_edge(18, sink, 5)
    graph.add_edge(19, sink, 10)

    max_flow = graph.edmonds_karp(source, sink)
    print(f"Maximum flow: {max_flow}")

    flow_matrix = graph.get_flows()

    print("\nFlow Table:")
    print("Terminal\tStore\tActual Flow")
    for u in range(vertices):
        for v in range(vertices):
            if flow_matrix[u][v] > 0:
                if u == 1 or u == 2 or u == 3:
                    terminal = "Terminal 1"
                elif u == 4 or u == 5:
                    terminal = "Terminal 2"
                else:
                    continue

                if 6 <= v <= 19:
                    store = f"Store {v - 5}"
                    print(f"{terminal}\t{store}\t{flow_matrix[u][v]}")
