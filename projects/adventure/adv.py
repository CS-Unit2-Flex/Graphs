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
visited = {}

past_rooms = []
opposites = {'n' : 's', 
            's' : 'n', 
            'e' : 'w', 
            'w' : 'e'
            }
# Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels, and logs that direction, then loops. This should cause your player to walk a depth-first traversal. When you reach a dead-end, walk back to the nearest room that does contain an unexplored path. 

reverse_path = []

def dft(room):
    # Pick a random room
    exits = room.get_exits()

    random.shuffle(exits)

    next_direction = exits[0]

    s = deque()
    s.append(next_direction)
    print(s)
    # print(s)
    last_room = 0
    if len(past_rooms) > 0:
        last_room = past_rooms[-1]
    
    traversal_path.append(next_direction)
    while len(s) > 0:
        r = s.pop()
        # traversal_path.append(r)
        print(next_direction, 'next direction')
        print(traversal_path, 'traversal path')
        if room.id not in visited:
            visited[room.id] = {}
            for e in room.get_exits():
                visited[room.id][e] = '?'
            for neighbor in room.get_exits():
                s.append(neighbor)
            if len(traversal_path) > 1:
                visited[room.id][opposites.get(traversal_path[-2])] = last_room
                visited[last_room][traversal_path[-2]] = room.id
            player.travel(next_direction)
            # return dft(room)
        # else:
            # visited[last_room][opposites.get(traversal_path[-1])] = room.id
        if len(exits) <= 1:
            bfs(next_direction, room)
    past_rooms.append(room.id)
    reverse_path.append(opposites.get(next_direction))
    return next_direction

def bfs(direction, room): 
    print(f"WE MADE IT HERE!!!!!")
    while len(reverse_path) > 0:
        next_direction = reverse_path.pop()
        player.travel(next_direction)
        traversal_path.append(next_direction)
        past_rooms.append(room.id)




r = 0
while r < 6:
# while len(visited) < len(room_graph):
    player.current_room.print_room_description(player)

    print('CURRENT ROOM', player.current_room.id)

    exits = player.current_room.get_exits()

    # if len(exits) == 1:
    #     visited[player.current_room.id][exits[0]] = past_rooms[-1]
    #     bfs(exits[0], player.current_room)

    last_direction = dft(player.current_room)

    # if len(past_rooms) == 1:
    #     visited[past_rooms[-1]][last_direction] = player.current_room.id
    # if len(past_rooms) > 1:
    #     visited[past_rooms[-1]][last_direction] = player.current_room.id
    #     visited[player.current_room.id][opposites.get(last_direction)] = past_rooms[-1]
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
