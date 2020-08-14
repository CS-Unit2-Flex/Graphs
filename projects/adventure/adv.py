from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels, and logs that direction, then loops. This should cause your player to walk a depth-first traversal. When you reach a dead-end, walk back to the nearest room that does contain an unexplored path. 

visited = {} # Copy of dictionary

past_rooms = []

opposites = {'n' : 's', 
            's' : 'n', 
            'e' : 'w', 
            'w' : 'e'
            }

reverse_path = []

rooms_with_unexplored_directions = deque()

def pick_random_room(l):
    random.shuffle(l)
    return l[0]

def dft(room):
    # Pick a random room
    exits = room.get_exits()

    print(visited)
    print(f"\n {reverse_path}\n")
    print(f"\n {past_rooms}\n")

    random.shuffle(exits)
    next_direction = exits[0]

    if len(reverse_path) > 0 and len(exits) > 1:
        if next_direction == reverse_path[-1]:
            next_direction = exits[1]


    s = deque()
    s.append(next_direction)
    # print(s)
    last_room = 0
    if len(past_rooms) > 0:
        last_room = past_rooms[-1]
    
    # If there are more than 2 unexplored directions in a room, append it to the list
    if len(exits) > 2:
        rooms_with_unexplored_directions.append(room.id)

    traversal_path.append(next_direction)
    reverse_path.append(opposites.get(next_direction))

    while len(s) > 0:
        # direction for the player to travel next
        r = s.pop()

        # If the room is not in visited, create its entry
        if room.id not in visited:
            visited[room.id] = {}
            for e in room.get_exits():
                visited[room.id][e] = '?'
            for neighbor in room.get_exits():
                s.append(neighbor)
            # If a room value already exists for a direction, don't overwrite it
            if len(traversal_path) > 1:
                if isinstance(opposites.get(traversal_path[-2]), int):
                    continue
                else:
                    visited[room.id][opposites.get(traversal_path[-2])] = last_room
                if isinstance(traversal_path[-2], int):
                    continue
                else:
                    visited[last_room][traversal_path[-2]] = room.id
            # player travels
            if len(exits) <= 1:
                return bfs(room)
            if len(rooms_with_unexplored_directions) > 1:
                if room.id == rooms_with_unexplored_directions[-1]:
                    return bfs(room)
            
        else:
            continue

        # If we hit a dead-end, do the breadth-first search

        player.travel(next_direction)
        past_rooms.append(room.id)
    return next_direction

def bfs(room): 
    print(f"WE MADE IT HERE!!!!!")
    stop = False
    if past_rooms[-1] == rooms_with_unexplored_directions[-1]:
        stop = True
    while stop is False:
        next_direction = reverse_path.pop()
        past_rooms.pop()
        player.travel(next_direction)
        # past_rooms.append(room.id)
        traversal_path.append(next_direction)
        print(room.id)
        # print(past_rooms, traversal_path)




r = 0
while r < 20:
# while len(visited) < len(room_graph):
    player.current_room.print_room_description(player)

    print('CURRENT ROOM', player.current_room.id)
    # print(past_rooms)

    last_direction = dft(player.current_room)

    print(rooms_with_unexplored_directions, 'unexplored paths')
    for room in rooms_with_unexplored_directions:
        # print(room, 'for loop')
        if '?' in visited[room].values():
            continue
        else:
            rooms_with_unexplored_directions.remove(room)

    r += 1

print(f"length of room graph: {len(room_graph)}")



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
    print(visited)



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
