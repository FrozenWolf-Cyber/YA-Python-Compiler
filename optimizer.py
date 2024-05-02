#!/usr/bin/env python
# coding: utf-8

# In[26]:


import os
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt


quads = open('quads.txt', 'r').readlines()
quads = [i.strip().split('\t') for i in quads]

start, end = 0, len(quads)
for idx, i in enumerate(quads):
    if '--All Quads--' in i[0]:
        start=idx
    if '------------------------------------' in i[0]:
        end = idx

quads = quads[start+1:end]



        
        
  
    
blocks = [[]]
next_block = [[]]

functions = {}

skip_f = False


idx = -1
returnto = []
labels = {}
mode="read" #read

# for i in quads:
#     print(i)

function_trig = []
# print("\n\nFLow graph")
while idx<len(quads):
    # print(idx, quads[idx])
    
    idx+=1
    if idx>=len(quads):
        break
    
    ith_quad = quads[idx]
    
    if 'BeginF' == ith_quad[1]:
        functions[ith_quad[2]] = idx
        skip_f = True
        
    if 'EndF' == ith_quad[1]:
        # print("Return to", returnto)
        if skip_f:
            skip_f = False
            continue
        else:
            idx = returnto.pop()
            blocks[-1].append(ith_quad)
            blocks.append([])
            continue
		
        
    if skip_f:
        continue
    
    
    if 'Label' == ith_quad[1]:
        if len(blocks[-1]) != 0:
            blocks.append([])
        labels[ith_quad[-1]] = len(blocks)-1
        
    if 'If False' == ith_quad[1]  or  'goto' == ith_quad[1]:
        blocks[-1].append(ith_quad)
        blocks.append([])
        continue
        
    blocks[-1].append(ith_quad)

    if 'Call' == ith_quad[1]:
        if ith_quad[2] not in function_trig:
            function_trig.append(ith_quad[2])
        else:
            continue
        if len(blocks[-1]) != 0:
            blocks.append([])
        returnto.append(idx)
        
        fname = ith_quad[2]
        blocks[-1].append(quads[functions[fname]])
        idx = functions[fname]
        
shift=0
for idx, block in enumerate(blocks):
    if len(block) == 0:
        blocks.pop(idx-shift)
        shift+=1


# In[27]:


blocks


# In[28]:


from pyvis.network import Network
plt.rcParams["figure.figsize"] = (28,28)
import networkx as nx

connections = []
edge = []
edge_labels = []
G = nx.DiGraph()
block_names = []
for idx, i in enumerate(blocks):
    # block_names.append(f"Block {idx}:\n"+'\n'.join([str(j) for j in i]))
    block_names.append(f"Block {idx}")
    G.add_node(block_names[-1])
    
for idx, (b_name, code_) in enumerate(zip(block_names, blocks)):
    if 'goto' in  code_[-1][1]:
        l = code_[-1][-1]
        G.add_edge(block_names[idx], block_names[labels[l]], label="goto")
        edge.append((block_names[idx], block_names[labels[l]]))
        edge_labels.append("goto")
        continue
    
    if 'If False' in code_[-1][1]:
        l = code_[-1][-1]
        G.add_edge(block_names[idx], block_names[labels[l]], label="If False")
        edge.append((block_names[idx], block_names[labels[l]]))
        edge_labels.append("If False")
        
    
    if idx+1<len(block_names):
        G.add_edge(block_names[idx], block_names[idx+1], label="next")
        edge.append((block_names[idx], block_names[idx+1]))
        edge_labels.append("next")




# for i, j in zip(block_names, blocks):
#     #pprint(i)
#     print("==============")
    
    
        


# In[29]:


# nx.draw_networkx(G, with_labels=True,  node_shape="s",  node_color="none", bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round'), font_size=10, alpha=1, width=2.)
pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
nx.draw_networkx_nodes(G, pos, node_size=20000, alpha=0.3,  node_shape="s")
# nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
# nx.draw_networkx_edges(G, pos, width=2)
# nx.draw_networkx_edge_labels(G, pos, font_size=10)

nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_edge_labels(G, pos, font_size=15)


# nx.draw_networkx(G, with_labels=True,  node_shape="s",  node_color="none", bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round'), font_size=10, alpha=1, width=2.)
#plt.show()


# In[30]:


from pyvis.network import Network
plt.rcParams["figure.figsize"] = (20,20)
import networkx as nx

connections = []
edge = []
edge_labels = []
G = nx.DiGraph()
block_names = []
for idx, i in enumerate(blocks):
    block_names.append(f"Block {idx}:\n"+'\n'.join([str(j) for j in i]))
    # block_names.append(f"Block {idx}")
    G.add_node(block_names[-1])
    
for idx, (b_name, code_) in enumerate(zip(block_names, blocks)):
    if 'goto' in  code_[-1][1]:
        l = code_[-1][-1]
        G.add_edge(block_names[idx], block_names[labels[l]], label="goto")
        edge.append((block_names[idx], block_names[labels[l]]))
        edge_labels.append("goto")
        continue
    
    if 'If False' in code_[-1][1]:
        l = code_[-1][-1]
        G.add_edge(block_names[idx], block_names[labels[l]], label="If False")
        edge.append((block_names[idx], block_names[labels[l]]))
        edge_labels.append("If False")
        
    
    if idx+1<len(block_names):
        G.add_edge(block_names[idx], block_names[idx+1], label="next")
        edge.append((block_names[idx], block_names[idx+1]))
        edge_labels.append("next")




# for i, j in zip(block_names, blocks):
#     #pprint(i)
#     print("==============")
    
    
        


# In[31]:


# nx.draw_networkx(G, with_labels=True,  node_shape="s",  node_color="none", bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round'), font_size=10, alpha=1, width=2.)
pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
nx.draw_networkx_nodes(G, pos, node_size=20000, alpha=0.3,  node_shape="s")
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_edge_labels(G, pos, font_size=12)

# nx.draw_networkx(G, with_labels=True,  node_shape="s",  node_color="none", bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round'), font_size=10, alpha=1, width=2.)
#plt.show()


# In[32]:


class ICG:
    def __init__(self, l) -> None:
        self.l = l
        self.lineno = l[0]
        self.op = l[1]
        l[2:] = [None if i=='-' else (i.strip() if i!=None else None) for i in l[2:]]
        self.op1 = l[2]
        self.op2 = l[3]
        self.result = l[4]
        
    def __repr__(self) -> str:
        return f"{self.l[0]}: {self.op}, {self.op1}, {self.op2}, {self.result}"
        

block1 = [ICG(i) for i in blocks[0]]


# In[33]:


blocks


# In[34]:


block1 = [ICG(i) for i in blocks[0]]
block1


# In[35]:


def plot_DAG(block1):
    nodes = []
    for i in block1:
            
        nodes.append(i.op1)
        nodes.append(i.op2)
        nodes.append(i.result)

    nodes = list(set(nodes))
    nodes.remove(None)
    # print(nodes)

    G = nx.DiGraph()

    for i in nodes:
        G.add_node(i)

    for i in block1:
        if i.result:
            
            if i.op == "goto":
                G.add_edge(i.result, i.result, label=i.op)
                continue
            
            if i.op1:
                G.add_edge(i.op1, i.result, label=i.op)
            if i.op2:
                G.add_edge(i.op2, i.result, label=i.op)
                
        elif i.op == 'Print':
            G.add_edge(i.op1, i.op, label=i.op)
            
                
    # nx.draw_networkx(G, with_labels=True,  node_shape="s",  node_color="none", bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round'), font_size=10, alpha=1, width=2.)
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    nx.draw_networkx_nodes(G, pos, node_size=5000, alpha=0.3,  node_shape="s")
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_edge_labels(G, pos, font_size=20)

    # nx.draw_networkx(G, with_labels=True,  node_shape="s",  node_color="none", bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round'), font_size=10, alpha=1, width=2.)
    #plt.show()
    
    
plot_DAG(block1)


# In[36]:


block1


# In[37]:


