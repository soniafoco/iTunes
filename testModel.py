from model.model import Model

myModel = Model()
myModel.buildGraph(120*60*1000)
print(myModel.getGraphDetails())

nodes = list(myModel._grafo.nodes)

print(myModel.getConnessaDetails(nodes[1]))

print(myModel.getSetAlbum(nodes[1], 80))

