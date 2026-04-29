"""
Product API endpoints.

This module defines all HTTP endpoints related to product operations.
Each endpoint delegates business logic to the service layer.
"""

from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.core.logging_config import StructuredLogger
from app.models.error import ErrorResponse
from app.models.product import ProductCategory, ProductFilterParams, ProductListResponse
from app.services import product_service

# Initialize router for product endpoints
router = APIRouter(prefix="/api/products", tags=["products"])

# Initialize structured logger
logger = StructuredLogger(__name__)


@router.get("", response_model=ProductListResponse)
async def get_products(
    min_price_usd: Decimal | None = Query(default=None, gt=0, description="Minimum price filter (inclusive)"),
    max_price_usd: Decimal | None = Query(default=None, gt=0, description="Maximum price filter (inclusive)"),
    category: ProductCategory | None = Query(default=None, description="Filter by product category"),
    search_keyword: str | None = Query(default=None, min_length=1, max_length=200, description="Keyword search in name/description"),
    sort_by: Literal["price_asc", "price_desc", "name_asc", "name_desc"] | None = Query(default=None, description="Sort order"),
) -> ProductListResponse | JSONResponse:
    """
    Get products from the catalog with optional filtering and search.

    All filter parameters are optional. When multiple are provided, they are
    combined with AND logic. Returns all products when no filters are given.

    Query Parameters:
        min_price_usd: Only return products >= this price
        max_price_usd: Only return products <= this price
        category: Filter to a specific product category
        search_keyword: Case-insensitive search in product name and description
        sort_by: Sort results by price or name (ascending or descending)

    Returns:
        ProductListResponse containing filtered products and their count

    Raises:
        HTTP 400: If min_price_usd > max_price_usd (invalid price range)
    """
    logger.info(
        "api_request_received",
        endpoint="/api/products",
        http_method="GET",
        operation="get_products",
        min_price_usd=str(min_price_usd) if min_price_usd else None,
        max_price_usd=str(max_price_usd) if max_price_usd else None,
        category=category,
        search_keyword=search_keyword,
        sort_by=sort_by,
    )

    # Validate price range — min must not exceed max
    if min_price_usd is not None and max_price_usd is not None and min_price_usd > max_price_usd:
        logger.warning(
            "invalid_price_range",
            min_price_usd=str(min_price_usd),
            max_price_usd=str(max_price_usd),
            operation="get_products",
        )
        error_response = ErrorResponse(
            error_code="invalid_price_range",
            error_message="Minimum price cannot exceed maximum price",
            error_details={"min_price_usd": str(min_price_usd), "max_price_usd": str(max_price_usd)},
        )
        return JSONResponse(status_code=400, content=error_response.model_dump())

    # Build filter params and delegate to service layer
    filters = ProductFilterParams(
        min_price_usd=min_price_usd,
        max_price_usd=max_price_usd,
        category=category,
        search_keyword=search_keyword,
        sort_by=sort_by,
    )

    products = product_service.get_filtered_products(filters)

    logger.info(
        "api_response_prepared",
        endpoint="/api/products",
        products_count=len(products),
        operation="get_products",
    )

    return ProductListResponse(products=products, total_count=len(products))
