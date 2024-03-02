from database_backend import database
from database_backend import website_functionality as wf

Product = database.ProductDatabase('TEST_PRODUCT')
ProductBook = database.ProductBookDatabase('TEST_PRODUCT', 'TEST_PRODUCT_BOOK')
ProductDigitalBook = database.ProductDigitalBookDatabase('TEST_PRODUCT', 'TEST_PRODUCT_BOOK', 'TEST_PRODUCT_DIGITAL_BOOK')
ProductPhysicalBook = database.ProductPhysicalBookDatabase('TEST_PRODUCT', 'TEST_PRODUCT_BOOK', 'TEST_PRODUCT_PHYSICAL_BOOK')
Account = database.AccountDatabase('TEST_ACCOUNT', 'TEST_PASSWORD')
Review = database.ReviewDatabase('TEST_REVIEW')
PaymentMethod = database.PaymentMethodDatabase('TEST_PAYMENT_METHOD')
DeliveryMethod = database.DeliveryMethodDatabase('TEST_DELIVERY_METHOD')
ProductList = database.ProductListDatabase('TEST_PRODUCT_LIST')
ProductListItems = database.ProductListItemsDatabase('TEST_PRODUCT_LIST_ITEMS')

ProductFunctions = wf.Product()
ReviewFunctions = wf.Review()
ProductBookFunctions = wf.ProductBook()
ProductListFunctions = wf.ProductList()
BasketFunctions = wf.Basket()
DeliveryMethodFunctions = wf.DeliveryMethod()
PaymentMethodFunctions = wf.PaymentMethod()
SearchFunctions = wf.Search()
AccountFunctions = wf.Account()
