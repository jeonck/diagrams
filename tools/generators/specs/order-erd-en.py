"""Order domain ERD — order-platform-en"""
from _bootstrap import N, E, Z, emit

nodes = [
 N(60,110,200,126,'storage','Customer',kind='entity',attrs=['PK  customer_id','email','name']),
 N(370,110,200,148,'process','Order',kind='entity',attrs=['PK  order_id','FK  customer_id','ordered_at','status']),
 N(680,110,200,126,'process','Payment',kind='entity',attrs=['PK  payment_id','FK  order_id','amount']),
 N(370,390,200,148,'process','Order Item',kind='entity',attrs=['PK  order_item_id','FK  order_id','FK  product_id','quantity']),
 N(680,390,200,126,'storage','Product',kind='entity',attrs=['PK  product_id','name','unit_price']),
]
edges = [
 E([(260,173),(370,173)], head='many', start='one-s'),
 E([(570,173),(680,173)], head='one',  start='one-s'),
 E([(470,258),(470,390)], head='many', start='one-s'),
 E([(570,460),(680,460)], head='one',  start='many-s'),
 # legend — the crow's foot notation explained inside the picture
 E([(60,612),(120,612)], head='one'),
 E([(240,612),(300,612)], head='many'),
]
labels = [
 (315,166,'places','middle'),
 (625,166,'paid by','middle'),
 (482,330,'contains',None),
 (625,453,'refers to','middle'),
 (130,616,'1 (one)',None),
 (310,616,'N (many) — crow’s foot notation',None),
]
emit('order-platform-en', 'order-erd-en', 'Order Domain ERD', 940, 700, 'Order Domain ERD',
     'How a customer places an order, and the order branches into items and a payment',
     nodes, edges, (),
     ['Note: Teal is master data that stands on its own; indigo is data that only exists once a transaction happens.'],
     labels, seed=801)
