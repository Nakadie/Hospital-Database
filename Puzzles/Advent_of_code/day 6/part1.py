# So, suppose you have a lanternfish with an internal timer value of 3:

# After one day, its internal timer would become 2.
# After another day, its internal timer would become 1.
# After another day, its internal timer would become 0.
# After another day, its internal timer would reset to 6, and it would create a new lanternfish with an internal timer of 8.
# After another day, the first lanternfish would have an internal timer of 5, and the second lanternfish would have an internal timer of 7.
# A lanternfish that creates a new fish resets its timer to 6, not 7 (because 0 is included as a valid timer value). The new lanternfish starts with an internal timer of 8 and does not start counting down until the next day.



txt = open('D:\python_projects\Advent_of_code\day 6\puzzle.txt', 'r')
txt = txt.read().splitlines()
txt = txt[0].split(',')
fish = [int(x) for x in txt]


for i in range(256):
    
    for i in range(len(fish)):
        
        #print(fish)
        if fish[i] == 0:
            fish.append(8)
            fish[i] = 6
        else:
            fish[i] -= 1
print(len(fish))
