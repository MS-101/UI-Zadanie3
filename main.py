import random
import copy


class Stone:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class Garden:
    def __init__(self, width, height, stones):
        self.width = width
        self.height = height
        self.stones = stones

        self.arr = self.get_arr()

    def get_arr(self):
        arr = []

        for pos_y in range(0, self.height):
            arr.append([])

            for pos_x in range(0, self.width):
                arr[pos_y].append(0)

        for stone in self.stones:
            arr[stone.pos_y][stone.pos_x] = -1

        return arr


class Monk:
    def __init__(self, genes, fitness, garden, entrance_count, turn_count):
        self.genes = genes
        self.fitness = fitness
        self.garden = garden

        self.entrance_count = entrance_count
        self.turn_count = turn_count


def get_stone_id(pos_x, pos_y, stones):
    stone_id = 0

    for stone in stones:
        if pos_x == stone.pos_x and pos_y == stone.pos_y:
            return stone_id

        stone_id += 1

    return -1


def turn(move_direction, turn_direction, cur_pos_x, cur_pos_y, garden):
    # move left, then right
    if (move_direction == "down" and turn_direction == "right") \
            or (move_direction == "up" and turn_direction == "left"):
        if cur_pos_x == 0:
            return "ok", -1, -1
        elif garden.arr[cur_pos_y][cur_pos_x - 1] == 0:
            cur_pos_x = cur_pos_x - 1
            cur_pos_y = cur_pos_y
            move_direction = "left"

            return move_direction, cur_pos_x, cur_pos_y
        elif cur_pos_x == garden.width - 1:
            return "ok", -1, -1
        elif garden.arr[cur_pos_y][cur_pos_x + 1] == 0:
            cur_pos_x = cur_pos_x + 1
            cur_pos_y = cur_pos_y
            move_direction = "right"

            return move_direction, cur_pos_x, cur_pos_y
        else:
            return "error", -1, -1
    # move right, then left
    if (move_direction == "down" and turn_direction == "left") \
            or (move_direction == "up" and turn_direction == "right"):
        if cur_pos_x == garden.width - 1:
            return "ok", -1, -1
        elif garden.arr[cur_pos_y][cur_pos_x + 1] == 0:
            cur_pos_x = cur_pos_x + 1
            cur_pos_y = cur_pos_y
            move_direction = "right"

            return move_direction, cur_pos_x, cur_pos_y
        elif cur_pos_x == 0:
            return "ok", -1, -1
        elif garden.arr[cur_pos_y][cur_pos_x - 1] == 0:
            cur_pos_x = cur_pos_x - 1
            cur_pos_y = cur_pos_y
            move_direction = "left"

            return move_direction, cur_pos_x, cur_pos_y
        else:
            return "error", -1, -1
    # move up, then down
    if (move_direction == "left" and turn_direction == "right") \
            or (move_direction == "right" and turn_direction == "left"):
        if cur_pos_y == 0:
            return "ok", -1, -1
        elif garden.arr[cur_pos_y - 1][cur_pos_x] == 0:
            cur_pos_x = cur_pos_x
            cur_pos_y = cur_pos_y - 1
            move_direction = "up"

            return move_direction, cur_pos_x, cur_pos_y
        elif cur_pos_y == garden.height - 1:
            return "ok", -1, -1
        elif garden.arr[cur_pos_y + 1][cur_pos_x] == 0:
            cur_pos_x = cur_pos_x
            cur_pos_y = cur_pos_y + 1
            move_direction = "down"

            return move_direction, cur_pos_x, cur_pos_y
        else:
            return "error", -1, -1
    # move down, then up
    if (move_direction == "left" and turn_direction == "left") \
            or (move_direction == "right" and turn_direction == "right"):
        if cur_pos_y == garden.height - 1:
            return "ok", -1, -1
        elif garden.arr[cur_pos_y + 1][cur_pos_x] == 0:
            cur_pos_x = cur_pos_x
            cur_pos_y = cur_pos_y + 1
            move_direction = "down"

            return move_direction, cur_pos_x, cur_pos_y
        elif cur_pos_y == 0:
            return "ok", -1, -1
        elif garden.arr[cur_pos_y - 1][cur_pos_x] == 0:
            cur_pos_x = cur_pos_x
            cur_pos_y = cur_pos_y - 1
            move_direction = "up"

            return move_direction, cur_pos_x, cur_pos_y
        else:
            return "error", -1, -1


