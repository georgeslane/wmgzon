from website import database_table_names as db

# db.ProductPhysicalBook.add_physical_book("The Physicist", 12.99, "A philosophical novel about a shepherd named Santiago who travels from Spain to Egypt in search of a treasure.", "Book", 150, "https://m.media-amazon.com/images/I/81fiotccNCL._AC_UF894,1000_QL80_.jpg", "2023-07-10", 9.99, 700, 0.23, "Paulo Coelho", "Paperback", "The Alchemist follows Santiago, a young shepherd who dreams of finding treasure. Along the journey, he learns about life, love, and the importance of following one's dreams.", "Fiction, Philosophy", "English", "HarperOne", "25th Anniversary Edition", "9780062315007", False, 0, 0, "2020-05-04", "New", "Mass Market Paperback", 4, 600)
# db.Review.add_review(1, 1, "This book is great", "This is a life changing experience", 3, "2020-04-04")

print(db.ProductBookFunctions.view_similar_author(1))