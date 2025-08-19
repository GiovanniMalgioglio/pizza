from typing import List, Callable, Tuple
from restaurant.nutritional import Nutritional, Ingredient, Teglia
from restaurant.exceptions import TrayException


class Pizzeria:
    def __init__(self) -> None:
        self._diz_ingredienti= {}
        self._diz_teglie = {}

    # R1
    def create_ingredient(self, name: str, carbs: float, fat: float, proteins: float) -> Nutritional:
        i = Ingredient(name, carbs, fat, proteins)
        self._diz_ingredienti[name] = i 
        return i 


    def get_ingredient(self, name: str) -> Nutritional:
        return self._diz_ingredienti[name]

    # R2
    def create_pizza_tray(self, name: str, size: int) -> None:
        teglia = Teglia(name, size)
        self._diz_teglie[name] = teglia


    def get_pizza_tray(self, name: str) -> Nutritional:
        return self._diz_teglie[name]

    def add_tray_ingredient(self, tray_name: str, ingredient_name: str, pos: Tuple[int, int], size, quantity: float) -> None:
        self._diz_teglie[tray_name].add_ingredient_alla_fetta(self._diz_ingredienti[ingredient_name], pos, size, quantity)


    def get_slice(self, tray_name: str, pos: Tuple[int, int]) -> List[Nutritional]:
        return  self._diz_teglie[tray_name].get_ingredienti_fetta(pos)

    def get_layer(self, tray_name: str, num_layer: int) -> List[List[str]]:
        tab_ingredienti_strato = self._diz_teglie[tray_name].get_ingredienti_strato(num_layer)
        return tab_ingredienti_strato
    # R4
    def get_contiguous_portion(self, tray_name: str, pos: Tuple[int, int], to_avoid: str) -> List[List[bool]]:
        tab = self._diz_teglie[tray_name].crea_tab_falsi()
        tab_valori = self._diz_teglie[tray_name].segna_true(pos[0],pos[1], to_avoid, tab)
        return tab_valori

    # R5
    def sort_slice(self, tray_name: str, pos: Tuple[int, int], score_func: Callable[[Nutritional], float]) -> List[Nutritional]:
        lista = self._diz_teglie[tray_name].ordina_ingredienti(pos, score_func)
        return lista 