def sweep_garden(movement_id, entrance_gene, turn_genes, garden):
    # read entrance gene
    if entrance_gene > 0:
        if entrance_gene <= garden.width:
            move_direction = "down"

            start_pos_x = entrance_gene - 1
            start_pos_y = 0
        else:
            move_direction = "right"

            start_pos_x = 0
            start_pos_y = entrance_gene - garden.width - 1
    else:
        if abs(entrance_gene) <= garden.width:
            move_direction = "up"

            start_pos_x = abs(entrance_gene) - 1
            start_pos_y = garden.height - 1
        else:
            move_direction = "left"

            start_pos_x = garden.width - 1
            start_pos_y = abs(entrance_gene) - garden.width - 1

    # read turn genes
    left_turn_counter = 0
    right_turn_counter = 0

    for turn_gene in turn_genes:
        if turn_gene == 0:
            left_turn_counter += 1
        else:
            right_turn_counter += 1

    if left_turn_counter < right_turn_counter:
        default_turn_direction = "left"
    else:
        default_turn_direction = "right"

    # start movement
    if garden.arr[start_pos_y][start_pos_x] != 0:
        if move_direction == "left":
            if garden.arr[start_pos_y][0] == 0:
                move_direction = "right"
                start_pos_x = 0
            else:
                return False, "ok"
        elif move_direction == "right":
            if garden.arr[start_pos_y][garden.width - 1] == 0:
                move_direction = "left"
                start_pos_x = garden.width - 1
            else:
                return False, "ok"
        elif move_direction == "up":
            if garden.arr[0][start_pos_x] == 0:
                move_direction = "down"
                start_pos_y = 0
            else:
                return False, "ok"
        elif move_direction == "down":
            if garden.arr[garden.height - 1][start_pos_x] == 0:
                move_direction = "up"
                start_pos_y = garden.height - 1
            else:
                return False, "ok"

    garden.arr[start_pos_y][start_pos_x] = movement_id

    cur_pos_x = start_pos_x
    cur_pos_y = start_pos_y

    while True:
        if move_direction == "left":
            # movement is out of range
            if cur_pos_x == 0:
                return True, "ok"

            # movement is legal
            if garden.arr[cur_pos_y][cur_pos_x - 1] == 0:
                garden.arr[cur_pos_y][cur_pos_x - 1] = movement_id

                cur_pos_x = cur_pos_x - 1
                cur_pos_y = cur_pos_y
            # movement is blocked by stone
            elif garden.arr[cur_pos_y][cur_pos_x - 1] == -1:
                stone_id = get_stone_id(cur_pos_x - 1, cur_pos_y, garden.stones)

                if stone_id == -1:
                    return True, "error"

                # first turn left
                if turn_genes[stone_id] == 0:
                    move_direction, cur_pos_x, cur_pos_y = turn(move_direction, "left", cur_pos_x, cur_pos_y,
                                                                garden)

                    if move_direction == "error":
                        return True, "error"
                    if move_direction == "ok":
                        return True, "ok"

                    garden.arr[cur_pos_y][cur_pos_x] = movement_id
                # first turn right
                else:
                    move_direction, cur_pos_x, cur_pos_y = turn(move_direction, default_turn_direction, cur_pos_x,
                                                                cur_pos_y, garden)

                    if move_direction == "error":
                        return True, "error"
                    if move_direction == "ok":
                        return True, "ok"

                    garden.arr[cur_pos_y][cur_pos_x] = movement_id
            # movement is blocked by previous movement
            elif garden.arr[cur_pos_y][cur_pos_x - 1] > 0:
                move_direction, cur_pos_x, cur_pos_y = turn(move_direction, default_turn_direction, cur_pos_x,
                                                            cur_pos_y, garden)

                if move_direction == "error":
                    return True, "error"
                if move_direction == "ok":
                    return True, "ok"

                garden.arr[cur_pos_y][cur_pos_x] = movement_id

        elif move_direction == "right":
            # movement is out of range
            if cur_pos_x == garden.width - 1:
                return True, "ok"

            # movement is legal
            if garden.arr[cur_pos_y][cur_pos_x + 1] == 0:
                garden.arr[cur_pos_y][cur_pos_x + 1] = movement_id

                cur_pos_x = cur_pos_x + 1
                cur_pos_y = cur_pos_y
            # movement is blocked by stone
            elif garden.arr[cur_pos_y][cur_pos_x + 1] == -1:
                stone_id = get_stone_id(cur_pos_x + 1, cur_pos_y, garden.stones)

                if stone_id == -1:
                    return True, "error"

                # first turn left
                if turn_genes[stone_id] == 0:
                    move_direction, cur_pos_x, cur_pos_y = turn(move_direction, "left", cur_pos_x, cur_pos_y,
                                                                garden)

                    if move_direction == "error":
                        return True, "error"
                    if move_direction == "ok":
                        return True, "ok"

                    garden.arr[cur_pos_y][cur_pos_x] = movement_id
                # first turn right
                else:
                    move_direction, cur_pos_x, cur_pos_y = turn(move_direction, default_turn_direction, cur_pos_x,
                                                                cur_pos_y, garden)

                    if move_direction == "error":
                        return True, "error"
                    if move_direction == "ok":
                        return True, "ok"

                    garden.arr[cur_pos_y][cur_pos_x] = movement_id
            # movement is blocked by previous movement
            elif garden.arr[cur_pos_y][cur_pos_x + 1] > 0:
                move_direction, cur_pos_x, cur_pos_y = turn(move_direction, default_turn_direction, cur_pos_x,
                                                            cur_pos_y, garden)

                if move_direction == "error":
                    return True, "error"
                if move_direction == "ok":
                    return True, "ok"

                garden.arr[cur_pos_y][cur_pos_x] = movement_id

        elif move_direction == "up":
            # movement is out of range
            if cur_pos_y == 0:
                return True, "ok"

            # movement is legal
            if garden.arr[cur_pos_y - 1][cur_pos_x] == 0:
                garden.arr[cur_pos_y - 1][cur_pos_x] = movement_id

                cur_pos_x = cur_pos_x
                cur_pos_y = cur_pos_y - 1
            # movement is blocked by stone
            elif garden.arr[cur_pos_y - 1][cur_pos_x] == -1:
                stone_id = get_stone_id(cur_pos_x, cur_pos_y - 1, garden.stones)

                if stone_id == -1:
                    return True, "error"

                # first turn left
                if turn_genes[stone_id] == 0:
                    move_direction, cur_pos_x, cur_pos_y = turn(move_direction, "left", cur_pos_x, cur_pos_y,
                                                                garden)

                    if move_direction == "error":
                        return True, "error"
                    if move_direction == "ok":
                        return True, "ok"

                    garden.arr[cur_pos_y][cur_pos_x] = movement_id
                # first turn right
                else:
                    move_direction, cur_pos_x, cur_pos_y = turn(move_direction, default_turn_direction, cur_pos_x,
                                                                cur_pos_y, garden)

                    if move_direction == "error":
                        return True, "error"
                    if move_direction == "ok":
                        return True, "ok"

                    garden.arr[cur_pos_y][cur_pos_x] = movement_id
            # movement is blocked by previous movement
            elif garden.arr[cur_pos_y - 1][cur_pos_x] > 0:
                move_direction, cur_pos_x, cur_pos_y = turn(move_direction, default_turn_direction, cur_pos_x,
                                                            cur_pos_y, garden)

                if move_direction == "error":
                    return True, "error"
                if move_direction == "ok":
                    return True, "ok"

                garden.arr[cur_pos_y][cur_pos_x] = movement_id

        elif move_direction == "down":
            # movement is out of range
            if cur_pos_y == garden.height - 1:
                return True, "ok"

            # movement is legal
            if garden.arr[cur_pos_y + 1][cur_pos_x] == 0:
                garden.arr[cur_pos_y + 1][cur_pos_x] = movement_id

                cur_pos_x = cur_pos_x
                cur_pos_y = cur_pos_y + 1
            # movement is blocked by stone
            elif garden.arr[cur_pos_y + 1][cur_pos_x] == -1:
                stone_id = get_stone_id(cur_pos_x, cur_pos_y + 1, garden.stones)

                if stone_id == -1:
                    return True, "error"

                # first turn left
                if turn_genes[stone_id] == 0:
                    move_direction, cur_pos_x, cur_pos_y = turn(move_direction, "left", cur_pos_x, cur_pos_y,
                                                                garden)

                    if move_direction == "error":
                        return True, "error"
                    if move_direction == "ok":
                        return True, "ok"

                    garden.arr[cur_pos_y][cur_pos_x] = movement_id
                # first turn right
                else:
                    move_direction, cur_pos_x, cur_pos_y = turn(move_direction, default_turn_direction, cur_pos_x,
                                                                cur_pos_y, garden)

                    if move_direction == "error":
                        return True, "error"
                    if move_direction == "ok":
                        return True, "ok"

                    garden.arr[cur_pos_y][cur_pos_x] = movement_id
            # movement is blocked by previous movement
            elif garden.arr[cur_pos_y + 1][cur_pos_x] > 0:
                move_direction, cur_pos_x, cur_pos_y = turn(move_direction, default_turn_direction, cur_pos_x,
                                                            cur_pos_y, garden)

                if move_direction == "error":
                    return True, "error"
                if move_direction == "ok":
                    return True, "ok"

                garden.arr[cur_pos_y][cur_pos_x] = movement_id


