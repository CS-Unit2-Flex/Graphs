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
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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

opposites = {'n' : 's', 
            's' : 'n', 
            'e' : 'w', 
            'w' : 'e'
            }

# Reverse path (basically acts almost like a queue)
reverse_path = deque()

past_rooms = []

starting_room_counter = 0

# Build dict entry (the defaultentry that has all "?'s")
def build_visited_entry(room):
    visited[room.id] = {}
    room_exits = room.get_exits()
    for e in room_exits:
        visited[room.id][e] = '?'

# Edge-case for the first entry in visited
if len(traversal_path) == 0 and player.current_room.id == 0:
    build_visited_entry(player.current_room)

# Depth-First-Traversal
def dft(room, unexplored_exits):
    # print(f"Room Id: {room.id}, \n Unexpected Array: {unexplored_exits}")
    previous_room = room.id # Keep track of previous room to update visited
    direction_to_travel = unexplored_exits.popleft() 
    player.travel(direction_to_travel) 
    next_room = player.current_room # keeps track of next room to update visited
    reverse_path.append(opposites.get(direction_to_travel))
    traversal_path.append(direction_to_travel)
    # Update the previous room's visited entry
    visited[previous_room][direction_to_travel] = next_room.id
    if next_room.id not in visited:
        build_visited_entry(next_room)
        visited[next_room.id][opposites.get(direction_to_travel)] = previous_room

    

# Breadth-First-Search



fork_rooms = []
# Where the main functionality takes place. Part of the dft takes place in here, since the deque() has to be a local variable here
while len(visited) < len(room_graph):
    # Lists the exits for the room
    room_exits = player.current_room.get_exits()

    # Fork Rooms
    if len(room_exits) == 4:
        print(player.current_room.id)
        if player.current_room.id not in room_exits:
            fork_rooms.append(player.current_room.id)
            print(fork_rooms)
        else:
            continue



    """
    ensw = 997
    nesw = 997
    senw = 997
    swen = 997
    esnw = 997
    swne = 997
    nsew = 1008
    snew = 1008
    wsne = 1005
    nwse = 1004
    wnse = 1005
    snwe = 1004
    nswe = 1004
    news = 1002
    enws = 1002
    wnes = 1005
    nwes = 1004
    ewns = 1002
    wens = 1005
    wesn = 1005
    ewsn = 1003
    wsen = 1005
    eswn = 1003
    sewn = 1003

    """

    # organized_directions = []

    # Instead of doing below, I might be able to use IDDFS or IDS
    # if player.current_room.id == 0:
    #     if 'e' in room_exits:
    #         organized_directions.append('e')
    #     if 'n' in room_exits:
    #         organized_directions.append('n')
    #     if 's' in room_exits:
    #         organized_directions.append('s')
    #     if 'w' in room_exits:
    #         organized_directions.append('w')
    # elif player.current_room.id == 1:
    #     if 's' in room_exits:
    #         organized_directions.append('s')
    #     if 'w' in room_exits:
    #         organized_directions.append('w')
    #     if 'n' in room_exits:
    #         organized_directions.append('n')
    #     if 'e' in room_exits:
    #         organized_directions.append('e')
    # else:
    #     # random.shuffle(room_exits)
    #     for e in room_exits:
    #         organized_directions.append(e)

    # print(organized_directions)
    # Shuffle the exits
    random.shuffle(room_exits)

    past_rooms.append(player.current_room.id)

    if player.current_room.id == 0:
        starting_room_counter += 1

    # dft Stack
    unexplored_exits = deque()

    # Assumes that room is already in dict and appends all directions with a "?" to the stack
    for e in room_exits:
        if visited[player.current_room.id][e] == '?':
            unexplored_exits.append(e)

    # If the stack is not empty, do a depth-first-traversal
    if len(unexplored_exits) > 0:
        dft(player.current_room, unexplored_exits)
    # Otherwise, do a Breadth-First-Search
    else:
        reverse_direction = reverse_path.pop()
        player.travel(reverse_direction)
        traversal_path.append(reverse_direction)
    

