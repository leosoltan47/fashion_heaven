from itertools import repeat
from random import choices, choice, randint
from faker import Faker
from pages.models import (
    Categories,
    ProductDetails,
    ProductImages,
    Products,
    Color,
    Features,
)


def main():
    fk = Faker()

    colors = [Color.objects.create(color_code=fk.hex_color()) for _ in repeat(None, 20)]
    features = [Features.objects.create(name=fk.first_name()) for _ in repeat(None, 20)]
    categories = [
        Categories.objects.create(name=fk.unique.first_name()) for _ in repeat(None, 20)
    ]
    products = [
        Products.objects.create(
            name=fk.name(),
            category=choice(categories),
            price_in_dollars=randint(0, 500) / float(randint(1, 300)),
            description=fk.text(),
            gender_and_age=choice(["W", "M", "K", "U", "B", "G"]),
        )
        for _ in repeat(None, 100)
    ]
    for product in products:
        pick = choices(features, k=2)
        product.feature.add(pick[0])
        product.feature.add(pick[1])

    product_details = [
        ProductDetails.objects.create(
            size=choice(["M", "L", "XL", "XXL"]),
            stock=randint(1, 100),
            product=products[i % len(products)],
        )
        for i in range(200)
    ]
    images = [
        ProductImages.objects.create(
            content="./media/Screenshot_From_2025-04-28_01-42-12.png",
            product_detail=product_details[i % len(product_details)],
        )
        for i in range(400)
    ]
    for image in images:
        pick = choices(colors, k=3)
        image.color_set.add(pick[0])
        if randint(0, 1) == 0:
            image.color_set.add(pick[1])


if __name__ == "__main__":
    main()
