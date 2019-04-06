import bif_parser
import pydotplus
from bayesian.bbn import *

name = 'asia'
module_name = bif_parser.parse(name)
module = __import__(module_name)
bg = module.create_bbn()

# Initialization
s0 = bg.get_graphviz_source()
graph0 = pydotplus.graph_from_dot_data(s0)
graph0.write_png('temp0.png')

# Moralization
gu = make_undirected_copy(bg)
m1 = make_moralized_copy(gu, bg)
s1 = m1.get_graphviz_source()
graph1 = pydotplus.graph_from_dot_data(s1)
graph1.write_png('temp1.png')

# Triangulation
cliques, elimination_ordering = triangulate(m1, priority_func)
s2 = m1.get_graphviz_source()
graph2 = pydotplus.graph_from_dot_data(s2)
graph2.write_png('temp2.png')

# Query with Evidences
bg.query(xray='yes')
bg.query(asia='yes')

# Building the join tree
jt = bg.build_join_tree()
s3 = jt.get_graphviz_source()
graph2 = pydotplus.graph_from_dot_data(s3)
graph2.write_png('temp3.png')

# Initializing Potentials
assignments = jt.assign_clusters(bg)
jt.initialize_potentials(assignments, bg)

# Message Passing
jt.propagate()

cluster = {}

print '-------------------------------'
for group in ['asia', 'tub', 'lung', 'either', 'smoke', 'bronc', 'xray', 'dysp']:
  cluster[group] = [i for i in jt.clique_nodes for v in i.variable_names if v == group]
  pot = cluster[group][0].potential_tt
  sum_assignments = lambda imap, tup: sum([v for k, v in imap.iteritems() for i in k if i == tup])

  yes = no = 0
  for k, v in pot.iteritems():
    for i in k:
      if i[0] == group:
        if i[1] == 'yes':
          yes += v
        else:
          no += v
  if (yes + no) > 0:
    print group, 'YES:', yes / float(yes + no)
    print group, 'NO:',  no / float(yes + no)
    print '-------------------------------'
  else:
    print group, 'YES:', 0
    print group, 'NO:',  0
    print '-------------------------------'