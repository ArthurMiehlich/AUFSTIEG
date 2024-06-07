import matplotlib.pyplot as plt
import networkx as nx
def plot_sol(Graph,x):
    colors={0:'r', 1:'g', 2:'b', 3:'c'}
    pos = nx.get_node_attributes(Graph, 'pos')
    #nx.draw(Graph, pos, with_labels=True, node_size=80, node_color='skyblue', font_size=10, alpha=0.1)
    nx.draw_networkx_nodes(Graph, pos, node_size=80, node_color='skyblue')
    nx.draw_networkx_labels(Graph, pos, font_size=8)
    for (d,u,v) in x:
        if x[d,u,v]==1:
            nx.draw_networkx_edges(Graph,pos,[(u,v)],3, colors[d])
    plt.show()
