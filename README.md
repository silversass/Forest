# Forest
Ecology simulator written in Python for Reddit programming challenge

# Entities
There are 3 entity types:
Tree (3 stages: sapling, tree, elder tree)
Lumberjack
Bear

# World
The forest is a 2-dimensional array. The size is N x N. 
The map is randomly populated with predefined percentages in populate() method (0.5 = 50% of the forest area).

# Time
The simulation cycles by months (ticks). 12 ticks = a year. Events happen monthly/yearly.
The simulation ends when month M is reached or there are no trees left in the forest.

# Trees
Trees (Tree object with stage 1+) have a 10% chance to spawn a new sapling in a random open space adjacent to the tree.
Elder trees have a 20% chance to spawn a new sapling.
After 12 months of being in existence, sapling matures into a tree. After 10 years (120 ticks) the tree becomes elder tree.

# Lumberjacks
Lumberjacks wander every month for up to 3 times to a random adjacent spot in any direction. When he encounters a tree, he will chop the tree down, gain lumber (1 for a tree, 2 for an elder tree) and the wandering for this month ends.

# Bears
Bears wander every month for up to 5 times. If a bear encounters a lumberjack, there will be 'maw' event and bear's wandering for this month ends. Lumberjack will be removed from the forest.

# Yearly events
The program tracks yearly lumber harvested and the number of maw accidents. 
If yearly lumber >= number of lumberjacks, new lumberjack(s) are randomly spawned. The formula is: yearlyLumber/10 rounded down (e.g. 39/10 = 3 lumberjacks to be hired). If yearly lumber is lower than the number of lumberjacks, 1 random lumberjack is removed from the forest.
If there has been atleast one maw event during the year, 1 random bear is removed from the forest, otherwise 1 bear will be randomly spawned.
If there is only one lumberjack left and he is mawed, new lumberjack will be spawned in a random spot.

# Example
Sample output for a 20x20 map with M = 480 (40 years):

*** END OF SIMULATION ***
Year  40 : [ TTTTTTTTLLL_______________________________________ ]
Month: 481
Trees: 67
Lumberjacks: 26
Bears: 0
Total lumber harvested: 1418
Total maw accidents: 110

              L             L          
        L           L                  
  L                                    
                                       
        L                     L        
                    L                  
                                       
        L                   L   L      
                L                      
        L           L   L              
  L             L                 S   S
                            T L   S T T
              T S   L     L     S   S S
              T S S   S S L L S S      
      S S S S S T T T   S L   S   S   T
        T T T T S S T T S              
      S S T L T L S T S S       T      
        T S     S T T T S   T S        
                    T T S   L T S      
        T   T       T S S              
