
def safe_fraction(num: int | float, den: int | float, *, default=0.0) -> float:
    return num / den if den != 0 else default
