import re
import math

def calculate(query: str) -> str:
    try:
        if "circle area" in query.lower():
            radius = float(re.search(r"radius (\d+)", query).group(1))
            area = math.pi * radius ** 2
            return f"Area of circle with radius {radius} is {area:.2f}."
        return "Unsupported calculation."
    except Exception as e:
        return f"Error calculating: {str(e)}"   