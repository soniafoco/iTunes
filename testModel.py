from model.model import Model

m = Model()
m.buildGrafo(120)
nodes = m.getNodes()
m.getConnessa(m._idMap[141])
path, score = m.getSetAlbum(120000, m._idMap[141])

for p in path:
    print(p)

print(score)
