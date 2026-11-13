from src.range_position import calculate_range_position


range_min = 82500.10
range_max = 84350.00

test_prices = [
    82500.10,
    83000.00,
    83537.00,
    84000.00,
    84350.00,
]


print("=" * 60)
print("TEST DE POSICIÓN DENTRO DEL RANGO")
print("=" * 60)

for price in test_prices:

    result = calculate_range_position(
        price=price,
        range_min=range_min,
        range_max=range_max,
    )

    print()
    print(f"PRECIO: {price:.2f}")
    print(f"POSICIÓN: {result['position_percent']:.2f}%")
    print(f"ZONA: {result['zone']}")
    print(f"DISTANCIA AL MÍNIMO: {result['distance_to_min']:.2f}")
    print(f"DISTANCIA AL MÁXIMO: {result['distance_to_max']:.2f}")

print()
print("=" * 60)
print("FIN DEL TEST")
print("=" * 60)