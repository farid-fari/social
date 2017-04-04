import threading
import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl
import scipy

mtpl.pyplot.cla()

n = 100
d = 3

people = list(range(n))

probas = scipy.linspace(0, 0.3, 100)
y = [0 for _ in range(100)]

def compute(q, p):
    global y
    sumoftries = 0
    for _ in range(1000):

        graph = nx.MultiDiGraph()
        graph.add_nodes_from(people, state=0, age=0, infections=0)
        graph.node[rand.randint(0, n - 1)]['state'] = 1

        for r in people:
            for j in people:
                if r != j and rand.random() < .1:
                    graph.add_edge(r, j, color=0)

        for _ in range(300):
            for node in [item for item in graph.nodes(data=True) if item[1]['state'] == 1]:
                if node[1]['age'] < d:
                    node[1]['age'] += 1
                    for other in graph[node[0]]:
                        if not graph.node[other]['state']:
                            if rand.random() < p:
                                graph.node[other]['state'] = 1
                                graph.node[other]['infections'] += 1
                else:
                    node[1]['state'] = 0
                    node[1]['age'] = 0

        sumoftries += sum([k[1]['infections'] for k in graph.nodes(data=True)])/n/300

    write.acquire()
    y[i] = sumoftries/1000
    print(q, y[q])
    write.release()

    amount.release()
    return True

amount = threading.BoundedSemaphore(value=6)
write = threading.Lock()

for i in range(100):
    amount.acquire()
    t = threading.Thread(target=compute, args=(i, probas[i]))
    t.start()

for i in range(6):
    amount.acquire()

deriv = [0] + [y[i+1]-y[i-1] for i in range(1, 99)] + [0]

mtpl.pyplot.plot(probas, y, color='r')
mtpl.pyplot.plot(probas, deriv, color='g')
mtpl.pyplot.grid()
mtpl.pyplot.show()