# Introduction
Ecology simulator written in Python for Reddit programming challenge.

More info: https://www.reddit.com/r/dailyprogrammer/comments/27h53e/662014_challenge_165_hard_simulated_ecology_the/

# Entities
There are 3 `entity` types:
`Tree` (3 stages: sapling, tree, elder tree),
`Lumberjack`,
`Bear`.

# Forest
The forest is a 2-dimensional array. The size is N x N. 

The map is randomly populated with predefined percentages in `populate()` method (0.5 = 50% of the forest area).

# Time
The simulation cycles by months (`tick`). 12 ticks = a year. Events happen monthly/yearly.

The simulation ends when month M is reached or there are no trees left in the forest.

# Trees
Trees (Tree object with `stage` 1+) have a 10% chance to spawn a new sapling in a random open space adjacent to the tree.
Elder trees have a 20% chance to spawn a new sapling.

After 12 months of being in existence, sapling matures into a tree. After 10 years (120 ticks) the tree becomes elder tree.

# Lumberjacks
Lumberjacks wander every month for up to 3 times to a random adjacent spot in any direction. When he encounters a tree, he will chop the tree down, gain `lumber` (1 for a tree, 2 for an elder tree) and the wandering for this month ends.

# Bears
Bears wander every month for up to 5 times. If a bear encounters a lumberjack, there will be `maw` event and bear's wandering for this month ends. Lumberjack will be removed from the forest.

# Yearly events
The program tracks yearly lumber harvested and the number of maw accidents. 

If `yearly lumber >= number of lumberjacks`, new lumberjack(s) are randomly spawned. The formula is: `yearlyLumber/10` rounded down (e.g. 39/10 = 3 lumberjacks to be hired). If yearly lumber is lower than the number of lumberjacks, 1 random lumberjack is removed from the forest.

If there has been atleast one maw event during the year, 1 random bear is removed from the forest, otherwise 1 bear will be randomly spawned.

If there is only one lumberjack left and he is mawed, new lumberjack will be spawned in a random spot.
