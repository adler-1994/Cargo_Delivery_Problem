import math
import random
import numpy as np
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from jmetal.core.solution import PermutationSolution

"""
 Problem: CDP : Cargo Delivery Problem
"""
S = TypeVar("S")

class Problem(Generic[S], ABC):
    """Class representing problems."""

    MINIMIZE = -1
    MAXIMIZE = 1

    def __init__(self):
        #self.reference_front: List[S] = []

        self.directions: List[int] = []
        self.labels: List[str] = []

    @abstractmethod
    def number_of_variables(self) -> int:
        pass

    @abstractmethod
    def number_of_objectives(self) -> int:
        pass

    @abstractmethod
    def number_of_constraints(self) -> int:
        pass

    @abstractmethod
    def create_solution(self) -> S:
        """Creates a random_search solution to the problem.

        :return: Solution."""
        pass
      
    @abstractmethod
    def evaluate(self, solution: S) -> S:
        """Evaluate a solution. For any new problem inheriting from :class:`Problem`, this method should be replaced.
        Note that this framework ASSUMES minimization, thus solutions must be evaluated in consequence.

        :return: Evaluated solution."""
        pass

    @abstractmethod
    def name(self) -> str:
        pass

class PermutationProblem(Problem[PermutationSolution], ABC):
    """Class representing permutation problems."""

    def __init__(self):
        super(PermutationProblem, self).__init__()

    def mutate(self, solution: S) -> S:
        """Mutate the soulation to the problem.

        :return: Solution."""
    
class CDP(PermutationProblem):
    
    def __init__(self, instance, PICKUPS, DROPOFF, LORRIES,COMPANIES: int = 0,
                 COMPFARES: float = 0, COMPLORRIES:int = 0, COMPDISTEMPTY:int = 0):
        super(CDP, self).__init__()

        self.distance_matrix, self.number_of_cities = self.__read_from_file(instance)
        self.obj_directions = [self.MINIMIZE]
        self.PICKUPS = PICKUPS
        self.DROPOFF = DROPOFF
        self.LORRIES = LORRIES
        self.COMPANIES= COMPANIES
        self.COMPFARES = COMPFARES
        self.COMPLORRIES = COMPLORRIES
        self.COMPDISTEMPTY = COMPDISTEMPTY
        self.LORRIES_REFERENCE = self.References()
        self.LORRIES_TP = self.LorriesTp()
        self.LORRIES_indexs = list(range(len(self.LORRIES_TP)))
        self.PICK_DROP_DIST= []
        for i in range(len(self.PICKUPS)): 
            self.PICK_DROP_DIST.append(self.distance_matrix[(self.PICKUPS[i]-1)*self.number_of_cities+self.DROPOFF[i]-1])
    
    def LorriesTp(self) -> int:
        LORRIES_TP = []

        TP = [self.COMPANIES[i] for i in range(len(self.COMPANIES)) for j in range(self.COMPLORRIES[i])]
        #print(f"TP lorries: {TP}")
        LORRIES_TP.extend(self.LORRIES)
        LORRIES_TP.extend(TP)
        #print(f"Lorries_TP: {LORRIES_TP}")
        return LORRIES_TP
    
    def References(self) -> int:
        LORRIES_REFERENCE = []
        LORRIES_REFERENCE.append(len(self.LORRIES)-1)
        for i in range (len(self.COMPANIES)):
            LORRIES_REFERENCE.append(LORRIES_REFERENCE[i] + self.COMPLORRIES[i])
        #print(f"LORRIES_REFERENCE: {LORRIES_REFERENCE}")
        return LORRIES_REFERENCE
    
    def number_of_variables(self) -> int:
        return self.number_of_cities

    def number_of_objectives(self) -> int:
        return 1

    def number_of_constraints(self) -> int:
        return 0

    def __read_from_file(self, instance):
        dist_matrix =  instance
        dimension = int(math.sqrt(len(dist_matrix.values)))
        matrix = np.empty(len(dist_matrix.values),dtype=np.float16)
        matrix[:] = dist_matrix.iloc[:,2]  
        #print(matrix.dtype)    
        return matrix, dimension

    def evaluate(self, solution: PermutationSolution) -> PermutationSolution:
        fitness = 0
        for i in range(len(self.PICKUPS)):
            index = next((d for d, val in enumerate(self.LORRIES_REFERENCE) if val >= solution.variables[i]), len(self.LORRIES_REFERENCE))
            if index == 0:
               fitness += self.PICK_DROP_DIST[i] + self.distance_matrix[(self.LORRIES_TP[solution.variables[i]]-1)*self.number_of_cities+self.PICKUPS[i]-1]
            elif self.distance_matrix[(self.LORRIES_TP[solution.variables[i]]-1)*self.number_of_cities+self.PICKUPS[i]-1] > self.COMPDISTEMPTY[index-1] :
              #fitness += 50000 
               fitness = float('inf')  # invalid soluation
               break
            else:
              fitness += self.PICK_DROP_DIST[i]*self.COMPFARES[index-1]
              
        solution.objectives[0] = fitness

        return solution

    def create_solution(self)-> PermutationSolution:
        new_solution = PermutationSolution(
            number_of_variables = len(self.PICKUPS), number_of_objectives=self.number_of_objectives()
        )    
        sample = random.sample(self.LORRIES_indexs, k=len(self.PICKUPS))
        # check if vaild, if not make it valid 
        i = 0
        while i < len(sample):
           # print(i)
            index = next((d for d, val in enumerate(self.LORRIES_REFERENCE) if val >= sample[i]), len(self.LORRIES_REFERENCE))
            if index == 0:
                i += 1
                continue
            elif self.distance_matrix[(self.LORRIES_TP[sample[i]]-1)*self.number_of_cities+self.PICKUPS[i]-1] <= self.COMPDISTEMPTY[index-1]:
                i += 1
                continue
            else:
                random_number = random.randint(self.LORRIES_indexs[0], self.LORRIES_indexs[-1])
                while random_number in sample:
                    random_number = random.randint(self.LORRIES_indexs[0], self.LORRIES_indexs[-1])
                sample[i]= random_number
             
        new_solution.variables = sample

        return new_solution
    
    def mutate(self, probability, solution: PermutationSolution)-> PermutationSolution:      
        for lorry_index in range(len(self.PICKUPS)): # fixed the problem of impossibility of mutating every gen in the chromosome
            rand = random.random()
            if rand <= probability: 
                #solution.variables[random_index] = -1
                # check if vaild, if not make it valid 
                while True:
                    random_Lorry = random.randint(self.LORRIES_indexs[0], self.LORRIES_indexs[-1])
                    index = next((d for d, val in enumerate(self.LORRIES_REFERENCE) if val >= random_Lorry), len(self.LORRIES_REFERENCE))
                    if random_Lorry in solution.variables:  # if the lorry already been chosen, try another one 
                      continue
                    elif index == 0:
                      break   
                    elif self.distance_matrix[(self.LORRIES_TP[random_Lorry]-1)*self.number_of_cities+self.PICKUPS[lorry_index]-1] <= self.COMPDISTEMPTY[index-1]:
                      break    
                solution.variables[lorry_index] = random_Lorry        

        return solution   

    def name(self):
        return "Package Delivery Problem"