def get_fitness(genes, garden):
    fitness = 0

    entrance_count = garden.width + garden.height
    turn_genes = genes[entrance_count:]

    entrance_id = 1
    for i in range(0, entrance_count):
        entrance_gene = genes[i]
        has_moved, end_message = sweep_garden(entrance_id, entrance_gene, turn_genes, garden)

        if end_message == "error":
            break

        if has_moved is True:
            entrance_id += 1

    for pos_y in range(0, garden.height):
        for pos_x in range(0, garden.width):
            if garden.arr[pos_y][pos_x] > 0:
                fitness += 1

    return garden, fitness


def print_genes(genes):
    is_first = True

    for gene in genes:
        if is_first is False:
            print("|", end="")
        else:
            is_first = False

        print(str(gene), end="")

    print()


def generate_genes(garden):
    genes = []

    entrance_count = garden.width + garden.height
    for i in range(0, entrance_count):
        entrance_gene = random.randint(1, entrance_count)

        random_num = random.randrange(100)
        if random_num < 50:
            entrance_gene *= -1

        genes.append(entrance_gene)

    turn_count = len(garden.stones)
    for i in range(0, turn_count):
        random_num = random.randrange(100)

        if random_num < 50:
            turn_gene = 0
        else:
            turn_gene = 1

        genes.append(turn_gene)

    return genes


