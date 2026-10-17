import os
import shutil
from app.database import SessionLocal, Base, engine
from app.models import Product, OrderItem, User, Order, ChatMessage
from app.utils.redis_client import get_redis

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
FRONTEND_IMAGES = os.path.join(BASE_DIR, "..", "ecommerce_frontend", "public", "images")

os.makedirs(STATIC_DIR, exist_ok=True)

# Copy all images from frontend public/images to backend static folder
if os.path.exists(FRONTEND_IMAGES):
    for f in os.listdir(FRONTEND_IMAGES):
        src_path = os.path.join(FRONTEND_IMAGES, f)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, os.path.join(STATIC_DIR, f))
    print("Synchronized all UI images to backend static folder.")

NEW_PRODUCTS = [
    # ==========================================
    # 1. BOYS COLLECTION
    # ==========================================
    {
        "name": "Noir Minimalist Utility Overshirt & Trousers",
        "description": "Clean architectural utility with matte black hardware and articulated sleeves. Crafted from Japanese Cotton-Nylon Twill with an architectural boxy fit and tapered leg.",
        "price": 165.00,
        "stock": 45,
        "image_url": "/static/boys_arch1.jpg",
    },
    {
        "name": "Earthy Olive Waffle Knit Vest & Oxford",
        "description": "Tactile moss-stitch waffle knit layered over crisp poplin tailored shirting. Crafted from Chunky Merino Wool & Organic Cotton in a relaxed sleeveless crewneck layer.",
        "price": 120.00,
        "stock": 38,
        "image_url": "/static/boys_arch2.jpg",
    },
    {
        "name": "Tailored Terracotta Clay Blazer & Turtleneck",
        "description": "Natural roll notched lapels draped in warm terracotta earth pigment dye. Italian Wool-Silk Blend with Cupro Lining in a deconstructed single-breasted modern blazer.",
        "price": 220.00,
        "stock": 25,
        "image_url": "/static/boys_arch3.jpg",
    },
    {
        "name": "Oatmeal Chunky Waffle Knit Pullover",
        "description": "Ultra-soft waffle knit with thermal warmth retention and raw edge hems. Heavyweight 480 GSM Organic Ribbed Cotton with drop-shoulder relaxed casual silhouette.",
        "price": 135.00,
        "stock": 50,
        "image_url": "/static/boys_arch4.jpg",
    },
    {
        "name": "Milanese Charcoal Double-Faced Overcoat",
        "description": "Elongated architectural drape with hand-stitched lapels and mockneck inner. Double-Faced Virgin Wool Blend in a structured knee-length tailored overcoat.",
        "price": 245.00,
        "stock": 20,
        "image_url": "/static/boys_arch5.jpg",
    },

    # ==========================================
    # 2. GIRLS COLLECTION
    # ==========================================
    {
        "name": "Noir Enchanté High-Neck Gown",
        "description": "Regal mock neckline with architectural side drape. Structured French Wool Crepe column gown with high slit and elegant runway silhouette.",
        "price": 180.00,
        "stock": 30,
        "image_url": "/static/girls_model1.jpg",
    },
    {
        "name": "Midnight Silk Voluminous Gown",
        "description": "Dramatic flowing sweep with cross-pleated bodice. Duchess Satin Silk in a flared halter silhouette for evening galas and formal events.",
        "price": 165.00,
        "stock": 28,
        "image_url": "/static/girls_model2.jpg",
    },
    {
        "name": "Siren Slit Velvet Runway Gown",
        "description": "Signature off-shoulder corset with cascading train. Crushed Silk Velvet with off-shoulder high slit design and handcrafted interior boning.",
        "price": 220.00,
        "stock": 22,
        "image_url": "/static/girls_model3.jpg",
    },
    {
        "name": "Architectural Strapless Mini Dress",
        "description": "Asymmetric neckline fold with tailored interior corset. Bonded Italian Satin in a sculptural origami mini silhouette.",
        "price": 140.00,
        "stock": 35,
        "image_url": "/static/girls_model4.jpg",
    },
    {
        "name": "Monochrome Geometric Cutout Gown",
        "description": "Precision waist cutout with elongated fluted hem. Heavy Stretch Crepe in a long-sleeve fishtail gown crafted for contemporary black-tie occasions.",
        "price": 195.00,
        "stock": 24,
        "image_url": "/static/girls_model5.jpg",
    },

    # ==========================================
    # 3. KIDS COLLECTION
    # ==========================================
    {
        "name": "Royal Highland Merino Cable-Knit Pullover & Chinos",
        "description": "Heirloom cable-stitch detailing knit from hypoallergenic non-itch merino fibers for tender skin. 100% Extrafine Australian Merino Wool & Pima Twill with reinforced elbow patches.",
        "price": 145.00,
        "stock": 40,
        "image_url": "/static/kids_arch1.jpg",
    },
    {
        "name": "Heritage Hunter Green Quilted Barn Jacket & Corduroys",
        "description": "Timeless country-estate barn jacket lined with brushed organic tartan cotton for thermal comfort. Water-Repellent Micro-Diamond Quilt with Corduroy Collar and antique brass snaps.",
        "price": 185.00,
        "stock": 32,
        "image_url": "/static/kids_arch2.jpg",
    },
    {
        "name": "Petit Prince Double-Breasted Velvet Tailored Blazer",
        "description": "Lustrous hunter green silk velvet adorned with handcrafted crested heraldic gold buttons. Italian Silk-Velvet with satin peaked lapels and pure silk lining.",
        "price": 230.00,
        "stock": 18,
        "image_url": "/static/kids_arch3.jpg",
    },
    {
        "name": "Organic Oatmeal Cashmere-Blend Cardigan & Linen Set",
        "description": "Whisper-soft breathable knit offering temperature-regulating luxury for play and formal celebrations. 70% Organic Pima Cotton, 30% Grade-A Mongolian Cashmere with mother-of-pearl buttons.",
        "price": 160.00,
        "stock": 36,
        "image_url": "/static/kids_arch4.jpg",
    },
    {
        "name": "Mayfair Classic Wool Duffle Coat with Horn Toggles",
        "description": "Authentic British heritage wool outerwear equipped with genuine polished buffalo horn toggles. Double-faced melton wool with windproof storm shield.",
        "price": 210.00,
        "stock": 25,
        "image_url": "/static/kids_arch5.jpg",
    },

    # ==========================================
    # 4. ACCESSORIES COLLECTION
    # ==========================================
    {
        "name": "AeroTitanium Polarized Navigator Sunglasses",
        "description": "Ultra-lightweight 18g titanium construction with custom flex hinges and distortion-free glaucous lenses. Grade-5 Aerospace Titanium & Nylon Polyamide Optics with matte DLC finish.",
        "price": 285.00,
        "stock": 50,
        "image_url": "/static/acc_arch1.jpg",
    },
    {
        "name": "Saffiano Leather Grand Weekender Duffel",
        "description": "Cross-hatch scratch-resistant saffiano calfskin in slate-blue with reinforced base and detachable shoulder strap. Full-Grain Italian Saffiano Calfskin with solid palladium hardware.",
        "price": 420.00,
        "stock": 22,
        "image_url": "/static/acc_arch2.jpg",
    },
    {
        "name": "Aura Chronometer Royal Edition Ice-Blue Timepiece",
        "description": "Iconic octagonal bezel with micro-tapisserie ice-blue sunburst dial and exhibition sapphire caseback. 316L Surgical Stainless Steel, Sapphire Crystal, and Swiss Automatic movement.",
        "price": 680.00,
        "stock": 15,
        "image_url": "/static/acc_arch3.jpg",
    },
    {
        "name": "CarbonShield RFID Titanium Money Clip & Bifold",
        "description": "Ultra-slim 8mm profile combining bulletproof carbon weave with buttery Italian leather linings. Aerospace 3K Carbon Fiber with spring titanium money clip and RFID anti-skimming shield.",
        "price": 165.00,
        "stock": 60,
        "image_url": "/static/acc_arch4.jpg",
    },
    {
        "name": "Reversible Full-Grain Calfskin & Palladium Belt",
        "description": "Twist-and-turn reversible buckle mechanism transitioning seamlessly from boardroom to evening. Dual-sided French calfskin in glaucous blue & deep charcoal with polished palladium buckle.",
        "price": 195.00,
        "stock": 45,
        "image_url": "/static/acc_arch5.jpg",
    },

    # ==========================================
    # 5. BEAUTY COLLECTION
    # ==========================================
    {
        "name": "Velvet Crimson Matte Lipstick 103",
        "description": "Signature velvet crimson lipstick in sculpted ribbed gold casing. Pure Velvet Pigment with Camellia Oil and Shea Butter for 16-hour hydrating comfort-matte wear.",
        "price": 58.00,
        "stock": 75,
        "image_url": "/static/beauty_prod1.jpg",
    },
    {
        "name": "Golden Radiance 24K Cellular Serum",
        "description": "Ultra-concentrated restorative youth fluid in fluted crystal with golden dropper. Colloidal 24K Gold, Damask Rose, and Hyaluronic Acid for luminous cellular radiance.",
        "price": 135.00,
        "stock": 40,
        "image_url": "/static/beauty_prod2.jpg",
    },
    {
        "name": "Amber Glow Luxury Crystal Perfume",
        "description": "Faceted octagonal crystal bottle crowned with hand-engraved filigree gold. Rare Bulgarian Rose, Golden Amber, and White Camellia in a bespoke long-lasting pure perfume extract.",
        "price": 240.00,
        "stock": 25,
        "image_url": "/static/beauty_prod3.jpg",
    },
    {
        "name": "Rose Petal Sculpted Illuminating Powder",
        "description": "Intricately embossed rose petal powder set in lacquered black and polished gold vanity compact. Micro-milled pearl pigment and organic rosehip oil for a soft-focus candlelight glow.",
        "price": 78.00,
        "stock": 55,
        "image_url": "/static/beauty_prod4.jpg",
    },
    {
        "name": "Restorative Botanical Night Repair Cream",
        "description": "Whipped regenerating restorative balm housed in heavy frosted glass with solid gold lid. Marine Peptides, Botanical Squalane, and Wild Lavender with a sculpting gold spatula.",
        "price": 155.00,
        "stock": 35,
        "image_url": "/static/beauty_prod5.jpg",
    },

]

