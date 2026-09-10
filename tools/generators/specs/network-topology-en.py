"""네트워크 토폴로지 (영문) — order-platform-en"""
from _bootstrap import N, E, Z, emit

# ── Network topology ──
zones = [Z(120,150,1000,600,'VPC 10.0.0.0/16'),
         Z(170,250,900,130,'Public subnets 10.0.1.0/24 · 10.0.2.0/24'),
         Z(170,470,900,240,'Private subnets 10.0.10.0/24 · 10.0.20.0/24')]
nodes = [
 N(490,40,230,80,'external','Internet'),
 N(220,275,220,80,'external','Internet Gateway'),
 N(620,275,220,80,'process','ALB'),
 N(880,275,170,80,'neutral','NAT'),
 N(220,500,220,90,'process','App Server (AZ-a)'),
 N(620,500,220,90,'process','App Server (AZ-c)'),
 N(420,620,300,80,'storage','RDS (Multi-AZ)'),
]
edges = [
 E([(600,120),(330,275)], None),
 E([(440,315),(620,315)], '443', ly=298),
 E([(700,355),(700,500)], '8080', lx=755, ly=430),
 E([(660,355),(360,500)], '8080', lx=430, ly=420),
 E([(330,590),(500,620)], '5432', lx=380, ly=612),
 E([(700,590),(650,620)], '5432', lx=790, ly=614),
 E([(840,545),(965,545),(965,355)], 'Outbound', dashed=True, lx=908, ly=532),
]
emit('order-platform-en', 'network-topology-en','Network topology',1180,830,'Network Topology',
     'Which subnet holds what, and over which ports they talk', nodes, edges, zones,
     ['Note: Inbound traffic from the internet reaches only as far as the ALB in the public subnet.',
      'App servers and RDS sit in private subnets, so nothing outside can connect to them directly; only outbound traffic passes through NAT.'],
     [], seed=802)