def print_garden(garden):
    for pos_y in range(0, garden.height):
        for pos_x in range(0, garden.width):
            if garden.arr[pos_y][pos_x] == -1:
                print("KK", end="")
            elif garden.arr[pos_y][pos_x] < 10:
                print("0" + str(garden.arr[pos_y][pos_x]), end="")
            else:
                print(garden.arr[pos_y][pos_x], end="")

            if pos_x < garden.width - 1:
                print(" ", end="")

        print()


def get_garden_from_file(input_file_name):
    input_file = open("Input/" + input_file_name, "r")

    width = 0
    height = 0
    stones = []

    is_first_line = True

    for line in input_file:
        words = line.split()

        if is_first_line is True:
            width = int(words[0])
            height = int(words[1])

            is_first_line = False

            continue

        pos_x = int(words[0])
        pos_y = int(words[1])

        new_stone = Stone(pos_x - 1, pos_y - 1)
        stones.append(new_stone)

    new_garden = Garden(width, height, stones)

    return new_garden


def roulette_selection(generation):
    generation_temp = generation.copy()

    parents = []
    roulette = []

    for picked_monk in generation_temp:
        for i in range(0, picked_monk.fitness):
            roulette.append(picked_monk)

    for i in range(0, 2):
        parents.append(random.choice(generation))

    return parents[0], parents[1]


