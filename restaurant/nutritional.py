from abc import ABC, abstractmethod
from restaurant.exceptions import TrayException

class Nutritional(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def carbs(self) -> float:
        pass

    @property
    @abstractmethod
    def fat(self) -> float:
        pass

    @property
    @abstractmethod
    def proteins(self) -> float:
        pass


class Ingredient(Nutritional):
    def __init__(self, name, carbs, fat, proteins):
        self._name = name 
        self._carbs = carbs 
        self._fat = fat 
        self._proteins = proteins 
        self._100g = True 

    @property
    def name(self) -> str:
        return self._name 

    @property
    def carbs(self) -> float:
        return self._carbs 
    
    @property
    def fat(self) -> float:
        return self._fat 

    @property
    def proteins(self) -> float:
        return self._proteins


    def __str__(self):
        return f'{self._name} {self._carbs:0.2f} {self._fat:0.2f} {self._proteins:0.2f}'
    
    def __lt__(self, other):

        return self.name < other.name 
        

class Teglia(Nutritional):

    @property
    def name(self) -> str:
        return self._name 

    @property
    def carbs(self) -> float:
        for i in self._diz_ingredienti:
            self._carbs+= self._diz_ingredienti[i][0].carbs*self._diz_ingredienti[i][1]
        return self._carbs/100
     

    @property
    def fat(self) -> float:
        for i in self._diz_ingredienti:
            self._fat+= self._diz_ingredienti[i][0].fat*self._diz_ingredienti[i][1]
        return self._fat/100
     

    @property
    def proteins(self) -> float:
        for i in self._diz_ingredienti:
            self._proteins+= self._diz_ingredienti[i][0].proteins*self._diz_ingredienti[i][1]
        return self._proteins /100
     
    
    def __init__(self, name, size):
        self._carbs = 0 
        self._fat = 0 
        self._proteins = 0 
        self._size = size 
        self._name = name 
        self._teglia = [[Fetta(self._name,(i,j)) for i in range(size)]for j in range(size)]
        self._diz_ingredienti= {}
    
    def add_ingredient_alla_fetta(self, ingrediente, pos, size, quantità):
        self._diz_ingredienti[ingrediente.name] = (ingrediente, quantità)
        
        for i in range(size):
            for j in range(size):
                if pos[0]+i >= len(self._teglia) or pos[1]+j >= len(self._teglia) or pos[0]+i< 0 or pos[1]+j<0:
                    raise TrayException
                else:
                    self._teglia[pos[0]+i][pos[1]+j].add_ingrediente(ingrediente, quantità)  
                   
         

    def get_ingredienti_fetta(self, pos):
        return self._teglia[pos[0]][pos[1]].get_ingredienti()
    
    def get_ingredienti_strato(self, num_layer):
        tab= [[None for i in range(self._size)]for i in range(self._size)]
        
        for riga in range(len(self._teglia)):
            for colonna in range(len(self._teglia)):
                ingrediente = (self._teglia[riga][colonna]).get_ingredienti_strato(num_layer)
                tab[riga][colonna] = ingrediente
        return tab  

    def crea_tab_falsi(self):
        tab = [[False for i in range(self._size )]for j in range(self._size)]
        return tab 
    
    def segna_true(self,x,y,to_avoid, tab, esplorati = None):
        if esplorati is None:
            esplorati = set()
        
        if x< 0 or x>= self._size or y<0 or y>= self._size:
            return 
        if not self._teglia[x][y].check_ingrediente(to_avoid):
            return 
        if (x,y) in esplorati:
            return 

        tab[x][y] = True 
        esplorati.add((x,y))
        self.segna_true(x+1,y,to_avoid,tab,esplorati)
        self.segna_true(x-1,y,to_avoid,tab,esplorati)
        self.segna_true(x,y+1,to_avoid,tab,esplorati)
        self.segna_true(x,y-1,to_avoid,tab,esplorati)

        return tab 
                    
    def ordina_ingredienti(self,pos, score_funzione):
        lista_ingredienti = self._teglia[pos[0]][pos[1]].get_ingredienti()
        lista_ingredienti.sort(key= score_funzione)
        return lista_ingredienti

class Fetta(Nutritional):
    @property
    def name(self) -> str:
        return self._name 

    @property
    def carbs(self) -> float:
        return self._carbs 

    @property
    def fat(self) -> float:
        return self._fat 

    @property
    def proteins(self) -> float:
        return self._proteins
    
    def __init__(self, tray_name, pos):
        self._name = None
        self._carbs = 0 
        self._fat = 0 
        self._proteins= 0 
        self._teglia = tray_name
        self._pos = pos 
        self._strato = 0 
        self._diz_ingredienti = {}
    
    def add_ingrediente(self, ingrediente, quantità):
        self._diz_ingredienti[self._strato] = (ingrediente, quantità) 
        self._carbs += ingrediente.carbs*quantità /100
        self._fat += ingrediente.fat*quantità/100
        self._proteins+= ingrediente.proteins*quantità/100  

        self._strato+=1 

    def get_ingredienti(self):
        lista = []
        for i in self._diz_ingredienti:
            if self._diz_ingredienti[i][0] not in lista:
                lista.append(self._diz_ingredienti[i][0])
        return lista 
    
    def get_ingredienti_strato(self, num_strato):
        if num_strato not in self._diz_ingredienti:
            return None
        else:
            return self._diz_ingredienti[num_strato][0].name 
        
    def check_ingrediente(self, ingrediente):
        insieme_ingredienti = set()
        for strato in self._diz_ingredienti:
            insieme_ingredienti.add(self._diz_ingredienti[strato][0].name)
        if ingrediente not in insieme_ingredienti:
            return True 
        else:
            return False 
        
    

    
