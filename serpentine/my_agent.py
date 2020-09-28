import numpy as np
from pommerman import characters
from pommerman.constants import Action, Item
from pommerman.agents import BaseAgent
from serpentine.utils.directions import Direction, Directions


class MyAgent(BaseAgent):
    """ Our version of the base agent. """

    def __init__(self, character=characters.Bomber):
        super().__init__(character)
        self.queue = []

    def act(self, obs, action_space):
        # Main event that is being called on every turn.
        if not self.queue:
            my_location = obs['position']
            board = obs['board']

            goal_location = self.move_to_safe_place(obs)

            if self.can_place_bomb(obs['board'], obs['bomb_life'], obs['ammo'], my_location):
                self.queue.append(Action.Bomb)

            direction = self.can_move_to(board, my_location, goal_location)
            self.queue.append(direction.action)

            # for direction in Directions.ALL:
            #     if self.check_direction_passable(board, my_location, direction):
            #         self.queue.append(direction.action)

            # If we cannot move in any direction, send a pass
            if not self.queue:
                self.queue.append(Action.Stop)

        return self.queue.pop(0)

    def check_direction_passable(self, board: np.array, location: tuple, direction: Direction) -> bool:
        """
            Checks for a given location and direction if the new position is a passage.

        :param board: The game board
        :param location: The location from which you start to move
        :param direction: The direction in which you are going to move (This is the Direction class)
        :return: True if the new location is a passage, False otherwise.
        """

        # Get new location
        new_location = np.array(location) + direction.array

        # Either the row or column value is not on the board.
        if min(new_location) < 0 or max(new_location) > 10:
            return False

        # Note that this is already a boolean (so no need for if statements)
        return board[tuple(new_location)] == Item.Passage.value

    def can_move_to(self, board: np.array, my_location: tuple, goal_location: tuple) -> Direction:
        """ BFS to a goal location.  Returns True if it can be reached.
        Works in the reverse way now (starting from goal_location)"""
        to_visit = [goal_location]
        visited = []

        # If we are already on the specified location!
        if my_location == goal_location:
            return Directions.ZERO

        while to_visit:
            point = to_visit.pop(0)

            for direction in Directions.ALL:
                # By making it a numpy array we can add the values
                new_point = tuple(np.array(point) + direction.array)

                # Check if we have found the location
                if new_point == my_location:
                    return Directions.reverse(direction)

                # We have already seen that point
                if new_point in visited:
                    continue

                # If we can reach this point add the point to the to visit list
                if self.check_direction_passable(board, point, direction):
                    to_visit.append(new_point)

            visited.append(point)
        return Directions.ZERO

    def can_place_bomb(self, board: np.ndarray, bomb_life: np.ndarray, ammo: int, my_location: tuple) -> bool:
        """ Checks if you can place a bomb,
        if there is no bomb already placed and
        you have enough ammo and
        there is a crate next to this location,
        return True. """

        # Check for bombs
        if not bomb_life[my_location] == 0:
            return False

        # Check for ammo
        if not ammo > 0:
            return False

        # Check for crates
        if self.find_explodables(board, my_location) < 1:
            return False

        return True

    def create_danger_map(self, obs: dict) -> np.ndarray:
        # Set our initial danger map
        danger_map = obs['flame_life']

        # Find all bomb locations, bomb timers and strength
        bombs = np.where(obs['bomb_life'] > 0)
        bombs_timers = map(int, obs['bomb_life'][bombs])
        bomb_strength = map(int, obs['bomb_blast_strength'][bombs])

        # Now we are going to set the danger information
        for row, col, timer, strength in zip(*bombs, bombs_timers, bomb_strength):

            # Reduce strength by one, since we are creating a `+` form, with the bomb as center.
            strength -= 1

            # Calculate the upper and lower ranges of the bombs (this is the + sign).
            row_low, row_high = max(row - strength, 0), min(row + strength, 10)
            col_low, col_high = max(col - strength, 0), min(col + strength, 10)

            # Set the information on the danger map, first row and then column.
            for row_danger in range(row_low, row_high + 1):
                danger_map[row_danger, col] = timer

            for col_danger in range(col_low, col_high + 1):
                danger_map[row, col_danger] = timer

        return danger_map

    def find_safe_bomb_place(self, board: np.ndarray, danger_map: np.ndarray, location: tuple) -> tuple:
        """ Returns the location of a safe space that can be reached from the current location.  """
        to_visit = [location]
        visited = []
        safest_place = location

        while to_visit:
            row, col = to_visit.pop(0)

            for direction in Directions.ALL:
                new_point = direction.array + np.array([row, col])

                # Check if position is on the board (2nd time we use this, refactor?)
                if min(new_point) < 0 or max(new_point) > 10:
                    continue

                # This makes checking the numpy positions easier
                new_point = tuple(new_point)

                # here we make the two checks, is it a passage, is it dangerous
                passage = board[new_point] == Item.Passage.value
                danger = danger_map[new_point] > 0

                # If we can move there and there is no danger we found a safe haven
                if passage and not danger:

                    # If there is something to blow up go there
                    if self.find_explodables(board, new_point):
                        return new_point

                    # It is still a safe place so move there
                    if danger_map[safest_place] > danger_map[new_point]:
                        safest_place = new_point

                # If we can move there but it is dangerous, check if it is safer than where we are now.
                if passage and danger:
                    if danger_map[safest_place] > danger_map[new_point]:
                        safest_place = new_point

                # Add the new point if we haven't been there before.
                if passage and new_point not in visited:
                    to_visit.append(new_point)

            visited.append((row, col))
        return safest_place

    def move_to_safe_place(self, obs: dict) -> tuple:
        """ Returns a location to which we can safely move.  """

        # Find all position that can lead to our destruction.
        danger_map = self.create_danger_map(obs)

        # Check if our current position is safe, if so we can go/stay there.
        my_location = obs['position']
        if danger_map[my_location] == 0 and self.find_explodables(obs['board'], my_location):
            return my_location

        # Find a reasonable safer location
        safe_position = self.find_safe_bomb_place(obs['board'], danger_map, my_location)
        return safe_position


    def find_explodables(self, board: np.ndarray, my_location: tuple) -> int:
        """ Returns the number of crates orthogonally adjacent to our position. """

        explodables = 0

        for direction in Directions.ALL:
            new_point = tuple(direction.array + np.array(my_location))

            # Check if it is on the board
            if min(new_point) < 0 or max(new_point) > 7:
                continue

            # Anything that is not us, a solid wall or a passage can be blown up
            if board[new_point] not in [Item.Agent0.value, Item.Rigid.value, Item.Passage.value]:
                explodables += 1

        return explodables












