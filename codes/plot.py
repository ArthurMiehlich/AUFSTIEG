import matplotlib.pyplot as plt
import networkx as nx
def plot_sol(Graph,x,drone_names):
    color_dict={}
    colors=['r', 'g', 'b', 'c']
    for ind, name in enumerate(drone_names):
        color_dict[name]=colors[ind]
    pos = nx.get_node_attributes(Graph, 'position')
    #nx.draw(Graph, pos, with_labels=True, node_size=80, node_color='skyblue', font_size=10, alpha=0.1)
    nx.draw_networkx_nodes(Graph, pos, node_size=80, node_color='skyblue')

    labels = {}
    for node, label in Graph.nodes(data=True):
        if node in ['Depot_s', 'Depot_t']:
            labels[node] = 'Depot'
        else:
            labels[node] = node

    nx.draw_networkx_labels(Graph, pos, labels, font_size=8)
    for (d,u,v) in x:
        if x[d,u,v]==1:
            nx.draw_networkx_edges(Graph,pos,[(u,v)],3, color_dict[d])
    legend_handles = [plt.Line2D([0], [0], color=color, lw=3, label=quadro) for quadro, color in color_dict.items()]
    plt.legend(handles=legend_handles, loc='best')
    plt.savefig('Solution.pdf')
    plt.show()