def seed_db():
    print("Ensuring all relational database tables exist...")
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as schema_err:
        print(f"Schema creation notice: {schema_err}")

    db = None
    try:
        db = SessionLocal()
        try:
            print("Cleaning up old order items...")
            db.query(OrderItem).delete()
            print("Removing all existing products from database...")
            db.query(Product).delete()
            db.commit()

            try:
                from sqlalchemy import text
                dialect = engine.dialect.name
                if dialect == "postgresql":
                    db.execute(text("ALTER SEQUENCE products_id_seq RESTART WITH 1;"))
                elif dialect == "sqlite":
                    db.execute(text("DELETE FROM sqlite_sequence WHERE name = 'products';"))
                db.commit()
            except Exception as seq_err:
                print(f"Sequence reset notice: {seq_err}")
                db.rollback()
        except Exception as cleanup_err:
            print(f"Notice during cleanup (safe to proceed): {cleanup_err}")
            db.rollback()

        print(f"Adding {len(NEW_PRODUCTS)} new products (Boys, Girls, Kids, Accessories, Beauty)...")
        for item in NEW_PRODUCTS:
            prod = Product(
                name=item["name"],
                description=item["description"],
                price=item["price"],
                stock=item["stock"],
                image_url=item["image_url"],
            )
            db.add(prod)
        db.commit()
        print(f"Successfully added all {len(NEW_PRODUCTS)} products to relational database!")

        # Seed essential accounts (synced from pgAdmin)
        USERS_TO_SEED = [
            {
                "email": "guntururohithsai@gmail.com",
                "hashed_password": "$2b$12$C6Wv5RzU8Jj7OBtdlMJU4.OTQr4uYyqX7gQjeGCz4lbD.ZKmhE7/C",
                "role": "admin",
            },
            {
                "email": "sanjay@gmail.com",
                "hashed_password": "$2b$12$rNomfd3X4ezLFzNv3Kxa0Oq2xeCQcbRZtzTPs77AFwCBGxOE.xwwG",
                "role": "customer",
            },
            {
                "email": "pardhu@gmail.com",
                "hashed_password": "$2b$12$l8ZijR2C8fGbcbZ9CZQT4.rB7nVKIYBcv2qbb76VKswZUNhIFkWOG",
                "role": "customer",
            },
            {
                "email": "revanth@gmail.com",
                "hashed_password": "$2b$12$rNomfd3X4ezLFzNv3Kxa0Oq2xeCQcbRZtzTPs77AFwCBGxOE.xwwG",
                "role": "customer",
            },
            {
                "email": "invoice_test@example.com",
                "hashed_password": "$2b$12$rNomfd3X4ezLFzNv3Kxa0Oq2xeCQcbRZtzTPs77AFwCBGxOE.xwwG",
                "role": "customer",
            },
        ]
        for u in USERS_TO_SEED:
            existing_user = db.query(User).filter(User.email == u["email"]).first()
            if not existing_user:
                new_u = User(
                    email=u["email"],
                    hashed_password=u["hashed_password"],
                    role=u["role"],
                )
                db.add(new_u)
            else:
                existing_user.role = u["role"]
        db.commit()
        print("Successfully synced user accounts from pgAdmin database!")

        # Seed the 7 Orders from pgAdmin
        ORDERS_TO_SEED = [
            {
                "user_email": "sanjay@gmail.com",
                "total_amount": 220.0,
                "status": "DELIVERED",
                "shipping_name": "Sanjay",
                "shipping_phone": "+91 9505368495",
                "shipping_address": "Main Bazaar Street, Brodipet",
                "shipping_city": "Guntur",
                "shipping_state": "Andhra Pradesh",
                "shipping_postal_code": "523187",
            },
            {
                "user_email": "sanjay@gmail.com",
                "total_amount": 680.0,
                "status": "PROCESSING",
                "shipping_name": "Sanjay",
                "shipping_phone": "+91 9505368495",
                "shipping_address": "Main Bazaar Street, Brodipet",
                "shipping_city": "Guntur",
                "shipping_state": "Andhra Pradesh",
                "shipping_postal_code": "523187",
            },
            {
                "user_email": "pardhu@gmail.com",
                "total_amount": 220.0,
                "status": "SHIPPED",
                "shipping_name": "Pardhu",
                "shipping_phone": "+91 9391135099",
                "shipping_address": "Old Club Road, Kothapet",
                "shipping_city": "Guntur",
                "shipping_state": "Andhra Pradesh",
                "shipping_postal_code": "523187",
            },
            {
                "user_email": "revanth@gmail.com",
                "total_amount": 230.0,
                "status": "CANCELLED",
                "shipping_name": "Revanth",
                "shipping_phone": "+91 9876543210",
                "shipping_address": "Plot 42, Jubilee Hills",
                "shipping_city": "Hyderabad",
                "shipping_state": "Telangana",
                "shipping_postal_code": "500081",
            },
            {
                "user_email": "sanjay@gmail.com",
                "total_amount": 330.0,
                "status": "PENDING",
                "shipping_name": "Sanjay Client",
                "shipping_phone": "+1 555-0199",
                "shipping_address": "450 Fashion Avenue, Suite 12B",
                "shipping_city": "New York",
                "shipping_state": "NY",
                "shipping_postal_code": "10001",
            },
            {
                "user_email": "invoice_test@example.com",
                "total_amount": 1299.99,
                "status": "PROCESSING",
                "shipping_name": "John Doe",
                "shipping_phone": "555-123-4567",
                "shipping_address": "123 Silicon Way",
                "shipping_city": "San Francisco",
                "shipping_state": "CA",
                "shipping_postal_code": "94105",
            },
            {
                "user_email": "invoice_test@example.com",
                "total_amount": 1299.99,
                "status": "PROCESSING",
                "shipping_name": "John Doe",
                "shipping_phone": "555-123-4567",
                "shipping_address": "123 Silicon Way",
                "shipping_city": "San Francisco",
                "shipping_state": "CA",
                "shipping_postal_code": "94105",
            },
        ]

        if db.query(Order).count() == 0:
            for ord_data in ORDERS_TO_SEED:
                target_user = db.query(User).filter(User.email == ord_data["user_email"]).first()
                if not target_user:
                    target_user = db.query(User).first()
                if target_user:
                    new_order = Order(
                        user_id=target_user.id,
                        total_amount=ord_data["total_amount"],
                        status=ord_data["status"],
                        shipping_name=ord_data["shipping_name"],
                        shipping_phone=ord_data["shipping_phone"],
                        shipping_address=ord_data["shipping_address"],
                        shipping_city=ord_data["shipping_city"],
                        shipping_state=ord_data["shipping_state"],
                        shipping_postal_code=ord_data["shipping_postal_code"],
                    )
                    db.add(new_order)
            db.commit()
            print("Successfully synced all 7 orders from pgAdmin into database!")

        # Seed Chat Messages from pgAdmin
        CHAT_MESSAGES_TO_SEED = [
            {'sender_email': 'sanjay@gmail.com', 'recipient_email': 'guntururohithsai@gmail.com', 'order_idx': 0, 'message': 'Hello, could you please confirm the delivery status for my Tailored Terracotta Clay Blazer?'},
            {'sender_email': 'guntururohithsai@gmail.com', 'recipient_email': 'sanjay@gmail.com', 'order_idx': 0, 'message': 'Hello Sanjay, your order has been dispatched via Express courier and is out for delivery today.'},
            {'sender_email': 'sanjay@gmail.com', 'recipient_email': 'guntururohithsai@gmail.com', 'order_idx': 0, 'message': 'Received in exquisite condition. The wool-silk texture and lapel tailoring are outstanding. Thank you!'},
            {'sender_email': 'guntururohithsai@gmail.com', 'recipient_email': 'sanjay@gmail.com', 'order_idx': 0, 'message': "You are very welcome, Sanjay! It's a pleasure having you with us. Enjoy your bespoke atelier piece."},
            {'sender_email': 'sanjay@gmail.com', 'recipient_email': 'guntururohithsai@gmail.com', 'order_idx': 1, 'message': 'Hi team, I just placed an order for the Aura Chronometer Ice-Blue Timepiece. Does it include the 5-year atelier warranty card?'},
            {'sender_email': 'guntururohithsai@gmail.com', 'recipient_email': 'sanjay@gmail.com', 'order_idx': 1, 'message': 'Yes, absolutely! The timepiece arrives with the official international warranty card, exhibition caseback certificate, and wooden presentation box.'},
            {'sender_email': 'sanjay@gmail.com', 'recipient_email': 'guntururohithsai@gmail.com', 'order_idx': 1, 'message': 'Wonderful, looking forward to receiving it!'},
            {'sender_email': 'pardhu@gmail.com', 'recipient_email': 'guntururohithsai@gmail.com', 'order_idx': 2, 'message': 'Hello, regarding my Siren Slit Velvet Runway Gown: is the internal corset adjustable?'},
            {'sender_email': 'guntururohithsai@gmail.com', 'recipient_email': 'pardhu@gmail.com', 'order_idx': 2, 'message': 'Hello Pardhu, yes, the handcrafted interior boning includes a dual-tier hook enclosure for a customized silhouette.'},
            {'sender_email': 'pardhu@gmail.com', 'recipient_email': 'guntururohithsai@gmail.com', 'order_idx': 2, 'message': 'Perfect, thank you for the prompt assistance!'},
            {'sender_email': 'guntururohithsai@gmail.com', 'recipient_email': 'pardhu@gmail.com', 'order_idx': 2, 'message': 'it takes sometime have a little patience'},
            {'sender_email': 'sanjay@gmail.com', 'recipient_email': 'guntururohithsai@gmail.com', 'order_idx': None, 'message': 'Hello Concierge, I need assistance with my luxury order.'},
            {'sender_email': 'guntururohithsai@gmail.com', 'recipient_email': 'pardhu@gmail.com', 'order_idx': 2, 'message': 'your order will be sent tommorow'},
            {'sender_email': 'pardhu@gmail.com', 'recipient_email': 'guntururohithsai@gmail.com', 'order_idx': None, 'message': 'ok'},
            {'sender_email': 'pardhu@gmail.com', 'recipient_email': 'guntururohithsai@gmail.com', 'order_idx': 2, 'message': 'ok'},
            {'sender_email': 'guntururohithsai@gmail.com', 'recipient_email': 'pardhu@gmail.com', 'order_idx': 2, 'message': 'done'},
        ]

        if db.query(ChatMessage).count() == 0:
            all_orders = db.query(Order).order_by(Order.id.asc()).all()
            for msg_item in CHAT_MESSAGES_TO_SEED:
                sender = db.query(User).filter(User.email == msg_item['sender_email']).first()
                recipient = db.query(User).filter(User.email == msg_item['recipient_email']).first()
                if sender and recipient:
                    target_order_id = None
                    if msg_item['order_idx'] is not None and len(all_orders) > msg_item['order_idx']:
                        target_order_id = all_orders[msg_item['order_idx']].id
                    chat_msg = ChatMessage(
                        sender_id=sender.id,
                        recipient_id=recipient.id,
                        order_id=target_order_id,
                        message=msg_item['message']
                    )
                    db.add(chat_msg)
            db.commit()
            print("Successfully synced all 16 live support chat messages!")

        # Clear Redis cache
        try:
            r = get_redis()
            keys = r.keys("products:*")
            if keys:
                r.delete(*keys)
            r.delete("products:all")
            print("Successfully cleared Redis product cache.")
        except Exception as err:
            print(f"Redis cache clear notice: {err}")

        # Sync ChromaDB Vector Store
        try:
            from app.ai.rag_service import rag_service, COLLECTION_NAME
            try:
                rag_service.client.delete_collection(COLLECTION_NAME)
            except Exception:
                pass
            rag_service.collection = rag_service.client.get_or_create_collection(
                name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
            )
            synced_count = rag_service.sync_all_products(db)
            print(f"Successfully indexed {synced_count} products into ChromaDB Vector Search!")
        except Exception as err:
            print(f"ChromaDB sync notice: {err}")

    except Exception as e:
        if db is not None:
            db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        if db is not None:
            db.close()

if __name__ == "__main__":
    seed_db()
