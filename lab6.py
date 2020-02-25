import pyrtl

rf = pyrtl.MemBlock(bitwidth=32, addrwidth=5, name='mem')

instr = pyrtl.Input(bitwidth=32, name='instr')
alu_out = pyrtl.WireVector(bitwidth=16, name='alu_out')

def decoder(instr):
    op = instr[-6:]
    rs = instr[21:26]
    rt = instr[16:21]
    rd = instr[11:16]
    sh = instr[6:11]
    func = instr[0:6]
    return op, rs, rt, rd, sh, func

op = pyrtl.WireVector(bitwidth=6, name='op')
rs = pyrtl.WireVector(bitwidth=5, name='rs')
rt = pyrtl.WireVector(bitwidth=5, name='rt')
rd = pyrtl.WireVector(bitwidth=5, name='rd')
sh = pyrtl.WireVector(bitwidth=5, name='sh')
func = pyrtl.WireVector(bitwidth=6, name='func')

t_op, t_rs, t_rt, t_rd, t_sh, t_func = decoder(instr)
op <<= t_op
rs <<= t_rs
rt <<= t_rt
rd <<= t_rd
sh <<= t_sh
func <<= t_func

data0 = pyrtl.WireVector(bitwidth=16, name='data0')
data1 = pyrtl.WireVector(bitwidth=16, name='data1')

data0 <<= rf[rs]
data1 <<= rf[rt]
    
def alu (rs, rt, sh, func):
    # Operation 0: ADD
    op0 = rs + rt
    # Operation 1: SUB
    op1 = rs - rt
    # Operation 2: AND
    op2 = rs & rt
    # Operation 3: OR
    op3 = rs | rt
    # Operation 4: XOR
    op4 = rs ^ rt
    # Operation 5: SLL
    op5 = pyrtl.corecircuits.shift_left_logical(rt, sh)
    # Operation 6: SRA
    op6 = pyrtl.corecircuits.shift_right_arithmetic(rt, sh)
    # Operation 7: SLT
    with pyrtl.conditional_assignment:
        with rs < rt:
            op7 = 1
        with rs >= rt:
            op7 = 0
    
    alu_out = pyrtl.WireVector(bitwidth=16)
    # < add your code here >
    with pyrtl.conditional_assignment:
        with func==32:
            alu_out |= op0
        with func==34:
            alu_out |= op1
        with func==36:
            alu_out |= op2
        with func==37:
            alu_out |= op3
        with func==38:
            alu_out |= op4
        with func==0:
            alu_out |= op5
        with func==3:
            alu_out |= op6
        with func==42:
            alu_out |= op7
    return alu_out

temp_out = alu(data0, data1, sh, func)
alu_out <<= temp_out

rf[rd] <<= alu_out
"""
init_values = {addr: 9 for addr in range(0, 2**rf.addrwidth)}
memvals = {rf: init_values}

print("---------memories----------")
print(pyrtl.working_block())

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace, memory_value_map=memvals)

sim_trace.render_trace()
"""
