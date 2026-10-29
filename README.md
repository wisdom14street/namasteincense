# Namaste Incense

Static storefront for **https://namasteincense.com**: incense sticks, cones, sacred resins, sage and palo santo, holders, burners and charcoal, and ritual candles.
Namaste Incense is a brand of Wealth Edge Ventures Inc. Checkout runs on Shopify through namastebookshop.com cart permalinks tagged `attributes[Storefront]=Namaste Incense`.

## Build
```
python3 scripts/fetch.py     # full public catalog from namastebookshop.com (all pages)
python3 scripts/pickup.py    # Shopify Local Pickup availability per variant
python3 scripts/build.py --site=https://namasteincense.com   # writes dist/ (incl. CNAME)
```
`scripts/catmap.py` decides which products are incense and which aisle they go in. `.github/workflows/pages.yml` rebuilds on every push and daily (09:17 UTC) and deploys to GitHub Pages.

## Store visit facts used
2 West 14th Street, New York, NY 10011 (steps from Union Square). Phone 646-876-1401. Hours: Mon to Thu 11 AM to 8 PM, Fri and Sat 11 AM to 9 PM, Sun 11 AM to 7 PM (namastebookshop.com contact page). Pickup text comes from Shopify's public pickup-availability section.
