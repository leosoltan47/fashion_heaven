from itertools import repeat
from random import choices, choice, randint
from faker import Faker
from pages.models import (
    Categories,
    Collections,
    ProductDetails,
    ProductImages,
    Products,
    Color,
    Features,
)


def main():
    # Clear existing data to ensure fresh generation
    # Delete in an order that respects foreign key dependencies,
    # or rely on on_delete=models.CASCADE if set.
    # Start with models that are depended upon by others, or M2M through models if handled manually.
    # Django's M2M fields handle their through tables automatically on deletion of an instance.
    # ProductImages depend on ProductDetails
    # ProductDetails depend on Products
    # Products depend on Categories (FK) and Features (M2M)
    # Collections have M2M with Products

    ProductImages.objects.all().delete()
    ProductDetails.objects.all().delete()
    # Deleting Products will also clear its M2M with Features.
    # Deleting Collections will also clear its M2M with Products.
    # Need to ensure Products are deleted before Categories if Categories are protected.
    # Or Collections before Products if there's a strict FK.
    # Assuming standard CASCADE or M2M handling:
    Products.objects.all().delete() # This should cascade to ProductDetails & ProductImages if using models.CASCADE
    Collections.objects.all().delete()
    Categories.objects.all().delete()
    Features.objects.all().delete()
    Color.objects.all().delete()

    fk = Faker()

    colors = [Color.objects.create(color_code=fk.hex_color()) for _ in repeat(None, 20)]
    features = [Features.objects.create(name=fk.first_name()) for _ in repeat(None, 20)]
    categories = [
        Categories.objects.create(name=fk.unique.first_name()) for _ in repeat(None, 20)
    ]
    product_collecions = [
        Collections.objects.create(
            name=fk.unique.name(),
            description=fk.text(),
            badge=fk.first_name_male(),
        )
        for _ in repeat(None, 20)
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

    for product, collection in zip(products, product_collecions):
        collection.product.add(product)
        pick = choices(products, k=4)
        collection.product.add(
            *pick,
        )

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
            content="placeholder.png",
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
