"""MVC structure — order-platform-en"""
from _bootstrap import N, E, Z, emit

nodes = [
 N(340,98,220,84,'input','User',['Browser · client']),
 N(70,306,240,104,'process','Controller',['Reads input · controls flow','Request routing · validation']),
 N(590,306,240,104,'external','View',['Presentation · rendering','Templates · screen layout']),
 N(330,522,240,104,'storage','Model',['Domain data · state','Business rules · persistence']),
]
edges = [
 E([(390,182),(190,306)]),
 E([(710,306),(510,182)]),
 E([(190,410),(390,522)]),
 E([(510,522),(710,410)]),
 E([(310,358),(590,358)], dashed=True),
]
# Arrow captions sit outside the lines; their alignment differs, so they are labels.
labels = [
 (250,246,'① User input · request','end'),
 (650,246,'④ Screen response',None),
 (270,490,'② State change request','end'),
 (630,490,'③ Notify change · read data',None),
 (450,348,'Pick view · trigger update','middle'),
]
emit('order-platform-en', 'mvc-structure-en', 'MVC Diagram', 900, 710,
     'MVC (Model–View–Controller) pattern',
     'A loop: user input → control → state change → screen refresh',
     nodes, edges, (),
     ['Note: the dashed line is the path that changes with the variant. In the Observer variant the',
      'Model notifies the View directly; in Passive View the Controller refreshes the View.'],
     labels, seed=501)
