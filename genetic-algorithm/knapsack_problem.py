import random
from tabulate import tabulate


#--------Configuration
NUMBER_CHROMOSOMES = 10
GENERATIONS = 50
CROSSOVER_PROB = 0.85
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.5

#--------Knapsack Problem Configuration
max_weight = 30

# Items
# 1. Decoy Detonators - Weight: 4, Value: 10
# 2. Love Potion - Weight: 2, Value: 8
# 3. Extendable Ears - Weight: 5, Value: 12
# 4. Skiving Snackbox - Weight: 5, Value: 6
# 5. Fever Fudge - Weight: 2, Value: 3
# 6. Puking Pastilles - Weight: 1.5, Value: 2
# 7. Nosebleed Nougat - Weight: 1, Value: 2
weights = [4, 2, 5, 5, 2, 1.5, 1]
values = [10, 8, 12, 6, 3, 2, 2]
necessary = [0, 3, 2, 0, 0, 0, 0]
n = len(weights)

#--------Functions

# <-- create chromosomes -->

# validate total weight
def valid_chromosome(chromosome):
    weight = 0
    
    for i in range(n):
        weight += chromosome[i] * weights[i]
    
    if weight > max_weight:
        return False
    
    return True

# generate a random chromosome with the necessary items
def generate_chromosome():
    chromosome = []
    for i in range(n):
        chromosome.append(random.randint(necessary[i], 10))
    return chromosome

# <-- create population -->

# generate the initial population
def generate_population():
    population = []
    
    for i in range(NUMBER_CHROMOSOMES):
        chromosome = generate_chromosome()
        
        while not valid_chromosome(chromosome):
            chromosome = generate_chromosome()
        
        population.append(chromosome)
        
    return population

def print_population(population):
    table = []
    
    for i, chromosome in enumerate(population):
        total_value = sum(chromosome[j] * values[j] for j in range(n))
        total_weight = sum(chromosome[j] * weights[j] for j in range(n))
        
        table.append([f"Chromosome {i}", chromosome, total_value, total_weight])
    
    headers = ["Chromosome", "Chromosome Representation", "Total Value", "Total Weight"]
    
    print(tabulate(table, headers=headers, tablefmt="pipe"))

# <-- Parent selection -->

# get the accumulated probability of each chromosome
def get_vector_probability(population):
    total_values = [sum(population[i][j] * values[j] for j in range(n)) for i in range(NUMBER_CHROMOSOMES)]
    
    total_sum = sum(total_values)
    probabilities = [value / total_sum for value in total_values]
    
    accumulated_probabilities = []
    cumulative_sum = 0
    for prob in probabilities:
        cumulative_sum += prob
        accumulated_probabilities.append(cumulative_sum)
    
    return accumulated_probabilities

def print_vector_probability(probabilities):
    table = [[i, probabilities[i]] for i in range(NUMBER_CHROMOSOMES)]
    headers = ["Chromosome", "Acculated Probability"]
    print(tabulate(table, headers=headers, tablefmt="pipe"))
    

# get the parents for the crossover
def get_parents(probabilities):
    parent1_ = -1
    parent2_ = -1

    r1 = random.uniform(0, 1)

    for i, prob in enumerate(probabilities):
        if r1 < prob: 
            parent1_ = i
            break
    
    r2 = random.uniform(0, 1)

    for i, prob in enumerate(probabilities):
        if r2 < prob:
            parent2_ = i
            break
    
    while parent1_ == parent2_:
        r2 = random.uniform(0, 1)

        for i, prob in enumerate(probabilities):
            if r2 < prob:
                parent2_ = i
                break

    return parent1_, parent2_

# <-- Crossover -->

# crossover function
def crossover(parent1, parent2):
    random_vector = [random.uniform(0, 1) for i in range(n)]
    # print(f"Random Vector: {random_vector}")
    random_vector_table = [[i,[val]] for i, val in enumerate(random_vector)]
    headers = ["Random Vector"]
    print(tabulate(random_vector_table, headers=headers, tablefmt="pipe"))
    print("\n")

    child1 = []
    child2 = []

    for i in range(n):
        if random_vector[i] <= CROSSOVER_RATE:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    
    return child1, child2

