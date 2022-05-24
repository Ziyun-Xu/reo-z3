from reo import *

c1 = Connector()

c1.connect('Sync','A','G')
c1.connect('LossySync','G','E')
c1.connect('LossySync','G','F')
c1.connect('Sync','E','I')
c1.connect('Sync','F','I')
c1.connect('SyncDrain','G','I')
c1.connect('Merger','E','F','I')
c1.connect('Sync','E','C')
c1.connect('Sync','F','D')
c1.connect('Timert(20)','C','C1')
c1.connect('Timert(20)','D','D1')
c1.connect('Merger','C1','D1','B')


result, counterexample, smt = c1.Teqt(10,20,'A','B')
print(result)
print(counterexample)