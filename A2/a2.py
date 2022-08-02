"""
CSSE1001 Assignment 2
Semester 2, 2020
"""
from a2_support import *

# Fill these in with your details
__author__ = "James Chen-Smith 46481326"
__email__ = "james@icbix.com"
__date__ = "2020-09-20"


class GameApp:
    def __init__(self):
        """ Constructor of the GameApp class.

            Parameters:
                void
        """
        self.game = GameLogic()  # Creates a GameLogic() instance.
        self.display = Display(self.game.get_game_information(),
                               self.game.get_dungeon_size())  # Creates a Display() instance.
        self.play()  # Starts the main game loop.

    def play(self):
        """ Handles the 'frontend', user input and when to render.

            Parameters:
                void AKA self
        """
        while not self.game.check_game_over():
            self.draw()  # Calls the draw function to display the game.
            move_direction = []  # Creates list move_direction for commands.
            while len(move_direction) != 2:  # Runs while the amount of commands "i.e. I W) is not 2.
                move_direction = input("Please input an action: ").split()  # Requests command inputs and splits
                # commands, if more than 1.
                if len(move_direction) < 2:  # If number of arguments is less than 2, i.e. not investigate.
                    move_direction.append(None)  # Add NoneType to the 1st item of the list move_direction.
                elif len(move_direction) > 2:  # If number of arguments is more than 2, i.e. I W X...
                    print(INVALID)
            command = move_direction[0]  # Creates variable for the 0th part of the user input.
            argument1 = move_direction[1]  # Creates variable for the 1st part of the user input.
            if argument1 is None:  # In the case there is only 1 argument, i.e. H, Q, W, S, A or D.
                if command == "I":  # If investigate is typed all by itself, without 2nd argument.
                    print(INVALID)
                elif command == "H":  # Print help information.
                    print(HELP_MESSAGE)
                elif command == "Q":  # User may want to quit.
                    quit = input("Are you sure you want to quit? (y/n): ")  # Confirms user's wish to quit.
                    if quit == "y":  # If user confirms to quit.
                        break  # Quit the loop.
                    elif quit == "n":  # If user changes mind and wants to continue.
                        continue  # Continue
                    else:  # Reject any other type of input.
                        print(INVALID)
                elif (command == "W"
                      or command == "S"
                      or command == "A"
                      or command == "D"):  # If W, S, A or D is given as a primary input.
                    if not self.game.collision_check(command):  # If collision_check returns False.
                        if self.game.get_entity_in_direction(command) is None:  # If it's Space(' ') in the way.
                            self.game.move_player(command)  # Moves the player in direction command.
                            self.game.get_player().change_move_count(-1)  # Reduces number of moves by -1.
                        else:  # If collision_check returns True.
                            entity = self.game.get_entity_in_direction(
                                command)  # Returns Entity(' ') type in direction.
                            entity.on_hit(
                                self.game)  # Calls each entity executing Entity().on_hit(self, game: GameLogic))
                            self.game.move_player(command)  # Moves the player in direction command.
                            self.game.get_player().change_move_count(-1)  # Reduces number of moves by -1.
                    else:  # If collision_check returns True.
                        print(INVALID)  # Cannot move, hence invalid.
                        self.game.get_player().change_move_count(-1)  # Reduces number of moves by -1.
                else:  # If valid commands are not inputted.
                    print(INVALID)
            elif (command == "I"
                  and len(argument1) == 1
                  and self.game.get_entity_in_direction(argument1) is not None
                  and argument1 in ["W", "S", "A", "D"]):  # Verifies inputs for investigate in direction.
                investigate = self.game.get_entity_in_direction(argument1)  # Gets entity_in_direction as investigate
                print(investigate, "is on the", argument1, "side.")  # Print investigation results.
                self.game.get_player().change_move_count(-1)  # Reduces number of moves by -1.
            else:  # Invalidates any other kind of input.
                print(INVALID)
        if self.game.check_game_over():  # If the game is over.
            if self.game.won():  # If the game has been won.
                print(WIN_TEXT)
            elif not self.game.won():  # Else if the game has not been won.
                print(LOSE_TEST)
        else:  # This should never be the case and is only true if something goes wrong.
            pass

    def draw(self):
        """ Renders the current state of the game by querying the game_information.

            Parameters:
                void AKA self
        """
        position = self.game.get_player().get_position()  # Gets the current player coordinates.
        self.display.display_game(position)  # Renders the game.
        self.display.display_moves(self.game.get_player().moves_remaining())  # Displays number of moves remaining.


