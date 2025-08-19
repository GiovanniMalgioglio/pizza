from restaurant.pizzeria import Pizzeria
from restaurant.exceptions import TrayException


def main():
    print("------------------------- R1 -------------------------")
    pizzeria = Pizzeria()
    pomodoro = pizzeria.create_ingredient("pomodoro", 17, 0.2, 4.2)
    mozzarella = pizzeria.create_ingredient("mozzarella", 2, 18, 17)
    prosciutto = pizzeria.create_ingredient("prosciutto", 25, 4.7, 11)
    acciughe = pizzeria.create_ingredient("acciughe", 0, 49.7, 12.5)

    print(pomodoro.name)                                    # pomodoro
    pomodoro = pizzeria.get_ingredient("pomodoro")
    print(pomodoro.carbs, pomodoro.fat, pomodoro.proteins)  # 17 0.2 4.2
    print(str(pomodoro))                                    # pomodoro 17.00 0.20 4.20

    ingredienti = [pomodoro, mozzarella, prosciutto, acciughe]
    ingredienti.sort()
    print([i.name for i in ingredienti])                    # ['acciughe', 'mozzarella', 'pomodoro', 'prosciutto']

    print("------------------------- R2 -------------------------")
    pizzeria.create_pizza_tray("pizza", 5)
    pizzeria.add_tray_ingredient("pizza", "mozzarella", (0, 0), 3, 50)
    pizzeria.add_tray_ingredient("pizza", "pomodoro", (0, 0), 5, 90)
    pizzeria.add_tray_ingredient("pizza", "acciughe", (2, 2), 3, 35)
    teglia = pizzeria.get_pizza_tray("pizza")
    print(teglia.name)                          # pizza
    print("{:.3f}".format(teglia.carbs))        # 16.300
    print("{:.3f}".format(teglia.fat))          # 26.575
    print("{:.3f}".format(teglia.proteins))     # 16.655

    pizzeria.create_pizza_tray("pizza_wrong", 5)
    try:
        pizzeria.add_tray_ingredient("pizza", "acciughe", (-1, 3), 6, 15)
        print("[ERROR]: Ingredient outside the tray not detected")
    except TrayException:
        print("Ingredient outside the tray correctly detected")  # Ingredient outside the tray correctly detected

    print("------------------------- R3 -------------------------")
    print([i.name for i in pizzeria.get_slice("pizza", (1, 1))])    # ['mozzarella', 'pomodoro']
    print([i.name for i in pizzeria.get_slice("pizza", (2, 2))])    # ['mozzarella', 'pomodoro', 'acciughe']
    print([i.name for i in pizzeria.get_slice("pizza", (3, 3))])    # ['pomodoro', 'acciughe']
    print()

    for row in pizzeria.get_layer("pizza", 0):
        print(row)
    print()

    # ['mozzarella', 'mozzarella', 'mozzarella', 'pomodoro', 'pomodoro']
    # ['mozzarella', 'mozzarella', 'mozzarella', 'pomodoro', 'pomodoro']
    # ['mozzarella', 'mozzarella', 'mozzarella', 'pomodoro', 'pomodoro']
    # ['pomodoro', 'pomodoro', 'pomodoro', 'pomodoro', 'pomodoro']
    # ['pomodoro', 'pomodoro', 'pomodoro', 'pomodoro', 'pomodoro']

    for row in pizzeria.get_layer("pizza", 1):
        print(row)
    print()

    # ['pomodoro', 'pomodoro', 'pomodoro', None, None]
    # ['pomodoro', 'pomodoro', 'pomodoro', None, None]
    # ['pomodoro', 'pomodoro', 'pomodoro', 'acciughe', 'acciughe']
    # [None, None, 'acciughe', 'acciughe', 'acciughe']
    # [None, None, 'acciughe', 'acciughe', 'acciughe']

    for row in pizzeria.get_layer("pizza", 1):
        print(row)
    print()

    # ['pomodoro', 'pomodoro', 'pomodoro', None, None]
    # ['pomodoro', 'pomodoro', 'pomodoro', None, None]
    # ['pomodoro', 'pomodoro', 'pomodoro', 'acciughe', 'acciughe']
    # [None, None, 'acciughe', 'acciughe', 'acciughe']
    # [None, None, 'acciughe', 'acciughe', 'acciughe']

    print("------------------------- R4 -------------------------")
    pizzeria.add_tray_ingredient("pizza", "acciughe", (0, 0), 3, 50)
    portion = pizzeria.get_contiguous_portion("pizza", (0, 3), "acciughe")
    for row in portion:
        print(row)

    # [False, False, False, True, True]
    # [False, False, False, True, True]
    # [False, False, False, False, False]
    # [False, False, False, False, False]
    # [False, False, False, False, False]

    print("------------------------- R5 -------------------------")
    sorted_slice_ingredients = pizzeria.sort_slice("pizza", (1, 1), lambda x: (x.fat + x.carbs)/x.proteins)
    print([i.name for i in sorted_slice_ingredients])   # ['mozzarella', 'acciughe', 'pomodoro']


if __name__ == "__main__":
    main()
