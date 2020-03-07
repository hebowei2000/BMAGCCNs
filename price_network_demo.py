#we will need some things from several places
from __future__ import division, absolute_import, print_function
import sys
if sys.version_info < (3,):
    range = xrange
import os
from pylab import * #for plotting
from numpy.random import * #for random sampling
seed(42)

# we need to import the graph_tool module itself
from graph_tool.all import *

#begin to construct a price network ( the one that exists before Barabasi). It is 
# a directed network., with preferential attachment. The algorithm below is very naive, and a bit slow, but quite simple.

####Initialization
  #we start with an empty, directed graph

g=Graph()

  # we want also to keep the age information for each vertex and edge. For that
  #Let's create some property maps
v_age = g.new_vertex_property("int")
e_age = g.new_edge_property("int")

   #the final size of the network
N = 100000

   #we have to start with one vertex
v = g.add_vertex()
v_age[v] = 0

   #we will keep a list of the vertices. The number of times is in this list will give the probability of it being selected
vlist = [v]
#########

#let's now add the new edges and vertices
for i in range(1,N):
        #create new vertex
        v = g.add_vertex()
        v_age[v] = i
        
        #we need to sample a new vertex to be the target, based on its in-degree +1 
        #For that, we simply randomly sample it from vlist
        i = randint(0,len(vlist))
        target = vlist[i]

        #add edge
        e = g.add_edge(v,target)
        e_age[e] = i

        #put v and target in the list
        vlist.append(target)
        vlist.append(v)
################

#########let's do a random walk on the graph and print the adge of the vertices we find, just for fun
v=g.vertex(randint(0,g.num_vertices()))
while True:
    print("vertex:",int(v),"in-degree:",v.in_degree(), "out-degree:",v.out_degree(),"age:",v_age[v])

    if v.out_degree() == 0:
        print("Nowwhere else to go... we found the main hub!")
        break

    n_list = []
    for w in v.out_neighbors():
        n_list.append(w)
    v = n_list[randint(0,len(n_list))]

#let's save our graph for posterity. we want to save the age properties as well...
# To do this, they must become "internal" properties:
g.vertex_properties["age"] = v_age
g.edge_properties["age"] = e_age

# now save it
g.save("price.xml.gz")


#lets's plot its in-degree distribution
in_hist = vertex_hist(g,"in")

y = in_hist[0]
err = sqrt(in_hist[0])
err[ err >=y ] = y[err>=y] - 1e-2

figure(figsize=(6,4))
errorbar(in_hist[1][:-1],in_hist[0],fmt="o",yerr=err,label="in")
gca().set_yscale("log")
gca().set_xscale("log")
gca().set_ylim(1e-1,1e5)
gca().set_xlim(0.8,1e3)
subplots_adjust(left=0.2,bottom=0.2)
xlabel("$k_{in}$")
ylabel("$NP(k_{in})$")
tight_layout()
savefig("price-dge-dist.pdf")
savefig("price-dge-dist.svg")

