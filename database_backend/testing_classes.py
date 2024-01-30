from database_backend import backend_classes as bc, database as db

product = bc.Product('Curious Anise', 10, 'A happy bunny', 'Books', 1000, 'bdbbdhdh')

print(product.product_id)

print(db.ProductTable.get_record(3))

