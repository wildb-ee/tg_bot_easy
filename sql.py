import sqlite3


conn = sqlite3.connect('my_base.db')
cursor = conn.cursor()


sql_inserts = """
-- Insert products into the product table with real names, placeholders from placehold.jp, and CURRENT_TIMESTAMP for created and updated fields
INSERT INTO product (name, description, price, image, created, updated)
VALUES
    ('Organic Avocado', 'Fresh and ripe organic avocado, perfect for salads and guacamole', 2.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Sparkling Lemonade', 'Refreshing lemonade with a sparkling twist, ideal for hot summer days', 3.49, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Artisanal Sourdough Bread', 'Handcrafted sourdough bread made with natural yeast, great for sandwiches and toasts', 4.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Single-Origin Coffee Beans', 'Premium coffee beans sourced from single origin, offering a rich and aromatic flavor profile', 12.79, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Organic Kale', 'Fresh and nutrient-rich organic kale, perfect for salads, smoothies, and stir-fries', 1.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Green Tea Matcha Powder', 'High-quality matcha powder with a vibrant green color and earthy flavor, ideal for making lattes and desserts', 9.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Wild-Caught Salmon Fillet', 'Fresh wild-caught salmon fillet, packed with omega-3 fatty acids and great for grilling or baking', 14.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Organic Coconut Water', 'Pure and hydrating organic coconut water, extracted from young coconuts for a refreshing taste', 3.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Quinoa & Chickpea Salad', 'Wholesome salad made with organic quinoa, chickpeas, fresh vegetables, and a tangy vinaigrette dressing', 7.49, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Cold-Pressed Juice Cleanse', 'Revitalize your body with a cleansing blend of cold-pressed juices made from organic fruits and vegetables', 29.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Artisanal Cheese Selection', 'Hand-selected artisanal cheeses from around the world, perfect for pairing with wine or charcuterie', 19.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Craft Beer Sampler Pack', 'Discover a variety of craft beers with this sampler pack, featuring unique flavors and styles from local breweries', 24.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Organic Mixed Berries', 'A delicious assortment of organic mixed berries, packed with antioxidants and perfect for smoothies or desserts', 6.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Gourmet Chocolate Truffles', 'Indulge in decadent gourmet chocolate truffles, handcrafted with premium cocoa and rich fillings', 11.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Farm Fresh Eggs', 'Farm-fresh eggs from pasture-raised hens, offering superior taste and nutritional benefits', 4.49, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Organic Herbal Tea Sampler', 'Explore a variety of organic herbal teas with this sampler pack, perfect for relaxation and wellness', 8.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Artisanal Pasta Collection', 'Elevate your pasta dishes with this collection of artisanal pastas, made with premium ingredients and traditional methods', 5.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Cold-Pressed Olive Oil', 'Pure and flavorful cold-pressed olive oil, extracted from select olives for a smooth and fruity taste', 9.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Handcrafted Ceramic Dinnerware Set', 'Add elegance to your table with this handcrafted ceramic dinnerware set, featuring unique designs and durable construction', 39.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Premium Steak Selection', 'Indulge in premium steaks with this selection of USDA Prime cuts, known for their exceptional tenderness and flavor', 29.99, 'https://placehold.jp/150x150.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


"""


cursor.executescript(sql_inserts)


conn.commit()


conn.close()