def check_str(a):
    return (a[0]=='"' and a[-1]=='"') or (a=='True' or a=='False')


def constant_propagation_replace(block1, idx, term, value):
	for i in range(idx, len(block1)):
		if block1[i].op1 == term:
			# print("Replacing", block1[i], "with", value)
			block1[i].op1 = value
		if block1[i].op2 == term:
			# print("Replacing", block1[i], "with", value)
			block1[i].op2 = value
   
		if block1[i].result == term: ## if term is result of any operation, then stop replacing
			break
   
	return block1




def constant_propagation(block1):
	for idx, i in enumerate(block1):
		if i.result !=None:
			if i.op2 == None and i.op1 is not None :
				if i.op1.isdigit() or check_str(i.op1):
					block1 = constant_propagation_replace(block1, idx+1, i.result, i.op1)
					continue

			elif i.op1 == None and i.op2 is not None:
				if i.op2.isdigit() or check_str(i.op2):
					block1 = constant_propagation_replace(block1, idx+1, i.result, i.op1)
					continue
	
			elif i.op1 == None and i.op2 == None:
				continue
	return block1



def constant_folding(block1):
	for idx, i in enumerate(block1):
		if i.op1 != None and i.op2 != None:
			if (i.op1.isdigit() or check_str(i.op1)) and (i.op2.isdigit() or check_str(i.op2)):
				# print("Constant folding", i)
				block1[idx] = ICG([i.lineno, "=", str(eval(f"{i.op1} {i.op} {i.op2}")), None, i.result])
    

	return block1


# In[38]:


block1 = constant_propagation(block1)
plot_DAG(block1)
block1 = constant_folding(block1)
# #pprint(block1)
plot_DAG(block1)


# In[39]:


def tot_repr(tot_icg):
	return '\n'.join(['\n'.join([j.__repr__() for j in i]) for i in tot_icg])


tot_icg = []
for i in blocks:
    tot_icg.append([ICG(j) for j in i])
    
from copy import deepcopy
before_copy = deepcopy(tot_icg)
while True:
	for i in range(len(tot_icg)):
		tot_icg[i] = constant_folding(tot_icg[i])
		tot_icg[i] = constant_propagation(tot_icg[i])
	
	#pprint(tot_icg)
	plot_DAG(tot_icg[0])
	
	if tot_repr(tot_icg) == tot_repr(before_copy):
		break

	before_copy = deepcopy(tot_icg)


# In[40]:


#pprint(tot_icg), plot_DAG(tot_icg[0])


# In[41]:


def deadcodeeliminations(blocks):
    in_use = {}
    for idx, block in enumerate(blocks):
        for idx_l, linel in enumerate(block):
            if linel.op1:
                if not linel.op1.isdigit() or (linel.op1[0]=='"' and linel.op1[-1]=='"'):
                    in_use[linel.op1] = True
            if linel.op2:
                if not linel.op2.isdigit() or (linel.op2[0]=='"' and linel.op2[-1]=='"'):
                    in_use[linel.op2] = True
                    
            if linel.result and linel.op == '=':
                if not linel.result.isdigit() or (linel.result[0]=='"' and linel.result[-1]=='"'):
                    in_use[linel.result] = False
                else:
                    continue
        blocks[idx] = block
        
    #pprint(in_use)
    for idx, block in enumerate(blocks):
        offset = 0
        for idx_l, linel in enumerate(block):
            if linel.op=="Label" or linel.op=="goto" or linel.op=="If False" or linel.op=="BeginF" or linel.op=="EndF":
                continue
            if linel.result:
                if linel.result in in_use:
                    if not in_use[linel.result]:
                        block.pop(idx_l-offset)
                        offset+=1
                    
    return blocks
       
before_copy = deepcopy(tot_icg)
while True:
    tot_icg = deadcodeeliminations(tot_icg)
    for i in range(len(tot_icg)):
        tot_icg[i] = constant_folding(tot_icg[i])
        tot_icg[i] = constant_propagation(tot_icg[i])
	
    if tot_repr(tot_icg) == tot_repr(before_copy):
        break
    else:
        before_copy = deepcopy(tot_icg)
        
    #pprint(tot_icg)
    plot_DAG(tot_icg[0])


