from random import choice, randint

directions = [(-1, -1),
              (0, -1),
              (1, -1),
              (-1, 0),
              (1, 0),
              (-1, 1),
              (0, 1),
              (1, 1)]


class Entity(object):

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def choose_spot(self, strArray):

        spots = []

        for d in directions:
            x = self.x + d[0]
            y = self.y + d[1]

            if (x >= 0) and (x < N) and (y >= 0) and (y < N):

                if str(forest[y][x]) in strArray:
                    spots.append(d)

        if len(spots) > 0:
            spot = choice(spots)
            return self.x + spot[0], self.y + spot[1]

        return None

    def move(self, moves, entityList):

        while moves > 0:

            spot = self.choose_spot(entityList)

            if spot is not None:

                x, y = spot

                forest[self.y][self.x] = ' '
                self.x, self.y = x, y

                if isinstance(self, Lumberjack):

                    # Chop tree
                    if isinstance(forest[y][x], Tree):

                        if str(forest[y][x]) == 'T':
                            lumber = 1
                        else:
                            lumber = 2

                        self.lumber += lumber
                        trees.remove(forest[y][x])
                        forest[y][x] = self
                        return lumber

                elif isinstance(self, Bear):

                    # Maw accident
                    if isinstance(forest[y][x], Lumberjack):
                        lumberjacks.remove(forest[y][x])
                        forest[y][x] = self

                        return 1

                forest[y][x] = self
                moves -= 1

            # If there are no possible moves, break the loop
            else:
                break

        return 0


class Tree(Entity):

    def __init__(self, x, y, age, stage):

        super(Tree, self).__init__(x, y)
        self.age = age
        self.stage = stage  # 0 - sapling, 1 - tree, 2 - elder tree

    def __str__(self):

        if self.stage == 0:
            return 'S'
        elif self.stage == 1:
            return 'T'
        else:
            return 'E'

    def grow(self):

        self.age += 1
        if (self.age == 12) or (self.age == 120):
            self.stage += 1

    def spawn(self):

        if self.stage > 0:

            if randint(1, 10) <= self.stage:
                spot = self.choose_spot([' '])

                if spot is not None:
                    x, y = spot
                    sapling = Tree(x, y, 0, 0)
                    forest[y][x] = sapling
                    trees.append(sapling)


class Lumberjack(Entity):

    def __init__(self, x, y):

            super(Lumberjack, self).__init__(x, y)
            self.lumber = 0

    def __str__(self):
        return 'L'


class Bear(Entity):

    def __init__(self, x, y):
        super(Bear, self).__init__(x, y)

    def __str__(self):
        return 'B'


def month_tick():

    lumberThisMonth = 0
    mawsThisMonth = 0

    for t in trees:
        t.spawn()
        t.grow()

    for l in lumberjacks:
        lumberThisMonth += l.move(3, [' ', 'T', 'E'])

    for b in bears:
        mawsThisMonth += b.move(5, [' ', 'L'])

    # Never let lumberjack population drop to 1
    global lumberjacks
    if len(lumberjacks) == 0:
            lumberjacks = add_objects('lumberjack', 1, lumberjacks)

    print_forest()

    return lumberThisMonth, mawsThisMonth


def populate():

    trees = add_objects('tree', N**2 * 0.5, [])
    lumberjacks = add_objects('lumberjack', N**2 * 0.1, [])
    bears = add_objects('bear', N**2 * 0.02, [])

    return trees, lumberjacks, bears


def add_objects(otype, amount, array):

    for i in range(int(amount)):

        while True:
            x = randint(0, N-1)
            y = randint(0, N-1)

            if forest[y][x] == ' ':

                if otype == 'tree':
                    obj = Tree(x, y, 12, 1)
                elif otype == 'lumberjack':
                    obj = Lumberjack(x, y)
                else:
                    obj = Bear(x, y)

                forest[y][x] = obj
                array.append(obj)
                break

    return array


def print_forest():

    data1 = (currentMonth, len(trees), len(lumberjacks), len(bears))
    data2 = (lumberTotal, mawsTotal)

    print 'Month: %d\nTrees: %d\nLumberjacks: %d\nBears: %d' % (data1)
    print 'Total lumber harvested: %d\nTotal maw accidents: %d\n' % (data2)

    for row in forest:
        print ' '.join(map(str, row))

    print '\n'


def print_ascii(year):

    final = ''

    # Add bears, trees and lumberjacks to final graph
    final += calc_data(len(bears), 'B')
    final += calc_data(len(trees), 'T')
    final += calc_data(len(lumberjacks), 'L')

    for i in range(50-len(final)):
        final += '_'

    print 'Year ', year, ': [', final, ']'


def calc_data(amount, string):

    result = ''
    percent = amount * 50/N**2

    for i in range(percent):
        result += string

    return result


N = 10
M = 4800
forest = [[' ' for _ in range(N)] for _ in range(N)]
trees, lumberjacks, bears = populate()

currentMonth = 1

lumberThisYear = 0
mawsThisYear = 0

lumberTotal = 0
mawsTotal = 0

while (currentMonth <= M) and (len(trees) > 0):

    lumber, maws = month_tick()

    lumberThisYear += lumber
    mawsThisYear += maws

    lumberTotal += lumber
    mawsTotal += maws

    if currentMonth % 12 == 0:

        if lumberThisYear > len(lumberjacks):
            toHire = int(lumberThisYear/10)
            lumberjacks = add_objects('lumberjack', toHire, lumberjacks)
            print 'Hired ', toHire, ' lumberjacks'

        # Fire random lumberjack
        else:
            if len(lumberjacks) > 0:
                l = choice(lumberjacks)
                x, y = l.x, l.y
                forest[y][x] = ' '
                lumberjacks.remove(l)

        # If no maw accidents, spawn a bear
        if mawsThisYear == 0:
            bears = add_objects('bear', 1, bears)

        else:
            b = choice(bears)
            x, y = b.x, b.y
            forest[y][x] = ' '
            bears.remove(b)

        # Never let lumberjack population drop below 1
        if len(lumberjacks) == 0:
            lumberjacks = add_objects('lumberjack', 1, lumberjacks)

        # Reset counters
        lumberThisYear = 0
        mawsThisYear = 0

        print_ascii(currentMonth/12)

    currentMonth += 1

print '*** END OF SIMULATION ***'
print_ascii(int(currentMonth/12) + 1)
print_forest()
