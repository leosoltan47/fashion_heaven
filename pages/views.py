from functools import reduce
from django.db.models import Q, Prefetch, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import ProductDetails, Products, ProductImages
import re


def get_product_slider_data(products):
    # Prefetch product images with their colors in a single query
    # Using a custom prefetch object to filter images by stock > 0
    products_with_images = Products.objects.filter(
        id__in=[p.id for p in products]
    ).prefetch_related(
        Prefetch(
            "productdetails_set__productimages_set",
            queryset=ProductImages.objects.filter(
                product_detail__stock__gt=0
            ).prefetch_related("color_set"),
            to_attr="available_images",
        ),
        "collections_set",
    )

    # Create a dictionary for quick lookup
    products_dict = {p.id: p for p in products_with_images}

    # Prepare the product data
    product_data = []
    for product in products:
        product_obj = products_dict.get(product.id)
        colors_list = []
        badge = ""  # Initialize badge to an empty string

        if product_obj:
            # Flatten the structure to get all images
            all_images = (
                image
                for detail in product_obj.productdetails_set.all()
                for image in detail.available_images
                if hasattr(detail, "available_images")
            )

            all_badges = [
                collection.badge
                for collection in product_obj.collections_set.all()
                if hasattr(collection, "badge")
            ]
            badge = all_badges[0] if all_badges else ""

            # Extract colors for each image
            for image in all_images:
                colors = [color.color_code for color in image.color_set.all()]
                if colors:  # Only add non-empty color lists
                    colors_list.append(colors)

        product_data.append(
            {
                "id": product.pk,
                "name": product.name,
                "price": product.price_in_dollars,
                "colors": colors_list,
                "badge": badge,
            }
        )
    return product_data


def home(request):
    # Get 10 products with their categories in a single query
    products = (
        Products.objects.select_related("category")
        .prefetch_related("collections_set")
        .filter(category__isnull=False)
        .order_by("id")[:10]
    )

    product_data = get_product_slider_data(products)

    context = {"products": product_data}
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


def bag(request, ids: str = ""):
    """
    View function for the shopping bag page.
    """
    variant_ids: list[int] = [int(id) for id in ids.split(sep="&") if id.isdigit()]
    if not variant_ids:
        return render(request, "pages/bag.html")

    products = list(
        ProductDetails.objects.select_related("product", "product__category")
        .annotate(
            category_name=F("product__category__name"),
            price=F("product__price_in_dollars"),
        )
        .filter(pk__in=variant_ids, stock__gt=0)
        .order_by("pk")
        .all()
    )

    total_price = reduce(lambda x, y: x + y.price, products, 0)
    context = {"total_price": total_price, "products": products}
    return render(request, "pages/bag.html", context)


def catalog(request, title, search=""):
    search = search.lower()
    gender_filters = {"women": ["W", "U"], "men": ["M", "U"], "kids": ["K", "B", "G"]}
    gender_fullname = {
        "W": "Women",
        "M": "Men",
        "K": "Kids",
        "U": "Unisex",
        "B": "Boys",
        "G": "Girls",
    }
    genders = gender_filters.get(title, ["W", "U", "M", "K", "B", "G"])

    products = (
        Products.objects.filter(gender_and_age__in=genders)
        .select_related("category")
        .order_by("id")
        .filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(category__name__icontains=search)
        )
    )

    product_data = get_product_slider_data(products)
    genders = {gender_fullname.get(p.gender_and_age) for p in products}
    categories = {p.category for p in products}
    sizes = (
        ProductDetails.objects.filter(product__in=[p.id for p in products], stock__gt=0)
        .distinct()
        .values_list("size", flat=True)
    )
    colors = {
        (*colors,) for product in product_data for colors in product.get("colors")
    }

    context = {
        "products": product_data,
        "genders": genders,
        "title": title,
        "colors": colors,
        "sizes": sizes,
        "categories": categories,
    }
    return render(request, "pages/catalog.html", context)


def product_detail_page(request, product_id):
    """
    View function for the product detail page.
    Fetches the product and its details (images, colors, sizes)
    and renders the HTML template.
    If product is not found, it renders the page with empty context.
    """
    product_instance = None
    product_images = []
    details_list = []

    try:
        # Prefetch related details for efficiency
        # Note: 'productdetails_set' is the reverse accessor for ProductDetails linked to Products
        details_prefetch = Prefetch(
            "productdetails_set",
            queryset=ProductDetails.objects.filter(stock__gt=0).prefetch_related(
                Prefetch("productimages_set", queryset=ProductImages.objects.prefetch_related("color_set"))
            ),
            to_attr="fetched_details"
        )

        product_instance = Products.objects.select_related("category").prefetch_related(details_prefetch).get(pk=product_id)

        # Extract images and details from the prefetched data
        if hasattr(product_instance, 'fetched_details'):
            details_list = product_instance.fetched_details
            for detail in details_list:
                product_images.extend(list(detail.productimages_set.all()))
        
    except Products.DoesNotExist:
        # Product not found, proceed with empty context to render a blank page
        pass

    context = {
        "product": product_instance,
        "product_images": product_images,
        "details": details_list,  # Pass details for color/size buttons
    }
    return render(request, "pages/product_details.html", context)


def support_page(request):
    """Renders the support page."""
    return render(request, "pages/support.html")


def returns_exchanges_view(request):
    """Renders the product details/returns page."""
    return render(request, "pages/product_details.html")
