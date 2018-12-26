# IsingTree
Solve the Minimum Energy Configuration Problem on Trees in nlogn time.
Input is a ' ' separated file with no headers and 3 columns
of the form (u,v, weight). Where weight represents the weight of
the edge between u and v or of the node if u=v. If not specified
nodes are assumed to have 0 weight.
Output is the minimum energy value and an ordered sequence of
spins represented by '+' and '-'.

Usage :

python ising_tree.py <input_filename> <output_filename>
