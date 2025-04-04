from collections import defaultdict

from flask import Blueprint, render_template

from ..models import MenuItem

bp = Blueprint("public", __name__, url_prefix="")

@bp.route("/", methods=["GET"])
def menu_home():
    image_map = {
        "Smoked Carrot Purée": "/static/images/carrot-puree.jpg",
        "Crispy Polenta Fries": "/static/images/crispy-polenta-fries.jpg",
        "Heirloom Veggies": "/static/images/roasted-heirloom-veggies.jpg",
        "Baby Gem Salad": "/static/images/baby-gem-salad.jpg",
        "Miso Glazed Brussels": "/static/images/brussels-sprouts.jpg",
        "Housemade Focaccia": "/static/images/focaccia-bread.jpg",
        "Mushroom Risotto": "/static/images/wild-mushroom-risotto.jpg",
        "Cauliflower Steak": "/static/images/charred-cauliflower.jpg",
        "Beet Wellington": "/static/images/beet-wellington.jpg",
        "Oyster Scallops": "/static/images/king-oyster-mushroom-scallops.jpg",
        "Delicata Squash": "/static/images/delicata-squash.jpg",
        "Tandoori Tofu Paneer": "/static/images/tofu-tikka.jpg",
        "Summer Mocktail": "/static/images/seasonal-mocktail.jpg",
        "Housemade Kombucha": "/static/images/kombucha.jpg",
        "Lavender Lemonade": "/static/images/lavender-lemonade.jpg",
        "Matcha Latte": "/static/images/matcha-oat-latte.jpg",
        "Hibiscus cooler": "/static/images/hibiscus-cooler.jpg",
        "Sparkling Water": "/static/images/artisan-sparkling-water.jpg",
    }
    items_by_type = defaultdict(list)
    for item in MenuItem.query.all():
        items_by_type[item.type.name].append(item)

    return render_template("public/menu.html", items_by_type=items_by_type, image_map=image_map)
