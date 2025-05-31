"""
Marketplace-specific configurations for intelligent crawling
"""

MARKETPLACE_CONFIGS = {
    'depop_au': {
        'name': 'Depop Australia',
        'base_url': 'https://www.depop.com',
        'search_pattern': '/search/?q={keywords}&countryId=29',
        'selectors': {
            'listings': '[data-testid="product"]',
            'title': '[data-testid="product-title"]',
            'price': '[data-testid="product-price"]',
            'url': 'a',
            'image': 'img',
            'seller': '[data-testid="product-seller"]'
        },
        'wait_for': '[data-testid="product"]',
        'crawl_config': {
            'timeout': 15000,
            'stealth': True,
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        },
        'features': ['working', 'fast', 'reliable']
    },
    
    'ebay_au': {
        'name': 'eBay Australia',
        'base_url': 'https://www.ebay.com.au',
        'search_pattern': '/sch/i.html?_nkw={keywords}&_sacat=0&LH_PrefLoc=1&_sop=10',
        'selectors': {
            'listings': '.s-item:not(.s-item--watch-at-auction)',
            'title': '.s-item__title',
            'price': '.s-item__price',
            'url': '.s-item__link',
            'image': '.s-item__image img',
            'seller': '.s-item__seller-info-text',
            'shipping': '.s-item__shipping'
        },
        'wait_for': '.s-item',
        'crawl_config': {
            'timeout': 25000,
            'stealth': True,
            'scroll_to_bottom': True,
            'delay': 2000,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        'features': ['pagination', 'filtering', 'anti_bot_protection']
    },
    
    'gumtree_au': {
        'name': 'Gumtree Australia',
        'base_url': 'https://www.gumtree.com.au',
        'search_pattern': '/s-ad/australia/{keywords}/k0c9296?sort=date',
        'selectors': {
            'listings': '.user-ad-row',
            'title': '.user-ad-row__title',
            'price': '.user-ad-price__price',
            'url': '.user-ad-row__title a',
            'image': '.user-ad-row__image img',
            'location': '.user-ad-row__location',
            'date': '.user-ad-row__date'
        },
        'wait_for': '.user-ad-row',
        'crawl_config': {
            'timeout': 20000,
            'stealth': True,
            'handle_pagination': True,
            'max_pages': 3,
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        },
        'features': ['location_filtering', 'date_sorting', 'pagination']
    },
    
    'facebook_marketplace': {
        'name': 'Facebook Marketplace',
        'base_url': 'https://www.facebook.com/marketplace',
        'search_pattern': '/search/?query={keywords}&sortBy=creation_time_descend&exact=false',
        'selectors': {
            'listings': '[data-testid="marketplace-search-result"]',
            'title': 'span[dir="auto"]',
            'price': 'span[dir="auto"]',
            'url': 'a',
            'image': 'img',
            'location': '[data-testid="marketplace-item-location"]'
        },
        'wait_for': '[data-testid="marketplace-search-result"]',
        'crawl_config': {
            'timeout': 45000,
            'stealth': True,
            'wait_for_network_idle': True,
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
        },
        'features': ['heavy_anti_bot', 'dynamic_content', 'location_based']
    }
}

def get_marketplace_config(marketplace_id):
    """Get configuration for a specific marketplace"""
    return MARKETPLACE_CONFIGS.get(marketplace_id, None)

def get_supported_marketplaces():
    """Get list of all supported marketplaces"""
    return list(MARKETPLACE_CONFIGS.keys())
