import random 
from collections import deque
class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        num_of_friendship_calls = 0

        # Add users
        [self.add_user(f"User {i}") for i in range(num_users)]
        # Create friendships
        possible_friendships = []

        [[possible_friendships.append((user_id, friend_id)) for friend_id in range(user_id + 1, self.last_id + 1)] for user_id in self.users]

        random.shuffle(possible_friendships)

        # [(friendship = possible_friendships[i], self.add_friendship(friendship[0], friendship[1])) for i in range(num_users * avg_friendships // 2)]
        for i in range(num_users * avg_friendships // 2 ):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])
            num_of_friendship_calls += 1
        print(f"Friendship Calls: {num_of_friendship_calls}")


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # pass
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        q = deque()
        q.append([user_id])



        while len(q) > 0:
            path = q.popleft()

            user = path[-1]

            if user not in visited:
                visited[user] = path
                
                for friend in self.friendships[user]:
                    path_copy = list(path)
                    path_copy.append(friend)
                    q.append(path_copy)

        network_percentages = len(visited) / len(self.users) 
        print(f"Network Percentage: {network_percentages}")

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    # sg.populate_graph(10, 2)
    # sg.populate_graph(100, 10) # For question 1
    sg.populate_graph(1000, 5)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
