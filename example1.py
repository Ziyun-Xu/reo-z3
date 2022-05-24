from reo import *

c1 = Connector()

c1.connect('Timert(20)','A','C')
c1.connect('Fifo1','A','D')
c1.connect('Fifo1','C','E')
c1.connect('SyncDrain','D','E')
c1.connect('Sync','D','B')

result1, counterexample1, smt1 = c1.Deq(100,'A','B')
print(result1)
print(counterexample1)
result2, counterexample2, smt2 = c1.Tltt(100,20,'A','B')
print(result2)
print(counterexample2)