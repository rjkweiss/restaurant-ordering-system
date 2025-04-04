from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

from app import app  # noqa: E402
from app.models import (  # noqa: E402
    Employee,
    Menu,
    MenuItem,
    MenuItemType,
    Order,
    Table,
    db,
)

with app.app_context():
    db.drop_all()
    db.create_all()

    # Employees
    alice = Employee(
        name='Alice Johnson',
        employee_number=101,
        hashed_password=generate_password_hash("alicepass")
    )
    bob = Employee(
        name='Bob Smith',
        employee_number=102,
        hashed_password=generate_password_hash('bobpass')
    )
    clara = Employee(
        name='Clara Lopez',
        employee_number=103,
        hashed_password=generate_password_hash('clarapass')
    )

    db.session.add_all([alice, bob, clara])

    # Tables -- capacity varies from 2 - 5
    tables = [Table(number=i, capacity=2 + (i % 4)) for i in range(1, 11)]
    db.session.add_all(tables)

    # Menu Item Types
    appetizers = MenuItemType(name="Appetizers")
    entrees = MenuItemType(name="Entrees")
    beverages = MenuItemType(name="Beverages")
    db.session.add_all([appetizers, entrees, beverages])

    # Menu and Items
    dinner = Menu(name="Dinner")

    # appetizers
    smoked_carrot_puree = MenuItem(
        name="Smoked Carrot Purée",
        description="citrus zest, chili oil",
        price=18,
        type=appetizers,
        menu=dinner
    )
    crispy_polenta_fries = MenuItem(
        name="Crispy Polenta Fries",
        description="garlic aioli",
        price=20,
        type=appetizers,
        menu=dinner
    )
    roasted_heirloom_veggies = MenuItem(
        name="Roasted Heirloom Veggies",
        description="sea salt, rosemary",
        price=21,
        type=appetizers,
        menu=dinner
    )
    baby_gem_salad = MenuItem(
        name="Baby Gem Salad",
        description="avocado, fennel, green goddess",
        price=19,
        type=appetizers,
        menu=dinner
    )
    miso_glazed_brussels = MenuItem(
        name="Miso Glazed Brussels",
        description="toasted sesame, scallion",
        price=22,
        type=appetizers,
        menu=dinner
    )
    grilled_housemade_focaccia = MenuItem(
        name="Grilled Housemade Focaccia",
        description="Rosemary, sea salt",
        price=17,
        type=appetizers,
        menu=dinner
    )

    # entrees
    wild_mushroom_risotto = MenuItem(
        name="Wild Mushroom Risotto",
        description="creamy arborio rice, porcini & truffle oil",
        price=28,
        type=entrees,
        menu=dinner
    )
    charred_cauliflower_steak = MenuItem(
        name="Charred Cauliflower Steak",
        description="romesco sauce, pistachio dukkah",
        price=26.75,
        type=entrees,
        menu=dinner
    )
    beet_wellington = MenuItem(
        name="Beet Wellington",
        description="golden pastry, root veg mash, red wine jus",
        price=36,
        type=entrees,
        menu=dinner
    )
    king_oyster_scallops = MenuItem(
        name="King Oyster Scallops",
        description="with saffron-coconut nage and crispy leeks",
        price=26,
        type=entrees,
        menu=dinner
    )
    stuffed_delicata_squash = MenuItem(
        name="Stuffed Delicata Squash",
        description="farro, cranberry, sage-almond drizzle",
        price=23,
        type=entrees,
        menu=dinner
    )
    tandoori_tofu_paneer = MenuItem(
        name="Tandoori Tofu Paneer",
        description="Ube sweet potato cake with curry",
        price=23,
        type=entrees,
        menu=dinner
    )

    # beverages
    summer_mocktail = MenuItem(
        name="Seasonal Summer Mocktail",
        description="red berries, lemonade, mint and cucumber",
        price=16,
        type=beverages,
        menu=dinner
    )
    housemade_kombucha = MenuItem(
        name="Housemade Kombucha",
        description="ginger-lime",
        price=16,
        type=beverages,
        menu=dinner
    )
    lavender_lemonade = MenuItem(
        name="Lavender Lemonade",
        description="sparkling or still",
        price=18,
        type=beverages,
        menu=dinner
    )
    matcha_oat_latte = MenuItem(
        name="Matcha Oat Latte",
        description="chilled",
        price=15,
        type=beverages,
        menu=dinner
    )
    hibiscus_cooler = MenuItem(
        name="Hibiscus cooler",
        description="spiced agave, citrus",
        price=13,
        type=beverages,
        menu=dinner
    )
    artisan_sparkling_water = MenuItem(
        name="Artisan Sparkling Water",
        description="cucumber-mint",
        price=17,
        type=beverages,
        menu=dinner
    )

    db.session.add(dinner)

    # Open order for Table 1
    open_order = Order(employee=alice, table=tables[0], finished=False)
    db.session.add(open_order)

    db.session.commit()
