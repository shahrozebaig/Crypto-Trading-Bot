import time
from decimal import Decimal, InvalidOperation
from .exceptions import ValidationError

def now_ms():
    return int(time.time() * 1000)

def validate_symbol(symbol: str) -> str:
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol is required")
    return symbol.upper()

def validate_side(side: str) -> str:
    if not side or side.upper() not in ("BUY", "SELL"):
        raise ValidationError("Side must be BUY or SELL")
    return side.upper()

def validate_positive_number(value, name="value"):
    try:
        num = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValidationError(f"{name} must be a valid number")

    if num <= 0:
        raise ValidationError(f"{name} must be > 0")

    return float(num)

def chunks(total: float, parts: int):
    if parts <= 0:
        raise ValidationError("Parts must be > 0")
    part = Decimal(str(total)) / Decimal(str(parts))
    arr = [float(part)] * parts
    diff = float(Decimal(str(total)) - sum(map(Decimal, arr)))
    arr[-1] += diff
    return arr
