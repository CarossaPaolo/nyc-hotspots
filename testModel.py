import datetime

from model.model import Model

model = Model()

model.buildGraph(2, "AT&T")
print(model.getInfoGraph())

print('—'*30)

bestList, best = model.getMoreVicini()

print(f"Vertici con più vicini: (valore massimo: {best} | numero vertici: {len(bestList)})")
for n in bestList:
    print(n)

print('—'*30)

allNodes = model.getAllNodes()
nodoSelezionato = "Near Vine St and Columbia Heights"
print(f"nodo end: {nodoSelezionato}")

print("ricerca in corso...")
tik = datetime.datetime.now()
bestPath = model.findBestPath(nodoSelezionato, "50")
tok = datetime.datetime.now()
print(f"(tempo ricerca: {(tok - tik).microseconds}ms)")
if len(bestPath) == 0:
    print("Nesunn percorso trovato")
else:
    print("Percorso trovato")
    for i, n in enumerate(bestPath):
        print(f"({i+1}) {n}")