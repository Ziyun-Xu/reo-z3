from z3 import *

timeout = Int('timeout')
off = Int('off')
reset = Int('reset')
expire = Int('expire')


def Conjunction(constraints):
    assert len(constraints) > 0

    result = None
    for c in constraints:
        if result is None:
            result = c
        else:
            result = And(result, c)

    return result

class Channel:
    @staticmethod
    def Sync(nodes, bound):
        assert len(nodes) == 2
        constraints = []
        for i in range(bound):
            constraints += [ nodes[0]['data'][i] == nodes[1]['data'][i] ]
            constraints += [ nodes[0]['time'][i] == nodes[1]['time'][i] ]

        return Conjunction(constraints)

    @staticmethod
    def Fifo1(nodes, bound):
        assert len(nodes) == 2
        constraints = []
        for i in range(bound):
            constraints += [ nodes[0]['data'][i] == nodes[1]['data'][i] ]
            constraints += [ nodes[0]['time'][i] <  nodes[1]['time'][i] ]
            if i != 0:
                constraints += [ nodes[0]['time'][i] > nodes[1]['time'][i-1] ]

        return Conjunction(constraints)

    @staticmethod
    def Fifo1e(e):
        def Fifo1eInstance(nodes, bound):
            assert len(nodes) == 2
            constraints = []
            constraints += [nodes[1]['data'][0] == e] 
            for i in range(bound-1):
                constraints += [nodes[0]['data'][i] == nodes[1]['data'][i + 1]]
                constraints += [nodes[0]['time'][i] < nodes[1]['time'][i + 1]]
            for i in range(bound):
                constraints += [nodes[0]['time'][i] > nodes[1]['time'][i]]

            return Conjunction(constraints)
        return Fifo1eInstance
        
    @staticmethod
    def SyncDrain(nodes, bound):
        assert len(nodes) == 2
        constraints = []
        for i in range(bound):
            constraints += [nodes[0]['time'][i] == nodes[1]['time'][i]]

        return Conjunction(constraints)
    
    @staticmethod
    def LossySync(nodes, bound, idx = 0, num = 0):
        assert len(nodes) == 2
        if bound == num:
            return True
        if bound == idx:
            return True
        constraints_0 = []
        constraints_1 = []
        constraints_0 += [ nodes[0]['time'][idx] < nodes[1]['time'][num]]
        constraints_1 += [ nodes[0]['data'][idx] == nodes[1]['data'][num]]
        constraints_1 += [ nodes[0]['time'][idx] == nodes[1]['time'][num]]
        return Or(And(Conjunction(constraints_0), Channel.LossySync(nodes, bound, idx + 1, num)),
                  And(Conjunction(constraints_1), Channel.LossySync(nodes, bound, idx + 1, num + 1)))
    
    @staticmethod
    def Timert(t):
        def TimertInstance(nodes,bound):
            assert len(nodes) == 2
            constraints = []
            for i in range(bound):
                constraints += [ nodes[0]['time'][i] + t ==  nodes[1]['time'][i] ]
                constraints += [ nodes[1]['data'][i] == timeout ]  
                if i != 0:
                    constraints += [ nodes[1]['time'][i-1] <= nodes[0]['time'][i] ]
            return Conjunction(constraints)
        return TimertInstance
        
    @staticmethod
    def OFFTimert(t):
        def OFFTimertInstance(nodes, bound, idx = 0, num = 0):
            assert len(nodes) == 2
            if idx == bound:
                return True
            if num == bound:
                return True
            if idx == bound-1:
                constraints_last = []
                constraints_last += [ nodes[0]['time'][idx] + t ==  nodes[1]['time'][num] ]
                constraints_last += [ nodes[1]['data'][num] == timeout ]  
                return Conjunction(constraints_last)
            else:
                constraints_0 = []
                constraints_1 = []
                constraints_0 += [ nodes[0]['data'][idx+1] == off ] 
                constraints_0 += [ nodes[0]['time'][idx+1] < nodes[0]['time'][idx] + t] 
                constraints_1 += [ nodes[0]['data'][idx+1] != off ]
                constraints_1 += [ nodes[0]['time'][idx] + t ==  nodes[1]['time'][num] ]
                constraints_1 += [ nodes[1]['data'][num] == timeout ]  
                if idx == 0 and num == 0:
                    constraints_all = []
                    for i in range(bound-1):
                        constraints_all += [ Or(nodes[0]['data'][i+1] == off , nodes[0]['time'][i+1] >= nodes[0]['time'][i] + t ) ]
                    return And(Or(And(Conjunction(constraints_0), Channel.OFFTimert(t)(nodes, bound, idx + 2, num)),
                              And(Conjunction(constraints_1), Channel.OFFTimert(t)(nodes, bound, idx + 1, num + 1))),
                               Conjunction(constraints_all))
                else:
                    return Or(And(Conjunction(constraints_0), Channel.OFFTimert(t)(nodes, bound, idx + 2, num)),
                              And(Conjunction(constraints_1), Channel.OFFTimert(t)(nodes, bound, idx + 1, num + 1)))
        return OFFTimertInstance
    
    @staticmethod
    def RSTTimert(t):
        def RSTTimertInstance(nodes, bound, idx = 0, num = 0):
            assert len(nodes) == 2
            if idx == bound:
                return True
            if num == bound:
                return True
            if idx == bound-1:
                constraints_last = []
                constraints_last += [ nodes[0]['time'][idx] + t ==  nodes[1]['time'][num] ]
                constraints_last += [ nodes[1]['data'][num] == timeout ]  
                return Conjunction(constraints_last)
            else:
                constraints_0 = []
                constraints_1 = []
                constraints_0 += [ nodes[0]['data'][idx+1] == reset ] 
                constraints_0 += [ nodes[0]['time'][idx+1] < nodes[0]['time'][idx] + t] 
                constraints_1 += [ nodes[0]['data'][idx+1] != reset ]
                constraints_1 += [ nodes[0]['time'][idx] + t ==  nodes[1]['time'][num] ]
                constraints_1 += [ nodes[1]['data'][num] == timeout ]  
                if idx == 0 and num == 0:
                    constraints_all = []
                    for i in range(bound-1):
                        constraints_all += [ Or(nodes[0]['data'][i+1] == reset , nodes[0]['time'][i+1] >= nodes[0]['time'][i] + t ) ]
                    return And(Or(And(Conjunction(constraints_0), Channel.RSTTimert(t)(nodes, bound, idx + 1, num)),
                              And(Conjunction(constraints_1), Channel.RSTTimert(t)(nodes, bound, idx + 1, num + 1))),
                               Conjunction(constraints_all))
                else:
                    return Or(And(Conjunction(constraints_0), Channel.RSTTimert(t)(nodes, bound, idx + 1, num)),
                              And(Conjunction(constraints_1), Channel.RSTTimert(t)(nodes, bound, idx + 1, num + 1)))
        return RSTTimertInstance
    
    
    @staticmethod
    def EXPTimert(t):
        def EXPTimertInstance(nodes, bound, idx = 0, num = 0):
            assert len(nodes) == 2
            if idx == bound:
                return True
            if num == bound:
                return True
            if idx == bound-1:
                constraints_last = []
                constraints_last += [ nodes[0]['time'][idx] + t ==  nodes[1]['time'][num] ]
                constraints_last += [ nodes[1]['data'][num] == timeout ]  
                return Conjunction(constraints_last)
            else:
                constraints_0 = []
                constraints_1 = []
                constraints_0 += [ nodes[0]['data'][idx+1] == expire ] 
                constraints_0 += [ nodes[0]['time'][idx+1] < nodes[0]['time'][idx] + t] 
                constraints_0 += [ nodes[1]['time'][num] == nodes[0]['time'][idx+1] ]
                constraints_0 += [ nodes[1]['data'][num] == timeout ]  
                constraints_1 += [ nodes[0]['data'][idx+1] != expire ]
                constraints_1 += [ nodes[0]['time'][idx] + t ==  nodes[1]['time'][num] ]
                constraints_1 += [ nodes[1]['data'][num] == timeout ]  
                if idx == 0 and num == 0:
                    constraints_all = []
                    for i in range(bound-1):
                        constraints_all += [ Or(nodes[0]['data'][i+1] == expire , nodes[0]['time'][i+1] >= nodes[0]['time'][i] + t ) ]
                    return And(Or(And(Conjunction(constraints_0), Channel.EXPTimert(t)(nodes, bound, idx + 1, num + 1)),
                              And(Conjunction(constraints_1), Channel.EXPTimert(t)(nodes, bound, idx + 1, num + 1))),
                               Conjunction(constraints_all))
                else:
                    return Or(And(Conjunction(constraints_0), Channel.EXPTimert(t)(nodes, bound, idx + 1, num + 1)),
                              And(Conjunction(constraints_1), Channel.EXPTimert(t)(nodes, bound, idx + 1, num + 1)))
        return EXPTimertInstance
    
    @staticmethod
    def Merger(nodes, bound, idx_1 = 0, idx_2 = 0):
        assert len(nodes) == 3
        if bound == idx_1 + idx_2:
            return True
        constraints_1 = []
        constraints_2 = []
        constraints_1 += [ nodes[0]['data'][idx_1] == nodes[2]['data'][idx_1 + idx_2]]
        constraints_1 += [ nodes[0]['time'][idx_1] == nodes[2]['time'][idx_1 + idx_2]]
        constraints_1 += [ nodes[0]['time'][idx_1] <  nodes[1]['time'][idx_2]]
        constraints_2 += [ nodes[1]['data'][idx_2] == nodes[2]['data'][idx_1 + idx_2]]
        constraints_2 += [ nodes[1]['time'][idx_2] == nodes[2]['time'][idx_1 + idx_2]]
        constraints_2 += [ nodes[1]['time'][idx_2] <  nodes[0]['time'][idx_1]]
        return Or(And(Conjunction(constraints_1), Channel.Merger(nodes, bound, idx_1 + 1, idx_2)),
                  And(Conjunction(constraints_2), Channel.Merger(nodes, bound, idx_1, idx_2 + 1)))
