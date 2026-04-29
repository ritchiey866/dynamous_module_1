/**
 * FilterPanel component for searching and filtering products.
 *
 * Provides:
 * - Keyword search input
 * - Category dropdown
 * - Min/max price inputs
 * - Sort order dropdown
 * - Clear filters button
 *
 * Props:
 * - filters: Current active filter values
 * - onFiltersChange: Callback fired when any filter value changes
 */

import { Search, X } from "lucide-react";
import type { ProductCategory, ProductFilterParams } from "@/types/product";

const CATEGORIES: { value: ProductCategory; label: string }[] = [
  { value: "electronics", label: "Electronics" },
  { value: "clothing", label: "Clothing" },
  { value: "home", label: "Home" },
  { value: "sports", label: "Sports" },
  { value: "books", label: "Books" },
];

const SORT_OPTIONS: { value: NonNullable<ProductFilterParams["sort_by"]>; label: string }[] = [
  { value: "price_asc", label: "Price: Low to High" },
  { value: "price_desc", label: "Price: High to Low" },
  { value: "name_asc", label: "Name: A to Z" },
  { value: "name_desc", label: "Name: Z to A" },
];

interface FilterPanelProps {
  filters: ProductFilterParams;
  onFiltersChange: (filters: ProductFilterParams) => void;
}

export function FilterPanel({ filters, onFiltersChange }: FilterPanelProps) {
  const hasActiveFilters =
    filters.search_keyword ||
    filters.category ||
    filters.min_price_usd !== undefined ||
    filters.max_price_usd !== undefined ||
    filters.sort_by;

  function handleClear() {
    onFiltersChange({});
  }

  function set<K extends keyof ProductFilterParams>(key: K, value: ProductFilterParams[K]) {
    onFiltersChange({ ...filters, [key]: value });
  }

  function handlePriceInput(key: "min_price_usd" | "max_price_usd", raw: string) {
    if (raw === "") {
      const next = { ...filters };
      delete next[key];
      onFiltersChange(next);
    } else {
      const num = parseFloat(raw);
      if (!Number.isNaN(num) && num > 0) {
        set(key, num);
      }
    }
  }

  return (
    <div className="bg-card border rounded-lg p-4 mb-6 space-y-4">
      {/* Search row */}
      <div className="flex flex-col sm:flex-row gap-3">
        {/* Keyword search */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
          <input
            type="search"
            placeholder="Search products..."
            value={filters.search_keyword ?? ""}
            onChange={(e) => set("search_keyword", e.target.value || undefined)}
            className="w-full pl-9 pr-3 py-2 border rounded-md bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>

        {/* Category */}
        <select
          value={filters.category ?? ""}
          onChange={(e) =>
            set("category", (e.target.value as ProductCategory) || undefined)
          }
          className="border rounded-md px-3 py-2 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring sm:w-44"
        >
          <option value="">All categories</option>
          {CATEGORIES.map((c) => (
            <option key={c.value} value={c.value}>
              {c.label}
            </option>
          ))}
        </select>

        {/* Sort */}
        <select
          value={filters.sort_by ?? ""}
          onChange={(e) =>
            set("sort_by", (e.target.value as ProductFilterParams["sort_by"]) || undefined)
          }
          className="border rounded-md px-3 py-2 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring sm:w-48"
        >
          <option value="">Default order</option>
          {SORT_OPTIONS.map((s) => (
            <option key={s.value} value={s.value}>
              {s.label}
            </option>
          ))}
        </select>
      </div>

      {/* Price range row */}
      <div className="flex flex-wrap items-center gap-3">
        <span className="text-sm text-muted-foreground">Price range:</span>
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">$</span>
          <input
            type="number"
            placeholder="Min"
            min="0.01"
            step="0.01"
            value={filters.min_price_usd ?? ""}
            onChange={(e) => handlePriceInput("min_price_usd", e.target.value)}
            className="w-24 border rounded-md px-3 py-2 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
        <span className="text-sm text-muted-foreground">—</span>
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">$</span>
          <input
            type="number"
            placeholder="Max"
            min="0.01"
            step="0.01"
            value={filters.max_price_usd ?? ""}
            onChange={(e) => handlePriceInput("max_price_usd", e.target.value)}
            className="w-24 border rounded-md px-3 py-2 bg-background text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>

        {/* Clear button — only shown when filters are active */}
        {hasActiveFilters && (
          <button
            type="button"
            onClick={handleClear}
            className="ml-auto flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-4 h-4" />
            Clear filters
          </button>
        )}
      </div>
    </div>
  );
}
