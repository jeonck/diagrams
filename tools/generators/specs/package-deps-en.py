"""Package dependencies — order-platform-en"""
from _bootstrap import N, E, Z, emit

# ── packages ──
nodes = [
 N(380,130,300,90,'input','web',['Controllers · Views · DTOs']),
 N(380,290,300,90,'process','application',['Use cases · Transaction boundary']),
 N(380,450,300,90,'storage','domain',['Entities · Value objects · Ports']),
 N(760,290,280,90,'neutral','infrastructure',['JPA · External API adapters']),
]
edges = [
 E([(530,220),(530,290)], '«use»', dashed=True, head='open', lx=575, ly=260),
 E([(530,380),(530,450)], '«use»', dashed=True, head='open', lx=575, ly=420),
 E([(880,380),(690,470)], '«use»', dashed=True, head='open', lx=768, ly=398),
]
emit('order-platform-en', 'package-deps-en','Package Dependencies',1080,660,'Package Dependencies',
     'Which package is allowed to know about which',  nodes, edges, (),
     ['Note: an arrow means "this package knows about that one".',
      'The point is that no arrow leaves domain — the domain depends on nothing.'],
     [(700,505,'No outgoing dependencies',None)], seed=602)
