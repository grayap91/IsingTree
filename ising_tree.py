# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 12:10:29 2018
Solve the Minimum Energy Configuration Problem on Trees in nlogn time.
Input is a ' ' separated file with no headers and 3 columns
of the form (u,v, weight). Where weight represents the weight of
the edge between u and v or of the node if u=v. If not specified
nodes are assumed to have 0 weight.
Output is the minimum energy value and an ordered sequence of
spins represented by '+' and '-'.
@author: Gautam
"""
import csv
import sys

class Node(object):
    def __init__(self, idn):
        self.idn = idn
        self.data = 0
        self.children = dict()
        self.parent = None
        self.parent_value=0
        self.energy = dict()
        self.values = dict()
    
    def add_child(self, key, val):
        self.children[key] = val
    
    def set_parent(self, val):
        self.parent = val
    
    def set_parent_value(self, val):
        self.parent_value = val
    
    def set_data(self, obj):
        self.data = obj
    

def read_csv_to_list(filename):
    out = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            if ''.join(row).strip():
                #deal with empty lines
                idn1 = int(row[0])
                idn2 = int(row[1])
                data = int(row[2])
                out.append((idn1,idn2,data))
    return out            
            
def construct_unrooted_tree(vals):
    my_dict = dict()
    for (u,v,data) in vals:
        node = None
        if u in my_dict:
            node = my_dict.get(u)
        else:
            node = Node(u)
        if u==v:
            node.set_data(data)
            my_dict[u] = node
        else:
            node2 = None
            if v in my_dict:
                node2 = my_dict.get(v)
            else:
                node2 = Node(v)
            node2.add_child(node, data)
            node.add_child(node2, data)
            my_dict[u] = node
            my_dict[v] = node2
    return my_dict
                

def construct_rooted_tree(my_dict):
    root_id = my_dict.keys()[0]
    root_node = my_dict.get(root_id)
    leaves = traverse_tree(root_node, [])
    compute_energy_by_state(root_node)
    out=get_min_configuration(root_node, dict(),1)
    return (root_node.energy[1], out)
    
def write_to_file(filename, energy, out):
    f = open(filename,'w+')
    f.write(str(energy))
    f.write('\n')
    for key in sorted(out.iterkeys()):
        val =''
        if(out[key]==1):
            val = '+'
        else:
            val = '-'
        f.write(val)
    f.close()
    


def get_min_configuration(root_node, out, pspin):
    val = root_node.values[pspin]
    out[root_node.idn] = val
    if not root_node.children:
        return out
    else:
        for child in root_node.children:
            temp = get_min_configuration(child, out, val)
            if temp:
                out.update(temp)
        return out    
    


def compute_energy_by_state(node):
    #compute energy by child state
    if not node.children:
        (node.energy[1],node.values[1]) = compute_min_energy(node,1)
        (node.energy[-1], node.values[-1]) = compute_min_energy(node,-1)
        return
        
    for child in node.children.keys():
        if not child.energy:
            compute_energy_by_state(child)
    (node.energy[1],node.values[1]) = compute_min_energy(node,1)
    (node.energy[-1],node.values[-1]) = compute_min_energy(node,-1)
        
def compute_min_energy(node,pspin):
    e1 = compute_energy(node,1,pspin)
    e2 = compute_energy(node,-1,pspin)
    if(e1<e2):
        return (e1,1)        
    else:
        return (e2,-1)
    

def compute_energy(node, spin, pspin):
    total = 0
    total += node.data*spin
    for child in node.children:
        total+=child.energy.get(spin)    
    total += node.parent_value*spin*pspin
    return total


def traverse_tree(root_node, leaves):
    for child in root_node.children.keys():
        child.set_parent(root_node)
        child.set_parent_value(child.children[root_node])
        child.children.pop(root_node)
        if not child.children:
            leaves.append(child)
        else:
            traverse_tree(child, leaves)
    return leaves
    
def main():
    # print command line arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    (energy, out) = construct_rooted_tree(construct_unrooted_tree(read_csv_to_list(input_file)))
    write_to_file(output_file, energy, out)
    #print sys.argv[1:]
    
if __name__ == "__main__":
    main()