class GameLogic:
    def __init__(self, dungeon_name="game1.txt"):
        """ Constructor of the GameLogic class.

            Parameters:
                dungeon_name (str): The name of the level.
        """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)

        self._player = Player(GAME_LEVELS[dungeon_name])
        self._game_information = self.init_game_information()

        self._win = False

    def get_positions(self, entity):
        """ Returns a list of tuples representing the positions of a given entity id.

            Parameters:
                entity (str): the id of an entity.

            Returns:
                (list<tuple<int, int>>)
        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row, col))

        return positions

    def get_dungeon_size(self):
        """Returns the width of the dungeon as a number"""
        return self._dungeon_size

    def init_game_information(self):
        """ Returns a dictionary containing the position and the corresponding Entity as the keys and values
        respectively. This method also sets the Player's position. At the start of the game this method should be
        called to find the position of all entities within the current dungeon.

            Parameters:
                void

            Returns:
                dict<tuple<int, int>>: Entity>
        """
        game_static_items = {}  # Creates dictionary.
        entities = [PLAYER, KEY, DOOR, WALL, MOVE_INCREASE]  # List includes types of Entities(' ').
        for entity in entities:  # For each entity type in the list of Entities(' ').
            for item in self.get_positions(entity):
                if entity == PLAYER:
                    self._player.set_position(item)
                elif entity == KEY:
                    game_static_items[item] = Key()
                elif entity == DOOR:
                    game_static_items[item] = Door()
                elif entity == WALL:
                    game_static_items[item] = Wall()
                elif entity == MOVE_INCREASE:
                    game_static_items[item] = MoveIncrease()

        return game_static_items

    def get_game_information(self):
        """ Returns a dictionary containing the position and the corresponding Entity, as the keys and values,
        for the current dungeon.

            Parameters:
                void

            Returns:
                dict: Returns the coordinates of the static items in the game.
        """
        return self._game_information

    def get_player(self):
        """ Returns the Player object within the game.

            Parameters:
                void

            Returns:
                Player
        """
        return self._player

    def get_entity(self, position: tuple):
        """ Returns the Entity at a given position in the dungeon.
        Entity in the given direction or if the direction is a space
        then this function should return None.

            Parameters:
                direction: str

            Returns:
                Entity
        """
        try:
            return self._game_information.get(position)
        except:
            return None

    def get_entity_in_direction(self, direction: str):
        """ Returns an Entity in the given direction of the Player’s position.
        If there is no Entity in the given direction or if the
        direction is off map then this function should return None.

            Parameters:
                direction: str

            Returns:
                Entity
        """
        try:
            new_position = self.new_position(direction)
            return self._game_information.get(new_position)
        except:
            return None

    def collision_check(self, direction: str):
        """ Returns False if a player can
        travel in the given direction, they won’t collide. True, they will collide.

            Parameters:
                direction: str

            Returns:
                bool
        """
        entity_in_front = self.get_entity_in_direction(direction)
        if entity_in_front is not None:
            can_collide = entity_in_front.can_collide()
            can_collide = not can_collide
            return can_collide
        else:
            return False

    def new_position(self, direction: str):
        """ Returns a tuple of integers that represents the new position given the direction.

            Parameters:
                direction: str

            Returns:
                tuple<int,int>
        """
        old_x, old_y = self._player.get_position()
        add_x, add_y = DIRECTIONS.get(direction)
        new_x, new_y = old_x + add_x, old_y + add_y
        new_position = (new_x, new_y)
        return new_position

    def move_player(self, direction):
        """ Update the Player’s position to place them one position in the given direction.

            Parameters:
                direction: str

            Returns:
                None
        """
        self._player.set_position(
            self.new_position(direction)
        )

    def check_game_over(self):
        """ Return True if the game has been lost and False otherwise.

            Parameters:
                void

            Returns:
                bool
        """
        if self._player.moves_remaining() < 1:
            return True
        else:
            if self.won():
                return True
            else:
                return False

    def set_win(self, win: bool):
        """ Set the game’s win state to be True or False.

            Parameters:
                win: bool

            Returns:
                None
        """
        self._win = win

    def won(self):
        """ Return game’s win state.

            Parameters:
                void

            Returns:
                bool
        """
        return self._win


class Entity:
    def __init__(self):
        """ Initiates Entity (should be all sub Entities).

            Parameters:
                void

            Returns:
                None
        """
        self._id = "Entity"
        self._collidable = True

    def get_id(self):
        """ Returns a string that represents the Entity’s ID.

            Parameters:
                void

            Returns:
                str
        """
        return self._id

    def set_collide(self, collidable: bool):
        """ Set the collision state for the Entity to be True.

            Parameters:
                collidable: bool

            Returns:
                None
        """
        self._collidable = collidable

    def can_collide(self):
        """ Returns True if the Entity can be collided with (another Entity can share the position that this one is in) and False otherwise.

            Parameters:
                void

            Returns:
                bool
        """
        return self._collidable

    def __str__(self):
        """ Returns the string representation of the Entity.

            Parameters:
                void

            Returns:
                str
        """
        id_string = str(self.get_id())
        return "Entity('" + id_string + "')"

    def __repr__(self):
        """ Same as str(self).

            Parameters:
                void

            Returns:
                str
        """
        return str(self)


class Wall(Entity):
    def __init__(self):
        """ Initiates Wall.

            Parameters:
                void

            Returns:
                None
        """
        super().__init__()
        self._id = "#"
        self._collidable = False

    def __str__(self):
        """ Returns the string representation of the Wall.

            Parameters:
                void

            Returns:
                str
        """
        id_string = str(self.get_id())
        return "Wall('" + id_string + "')"


class Item(Entity):
    def __init__(self):
        """ Initiates Item (should be all sub Items).

            Parameters:
                void

            Returns:
                None
        """
        super().__init__()

    def __str__(self):
        """ Returns the string representation of the Item.

            Parameters:
                void

            Returns:
                str
        """
        id_string = str(self.get_id())
        return "Item('" + id_string + "')"

    def on_hit(self, game: GameLogic):
        """ This function should raise the NotImplementedError.

            Parameters:
                game: GameLogic

            Returns:
                None
        """
        raise NotImplementedError


class Key(Item):
    def __init__(self):
        """ Initiates Key.

            Parameters:
                void

            Returns:
                None
        """
        super().__init__()
        self._id = "K"

    def __str__(self):
        """ Returns the string representation of the Key. See example output below.

            Parameters:
                void

            Returns:
                str
        """
        id_string = str(self.get_id())
        return "Key('" + id_string + "')"

    def on_hit(self, game: GameLogic):
        """ When the player takes the Key the Key should be added to the Player’s inventory. The Key should then be
        removed from the dungeon once it’s in the Player’s inventory

            Parameters:
                game: GameLogic

            Returns:
                None
        """
        game.get_player().add_item(Key())
        position = game.get_positions(KEY)
        game.get_game_information().pop(position[0])


class MoveIncrease(Item):
    def __init__(self, moves=5):
        """ Initiates MoveIncrease.

            Parameters:
                move_count: int

            Returns:
                None
        """
        super().__init__()
        self._id = "M"
        self._moves = moves

    def __str__(self):
        """ Returns a tuple of integers that represents the new position given the direction.

            Parameters:
                void

            Returns:
                str
        """
        id_string = str(self.get_id())
        return "MoveIncrease('" + id_string + "')"

    def on_hit(self, game: GameLogic):
        """ When the player hits the MoveIncrease (M) item the number of moves for the player increases and the M
        item is removed from the game. These actions are implemented via the on_hit method. Specifically, extra moves
        should be granted to the Player and the M item should be removed from the game.

            Parameters:
                game: GameLogic

            Returns:
                 None
        """
        game.get_player().change_move_count(self._moves)
        move_increase_position = game.get_positions(MOVE_INCREASE)
        game.game_information.pop(move_increase_position[0])


class Door(Entity):
    def __init__(self):
        """ Initiates Door.

            Parameters:
                void

            Returns:
                None
        """
        super().__init__()
        self._id = "D"

    def __str__(self):
        """ Returns the string representation of the Door.

            Parameters:
                void

            Returns:
                str
        """
        id_string = str(self.get_id())
        return "Door('" + id_string + "')"

    def on_hit(self, game: GameLogic):
        """ If the Player’s inventory contains a Key Entity then this method should set the ‘game over’ state to be True.


            Parameters:
                game: GameLogic

            Returns:
                None
        """
        inventory = game.get_player().get_inventory()
        if "K" in str(inventory):
            game.set_win(True)
        else:
            print("You don't have the key!")
            pass


class Player(Entity):
    def __init__(self, move_count: int):
        """ Initiates Player.

            Parameters:
                move_count: int

            Returns:
                None
        """
        super().__init__()
        self._id = "O"
        self._position = None
        self._moves = move_count
        self._inventory = []

    def __str__(self):
        """ Returns the string representation of the Player.

            Parameters:
                void

            Returns:
                str
        """
        id_string = str(self.get_id())
        return "Player('" + id_string + "')"

    def set_position(self, position: tuple):
        """ Sets the position of the Player.

            Parameters:
                position: tuple<int, int>

            Returns:
                None
        """
        self._position = position

    def get_position(self):
        """ Returns a tuple of ints representing the position of the Player. If the Player’s position hasn’t been set yet then this method should return None.

            Parameters:
                direction: str

            Returns:
                tuple<int,int>
        """
        return self._position

    def change_move_count(self, number: int):
        """ Number to be added to the Player’s move count.

            Parameters:
                number: int

            Returns:
                None
        """
        self._moves = self._moves + number

    def moves_remaining(self):
        """Returns an int representing how many moves the Player has left before they reach the maximum move count.

            Parameters:
                void

            Returns:
                int
        """
        return self._moves

    def add_item(self, item: Entity):
        """Adds the item to the Player’s Inventory.

            Parameters:
                item: Entity

            Returns:
                None
        """
        self._inventory.append(item)

    def get_inventory(self):
        """Returns a list that represents the Player’s inventory. If the Player has nothing in their inventory then an empty list should be returned.

            Parameters:
                void

            Returns:
                list<Entity>
        """
        return self._inventory


def main():
    """Initiates GameApp()

        Parameters:
            void

        Returns:
            None
    """
    GameApp()  # Run GameApp().__init__()


if __name__ == "__main__":  # If True.
    main()  # Execute main.