# <-- Mutation -->

# mutation function
def mutation(chromosome):
    r = random.uniform(0, 1)
    print(f"Mutation Rate: {r}")
    
    if r < MUTATION_RATE:
        new_chromosome = generate_chromosome()

        while not valid_chromosome(new_chromosome):
            new_chromosome = generate_chromosome()
        return new_chromosome
    
    return chromosome

def best_chromosome(chrom_1, chrom_2):
    value_1 = sum(chrom_1[i] * values[i] for i in range(n))
    value_2 = sum(chrom_2[i] * values[i] for i in range(n))
    
    if value_1 > value_2:
        return chrom_1
    return chrom_2


if __name__ == "__main__":

    title = "Initial Population" 
    print("=" * len(title))
    print(title)
    print("=" * len(title))


    population = generate_population()
    print_population(population)
    print("\n")

    for generation in range(GENERATIONS):
        print("=" * len(f"Generation {generation+1}"))
        print(f"Generation {generation+1}")
        print("=" * len(f"Generation {generation+1}"))
        print("\n")
        probability = get_vector_probability(population)
        print( "=" * len("Roulette probability"))
        print("Roulette probability")
        print( "=" * len("Roulette probability"))
        print_vector_probability(probability)


        # print(probability)

        new_population = []

        for i in range(NUMBER_CHROMOSOMES//2):
            print("\n")
            print( "-" * len(f"Chromosome {i}"))
            print(f"Chromosome {i}")
            print( "-" * len(f"Chromosome {i}"))
            print("\n")

            parent1_idx, parent2_idx = get_parents(probability)
            # print(f"Parent 1: {parent1_idx}, Parent 2: {parent2_idx}")
            parent_table = [[parent1_idx, parent2_idx]]
            headers = ["Parent 1", "Parent 2"]
            print(tabulate(parent_table, headers=headers, tablefmt="pipe"))
            print("\n")

            parent1 = population[parent1_idx]
            parent2 = population[parent2_idx]
            
            crossover_or_not = random.uniform(0, 1)
            crossover_table = [[crossover_or_not]]
            headers = ["Crossover Rate"]
            print(tabulate(crossover_table, headers=headers, tablefmt="pipe"))
            # print(f"Crossover Rate: {crossover_or_not}")
            print("\n")

            if crossover_or_not < CROSSOVER_PROB:
                child1, child2 = crossover(parent1, parent2)
                child_table = [[child1, child2]]
                headers = ["Child 1", "Child 2"]
                print(tabulate(child_table, headers=headers, tablefmt="pipe"))
                print("\n")
                # print(f"Child 1: {child1}, Child 2: {child2}")

                child1_copy , child2_copy = child1, child2

                child1 = mutation(child1)
                child2 = mutation(child2)
                print("\n")

                # check if the new chromosomes are valid
                # if not, generate a new one but keep the best one
                # uncomment the code below to use this feature if it is necessary
                if not valid_chromosome(child1):
                    child1 = generate_chromosome()
                    while not valid_chromosome(child1):
                        child1 = generate_chromosome()

                if not valid_chromosome(child2):
                    child2 = generate_chromosome()
                    while not valid_chromosome(child2):
                        child2 = generate_chromosome()

                # verificar si hubo cambios en los hijos
                if child1 != child1_copy or child2 != child2_copy:
                    child_table = [[child1, child2]]
                    headers = ["Child 1", "Child 2"]
                    print(tabulate(child_table, headers=headers, tablefmt="pipe"))
                    print("\n")
                

                
                new_chrom1 = best_chromosome(parent1, child1)
                new_chrom2 = best_chromosome(parent2, child2)

                new_population.append(new_chrom1)
                new_population.append(new_chrom2)

            else:
                new_population.append(parent1)
                new_population.append(parent2)

        population = new_population
        print_population(population)
