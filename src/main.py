import random
import time
import os
import matplotlib.pyplot as plt
from generators import generate_polygon, visualize_polygon
from algorithms import gauss_area, monte_carlo_area, calculate_relative_error


def task_1_generate_polygons():
    """
    Завдання 1: Генерація та візуалізація полігонів з різною кількістю вершин
    """
    print("=" * 60)
    print("ЗАВДАННЯ 1: Генерація та візуалізація полігонів")
    print("=" * 60)

    # Створюємо папку для зображень, якщо її немає
    os.makedirs('images', exist_ok=True)

    # Фіксуємо seed для відтворюваності результатів
    random.seed(42)

    # Генеруємо полігони з різною кількістю вершин
    vertex_counts = [10, 50, 100]

    for n in vertex_counts:
        print(f"\nГенерація полігону з {n} вершинами...")
        poly = generate_polygon(num_points=n, radius=50)

        # Візуалізація та збереження
        filename = f'images/polygon_{n}_vertices.png'
        visualize_polygon(poly, filename)

        # Виводимо еталонну площу (Shapely)
        print(f"  Площа (Shapely): {poly.area:.2f}")


def task_2_test_algorithms():
    """
    Завдання 2: Тестування реалізованих алгоритмів
    """
    print("\n" + "=" * 60)
    print("ЗАВДАННЯ 2: Тестування алгоритмів")
    print("=" * 60)

    random.seed(42)
    test_poly = generate_polygon(num_points=50, radius=50)

    # Еталонна площа (Shapely)
    shapely_area = test_poly.area

    # Метод Гауса
    gauss_result = gauss_area(test_poly)
    gauss_error = calculate_relative_error(gauss_result, shapely_area)

    # Метод Монте-Карло (10000 точок)
    mc_result = monte_carlo_area(test_poly, num_points=10000)
    mc_error = calculate_relative_error(mc_result, shapely_area)

    print(f"\nРезультати для полігону з 50 вершинами:")
    print(f"  Shapely (еталон): {shapely_area:.2f}")
    print(f"  Метод Гауса:      {gauss_result:.2f} (похибка: {gauss_error:.4f}%)")
    print(f"  Монте-Карло:      {mc_result:.2f} (похибка: {mc_error:.2f}%)")


def task_3_monte_carlo_accuracy():
    """
    Завдання 3: Дослідження точності методу Монте-Карло
    """
    print("\n" + "=" * 60)
    print("ЗАВДАННЯ 3: Дослідження точності методу Монте-Карло")
    print("=" * 60)

    random.seed(42)
    test_poly = generate_polygon(num_points=50, radius=50)
    shapely_area = test_poly.area

    # Різна кількість точок для тестування
    point_counts = [100, 500, 1000, 5000, 10000, 50000, 100000]
    errors = []

    print(f"\nЕталонна площа (Shapely): {shapely_area:.2f}\n")
    print(f"{'Кількість точок':<20} {'Обчислена площа':<20} {'Похибка (%)':<15}")
    print("-" * 55)

    for num_points in point_counts:
        mc_area = monte_carlo_area(test_poly, num_points)
        error = calculate_relative_error(mc_area, shapely_area)
        errors.append(error)

        print(f"{num_points:<20} {mc_area:<20.2f} {error:<15.4f}")

    # Побудова графіку залежності похибки від кількості точок
    plt.figure(figsize=(10, 6))
    plt.plot(point_counts, errors, marker='o', linewidth=2, markersize=8, color='#2E86AB')
    plt.xscale('log')
    plt.xlabel('Кількість точок (логарифмічна шкала)', fontsize=12)
    plt.ylabel('Відносна похибка (%)', fontsize=12)
    plt.title('Залежність похибки методу Монте-Карло від кількості точок', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('images/error_plot.png', dpi=150)
    print("\nГрафік збережено: images/error_plot.png")
    plt.close()


def task_4_benchmark():
    """
    Завдання 4: Аналіз продуктивності (Benchmark)
    """
    print("\n" + "=" * 60)
    print("ЗАВДАННЯ 4: Benchmark (аналіз продуктивності)")
    print("=" * 60)

    vertex_counts = [10, 50, 100, 1000]
    results = {
        'vertices': [],
        'shapely': [],
        'gauss': [],
        'monte_carlo': []
    }

    print(f"\n{'Вершини':<12} {'Shapely (s)':<15} {'Гаус (s)':<15} {'Монте-Карло (s)':<20}")
    print("-" * 62)

    for n in vertex_counts:
        random.seed(42)
        poly = generate_polygon(num_points=n, radius=50)

        results['vertices'].append(n)

        # Вимірювання часу для Shapely (100 повторів для точності)
        start = time.time()
        for _ in range(100):
            _ = poly.area
        shapely_time = (time.time() - start) / 100
        results['shapely'].append(shapely_time)

        # Вимірювання часу для методу Гауса (100 повторів)
        start = time.time()
        for _ in range(100):
            _ = gauss_area(poly)
        gauss_time = (time.time() - start) / 100
        results['gauss'].append(gauss_time)

        # Вимірювання часу для Монте-Карло (1 повтор, бо він і так повільний)
        start = time.time()
        _ = monte_carlo_area(poly, num_points=10000)
        mc_time = time.time() - start
        results['monte_carlo'].append(mc_time)

        print(f"{n:<12} {shapely_time:<15.6f} {gauss_time:<15.6f} {mc_time:<20.6f}")

    # Побудова графіку порівняння продуктивності
    plt.figure(figsize=(10, 6))
    plt.plot(results['vertices'], results['shapely'], marker='o', label='Shapely', linewidth=2)
    plt.plot(results['vertices'], results['gauss'], marker='s', label='Гаус', linewidth=2)
    plt.plot(results['vertices'], results['monte_carlo'], marker='^', label='Монте-Карло', linewidth=2)

    plt.xlabel('Кількість вершин', fontsize=12)
    plt.ylabel('Час виконання (секунди)', fontsize=12)
    plt.title('Порівняння продуктивності методів обчислення площі', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')  # Логарифмічна шкала для кращої читабельності
    plt.tight_layout()
    plt.savefig('images/time_benchmark.png', dpi=150)
    print("\nГрафік збережено: images/time_benchmark.png")
    plt.close()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ЛАБОРАТОРНА РОБОТА: Обчислення площі полігонів")
    print("Алгоритмічні та евристичні методи")
    print("=" * 60)

    # Виконуємо всі завдання по порядку
    task_1_generate_polygons()
    task_2_test_algorithms()
    task_3_monte_carlo_accuracy()
    task_4_benchmark()

    print("\n" + "=" * 60)
    print("ВСІ ЗАВДАННЯ ВИКОНАНО УСПІШНО!")
    print("Результати збережено в папці 'images/'")
    print("=" * 60 + "\n")