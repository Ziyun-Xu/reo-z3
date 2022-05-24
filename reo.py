from z3 import *
from channel import *
from lib import *

import sys

class Connector:
    def __init__(self):
        self.channels = []

    def connect(self, channel, *nodes):
        self.channels += [(channel, nodes)]
        return self
    
    def Deq(self, bound, *nodes):
        assert len(nodes) == 2
        nd_0 = nodes[0]
        nd_1 = nodes[1]
        allnodes = self.AllNodes()
        assert nd_0 in allnodes
        assert nd_1 in allnodes
        constr = True
        for i in range(bound):
            constr = And(constr,Int(nd_0 + '_d_' + str(i)) == Int(nd_1 + '_d_' + str(i)))
        
        solver = Solver()
        solver.add(Not(Implies(self.AllConstraints(bound), constr)))
        result = solver.check()
        
        # DEBUG USE
        if 'counterexample' in sys.argv and str(result) == 'sat':
            print(solver.model())

        if 'smt2' in sys.argv:
            print(solver.to_smt2())

        if str(result) == 'sat':
            return False, solver.model(), solver.to_smt2()
        else:
            return True, None, solver.to_smt2()
        pass     
    
    def Teq(self, bound, *nodes):
        assert len(nodes) == 2
        nd_0 = nodes[0]
        nd_1 = nodes[1]
        allnodes = self.AllNodes()
        assert nd_0 in allnodes
        assert nd_1 in allnodes
        constr = True
        for i in range(bound):
            constr = And(constr,Real(nd_0 + '_t_' + str(i)) == Real(nd_1 + '_t_' + str(i)))
        
        solver = Solver()
        solver.add(Not(Implies(self.AllConstraints(bound), constr)))
        result = solver.check()
        
        # DEBUG USE
        if 'counterexample' in sys.argv and str(result) == 'sat':
            print(solver.model())

        if 'smt2' in sys.argv:
            print(solver.to_smt2())

        if str(result) == 'sat':
            return False, solver.model(), solver.to_smt2()
        else:
            return True, None, solver.to_smt2()
        pass     
    
    def Tneq(self, bound, *nodes):
        assert len(nodes) == 2
        nd_0 = nodes[0]
        nd_1 = nodes[1]
        allnodes = self.AllNodes()
        assert nd_0 in allnodes
        assert nd_1 in allnodes
        constr = True
        for i in range(bound):
            constr = And(constr,Real(nd_0 + '_t_' + str(i)) != Real(nd_1 + '_t_' + str(i)))
        
        solver = Solver()
        solver.add(Not(Implies(self.AllConstraints(bound), constr)))
        result = solver.check()
        
        # DEBUG USE
        if 'counterexample' in sys.argv and str(result) == 'sat':
            print(solver.model())

        if 'smt2' in sys.argv:
            print(solver.to_smt2())

        if str(result) == 'sat':
            return False, solver.model(), solver.to_smt2()
        else:
            return True, None, solver.to_smt2()
        pass     
    
    def Tlt(self, bound, *nodes):
        assert len(nodes) == 2
        nd_0 = nodes[0]
        nd_1 = nodes[1]
        allnodes = self.AllNodes()
        assert nd_0 in allnodes
        assert nd_1 in allnodes
        constr = True
        for i in range(bound):
            constr = And(constr,Real(nd_0 + '_t_' + str(i)) < Real(nd_1 + '_t_' + str(i)))
        
        solver = Solver()
        solver.add(Not(Implies(self.AllConstraints(bound), constr)))
        result = solver.check()
        
        # DEBUG USE
        if 'counterexample' in sys.argv and str(result) == 'sat':
            print(solver.model())

        if 'smt2' in sys.argv:
            print(solver.to_smt2())

        if str(result) == 'sat':
            return False, solver.model(), solver.to_smt2()
        else:
            return True, None, solver.to_smt2()
        pass     
    
    def Tgt(self, bound, *nodes):
        assert len(nodes) == 2
        nd_0 = nodes[0]
        nd_1 = nodes[1]
        allnodes = self.AllNodes()
        assert nd_0 in allnodes
        assert nd_1 in allnodes
        constr = True
        for i in range(bound):
            constr = And(constr,Real(nd_0 + '_t_' + str(i)) > Real(nd_1 + '_t_' + str(i)))
        
        solver = Solver()
        solver.add(Not(Implies(self.AllConstraints(bound), constr)))
        result = solver.check()
        
        # DEBUG USE
        if 'counterexample' in sys.argv and str(result) == 'sat':
            print(solver.model())

        if 'smt2' in sys.argv:
            print(solver.to_smt2())

        if str(result) == 'sat':
            return False, solver.model(), solver.to_smt2()
        else:
            return True, None, solver.to_smt2()
        pass     
    
    def Teqt(self, bound, time, *nodes):
        assert len(nodes) == 2
        nd_0 = nodes[0]
        nd_1 = nodes[1]
        allnodes = self.AllNodes()
        assert nd_0 in allnodes
        assert nd_1 in allnodes
        constr = True
        for i in range(bound):
            constr = And(constr,Real(nd_0 + '_t_' + str(i)) + time == Real(nd_1 + '_t_' + str(i)))
        
        solver = Solver()
        solver.add(Not(Implies(self.AllConstraints(bound), constr)))
        result = solver.check()
        
        # DEBUG USE
        if 'counterexample' in sys.argv and str(result) == 'sat':
            print(solver.model())

        if 'smt2' in sys.argv:
            print(solver.to_smt2())

        if str(result) == 'sat':
            return False, solver.model(), solver.to_smt2()
        else:
            return True, None, solver.to_smt2()
        pass
        
    def Tltt(self, bound, time, *nodes):
        assert len(nodes) == 2
        nd_0 = nodes[0]
        nd_1 = nodes[1]
        allnodes = self.AllNodes()
        assert nd_0 in allnodes
        assert nd_1 in allnodes
        constr = True
        for i in range(bound):
            constr = And(constr,Real(nd_0 + '_t_' + str(i)) + time < Real(nd_1 + '_t_' + str(i)))
        
        solver = Solver()
        solver.add(Not(Implies(self.AllConstraints(bound), constr)))
        result = solver.check()
        
        # DEBUG USE
        if 'counterexample' in sys.argv and str(result) == 'sat':
            print(solver.model())

        if 'smt2' in sys.argv:
            print(solver.to_smt2())

        if str(result) == 'sat':
            return False, solver.model(), solver.to_smt2()
        else:
            return True, None, solver.to_smt2()
        pass
    
    def Tgtt(self, bound, time, *nodes):
        assert len(nodes) == 2
        nd_0 = nodes[0]
        nd_1 = nodes[1]
        allnodes = self.AllNodes()
        assert nd_0 in allnodes
        assert nd_1 in allnodes
        constr = True
        for i in range(bound):
            constr = And(constr,Real(nd_0 + '_t_' + str(i)) + time > Real(nd_1 + '_t_' + str(i)))
        
        solver = Solver()
        solver.add(Not(Implies(self.AllConstraints(bound), constr)))
        result = solver.check()
        
        # DEBUG USE
        if 'counterexample' in sys.argv and str(result) == 'sat':
            print(solver.model())

        if 'smt2' in sys.argv:
            print(solver.to_smt2())

        if str(result) == 'sat':
            return False, solver.model(), solver.to_smt2()
        else:
            return True, None, solver.to_smt2()
        pass
        
        
    def AllNodes(self):
        allnodes = []
        for chan in self.channels:
            for nd in chan[1]:
                if nd not in allnodes:
                    allnodes += [nd]
        return allnodes
    
    def AllConstraints(self,bound):
        nodes = {}
        allConstraints = None
        absGlobalConstr = None
        absTimeConstr = None
        
        for chan in self.channels:
            for nd in chan[1]:
                if nd not in nodes:
                    nodes[nd] = {
                        'time': [Real(nd + '_t_' + str(i)) for i in range(bound)],  
                        'data': [Int(nd + '_d_' + str(i)) for i in range(bound)]   
                        }
           
                    currTimeConstr = (nodes[nd]['time'][0] >= 0)
                    for i in range(bound - 1):
                        currTimeConstr = And(currTimeConstr, nodes[nd]['time'][i] < nodes[nd]['time'][i + 1])

                    if absTimeConstr is None:
                        absTimeConstr = currTimeConstr
                    else:
                        absTimeConstr = And(absTimeConstr, currTimeConstr)

            # generate constraint for channels
            channelDecl = eval('Channel.' + chan[0])
            paramnodes = list(map(lambda name: nodes[name], chan[1]))
            
            constr = channelDecl(paramnodes, bound)
            if absGlobalConstr is None:
                absGlobalConstr = constr
            else:
                absGlobalConstr = And(constr, absGlobalConstr)
        
        if absTimeConstr is not None:
            allConstraints = And(absTimeConstr, absGlobalConstr)
        else:
            allConstraints = absGlobalConstr
            
        return allConstraints


    