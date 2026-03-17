"""Mock tea product data generator."""

import json
from pathlib import Path
from typing import List, Dict


def generate_mock_products() -> List[Dict]:
    """Generate 50+ realistic tea products across 5 categories.

    Returns:
        List of product dictionaries
    """
    products = []

    # Green Tea (10 products)
    green_teas = [
        {
            "id": 1,
            "name": "Premium Sencha Green Tea",
            "description": "Authentic Japanese green tea with vibrant green color and fresh grassy aroma. Grown in the Shizuoka region, this first-flush sencha offers a perfect balance of umami and sweetness. Best brewed at 70-80°C for 1-2 minutes. Rich in antioxidants and L-theanine for calm focus.",
            "category_id": 1,
            "category_name": "Green Tea",
            "price_cents": 1899,
            "origin": "Japan",
            "flavor_notes": ["grassy", "umami", "sweet", "vegetal"]
        },
        {
            "id": 2,
            "name": "Organic Matcha Powder",
            "description": "Ceremonial grade matcha from Uji, Japan. Stone-ground tencha leaves produce a vibrant green powder with a smooth, creamy texture. Perfect for traditional tea ceremonies or modern lattes. High in chlorophyll and catechins. Whisk with 70°C water for best results.",
            "category_id": 1,
            "category_name": "Green Tea",
            "price_cents": 2899,
            "origin": "Japan",
            "flavor_notes": ["vegetal", "creamy", "sweet", "umami"]
        },
        {
            "id": 3,
            "name": "Dragon Well (Longjing) Green Tea",
            "description": "Legendary Chinese green tea from Hangzhou's West Lake region. Flat, jade-colored leaves produce a mellow, slightly sweet infusion with chestnut notes. Pan-fired processing gives it a distinctive toasted aroma. Steep at 75-80°C for 2-3 minutes.",
            "category_id": 1,
            "category_name": "Green Tea",
            "price_cents": 2499,
            "origin": "China",
            "flavor_notes": ["chestnut", "sweet", "mellow", "toasted"]
        },
        {
            "id": 4,
            "name": "Jasmine Green Tea Pearls",
            "description": "Hand-rolled green tea pearls scented with fresh jasmine blossoms. Each pearl unfurls into a beautiful leaf, releasing delicate floral aromas. Night-scenting process repeated 6 times for maximum fragrance. Refreshing and aromatic, perfect for afternoon tea.",
            "category_id": 1,
            "category_name": "Green Tea",
            "price_cents": 1699,
            "origin": "China",
            "flavor_notes": ["floral", "jasmine", "sweet", "aromatic"]
        },
        {
            "id": 5,
            "name": "Organic Gyokuro Green Tea",
            "description": "Premium shade-grown Japanese green tea with intense umami flavor. Covered for 20 days before harvest, increasing chlorophyll and amino acids. Deep green color with sweet, marine notes. The champagne of green teas. Brew at 50-60°C to preserve delicate flavors.",
            "category_id": 1,
            "category_name": "Green Tea",
            "price_cents": 3499,
            "origin": "Japan",
            "flavor_notes": ["umami", "sweet", "marine", "rich"]
        },
        {
            "id": 6,
            "name": "Moroccan Mint Green Tea",
            "description": "Refreshing blend of Chinese gunpowder green tea and spearmint leaves. Traditional North African tea blend, perfect served hot with sugar or iced. Crisp, minty flavor with a slight smokiness from the rolled tea leaves. Energizing and cooling.",
            "category_id": 1,
            "category_name": "Green Tea",
            "price_cents": 1299,
            "origin": "Morocco",
            "flavor_notes": ["minty", "refreshing", "crisp", "smoky"]
        },
        {
            "id": 7,
            "name": "Genmaicha Green Tea with Roasted Rice",
            "description": "Japanese green tea blended with toasted brown rice kernels. Nutty, popcorn-like aroma with a smooth, mellow flavor. Lower in caffeine than pure green tea. Perfect for all-day drinking. The rice adds a satisfying, comforting quality.",
            "category_id": 1,
            "category_name": "Green Tea",
            "price_cents": 1199,
            "origin": "Japan",
            "flavor_notes": ["nutty", "toasted", "mellow", "comforting"]
        },
        {
            "id": 8,
            "name": "Gunpowder Green Tea",
            "description": "Tightly rolled Chinese green tea resembling gunpowder pellets. Bold, slightly smoky flavor with a hint of pepper. Withstands multiple infusions without losing character. Strong and robust, excellent with mint. Traditionally served in Moroccan tea ceremonies.",
            "category_id": 1,
            "category_name": "Green Tea",
            "price_cents": 999,
            "origin": "China",
            "flavor_notes": ["bold", "smoky", "peppery", "robust"]
        },
        {
            "id": 9,
            "name": "Organic Spring Green Tea",
            "description": "First flush organic green tea from high mountain gardens. Tender young leaves picked in early spring for maximum freshness. Light, delicate flavor with natural sweetness. No bitterness even with longer steeping. Perfect introduction to green tea.",
            "category_id": 1,
            "category_name": "Green Tea",
            "price_cents": 1599,
            "origin": "China",
            "flavor_notes": ["delicate", "sweet", "fresh", "light"]
        },
        {
            "id": 10,
            "name": "White Peach Green Tea",
            "description": "Premium green tea blended with natural white peach essence and peach pieces. Fruity, aromatic infusion with a delicate sweetness. Perfect hot or iced. The peach complements the vegetal notes of green tea beautifully. A summer favorite.",
            "category_id": 1,
            "category_name": "Green Tea",
            "price_cents": 1399,
            "origin": "China",
            "flavor_notes": ["fruity", "peachy", "sweet", "aromatic"]
        }
    ]

    # Black Tea (12 products)
    black_teas = [
        {
            "id": 11,
            "name": "Earl Grey Black Tea",
            "description": "Classic black tea scented with oil of bergamot. Bold, malty base with bright citrus notes from Italian bergamot. Perfect with milk or lemon. A timeless British favorite, excellent for afternoon tea. Medium caffeine content for an energizing lift.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 1499,
            "origin": "India",
            "flavor_notes": ["citrus", "bergamot", "malty", "bold"]
        },
        {
            "id": 12,
            "name": "Assam Golden Tip Black Tea",
            "description": "Premium Assam tea with golden tips from the second flush harvest. Full-bodied, malty flavor with honey-like sweetness. Grown in India's Brahmaputra Valley. Excellent breakfast tea, robust enough to take milk and sugar. Rich in theaflavins.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 1799,
            "origin": "India",
            "flavor_notes": ["malty", "honey", "bold", "robust"]
        },
        {
            "id": 13,
            "name": "Ceylon Orange Pekoe Black Tea",
            "description": "High-grown Ceylon tea from Sri Lanka's mountain estates. Bright, crisp character with citrus notes. Medium-bodied with a clean finish. Brisk and refreshing, perfect plain or with a touch of honey. Classic afternoon tea.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 1399,
            "origin": "Sri Lanka",
            "flavor_notes": ["crisp", "citrus", "brisk", "clean"]
        },
        {
            "id": 14,
            "name": "English Breakfast Black Tea",
            "description": "Traditional blend of Assam, Ceylon, and Kenyan black teas. Full-bodied and robust, perfect for starting your day. Strong enough to take milk, yet flavorful on its own. The quintessential morning tea. High caffeine for energy and alertness.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 1299,
            "origin": "India",
            "flavor_notes": ["robust", "malty", "bold", "strong"]
        },
        {
            "id": 15,
            "name": "Darjeeling First Flush Black Tea",
            "description": "The 'Champagne of Teas' from India's Darjeeling region. Light, floral character with muscatel notes. Spring-harvested from high elevation gardens. Delicate and aromatic, best enjoyed without milk. A tea connoisseur's delight.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 2799,
            "origin": "India",
            "flavor_notes": ["floral", "muscatel", "delicate", "aromatic"]
        },
        {
            "id": 16,
            "name": "Lapsang Souchong Smoked Black Tea",
            "description": "Distinctive Chinese black tea smoke-dried over pinewood fires. Bold, smoky flavor reminiscent of a campfire. Unique and polarizing - you'll either love it or hate it. Pairs well with savory foods. A true adventure in a cup.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 1599,
            "origin": "China",
            "flavor_notes": ["smoky", "bold", "pine", "distinctive"]
        },
        {
            "id": 17,
            "name": "Chai Spice Black Tea",
            "description": "Robust Assam black tea blended with traditional Indian spices: cinnamon, cardamom, ginger, cloves, and black pepper. Warming and aromatic. Perfect with milk and honey for authentic masala chai. Spicy, sweet, and energizing.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 1399,
            "origin": "India",
            "flavor_notes": ["spicy", "warm", "aromatic", "bold"]
        },
        {
            "id": 18,
            "name": "Yunnan Golden Needle Black Tea",
            "description": "Premium Chinese black tea made entirely from golden buds. Smooth, malty flavor with honey and cocoa notes. Less astringent than typical black teas. Naturally sweet with a velvety texture. One of China's finest black teas.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 2199,
            "origin": "China",
            "flavor_notes": ["malty", "honey", "cocoa", "smooth"]
        },
        {
            "id": 19,
            "name": "Irish Breakfast Black Tea",
            "description": "Bold blend of Assam teas, stronger than English Breakfast. Malty, robust character perfect with milk. The traditional wake-up tea of Ireland. Full-bodied and energizing. Pairs excellently with a hearty breakfast.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 1299,
            "origin": "India",
            "flavor_notes": ["malty", "robust", "bold", "strong"]
        },
        {
            "id": 20,
            "name": "Russian Caravan Black Tea",
            "description": "Traditional blend of Chinese black teas with a slight smokiness. Reminiscent of the tea caravans that traveled the Silk Road. Smooth, malty base with subtle pine notes. Excellent with sweets or on its own.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 1599,
            "origin": "China",
            "flavor_notes": ["smoky", "malty", "smooth", "pine"]
        },
        {
            "id": 21,
            "name": "Vanilla Black Tea",
            "description": "Smooth black tea blended with natural vanilla flavoring. Sweet, creamy aroma with a comforting flavor. Perfect dessert tea or afternoon treat. Delicious with milk for a vanilla latte-like experience. Naturally caffeine-free option available.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 1299,
            "origin": "Sri Lanka",
            "flavor_notes": ["vanilla", "creamy", "sweet", "smooth"]
        },
        {
            "id": 22,
            "name": "Keemun Black Tea",
            "description": "Famous Chinese black tea known as the 'Burgundy of Teas'. Smooth, wine-like character with subtle orchid notes. Slightly sweet with no astringency. Perfect for evening drinking. Sophisticated and complex flavor profile.",
            "category_id": 2,
            "category_name": "Black Tea",
            "price_cents": 1899,
            "origin": "China",
            "flavor_notes": ["wine-like", "orchid", "smooth", "sweet"]
        }
    ]

    # Herbal Tea (10 products)
    herbal_teas = [
        {
            "id": 23,
            "name": "Chamomile Herbal Tea",
            "description": "Pure chamomile flowers for a calming, caffeine-free infusion. Gentle apple-like flavor with honey notes. Perfect before bedtime for relaxation. Known for soothing properties. Naturally sweet, no sugar needed. Traditionally used for centuries.",
            "category_id": 3,
            "category_name": "Herbal Tea",
            "price_cents": 1199,
            "origin": "Egypt",
            "flavor_notes": ["floral", "apple", "honey", "soothing"]
        },
        {
            "id": 24,
            "name": "Peppermint Herbal Tea",
            "description": "Refreshing pure peppermint leaves. Cool, menthol flavor that awakens the senses. Caffeine-free and naturally sweet. Excellent for digestion and breath freshening. Cooling in summer, warming in winter. Crisp and invigorating.",
            "category_id": 3,
            "category_name": "Herbal Tea",
            "price_cents": 999,
            "origin": "USA",
            "flavor_notes": ["minty", "cool", "refreshing", "crisp"]
        },
        {
            "id": 25,
            "name": "Rooibos Red Tea",
            "description": "South African red bush tea, naturally caffeine-free. Sweet, slightly nutty flavor with hints of vanilla and honey. Rich in antioxidants and minerals. Smooth and naturally sweet. Perfect any time of day. Great with milk.",
            "category_id": 3,
            "category_name": "Herbal Tea",
            "price_cents": 1299,
            "origin": "South Africa",
            "flavor_notes": ["nutty", "sweet", "vanilla", "smooth"]
        },
        {
            "id": 26,
            "name": "Lavender Herbal Tea",
            "description": "Delicate lavender buds for a floral, calming infusion. Aromatic and soothing with a subtle sweetness. Perfect for stress relief and relaxation. Caffeine-free for evening enjoyment. Often blended with chamomile for extra calm.",
            "category_id": 3,
            "category_name": "Herbal Tea",
            "price_cents": 1399,
            "origin": "France",
            "flavor_notes": ["floral", "lavender", "calming", "aromatic"]
        },
        {
            "id": 27,
            "name": "Ginger Turmeric Herbal Tea",
            "description": "Warming blend of ginger root and turmeric. Spicy, earthy flavor with anti-inflammatory properties. Caffeine-free wellness tea. Add honey and lemon for a soothing drink. Popular for immune support and digestion.",
            "category_id": 3,
            "category_name": "Herbal Tea",
            "price_cents": 1499,
            "origin": "India",
            "flavor_notes": ["spicy", "warming", "earthy", "zingy"]
        },
        {
            "id": 28,
            "name": "Hibiscus Berry Herbal Tea",
            "description": "Tart hibiscus flowers blended with berries. Bright red infusion with cranberry-like tartness. Rich in Vitamin C. Refreshing hot or iced. Naturally caffeine-free. Slightly sweet with a tangy finish.",
            "category_id": 3,
            "category_name": "Herbal Tea",
            "price_cents": 1199,
            "origin": "Egypt",
            "flavor_notes": ["tart", "berry", "tangy", "refreshing"]
        },
        {
            "id": 29,
            "name": "Lemon Balm Herbal Tea",
            "description": "Calming lemon balm leaves with a gentle citrus flavor. Traditionally used for relaxation and sleep support. Caffeine-free with a mild, pleasant taste. Slightly minty with lemon notes. Perfect evening tea.",
            "category_id": 3,
            "category_name": "Herbal Tea",
            "price_cents": 1299,
            "origin": "USA",
            "flavor_notes": ["citrus", "lemony", "calming", "mild"]
        },
        {
            "id": 30,
            "name": "Nettle Leaf Herbal Tea",
            "description": "Nutrient-rich nettle leaves for a earthy, grassy infusion. Packed with vitamins and minerals. Caffeine-free wellness tea. Mild, vegetal flavor. Traditionally used for seasonal support. Blends well with peppermint.",
            "category_id": 3,
            "category_name": "Herbal Tea",
            "price_cents": 1199,
            "origin": "Bulgaria",
            "flavor_notes": ["earthy", "grassy", "vegetal", "mild"]
        },
        {
            "id": 31,
            "name": "Liquorice Root Herbal Tea",
            "description": "Sweet liquorice root for a naturally sweet infusion. No sugar needed! Soothing for throat and digestion. Distinctive anise-like flavor. Caffeine-free. Often blended with peppermint or fennel. Not for high blood pressure.",
            "category_id": 3,
            "category_name": "Herbal Tea",
            "price_cents": 999,
            "origin": "Turkey",
            "flavor_notes": ["sweet", "anise", "soothing", "distinctive"]
        },
        {
            "id": 32,
            "name": "Passionflower Herbal Tea",
            "description": "Calming passionflower for relaxation and sleep support. Mild, slightly earthy flavor with floral notes. Caffeine-free evening tea. Traditionally used for stress relief. Gentle and soothing. Often combined with valerian root.",
            "category_id": 3,
            "category_name": "Herbal Tea",
            "price_cents": 1399,
            "origin": "Peru",
            "flavor_notes": ["floral", "earthy", "calming", "mild"]
        }
    ]

    # Oolong Tea (8 products)
    oolong_teas = [
        {
            "id": 33,
            "name": "Ti Kuan Yin (Iron Goddess) Oolong",
            "description": "Legendary Chinese oolong from Fujian province. Lightly oxidized for a floral, orchid-like aroma. Smooth, creamy texture with a sweet aftertaste. Multiple infusions reveal evolving flavors. One of China's most famous teas.",
            "category_id": 4,
            "category_name": "Oolong Tea",
            "price_cents": 2299,
            "origin": "China",
            "flavor_notes": ["floral", "orchid", "creamy", "sweet"]
        },
        {
            "id": 34,
            "name": "Taiwanese High Mountain Oolong",
            "description": "Premium oolong from Taiwan's high altitude tea gardens. Light oxidation preserves fresh, floral character. Buttery smooth with natural sweetness. Complex flavor profile that changes with each steep. A tea lover's treasure.",
            "category_id": 4,
            "category_name": "Oolong Tea",
            "price_cents": 2799,
            "origin": "Taiwan",
            "flavor_notes": ["floral", "buttery", "sweet", "complex"]
        },
        {
            "id": 35,
            "name": "Da Hong Pao (Big Red Robe) Oolong",
            "description": "Famous rock oolong from Wuyi Mountains. Deep, mineral-rich flavor with roasted notes. Heavily oxidized for a robust, complex character. Smooth with a lingering sweet aftertaste. Legendary status in Chinese tea culture.",
            "category_id": 4,
            "category_name": "Oolong Tea",
            "price_cents": 3299,
            "origin": "China",
            "flavor_notes": ["roasted", "mineral", "robust", "sweet"]
        },
        {
            "id": 36,
            "name": "Milk Oolong (Jin Xuan)",
            "description": "Taiwanese oolong with natural creamy, milky notes. No milk added - the flavor comes from the tea cultivar and processing. Smooth, buttery texture with a light orchid aroma. Sweet and satisfying. Perfect introduction to oolong.",
            "category_id": 4,
            "category_name": "Oolong Tea",
            "price_cents": 1999,
            "origin": "Taiwan",
            "flavor_notes": ["creamy", "milky", "buttery", "orchid"]
        },
        {
            "id": 37,
            "name": "Phoenix Dan Cong Oolong",
            "description": "Single-bush oolong from Guangdong province. Intensely aromatic with fruit and floral notes. Each bush produces unique flavors. Medium oxidation creates complexity. Honey orchid variety is most popular. Very fragrant.",
            "category_id": 4,
            "category_name": "Oolong Tea",
            "price_cents": 2599,
            "origin": "China",
            "flavor_notes": ["fruity", "floral", "honey", "aromatic"]
        },
        {
            "id": 38,
            "name": "Oriental Beauty Oolong",
            "description": "Unique Taiwanese oolong bitten by insects, creating honey-like sweetness. Heavily oxidized for a fruity, muscatel character. Beautiful multicolored leaves. Sweet and mellow. Also called Bai Hao or Champagne Oolong.",
            "category_id": 4,
            "category_name": "Oolong Tea",
            "price_cents": 2999,
            "origin": "Taiwan",
            "flavor_notes": ["honey", "fruity", "muscatel", "sweet"]
        },
        {
            "id": 39,
            "name": "Aged Oolong Tea",
            "description": "Traditionally roasted oolong aged for years. Deep, mellow flavor with toasted notes. Smooth and warming. Lower caffeine than fresh oolong. Complex and sophisticated. Prized for smooth, aged character.",
            "category_id": 4,
            "category_name": "Oolong Tea",
            "price_cents": 2499,
            "origin": "Taiwan",
            "flavor_notes": ["toasted", "mellow", "smooth", "aged"]
        },
        {
            "id": 40,
            "name": "Pouchong (Baozhong) Oolong",
            "description": "Lightly oxidized Taiwanese oolong, closest to green tea. Floral, delicate character with natural sweetness. Twisted leaf style. Refreshing and aromatic. Perfect for those new to oolong. Lower caffeine content.",
            "category_id": 4,
            "category_name": "Oolong Tea",
            "price_cents": 1799,
            "origin": "Taiwan",
            "flavor_notes": ["floral", "delicate", "sweet", "refreshing"]
        }
    ]

    # White Tea (10 products)
    white_teas = [
        {
            "id": 41,
            "name": "Silver Needle White Tea (Bai Hao Yin Zhen)",
            "description": "The king of white teas, made entirely from unopened buds covered in silver down. Delicate, naturally sweet flavor with subtle hay and melon notes. Minimal processing preserves maximum antioxidants. Rare and precious. Low caffeine.",
            "category_id": 5,
            "category_name": "White Tea",
            "price_cents": 3499,
            "origin": "China",
            "flavor_notes": ["delicate", "sweet", "hay", "melon"]
        },
        {
            "id": 42,
            "name": "White Peony (Bai Mu Dan) White Tea",
            "description": "Classic white tea made from buds and young leaves. More full-bodied than Silver Needle. Sweet, floral character with fruity notes. Golden-silver appearance. Smooth and naturally sweet. Perfect introduction to white tea.",
            "category_id": 5,
            "category_name": "White Tea",
            "price_cents": 1999,
            "origin": "China",
            "flavor_notes": ["floral", "sweet", "fruity", "smooth"]
        },
        {
            "id": 43,
            "name": "Organic White Tea",
            "description": "Certified organic white tea from Fujian province. Light, refreshing character with natural sweetness. Minimally processed for maximum health benefits. Delicate flavor perfect for all-day drinking. Rich in polyphenols and antioxidants.",
            "category_id": 5,
            "category_name": "White Tea",
            "price_cents": 2199,
            "origin": "China",
            "flavor_notes": ["light", "refreshing", "sweet", "delicate"]
        },
        {
            "id": 44,
            "name": "Moonlight White Tea",
            "description": "Yunnan white tea with striking black and white leaves. Sweet, honey-like flavor with fruity notes. Unique processing creates distinctive appearance. Smooth and mellow. Can be aged like pu-erh. Exotic and intriguing.",
            "category_id": 5,
            "category_name": "White Tea",
            "price_cents": 2399,
            "origin": "China",
            "flavor_notes": ["honey", "fruity", "smooth", "mellow"]
        },
        {
            "id": 45,
            "name": "Jasmine Silver Needle White Tea",
            "description": "Premium silver needle white tea scented with fresh jasmine blossoms. Delicate tea base perfectly complements floral jasmine. Sweet and aromatic. Multiple scenting creates intense fragrance. Luxurious and elegant.",
            "category_id": 5,
            "category_name": "White Tea",
            "price_cents": 2999,
            "origin": "China",
            "flavor_notes": ["jasmine", "floral", "sweet", "delicate"]
        },
        {
            "id": 46,
            "name": "Aged White Tea (Shou Mei)",
            "description": "Traditionally aged white tea for deeper flavor. Mellow, smooth character with earthy notes. Aged for 3+ years. Lower caffeine than fresh white tea. Soothing and contemplative. Prized for medicinal properties in China.",
            "category_id": 5,
            "category_name": "White Tea",
            "price_cents": 2199,
            "origin": "China",
            "flavor_notes": ["mellow", "earthy", "smooth", "aged"]
        },
        {
            "id": 47,
            "name": "White Tea with Berries",
            "description": "Delicate white tea blended with strawberries, blueberries, and raspberries. Naturally sweet and fruity. Light, refreshing infusion perfect hot or iced. Antioxidant-rich from both tea and berries. Low caffeine summer favorite.",
            "category_id": 5,
            "category_name": "White Tea",
            "price_cents": 1799,
            "origin": "China",
            "flavor_notes": ["berry", "sweet", "fruity", "refreshing"]
        },
        {
            "id": 48,
            "name": "Lemon White Tea",
            "description": "Light white tea with natural lemon flavor and lemon peel. Bright, citrusy character. Refreshing and uplifting. Perfect iced tea base. Low caffeine for all-day enjoyment. Natural Vitamin C boost.",
            "category_id": 5,
            "category_name": "White Tea",
            "price_cents": 1599,
            "origin": "China",
            "flavor_notes": ["citrus", "lemon", "refreshing", "bright"]
        },
        {
            "id": 49,
            "name": "White Coconut Cream Tea",
            "description": "Smooth white tea with coconut essence and vanilla. Creamy, tropical flavor. Naturally sweet without added sugar. Perfect dessert tea. Low caffeine. Delicious hot or iced with coconut milk.",
            "category_id": 5,
            "category_name": "White Tea",
            "price_cents": 1699,
            "origin": "China",
            "flavor_notes": ["coconut", "creamy", "vanilla", "tropical"]
        },
        {
            "id": 50,
            "name": "Pai Mu Tan Organic White Tea",
            "description": "Certified organic White Peony tea from sustainable gardens. Traditional processing preserves delicate flavor. Smooth, slightly sweet with floral notes. Clean and pure. Perfect for health-conscious tea lovers. Naturally low caffeine.",
            "category_id": 5,
            "category_name": "White Tea",
            "price_cents": 2299,
            "origin": "China",
            "flavor_notes": ["floral", "sweet", "smooth", "pure"]
        }
    ]

    # Combine all products
    products.extend(green_teas)
    products.extend(black_teas)
    products.extend(herbal_teas)
    products.extend(oolong_teas)
    products.extend(white_teas)

    return products


def load_mock_products() -> List[Dict]:
    """Load mock products from JSON file or generate if not exists.

    Returns:
        List of product dictionaries
    """
    json_path = Path(__file__).parent / "products.json"

    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Generate and save
        products = generate_mock_products()
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        return products


if __name__ == "__main__":
    # Generate and save products
    products = generate_mock_products()
    json_path = Path(__file__).parent / "products.json"

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(products)} products and saved to {json_path}")
    print(f"\nBreakdown by category:")
    from collections import Counter
    categories = Counter(p['category_name'] for p in products)
    for category, count in categories.items():
        print(f"  {category}: {count} products")