def tournament_selection(generation):
    parents = []

    for i in range(0, 2):
        generation_temp = generation.copy()

        participants = []
        for i in range(0, 3):
            new_participant = random.choice(generation_temp)
            generation_temp.remove(new_participant)
            participants.append(new_participant)

        winner = participants[0]
        for i in range(1, 3):
            if participants[i].fitness > winner.fitness:
                winner = participants[i]

        parents.append(winner)

    return parents[0], parents[1]


def crossover(parent1, parent2):
    genes_count = len(parent1.genes)

    split_point = random.randint(1, genes_count - 2)

    child_genes = []

    random_num = random.randrange(100)

    if random_num < 50:
        for i in range(0, split_point):
            child_genes.append(parent1.genes[i])

        for i in range(split_point, genes_count):
            child_genes.append(parent2.genes[i])
    else:
        for i in range(0, split_point):
            child_genes.append(parent2.genes[i])

        for i in range(split_point, genes_count):
            child_genes.append(parent1.genes[i])

    return child_genes


def mutate(genes, entrance_count):
    for gene_id in range(0, len(genes)):
        random_num = random.randrange(100)

        # 2 % chance to mutate
        if random_num < 2:
            if gene_id < entrance_count:
                new_gene_val = random.randint(1, entrance_count)

                while genes[gene_id] == new_gene_val:
                    new_gene_val = random.randint(1, entrance_count)
            else:
                if genes[gene_id] == 0:
                    new_gene_val = 1
                else:
                    new_gene_val = 0

            genes[gene_id] = new_gene_val


while True:
    inputFileName = input("Zadajte názov vstupného súboru (s príponou): ")

    try:
        inputFile = open("Input/" + inputFileName, "r")
        inputFile.close()
        break
    except IOError:
        print("Zadaný súbor neexistuje!")

while True:
    inputMethod = input("Zadajte metódu výberu rodičov (A - ruleta, B - turnaj): ")
    inputMethod = inputMethod.upper()

    if inputMethod == "A" or inputMethod == "B":
        break
    else:
        print("Bol zadaný nesprávny vstup!")

print()

myGarden = get_garden_from_file(inputFileName)

entranceCount = myGarden.width + myGarden.height
turnCount = len(myGarden.stones)

"""
print("Garden:")
print_garden(myGarden)
print()
"""


# create first generation
curGeneration = []
for generationID in range(0, 10):
    monkGenes = generate_genes(myGarden)
    monkGarden, monkFitness = get_fitness(monkGenes, copy.deepcopy(myGarden))
    myMonk = Monk(monkGenes, monkFitness, monkGarden, entranceCount, turnCount)

    curGeneration.append(myMonk)

"""
print("First generation:")
for pickedMonk in curGeneration:
    print("Genes: ", end="")
    print_genes(pickedMonk.genes)
    # print_garden(pickedMonk.garden)
    print("Fitness = " + str(pickedMonk.fitness))
print()
"""

for generationID in range(0, 50):
    newGeneration = []
    for i in range(0, 20):
        if inputMethod == "A":
            parent1, parent2 = roulette_selection(curGeneration)
        else:
            parent1, parent2 = tournament_selection(curGeneration)
        childGenes = crossover(parent1, parent2)
        mutate(childGenes, entranceCount)
        childGarden, childFitness = get_fitness(childGenes, copy.deepcopy(myGarden))

        newChild = Monk(childGenes, childFitness, childGarden, entranceCount, turnCount)
        newGeneration.append(newChild)

    curGeneration = newGeneration

    """
    print("Generation " + str(generationID + 1) + ":")
    for pickedMonk in curGeneration:
        print("Genes: ", end="")
        print_genes(pickedMonk.genes)
        # print_garden(pickedMonk.garden)
        print("Fitness = " + str(pickedMonk.fitness))
    print()
    """

bestMonk = curGeneration[0]
for i in range(1, len(curGeneration)):
    if curGeneration[i].fitness > bestMonk.fitness:
        bestMonk = curGeneration[i]

print("Výsledný mních:")
print_genes(bestMonk.genes)
print("Fitness - " + str(bestMonk.fitness))
print()

print_garden(bestMonk.garden)
print()
