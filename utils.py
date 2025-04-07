def pad_right(text, width):
    return f"{text:<{width}}"[:width]

def format_amount(amount):
    return f"{int(amount * 100):012d}"

def parse_amount(amount_str):
    return int(amount_str) / 100
