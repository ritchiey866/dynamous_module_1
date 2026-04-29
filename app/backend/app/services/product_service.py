"""
Product service containing business logic for product operations.

This service layer separates business logic from API routing logic,
making the code more testable and maintainable.
"""

from app.core.logging_config import StructuredLogger
from app.data.seed_products import get_seed_products
from app.models.product import Product, ProductFilterParams

# Initialize structured logger for this module
logger = StructuredLogger(__name__)

# In-memory product storage (in a real app, this would be a database)
_PRODUCTS_DATABASE: list[Product] = get_seed_products()


def get_all_products() -> list[Product]:
    """
    Retrieve all products from the catalog without filtering.

    Returns:
        List of all Product objects in the catalog
    """
    logger.info(
        "retrieving_all_products", total_products_in_database=len(_PRODUCTS_DATABASE), operation="get_all_products"
    )

    logger.info(
        "products_retrieved_successfully", products_returned=len(_PRODUCTS_DATABASE), operation="get_all_products"
    )

    return _PRODUCTS_DATABASE


def get_filtered_products(filters: ProductFilterParams) -> list[Product]:
    """
    Retrieve products matching the given filter parameters.

    Filters are applied with AND logic — a product must satisfy ALL provided
    filters to be included in the result.

    Args:
        filters: ProductFilterParams with optional min/max price, category,
                 keyword search, and sort order.

    Returns:
        Filtered and optionally sorted list of Product objects.
    """
    logger.info(
        "filtering_products",
        min_price_usd=str(filters.min_price_usd) if filters.min_price_usd else None,
        max_price_usd=str(filters.max_price_usd) if filters.max_price_usd else None,
        category=filters.category,
        search_keyword=filters.search_keyword,
        sort_by=filters.sort_by,
        operation="get_filtered_products",
    )

    results = _PRODUCTS_DATABASE[:]

    # Apply minimum price filter
    if filters.min_price_usd is not None:
        results = [p for p in results if p.product_price_usd >= filters.min_price_usd]

    # Apply maximum price filter
    if filters.max_price_usd is not None:
        results = [p for p in results if p.product_price_usd <= filters.max_price_usd]

    # Apply category filter
    if filters.category is not None:
        results = [p for p in results if p.product_category == filters.category]

    # Apply keyword search (case-insensitive, searches name and description)
    if filters.search_keyword is not None:
        keyword = filters.search_keyword.lower()
        results = [
            p for p in results
            if keyword in p.product_name.lower() or keyword in p.product_description.lower()
        ]

    # Apply sort order
    if filters.sort_by == "price_asc":
        results.sort(key=lambda p: p.product_price_usd)
    elif filters.sort_by == "price_desc":
        results.sort(key=lambda p: p.product_price_usd, reverse=True)
    elif filters.sort_by == "name_asc":
        results.sort(key=lambda p: p.product_name.lower())
    elif filters.sort_by == "name_desc":
        results.sort(key=lambda p: p.product_name.lower(), reverse=True)

    logger.info(
        "products_filtered_successfully",
        products_returned=len(results),
        total_in_database=len(_PRODUCTS_DATABASE),
        operation="get_filtered_products",
    )

    return results