# In[42]:


#pprint(tot_icg)


# In[43]:


for i in tot_icg:
	#pprint(i)
	plot_DAG(i)


# In[44]:


blocks


# In[45]:


#pprint(tot_icg)


# In[46]:


def remove_unreachable(tot_icg):
	reachable = {}
	for idx, block in enumerate(tot_icg):
		for idx_l, linel in enumerate(block):
			if linel.op == 'goto':
				reachable[linel.result] = True
			if linel.op == 'If False':
				reachable[linel.result] = True
    
	print(reachable)
	offset = 0
	for idx, block in enumerate(tot_icg):
		if block[0].op == 'Label':
			if block[-1].result not in reachable:
				tot_icg.pop(idx-offset)
				offset+=1
    
	return tot_icg

def peephole(tot_icg):
    
	tot_icg = remove_unreachable(tot_icg)
	for idx, block in enumerate(tot_icg):
		offset = 0
		for idx_l, linel in enumerate(block):
			if linel.op == 'If False':
				if linel.op1 in ['True', 'False']:
					if linel.op1 == 'False':
						block[idx_l] = ICG([linel.lineno, 'goto', linel.result, None, None])
					else:
						block.pop(idx_l-offset)
						offset+=1
      
	tot_icg = remove_unreachable(tot_icg)
			
	return tot_icg


# In[47]:


tot_icg = peephole(tot_icg)
tot_icg


# In[48]:


plt.rcParams["figure.figsize"] = (10,10)
for i in tot_icg:
	#pprint(i)
	plot_DAG(i)


# In[49]:


icg_tolist = []
for i in tot_icg:
	temp = []
	for j in i:
		temp.append([j.op, j.op1, j.op2, j.result])
		for _i in range(len(temp[-1])):
			if temp[-1][_i] == None:
				temp[-1][_i] = '-'
	icg_tolist.append(temp)
blocks = icg_tolist

blocks


# In[50]:


from pyvis.network import Network
plt.rcParams["figure.figsize"] = (10,10)
import networkx as nx

connections = []
edge = []
edge_labels = []
G = nx.DiGraph()
block_names = []
for idx, i in enumerate(blocks):
    block_names.append(f"Block {idx}:\n"+'\n'.join([str(j) for j in i]))
    # block_names.append(f"Block {idx}")
    G.add_node(block_names[-1])
    
for idx, (b_name, code_) in enumerate(zip(block_names, blocks)):
    if 'goto' in  code_[-1][1]:
        l = code_[-1][-1]
        G.add_edge(block_names[idx], block_names[labels[l]], label="goto")
        edge.append((block_names[idx], block_names[labels[l]]))
        edge_labels.append("goto")
        continue
    
    if 'If False' in code_[-1][1]:
        l = code_[-1][-1]
        G.add_edge(block_names[idx], block_names[labels[l]], label="If False")
        edge.append((block_names[idx], block_names[labels[l]]))
        edge_labels.append("If False")
        
    
    if idx+1<len(block_names):
        G.add_edge(block_names[idx], block_names[idx+1], label="next")
        edge.append((block_names[idx], block_names[idx+1]))
        edge_labels.append("next")




# for i, j in zip(block_names, blocks):
#     #pprint(i)
#     print("==============")
    

# nx.draw_networkx(G, with_labels=True,  node_shape="s",  node_color="none", bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round'), font_size=10, alpha=1, width=2.)
pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
nx.draw_networkx_nodes(G, pos, node_size=20000, alpha=0.3,  node_shape="s")
nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_edge_labels(G, pos, font_size=12)

# nx.draw_networkx(G, with_labels=True,  node_shape="s",  node_color="none", bbox=dict(facecolor="skyblue", edgecolor='black', boxstyle='round'), font_size=10, alpha=1, width=2.)
#plt.show()

print("-----------After all optimization: Code propagation, folding, peephole----------------");
for i in icg_tolist:
	for j in i:
		print('\t'.join(j))