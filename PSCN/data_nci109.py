import scipy.io as sio
import graph_tool
import graph_tool.draw

mutag = sio.loadmat('NCI109.mat')
data = mutag['NCI109']
label = mutag['lnci109']
f_text=open("NCI109/text.tx","w")
for i in range (len(label)):
    g = graph_tool.Graph()
    g.set_directed(False)
    #read data from .mat file
    node = list(data['n109'][0,i].item(0))[0]
    edge = list(data['e109'][0,i])[0].item(0)[0]
    #print(len(edge))
    #print(type(edge))
    #construct the graph
    g.add_vertex(len(node))

    vprop_name = g.new_vertex_property("string")
    g.vp.name = vprop_name
    vprop_value = g.new_vertex_property("init")
    g.vp.label = vprop_value

    for i in range(len(node)):
        g.vp.name[g.vertex(j)]="n"+str(j)
        g.vp.lable[g.vertex(j)]=node(j).item(0)

    for j in range(int(len(edeg))):
        if len(edge[j][0]) != 0:
            node_edge = list(edge[j][0][0])

            for k in range(len(node_edge)):
                g.add_edge(g.vertex(j),g.vertex(node_edge[k]-1))
    #eprop = g.new_edge_property("init")
    #g.edge.properties['weight'] = eprop
    # for j in range(len(edge)):
    #    g.edge_index(j).weight = edge[j][2]
    #print(g)
      file_name = "nci109_"+str(i)
      g.save("NCI109/"+file_name+".xml.gz")
      f_text.write(file_name + ".xml.gz" + " " +str(label[i].item(0)) + '\n')

    print(g)
    #f_text.close()
    _