print(visited)
# print(past_rooms, len(past_rooms))





# 995 TRAVERSAL PATH
"""
[ 0, 8, 16, 8, 0, 4, 0, 1, 7, 9, 13, 14, 47, 14, 17, 46, 79, 106, 161, 166, 208, 307, 208, 166, 161, 106, 112, 124, 174, 277, 331, 387, 444, 387, 331, 277, 174, 221, 250, 295, 332, 351, 417, 442, 417, 351, 453, 351, 332, 295, 250, 289, 324, 391, 489, 491, 489, 391, 396, 391, 324, 411, 428, 452, 428, 429, 451, 429, 428, 411, 324, 289, 319, 441, 319, 289, 250, 221, 342, 357, 342, 221, 174, 124, 112, 210, 112, 106, 79, 46, 61, 63, 140, 63, 61, 82, 155, 185, 292, 316, 341, 316, 292, 185, 195, 185, 155, 82, 61, 46, 17, 28, 60, 64, 111, 114, 120, 114, 111, 121, 123, 138, 139, 176, 139, 147, 154, 192, 239, 336, 421, 336, 373, 336, 239, 255, 239, 192, 154, 184, 154, 147, 152, 233, 240, 304, 321, 334, 384, 435, 384, 334, 321, 354, 361, 366, 497, 366, 361, 354, 386, 388, 257, 163, 165, 169, 385, 169, 223, 483, 223, 169, 165, 197, 199, 281, 392, 408, 443, 477, 443, 408, 392, 281, 350, 425, 434, 425, 350, 281, 199, 318, 340, 374, 340, 318, 394, 422, 461, 422, 394, 426, 394, 318, 199, 197, 165, 163, 228, 253, 285, 253, 228, 163, 148, 121, 148, 178, 148, 121, 148, 163, 257, 388, 386, 354, 321, 304, 240, 233, 152, 196, 224, 287, 313, 287, 353, 380, 445, 480, 445, 446, 445, 380, 476, 380, 353, 287, 224, 196, 278, 338, 278, 196, 152, 147, 139, 138, 143, 138, 123, 121, 111, 64, 102, 107, 141, 175, 200, 204, 200, 328, 200, 175, 141, 107, 102, 64, 60, 28, 30, 28, 17, 33, 17, 14, 13, 15, 19, 40, 74, 40, 45, 85, 45, 81, 92, 100, 92, 128, 162, 205, 254, 284, 349, 418, 479, 418, 463, 458, 359, 344, 367, 462, 486, 462, 367, 344, 230, 220, 215, 177, 156, 149, 191, 193, 203, 269, 315, 406, 410, 406, 315, 335, 378, 466, 472, 481, 485, 481, 472, 495, 472, 466, 378, 335, 346, 335, 315, 269, 203, 193, 241, 256, 327, 362, 469, 362, 395, 423, 395, 362, 327, 256, 279, 323, 279, 256, 241, 193, 191, 149, 135, 126, 104, 89, 72, 69, 41, 36, 21, 3, 11, 80, 83, 99, 122, 99, 83, 80, 11, 3, 0, 3, 0, 3, 21, 36, 41, 76, 41, 69, 72, 89, 104, 105, 129, 190, 222, 274, 222, 190, 129, 105, 225, 226, 260, 266, 379, 266, 260, 226, 225, 105, 104, 126, 158, 164, 180, 164, 158, 235, 158, 126, 135, 149, 156, 209, 213, 217, 271, 310, 271, 217, 213, 216, 236, 258, 236, 263, 299, 312, 355, 457, 494, 457, 355, 312, 347, 437, 347, 375, 413, 478, 493, 478, 413, 419, 413, 375, 393, 375, 347, 312, 299, 356, 405, 432, 449, 450, 449, 432, 473, 432, 405, 356, 299, 263, 372, 433, 372, 263, 236, 216, 213, 209, 156, 177, 215, 243, 215, 220, 314, 339, 404, 482, 484, 482, 404, 339, 314, 220, 230, 344, 359, 458, 463, 418, 349, 284, 470, 284, 368, 465, 368, 436, 368, 284, 254, 205, 162, 128, 194, 227, 194, 128, 92, 81, 137, 168, 207, 297, 207, 168, 171, 168, 137, 81, 108, 167, 187, 301, 187, 303, 352, 303, 333, 358, 399, 400, 492, 400, 399, 358, 397, 358, 333, 365, 414, 365, 447, 365, 333, 303, 187, 167, 108, 81, 45, 40, 19, 32, 19, 15, 13, 9, 7, 12, 18, 34, 39, 52, 39, 71, 115, 160, 214, 246, 412, 246, 325, 246, 214, 160, 115, 71, 150, 251, 150, 71, 39, 34, 35, 44, 59, 189, 275, 283, 376, 468, 376, 283, 275, 189, 59, 44, 48, 53, 75, 88, 103, 88, 125, 238, 293, 238, 381, 431, 381, 238, 125, 198, 270, 300, 320, 471, 320, 300, 270, 198, 125, 88, 75, 78, 90, 142, 245, 343, 245, 142, 90, 98, 186, 262, 390, 398, 487, 398, 390, 262, 186, 98, 90, 78, 75, 53, 48, 44, 35, 34, 18, 24, 29, 54, 29, 24, 25, 43, 49, 119, 131, 329, 407, 329, 131, 119, 219, 305, 330, 348, 330, 454, 330, 305, 219, 242, 286, 288, 498, 288, 326, 288, 286, 309, 377, 456, 377, 309, 371, 430, 440, 430, 371, 309, 286, 242, 219, 119, 49, 43, 77, 130, 77, 43, 25, 24, 18, 12, 20, 31, 37, 91, 101, 91, 37, 42, 51, 93, 51, 42, 37, 31, 20, 26, 27, 55, 56, 67, 84, 86, 146, 86, 95, 109, 136, 231, 294, 311, 389, 311, 499, 311, 294, 363, 294, 231, 282, 231, 136, 109, 95, 86, 84, 67, 56, 73, 132, 172, 132, 73, 56, 55, 27, 26, 20, 12, 7, 1, 22, 1, 2, 10, 38, 10, 2, 5, 6, 23, 57, 94, 97, 110, 118, 133, 234, 259, 291, 306, 415, 306, 291, 259, 234, 280, 234, 247, 369, 247, 234, 133, 151, 188, 151, 133, 118, 218, 144, 134, 65, 62, 6, 62, 6, 62, 65, 134, 144, 218, 252, 261, 345, 409, 488, 409, 345, 261, 252, 218, 118, 110, 157, 110, 97, 153, 97, 94, 113, 145, 183, 145, 113, 94, 57, 68, 57, 23, 58, 23, 6, 5, 50, 70, 116, 159, 116, 70, 87, 117, 170, 182, 211, 248, 272, 248, 211, 182, 170, 117, 127, 173, 202, 249, 202, 267, 302, 402, 403, 439, 403, 402, 302, 267, 202, 173, 127, 212, 229, 237, 370, 237, 229, 212, 127, 117, 87, 70, 50, 66, 96, 179, 181, 179, 201, 206, 232, 244, 264, 290, 264, 244, 232, 265, 268, 276, 322, 424, 322, 276, 459, 467, 459, 276, 268, 265, 273, 298, 360, 364, 401, 427, 438, 448, 475, 496, 475, 448, 490, 448, 438, 427, 474, 427, 401, 420, 464, 420, 401, 364, 360, 298, 273, 296, 308, 317, 416, 317, 308, 337, 383, 460, 383, 337, 308, 296, 382] 995
"""


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
