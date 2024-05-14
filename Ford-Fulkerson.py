from collections import defaultdict

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.ROW = len(graph)

    def BFS(self, s, t, parent):
        visited = [False] * (self.ROW)
        queue = [s]
        visited[s] = True
        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] is False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
        return True if visited[t] else False

    def FordFulkerson(self, source, sink):
        parent = [-1] * (self.ROW)
        max_flow = 0
        paths = []  # 用于存储水流路径（0——0）
        while self.BFS(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # 记录水流路径{*_*}
            path = []
            v = sink
            while v != source:
                path.append(v)
                v = parent[v]
            path.append(source)
            paths.append((path[::-1], path_flow))  # 将路径反转并存储 [--]!

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow, paths

def main(test_network, s, d):
    g = Graph(test_network)
    max_flow, paths = g.FordFulkerson(s, d)
    print(f"最大流：{max_flow}")
    for i, (path, flow) in enumerate(paths):
        print(f"router-{i+1}：{path} 流值：{flow}")

if __name__ == '__main__':
    test_network = [
        [0, 70, 100, 90, 0, 0],
        [0, 0, 0, 0, 0, 80],
        [0, 0, 0, 40, 70, 0],
        [0, 0, 0, 0, 40, 100],
        [0, 0, 0, 0, 0, 90],
        [0, 0, 0, 0, 0, 0],
    ]
    s = 0
    d = 5
    main(test_network, s, d)
