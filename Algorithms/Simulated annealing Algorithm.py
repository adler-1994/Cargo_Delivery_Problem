# Simulated annealing implementation on the package delivery problem

import pandas as pd

from jmetal.operator.mutation import PermutationCDPMutation
from jmetal.util.observer import PrintObjectivesObserver
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.algorithm.singleobjective.simulated_annealing import SimulatedAnnealing

from CDP import CDP 

Case = "481.5"
#Read the problem instance and chose pased on the problem
#instance = pd.read_csv(r"481.csv")

#with open('481.1.txt', 'r') as file: # change to the defined problem
with open(Case + ".txt", 'r') as file:
    lines = file.readlines()
PICKUPS = list(map(int, lines[0].strip().split()))
DROPOFF = list(map(int, lines[1].strip().split()))
LORRIES = list(map(int, lines[2].strip().split()))
COMPANIES = list(map(int, lines[3].strip().split()))
COMPFARES = list(map(float, lines[5].strip().split()))
COMPLORRIES = list(map(int, lines[4].strip().split()))
COMPDISTEMPTY = list(map(int, lines[6].strip().split()))

Case = Case[:-2]
instance = pd.read_csv(Case + ".csv")

# sort the indexes of COMPANIES in desending order 
companies_lorries = list(zip(COMPANIES, COMPLORRIES, COMPDISTEMPTY,COMPFARES))     
sorted_companies_lorries = sorted(companies_lorries, key=lambda x: x[1], reverse=True)
COMPANIES = [x[0] for x in sorted_companies_lorries]
COMPLORRIES = [x[1] for x in sorted_companies_lorries]
COMPDISTEMPTY = [x[2] for x in sorted_companies_lorries]  
COMPFARES = [x[3] for x in sorted_companies_lorries]    

  
# instance is the file where cities are csv
if __name__ == "__main__":
    problem = CDP(instance, PICKUPS, DROPOFF, LORRIES,COMPANIES,COMPFARES,COMPLORRIES,COMPDISTEMPTY)
    algorithm = SimulatedAnnealing(
        problem=problem,
        mutation= PermutationCDPMutation(0.03),
        termination_criterion=StoppingByEvaluations(max_evaluations=250000),
    )
    
    algorithm.observable.register(observer=PrintObjectivesObserver(1000))
    algorithm.run()
    result = algorithm.get_result()

    print("Algorithm: {}".format(algorithm.get_name()))
    print("Problem: {}".format(problem.name()))
    print("Solution: {}".format(result.variables))
    print("Fitness: {}".format(result.objectives[0]))
    print("Computing time: {}".format(algorithm.total_computing_time))
    
    """
    seen = set()
    for number in result.variables:
        if number in seen:
            print( "there are two similar number")
        seen.add(number)   
  
    """
    # write result to a file
    with open(Case+"_SA.txt", "a") as file:
          file.write(str(result.objectives[0]) + "\n")
