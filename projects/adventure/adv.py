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

rooms_with_unexplored_directions = []
length_of_unknown = len(rooms_with_unexplored_directions)

def dft(room):
    # Pick a random room
    exits = room.get_exits()
    random.shuffle(exits)
    next_direction = exits[0]

    if len(reverse_path) > 0 and len(exits) > 1:
        if next_direction == reverse_path[-1]:
            next_direction = exits[1]

    s = deque()
    s.append(next_direction)
    last_room = 0
    if len(past_rooms) > 0:
        last_room = past_rooms[-1]
    
    # If there are more than 2 unexplored directions in a room, append it to the list
    if len(exits) > 2:
        rooms_with_unexplored_directions.append(room.id)

    # if len(past_rooms) > 0 and room.id == rooms_with_unexplored_directions[-1]:
    #     bfs(room)

    traversal_path.append(next_direction)
    reverse_path.append(opposites.get(next_direction))

    last_unknown = None
    if len(rooms_with_unexplored_directions) == 1:
        last_unknown = rooms_with_unexplored_directions[0]
    elif len(rooms_with_unexplored_directions) > 1:
        last_unknown = rooms_with_unexplored_directions[-1]


    print(f"Stack: {s}")
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
                    visited[last_room][traversal_path[-2]] = room.id
                if isinstance(traversal_path[-2], int):
                    continue
                else:
                    visited[last_room][traversal_path[-2]] = room.id
            # player travels
            if len(exits) <= 1:
                return bfs(room, length_of_unknown)
            player.travel(next_direction)
        # else:
        #     print('hello :D ')
        #     if len(traversal_path) > 1:
        #         if isinstance(opposites.get(traversal_path[-2]), int):
        #             continue
        #         else:
        #             visited[room.id][opposites.get(traversal_path[-2])] = last_room

        # If we hit a dead-end, do the breadth-first search

    past_rooms.append(room.id)
    return next_direction


def bfs(room, length_of_unknown): 
    print(f"WE MADE IT HERE!!!!!")
    print(reverse_path)
    while len(reverse_path) > length_of_unknown:
        next_direction = reverse_path.pop()
        # past_rooms.pop()
        player.travel(next_direction)
        # past_rooms.append(room.id)
        traversal_path.append(next_direction)



r = 0
while r < 20:
# while len(visited) < len(room_graph):
    print(rooms_with_unexplored_directions, 'unexplored')
    player.current_room.print_room_description(player)

    # dft(player.current_room)

    # last_unknown = rooms_with_unexplored_directions[-1]

    # Updates last room when loop is entered
    if player.current_room.id not in visited:
        dft(player.current_room)
    else:
        if len(traversal_path) > 0:
            if player.current_room.id == rooms_with_unexplored_directions[-1]:
                visited[past_rooms[-1]][traversal_path[-1]] = player.current_room.id
                bfs(player.current_room, length_of_unknown)

        dft(player.current_room)
        visited[past_rooms[-1]][traversal_path[-1]] = player.current_room.id

    for room in rooms_with_unexplored_directions:
        if '?' in visited[room].values():
            continue
        else:
            rooms_with_unexplored_directions.remove(room)

    r += 1



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
