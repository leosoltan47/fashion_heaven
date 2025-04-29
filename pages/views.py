from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import ProductDetails, Products
import re


# TODO: Add search bar that renders page specified in the search
def home(request):
    in_stock = ProductDetails.objects.filter(stock__gt=0)
    # Show 10 products that has at least one variant
    # as information like color are stored in variants
    objects = (
        Products.objects.filter(category__isnull=False)
        .prefetch_related(Prefetch("details", queryset=in_stock))
        .distinct()
        .filter(details__isnull=False)
        .order_by("id")[:10]
    )
    products = [
        {
            "id": obj.pk,
            "name": obj.name,
            "price": obj.price_in_dollars,
            "colors": [
                [color.color_code for color in image.color_set.all()]
                for variant in obj.details.all()
                for image in variant.productimages_set.all()
            ],
        }
        for obj in objects
    ]
    context = {"products": products}
    return render(request, "pages/home.html", context)


def product(request, product_id):
    """
    View function that retrieves product information from get URL
    """
    obj = get_object_or_404(Products, pk=product_id)
    product = {
        "id": obj.pk,
        "name": obj.name,
        "price": obj.price_in_dollars,
        "category": obj.category.name,
    }
    return JsonResponse(product)


def empty_wishlist(request):
    return render(request, "pages/wishlist.html")


def wishlist(request, id_list: str):
    """
    View function for the wishlist page.
    """
    regex = re.compile(r"ids\[\]=(\d+)")
    ids = regex.findall(id_list)
    if len(ids) == 0:
        return render(request, "pages/wishlist.html")
    products = Products.objects.filter(id__in=ids)
    context = {"wishlist_items": products}
    return render(request, "pages/wishlist.html", context)


def bag(request):
    """
    View function for the shopping bag page.
    """
    return render(request, "pages/bag.html")


def catalog(request, title):
    gender_filters = {"women": ["W", "U"], "men": ["M", "U"], "kids": ["K", "B", "G"]}
    gender_fullname = {
        "W": "Womem",
        "M": "Men",
        "K": "Kids",
        "U": "Unisex",
        "B": "Boys",
        "G": "Girls",
    }

    # In order to reduce number of SQL queries prefetch `ProductImages` and `Color` tables
    # as they're going to be used to populate context
    in_stock = ProductDetails.objects.filter(stock__gt=0).prefetch_related(
        "productimages_set", "productimages_set__color_set"
    )
    objects = (
        Products.objects.select_related("category")
        .prefetch_related(Prefetch("details", queryset=in_stock))
        .distinct()
        .filter(details__isnull=False)
        # Get only the records corresponding to catalog
        # Ex: catalog/men will show only outfits for Men, catalog/women for Women etc
        .filter(
            gender_and_age__in=gender_filters.get(title, ["W", "M", "U", "G", "B", "K"])
        )
        .order_by("id")
    )

    products = [
        {
            "id": obj.pk,
            "name": obj.name,
            "price": obj.price_in_dollars,
            "colors": [
                (*[color.color_code for color in image.color_set.all()],)
                for variant in obj.details.all()
                for image in variant.productimages_set.all()
            ],
        }
        for obj in objects
    ]
    context = {
        "products": products,
        "title": title,
        "genders": {gender_fullname[obj.gender_and_age] for obj in objects},
        "categories": {obj.category for obj in objects},
        "sizes": {variant.size for obj in objects for variant in obj.details.all()},
        "colors": {
            (*sorted(color),)
            for product in products
            for color in product.get("colors", [])
        },
    }
    return render(request, f"pages/catalog.html", context)


def product_detail_page(request, product_id):
    """
    View function for the product detail page.
    Fetches the product and its details (images, colors, sizes)
    and renders the HTML template.
    """
    # Prefetch related details for efficiency
    details_prefetch = Prefetch(
        'details',
        queryset=ProductDetails.objects.filter(stock__gt=0).prefetch_related(
            'productimages_set',
            'color_set',
            'size_set'
        )
    )

    product = get_object_or_404(
        Products.objects.select_related('category').prefetch_related(details_prefetch),
        pk=product_id
    )

    # Extract images from the prefetched details
    product_images = []
    details_list = [] # Also pass details to template for color/size info
    if product.details.exists():
        details_list = list(product.details.all()) # Convert queryset to list for template
        for detail in details_list:
            product_images.extend(list(detail.productimages_set.all()))

    context = {
        'product': product,
        'product_images': product_images,
        'details': details_list, # Pass details for color/size buttons
    }
    return render(request, 'pages/product_detail.html', context)
