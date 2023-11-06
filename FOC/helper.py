def parse_price(price_str):
    # Remove dollar sign and convert to float
    return float(price_str.replace('$', '').strip()) if price_str else None

def parse_volume(volume_str):
    # Convert volume to float
    return float(volume_str) if volume_str else None