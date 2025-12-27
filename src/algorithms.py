
import random
from shapely.geometry import Polygon, Point


def gauss_area(polygon: Polygon) -> float:
    """
    Обчислення площі полігону за методом Гауса (Shoelace formula).

    Формула: A = 0.5 * |Σ(x_i * y_{i+1} - x_{i+1} * y_i)|

    Args:
        polygon (Polygon): Об'єкт полігону Shapely

    Returns:
        float: Площа полігону
    """
    # Отримуємо координати вершин
    coords = list(polygon.exterior.coords)
    n = len(coords) - 1  # Остання точка дублює першу, тому -1

    area_sum = 0.0

    # Проходимо по всіх парах сусідніх вершин
    for i in range(n):
        x_i, y_i = coords[i]
        x_next, y_next = coords[i + 1]

        # Додаємо до суми: x_i * y_{i+1} - x_{i+1} * y_i
        area_sum += (x_i * y_next - x_next * y_i)

    # Повертаємо половину абсолютного значення
    return abs(area_sum) / 2.0


def monte_carlo_area(polygon: Polygon, num_points: int = 10000) -> float:
    """
    Обчислення площі полігону методом Монте-Карло.

    Алгоритм:
    1. Визначаємо bounding box (прямокутник) навколо полігону
    2. Генеруємо num_points випадкових точок всередині bounding box
    3. Перевіряємо, скільки з них потрапили всередину полігону
    4. Площа = (точки_в_полігоні / всього_точок) * площа_bounding_box

    Args:
        polygon (Polygon): Об'єкт полігону Shapely
        num_points (int): Кількість випадкових точок для генерації

    Returns:
        float: Приблизна площа полігону
    """
    # Отримуємо bounding box (мінімальний прямокутник навколо полігону)
    minx, miny, maxx, maxy = polygon.bounds

    # Обчислюємо площу bounding box
    bbox_area = (maxx - minx) * (maxy - miny)

    # Лічильник точок всередині полігону
    points_inside = 0

    # Генеруємо випадкові точки та перевіряємо їх
    for _ in range(num_points):
        # Генеруємо випадкову точку всередині bounding box
        random_x = random.uniform(minx, maxx)
        random_y = random.uniform(miny, maxy)

        # Створюємо об'єкт Point
        point = Point(random_x, random_y)

        # Перевіряємо, чи точка всередині полігону
        if polygon.contains(point):
            points_inside += 1

    # Обчислюємо площу за пропорцією
    ratio = points_inside / num_points
    estimated_area = ratio * bbox_area

    return estimated_area


def calculate_relative_error(estimated: float, true_value: float) -> float:
    """
    Обчислення відносної похибки у відсотках.

    Формула: error = |estimated - true_value| / true_value * 100%

    Args:
        estimated (float): Оцінене значення
        true_value (float): Справжнє (еталонне) значення

    Returns:
        float: Відносна похибка у відсотках
    """
    if true_value == 0:
        return 0.0

    error = abs(estimated - true_value) / true_value * 100
    return error