class Node:
    def __init__(self, name, arc_dict):
        self.name = name
        self.arc_dict = arc_dict


def create_node(name, next_list, flow_list):
    arc_dict = {}
    for i in range(len(next_list)):
        arc_dict[next_list[i]] = flow_list[i]
    return Node(name, arc_dict)


def Ford_Fulkerson_Solve(s, e, node_list, name_index_dict):
   
    routes = []
    while True:
        res = dfs(e, [s], None, node_list, name_index_dict)
        if res is None:
            return routes
        routes.append(res)
        route, flow = res
        for i in range(len(route) - 1):
            n1 = node_list[name_index_dict[route[i]]]
            n2 = node_list[name_index_dict[route[i + 1]]]
            if n2.name in n1.arc_dict.keys() and n1.arc_dict[n2.name] is not None:
                n1.arc_dict[n2.name] = n1.arc_dict[n2.name] - flow
            if n1.name in n2.arc_dict.keys() and n2.arc_dict[n1.name] is not None:
                n2.arc_dict[n1.name] = n2.arc_dict[n1.name] + flow


def dfs(e, cur_route, last_flow, node_list, name_index_dict):
   
    if cur_route[-1] == e:
        return cur_route, last_flow
    index = name_index_dict[cur_route[-1]]
    for next_node_name in node_list[index].arc_dict.keys():
        if next_node_name not in cur_route:
            flow = node_list[index].arc_dict[next_node_name]
            if flow is None or flow > 0:
                cur_route.append(next_node_name)
                res = dfs(e, cur_route, min_flow(last_flow, flow), node_list, name_index_dict)
                if res is not None:
                    return res
                cur_route.pop(-1)


def min_flow(f1, f2):
   
    if f1 is None:
        return f2
    elif f2 is None:
        return f1
    else:
        return min(f1, f2)


def main(network, source, destination):
    nn = len(network)  
    max_flow = 0  
    pred_node = [-1] * nn  

    while True:
        visited = [0] * nn
        queue = [source]
        visited[source] = 1

        while queue:
            node = queue.pop()
            for next_node, val in enumerate(network[node]):
                if visited[next_node] == 0 and val > 0:
                    queue.append(next_node)
                    visited[next_node] = 1
                    pred_node[next_node] = node

        if visited[destination] == 0:
            break

        flow = float('inf')
        node = destination
        while node != source:
            flow = min(flow, network[pred_node[node]][node])
            node = pred_node[node]
        max_flow += flow

        node = destination
        while node != source:
            network[node][pred_node[node]] += flow
            network[pred_node[node]][node] -= flow
            node = pred_node[node]
    return max_flow


if __name__ == '__main__':
    test_network = [
        [0, 70, 100, 90, 0, 0],
        [0, 0, 0, 0, 0, 80],
        [0, 0, 0, 40, 70, 0],
        [0, 0, 0, 0, 40, 100],
        [0, 0, 0, 0, 0, 50],
        [0, 0, 0, 0, 0, 0],
    ]
    s = 0
    d = 5

    # 构建节点网络
    node_list = []
    name_index_dict = {}
    for i in range(len(test_network)):
        node_list.append(create_node(str(i), [str(j) for j in range(len(test_network[i]))], test_network[i]))
        name_index_dict[str(i)] = i

    # 调用 Ford-Fulkerson 算法求解最大流
    max_flow = main(test_network, s, d)
    print(f"Max flow: {max_flow}")

    # 调用 Ford-Fulkerson-Solve 算法求解增广路径
    routes = Ford_Fulkerson_Solve(str(s), str(d), node_list, name_index_dict)
    for i, (route, flow) in enumerate(routes):
        print(f"Route-{i + 1}: {route} , flow: {flow}")
