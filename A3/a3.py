import tkinter, tkinter.filedialog
from PIL import ImageTk, Image

TASK_ONE = "task1"
TASK_TWO = "task2"


class GameApp:
    def __init__(self, master, task=TASK_TWO, dungeon_name="game3.txt", **kwargs):

        """This section manages the keyword arguments passed by restart()"""
        for key, value in kwargs.items():
            if key == "size":
                self._size = value
                self._gamelogic = GameLogic(dungeon_name, dungeon_size=self._size)
            else:
                pass
        try:
            if self._size is not None:
                pass
            else:
                self._gamelogic = GameLogic(dungeon_name)
                self._size = self._gamelogic.get_dungeon_size()
        except:
            self._gamelogic = GameLogic(dungeon_name)
            self._size = self._gamelogic.get_dungeon_size()

        """This section enable/disables skin based on if it's TASK_ONE or TASK_TWO"""
        if task == "task1":
            self._skin = False
        elif task == "task2":
            self._skin = True
        else:
            pass

        """This section configures the tkinter instance"""
        self._master = master
        self._master.title("Game Beta")

        """This section creates the top menu."""
        self._menu = tkinter.Menu(self._master, tearoff=False)
        self._filemenu = tkinter.Menu(self._menu)
        self._filemenu.add_command(label="Save", command=self.save)
        self._filemenu.add_command(label="Load", command=load)
        self._filemenu.add_command(label="New Game", command=restart)
        self._filemenu.add_command(label="Quit", command=self.quit)
        self._menu.add_cascade(menu=self._filemenu, label="File")
        self._master.config(menu=self._menu)

        """This section creates the frame and the title bar 'Key Cave Adventure Game' at the top"""
        self._title_frame = tkinter.Frame(self._master, bg='lightgreen')
        self._title_frame.grid(row=0, sticky='nsew')
        self._title_label = tkinter.Label(self._title_frame, text='Key Cave Adventure Game', font=('Arial', 20),
                                          bg='lightgreen')
        self._title_label.pack()

        """This section creates the main frame, DungeonMap and key bindings"""
        self._gamebox = tkinter.Frame(self._master, bg='white', borderwidth=0)
        self._gamebox.bind_all('<Key>', self.key)
        self._gamebox.grid(row=1, sticky='nsew')
        if not self._skin:  # If skin is disabled, i.e. task=TASK_ONE
            self._dungeonmap = DungeonMap(self._gamebox, self._size, gamelogic=self._gamelogic)
        elif self._skin:  # If skin is enabled, i.e. task=TASK_TWO
            self._dungeonmap = AdvancedDungeonMap(self._gamebox, self._size, gamelogic=self._gamelogic)

        """This section initially draws the game and player"""
        self._dungeonmap.draw(self._gamelogic)

        """This section creates the KeyPad canvas and assigns bindings"""
        self._keypad = KeyPad(self._gamebox)
        self._keypad._abstractgrid.tag_bind(self._keypad.n, '<Button-1>', self.click_n)
        self._keypad._abstractgrid.tag_bind(self._keypad.n_label, '<Button-1>', self.click_n)
        self._keypad._abstractgrid.tag_bind(self._keypad.w, '<Button-1>', self.click_w)
        self._keypad._abstractgrid.tag_bind(self._keypad.w_label, "<Button-1>", self.click_w)
        self._keypad._abstractgrid.tag_bind(self._keypad.s, '<Button-1>', self.click_s)
        self._keypad._abstractgrid.tag_bind(self._keypad.s_label, '<Button-1>', self.click_s)
        self._keypad._abstractgrid.tag_bind(self._keypad.e, '<Button-1>', self.click_e)
        self._keypad._abstractgrid.tag_bind(self._keypad.e_label, '<Button-1>', self.click_e)

        self._key_lock = False

        """This section creates the StatusBar"""
        if not self._skin:
            pass
        if self._skin:
            self._statusbar = StatusBar(self._master, self, self._gamelogic)

    def key(self, event):
        """ Event listener for key bindings within application.

            Parameters:
                event (event): the keypress event

            Returns:
                void
        """
        if event.char in "wW":
            self.move_player("W")
        elif event.char in "aA":
            self.move_player("A")
        elif event.char in "sS":
            self.move_player("S")
        elif event.char in "dD":
            self.move_player("D")
        else:
            pass

    """This section manages the keyboard events and executes move_player as required"""

    def click_n(self, event):
        self.move_player("W")

    def click_w(self, event):
        self.move_player("A")

    def click_s(self, event):
        self.move_player("S")

    def click_e(self, event):
        self.move_player("D")

    def move_player(self, direction):
        """This method moves the player, similar to A2, implementing GameLogic"""
        if not self._gamelogic.check_game_over():
            if not self._gamelogic.collision_check(direction):  # If collision_check returns False.
                if self._gamelogic.get_entity_in_direction(direction) is None:  # If it's Space(' ') in the way.
                    self._gamelogic.move_player(direction)  # Moves the player in direction command.
                    self._gamelogic.get_player().change_move_count(-1)  # Reduces number of moves by -1.
                    print(self._gamelogic.get_player().moves_remaining())
                else:  # If collision_check returns True.
                    entity = self._gamelogic.get_entity_in_direction(
                        direction)  # Returns Entity(' ') type in direction.
                    entity.on_hit(self,
                                  self._gamelogic)  # Calls each entity executing Entity().on_hit(self, game: GameLogic))
                    self._gamelogic.move_player(direction)  # Moves the player in direction command.
                    self._gamelogic.get_player().change_move_count(-1)  # Reduces number of moves by -1.
            self.draw()
            if self._skin == True:
                self._statusbar.update_moves(self._gamelogic)  # Updates moves in StatusBar
            else:
                pass
        elif self._key_lock == False:
            if self._gamelogic.won():
                self._key_lock = True  # Reject key-presses if game is over.
                self.win()
            else:
                self._key_lock = True  # Reject key-presses if game is over.
                self.lose()
        else:
            pass

    def draw(self):
        self._dungeonmap.draw(self._gamelogic)

    def win(self):
        """This method creates the win dialog box"""
        if self._skin == True:
            self._statusbar._time_stop = True
            self._win_dialog = tkinter.Tk()
            self._win_dialog.geometry("+300+300")
            self._win_text = str("You won with a score of: " + str(self._statusbar.get_time()[2]) + ". Good job!")
            self._win_dialog.title("You lost!")
            self._win_label = tkinter.Label(self._win_dialog, text=self._win_text)
            self._win_label.grid(row=0, columnspan=2, sticky="nwse")
            self._restart_button = tkinter.Button(self._win_dialog, text="Restart Game",
                                                  command=lambda: [self._win_dialog.destroy(), restart()])
            self._restart_button.grid(row=1, column=0)
            self._quit_button = tkinter.Button(self._win_dialog, text="Quit Game",
                                               command=lambda: [self._win_dialog.destroy(), self.quit()])
            self._quit_button.grid(row=1, column=1)
            self._win_dialog.mainloop()
        else:
            self._win_dialog = tkinter.Tk()
            self._win_dialog.geometry("+300+300")
            self._win_dialog.title("You won!")
            self._win_label = tkinter.Label(self._win_dialog,
                                            text="You won! Please switch to TASK_TWO for more precise information.")
            self._win_label.grid(row=0, columnspan=2, sticky="nwse")
            self._restart_button = tkinter.Button(self._win_dialog, text="Restart Game",
                                                  command=lambda: [self._win_dialog.destroy(), restart()])
            self._restart_button.grid(row=1, column=0)
            self._quit_button = tkinter.Button(self._win_dialog, text="Quit Game",
                                               command=lambda: [self._win_dialog.destroy(), self.quit()])
            self._quit_button.grid(row=1, column=1)
            self._win_dialog.mainloop()

    def lose(self):
        """This method creates the lose dialog box"""
        if self._skin == True:
            self._statusbar._time_stop = True
            self._lose_dialog = tkinter.Tk()
            self._lose_dialog.geometry("+300+300")
            self._lose_text = str("You lost in: " + str(self._statusbar.get_time()[0]) + "m " + str(
                self._statusbar.get_time()[1]) + "s. Good job!")
            self._lose_dialog.title("You lost!")
            self._lose_label = tkinter.Label(self._lose_dialog, text=self._lose_text)
            self._lose_label.grid(row=0, columnspan=2, sticky="nwse")
            self._restart_button = tkinter.Button(self._lose_dialog, text="Restart Game",
                                                  command=lambda: [self._lose_dialog.destroy(), restart()])
            self._restart_button.grid(row=1, column=0)
            self._quit_button = tkinter.Button(self._lose_dialog, text="Quit Game",
                                               command=lambda: [self._lose_dialog.destroy(), self.quit()])
            self._quit_button.grid(row=1, column=1)
            self._lose_dialog.mainloop()
        else:
            self._lose_dialog = tkinter.Tk()
            self._lose_dialog.geometry("+300+300")
            self._lose_dialog.title("You lost!")
            self._lose_label = tkinter.Label(self._lose_dialog,
                                             text="You lost! Please switch to TASK_TWO for more precise information.")
            self._lose_label.grid(row=0, columnspan=2, sticky="nwse")
            self._restart_button = tkinter.Button(self._lose_dialog, text="Restart Game",
                                                  command=lambda: [self._lose_dialog.destroy(), restart()])
            self._restart_button.grid(row=1, column=0)
            self._quit_button = tkinter.Button(self._lose_dialog, text="Quit Game",
                                               command=lambda: [self._lose_dialog.destroy(), self.quit()])
            self._quit_button.grid(row=1, column=1)
            self._lose_dialog.mainloop()

    def save(self):
        """Method takes the data in the game and saves it to a file."""
        pulled_game_information = self._gamelogic.get_game_information()
        game_information = []
        for coord, entity in pulled_game_information.items():
            game_information.append(str(coord))
            game_information.append(str(entity))
        game_information = ";".join(game_information)
        moves_remaining = str(self._gamelogic.get_player().moves_remaining())
        elapsed_time = str(self._statusbar.get_time())
        player_position = str(self._gamelogic.get_player().get_position())

        save_data = (game_information, moves_remaining, elapsed_time, player_position)
        save_string = str(save_data)

        file_type = [('Text File (*.txt)', '*.txt')]
        save_location = tkinter.filedialog.asksaveasfile(mode="w", filetypes=file_type, defaultextension=".txt").name
        save_file = open(save_location, "w")
        for item in save_data:
            save_file.write(item)
            save_file.write("\n")
        save_file.close()

    def quit(self):
        """Method quits the game by dialog prompt confirmation."""
        self._quit_dialog = tkinter.Tk()
        self._quit_dialog.geometry("+300+300")
        self._quit_dialog.title("Quit")
        self._quit_label = tkinter.Label(self._quit_dialog, text="You sure? You should be addicted by now :(")
        self._quit_label.grid(row=0, columnspan=2, sticky="nwse")
        self._yes_button = tkinter.Button(self._quit_dialog, text="Yes",
                                          command=lambda: [self._quit_dialog.destroy(), quit()])
        self._yes_button.grid(row=1, column=0)
        self._no_button = tkinter.Button(self._quit_dialog, text="No",
                                         command=lambda: [self._quit_dialog.destroy()])
        self._no_button.grid(row=1, column=1)
        self._quit_dialog.mainloop()


class AbstractGrid:
    def __init__(self, master, rows, cols, width, height, **kwargs):
        """Initiates AbstractGrid superclass."""
        self._abstractgrid = tkinter.Canvas(master, width=width + 1, height=height + 1, highlightthickness=0)
        self._rows = rows
        self._cols = cols
        self._width = width
        self._height = height

        self._player_grid = self._abstractgrid.create_rectangle(0, 0, 0, 0)
        self._player_tag = self._abstractgrid.create_text(0, 0, text='')


class DungeonMap(AbstractGrid):
    def __init__(self, master, size, width=600, **kwargs):
        """Initiates DungeonMap, extending AbstractGrid."""
        for key, value in kwargs.items():
            if key == "gamelogic":
                self._gamelogic = value
            else:
                pass
        height = width
        super().__init__(master, size, size, width, height)
        self._abstractgrid.grid(row=0, column=0)
        self._grid_width = self._width / self._cols
        self._grid_height = self._height / self._rows

    def draw(self, gamelogic):
        """Redraws the DungeonMap, reading from the game_information."""
        self._abstractgrid.delete('all')
        game_information = gamelogic.get_game_information()
        for item in game_information:
            row, column = item
            x_topleft, y_topleft, x_bottomright, y_bottomright = self.translate(row, column)
            if str(game_information.get(item)) == str(Wall()):
                self._abstractgrid.create_rectangle(x_topleft, y_topleft, x_bottomright, y_bottomright,
                                                    fill='darkgray')
                self._abstractgrid.create_text(x_topleft + (1 / 2) * (self._grid_width),
                                               y_topleft + (1 / 2) * (self._grid_height), text='')
            elif str(game_information.get(item)) == str(Key()):
                self._abstractgrid.create_rectangle(x_topleft, y_topleft, x_bottomright, y_bottomright,
                                                    fill='yellow')
                self._abstractgrid.create_text(x_topleft + (1 / 2) * (self._grid_width),
                                               y_topleft + (1 / 2) * (self._grid_height), text='Key')
            elif str(game_information.get(item)) == str(Door()):
                self._abstractgrid.create_rectangle(x_topleft, y_topleft, x_bottomright, y_bottomright,
                                                    fill='red')
                self._abstractgrid.create_text(x_topleft + (1 / 2) * self._grid_width,
                                               y_topleft + (1 / 2) * self._grid_height, text='Door')
            elif str(game_information.get(item)) == str(MoveIncrease()):
                self._abstractgrid.create_rectangle(x_topleft, y_topleft, x_bottomright, y_bottomright,
                                                    fill='orange')
                self._abstractgrid.create_text(x_topleft + (1 / 2) * self._grid_width,
                                               y_topleft + (1 / 2) * self._grid_height, text='Move Increase')
            else:
                pass
        row, column = gamelogic.get_player().get_position()
        x_topleft, y_topleft, x_bottomright, y_bottomright = self.translate(row, column)
        self._player_grid = self._abstractgrid.create_rectangle(x_topleft, y_topleft, x_bottomright, y_bottomright,
                                                                fill='lightgreen')
        self._player_tag = self._abstractgrid.create_text(x_topleft + (1 / 2) * self._grid_width,
                                                          y_topleft + (1 / 2) * self._grid_height, text='Ibis')

    def translate(self, row, column):
        """ Translates grid-coordinates into pixel-coordinates and returns the values of the edges.

            Parameters:
                row (int): the y grid-coordinate of an entity.
                column (int): the x grid-coordinate of an entity.

            Returns:
                (list<tuple<int, int, int, int>>)
        """
        x_topleft = column * self._grid_width
        y_topleft = row * self._grid_height
        x_bottomright = x_topleft + self._grid_width
        y_bottomright = y_topleft + self._grid_height
        return x_topleft, y_topleft, x_bottomright, y_bottomright


class AdvancedDungeonMap(DungeonMap):
    def __init__(self, master, size, width=600, **kwargs):
        """Initiates assets required for skinned DungeonMap."""
        super().__init__(master, size, width=600, **kwargs)
        self._grid_height = int(self._grid_height)
        self._grid_width = int(self._grid_width)
        self._img_wall = ImageTk.PhotoImage(
            (Image.open("images/wall.png")).resize((self._grid_height, self._grid_width), Image.BICUBIC))
        self._img_grass = ImageTk.PhotoImage(
            (Image.open("images/empty.png")).resize((self._grid_height, self._grid_width), Image.BICUBIC))
        self._img_moveincrease = ImageTk.PhotoImage(
            (Image.open("images/moveIncrease.png")).resize((self._grid_height, self._grid_width), Image.BICUBIC))
        self._img_door = ImageTk.PhotoImage(
            (Image.open("images/door.png")).resize((self._grid_height, self._grid_width), Image.BICUBIC))
        self._img_key = ImageTk.PhotoImage(
            (Image.open("images/key.png")).resize((self._grid_height, self._grid_width), Image.BICUBIC))

    def draw(self, gamelogic):
        """Redraws skinned Dungeonmap."""
        self._abstractgrid.delete('all')
        game_information = gamelogic.get_game_information()
        for row in range(gamelogic.get_dungeon_size()):
            for column in range(gamelogic.get_dungeon_size()):
                item = (row, column)
                x_topleft, y_topleft, x_bottomright, y_bottomright = self.translate(row, column)
                if str(game_information.get(item)) == str(Wall()):
                    self._abstractgrid.create_image(x_topleft, y_topleft, image=self._img_wall)
                elif str(game_information.get(item)) == str(Key()):
                    self._abstractgrid.create_image(x_topleft, y_topleft, image=self._img_key)
                elif str(game_information.get(item)) == str(Door()):
                    self._abstractgrid.create_image(x_topleft, y_topleft, image=self._img_door)
                elif str(game_information.get(item)) == str(MoveIncrease()):
                    self._abstractgrid.create_image(x_topleft, y_topleft, image=self._img_moveincrease)
                else:
                    self._abstractgrid.create_image(x_topleft, y_topleft, image=self._img_grass)
        row, column = gamelogic.get_player().get_position()
        x_topleft, y_topleft, x_bottomright, y_bottomright = self.translate(row, column)
        self._img_ibis = ImageTk.PhotoImage(
            (Image.open("images/player.png")).resize((self._grid_height, self._grid_width), Image.BICUBIC))
        self._player_grid = self._abstractgrid.create_image(x_topleft, y_topleft, image=self._img_ibis)


class KeyPad(AbstractGrid):
    def __init__(self, master, width=200, height=100, **kwargs):
        """Initiates KeyPad instance, extends AbstractGrid."""
        self._rows = 2
        self._cols = 3
        grid_width = width / self._cols
        grid_height = height / self._rows
        super().__init__(master, self._rows, self._cols, width=width, height=height)

        """This section constructs the NWSE keys"""
        self._abstractgrid.grid(row=0, column=1)

        self.n = self._abstractgrid.create_rectangle((1 * grid_width), (0 * grid_height), (2 * grid_width),
                                                     (1 * grid_height),
                                                     fill='darkgray')
        self.n_label = self._abstractgrid.create_text((1 * grid_width) + (1 / 2) * grid_width,
                                                      (0 * grid_height) + (1 / 2) * (grid_height), text="N")
        self.w = self._abstractgrid.create_rectangle((0 * grid_width), (1 * grid_height), (1 * grid_width),
                                                     (2 * grid_height),
                                                     fill='darkgray')
        self.w_label = self._abstractgrid.create_text((0 * grid_width) + (1 / 2) * (grid_width),
                                                      (1 * grid_height) + (1 / 2) * (grid_height), text="W")
        self.s = self._abstractgrid.create_rectangle((1 * grid_width), (1 * grid_height), (2 * grid_width),
                                                     (2 * grid_height),
                                                     fill='darkgray')
        self.s_label = self._abstractgrid.create_text((1 * grid_width) + (1 / 2) * (grid_width),
                                                      (1 * grid_height) + (1 / 2) * (grid_height), text="S")
        self.e = self._abstractgrid.create_rectangle((2 * grid_width), (1 * grid_height), (3 * grid_width),
                                                     (2 * grid_height),
                                                     fill='darkgray')
        self.e_label = self._abstractgrid.create_text((2 * grid_width) + (1 / 2) * (grid_width),
                                                      (1 * grid_height) + (1 / 2) * (grid_height), text="E")


class StatusBar:
    def __init__(self, master, gameapp, gamelogic, height=50):
        """Initiates StatusBar item, as a frame in self._master."""
        self._master = master

        self._bar = tkinter.Frame(self._master, height=height)
        self._bar.grid(row=2, sticky='nsew')

        """This section creates the moves, timer variables and executes timer loop"""
        self._movesvar = tkinter.IntVar()
        self._moves = gamelogic.get_player().moves_remaining()
        self._movesvar.set(self._moves)
        self._secvar = tkinter.IntVar()
        self._minvar = tkinter.IntVar()
        self._time_seconds = 0
        self._time_stop = False
        self.timer()

        """This section creates the restart, quit buttons in statusbar"""
        self._restart_button = tkinter.Button(self._bar, text="New Game", command=restart)
        self._restart_button.grid(column=0, row=0, pady=5, padx=20)
        self._quit_button = tkinter.Button(self._bar, text="Quit", command=gameapp.quit)
        self._quit_button.grid(column=0, row=1, pady=5, padx=10)

        """This section creates the sand timer icon as well as time elapsed heading in statusbar"""
        self._img_time = ImageTk.PhotoImage(Image.open("images/clock.png").resize((height, height), Image.BICUBIC))
        self._time_icon = tkinter.Label(self._bar, image=self._img_time).grid(column=1, row=0, rowspan=2)
        self._time_label_heading = tkinter.Label(self._bar, text="Time elapsed")
        self._time_label_heading.grid(column=2, row=0)

        """This section creates the lightning bolt as well as moves remaining indicator"""
        self._img_moves = ImageTk.PhotoImage(Image.open("images/lightning.png").resize((height, height), Image.BICUBIC))
        self._moves_icon = tkinter.Label(self._bar, image=self._img_moves).grid(column=3, row=0, rowspan=2)
        self._moves_label_heading = tkinter.Label(self._bar, text="Moves left")
        self._moves_label_heading.grid(column=4, row=0)
        self._moves_label_text = (str(self._movesvar.get()) + " moves remaining")
        self._moves_label = tkinter.Label(self._bar, text=self._moves_label_text)
        self._moves_label.grid(column=4, row=1)

    def timer(self):
        """This method initiates the after() timer in StatusBar"""
        if self._time_stop == False:
            self._time_label_text = (self._minvar.get(), "m", self._secvar.get(), "s")
            self._time_label = tkinter.Label(self._bar, text=self._time_label_text)
            self._time_label.grid(column=2, row=1)

            """This section manages the conversion of time in to seconds into minutes/seconds"""
            self._time_seconds = self._time_seconds + 1
            self._time_seconds_mod = self._time_seconds % 60
            self._time_minutes = self._time_seconds // 60

            """This section updates the IntVars"""
            self._secvar.set(self._time_seconds_mod)
            self._minvar.set(self._time_minutes)
            self._bar.after(1000, self.timer)
        else:
            pass

    def update_moves(self, gamelogic):
        """This method reads from self._gamelogic and updates moves remaining"""
        self._moves = gamelogic.get_player().moves_remaining()
        self._movesvar.set(self._moves)
        self._moves_label_text = (str(self._movesvar.get()) + " moves remaining")
        self._moves_label = tkinter.Label(self._bar, text=self._moves_label_text)
        self._moves_label.grid(column=4, row=1)

    def get_time(self):
        return self._time_minutes, self._time_seconds_mod, self._time_seconds


class GameLogic:
    def __init__(self, dungeon_name, **kwargs):
        """ Constructor of the GameLogic class.

            Parameters:
                dungeon_name (str): The name of the level.
        """
        self._dungeon = load_game(dungeon_name)

        for key, value in kwargs.items():
            if key == "dungeon_size":
                self._dungeon_size = value
            else:
                pass

        try:
            if self._dungeon_size == None:
                self._dungeon_size = len(self._dungeon)
            else:
                pass
        except:
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

    def on_hit(self, gameapp: GameApp, game: GameLogic):
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
        print('Got key!')


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

    def on_hit(self, gameapp: GameApp, game: GameLogic):
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
        game._game_information.pop(move_increase_position[0])


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

    def on_hit(self, gameapp: GameApp, game: GameLogic):
        """ If the Player’s inventory contains a Key Entity then this method should set the ‘game over’ state to be True.


            Parameters:
                game: GameLogic

            Returns:
                None
        """
        inventory = game.get_player().get_inventory()
        if "K" in str(inventory):
            game.set_win(True)
            gameapp.win()
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


"""Code below is to ensure compatibility with a2_support.py"""
GAME_LEVELS = {
    # dungeon layout: max moves allowed
    "game1.txt": 7,
    "game2.txt": 12,
    "game3.txt": 19,
}
PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "
DIRECTIONS = {
    "W": (-1, 0),
    "S": (1, 0),
    "D": (0, 1),
    "A": (0, -1)
}


def load_game(filename):
    dungeon_layout = []

    with open(filename, 'r') as file:
        file_contents = file.readlines()

    for i in range(len(file_contents)):
        line = file_contents[i].strip()
        row = []
        for j in range(len(file_contents)):
            row.append(line[j])
        dungeon_layout.append(row)

    return dungeon_layout


"""Code above is to ensure compatibility with a2_support.py"""


def main():
    """This function runs the initial program."""
    global root, gameapp
    root = tkinter.Tk()
    gameapp = GameApp(root)
    print(gameapp._size)
    root.mainloop()


def load():
    """This function loads the game from a save file."""
    global root, gameapp
    file_type = [('Text File (*.txt)', '*.txt')]
    save_location = tkinter.filedialog.askopenfile(mode="r", filetypes=file_type, defaultextension=".txt").name
    file = open(save_location, 'r')

    lines = file.readlines()
    count = 0
    save_data = []
    for line in lines:
        save_data.append(line.strip())

    """This section parses the game_information loaded."""
    game_information_list = save_data[0].split(";")
    item_pos = 0
    game_information = {}

    """This section parses the game_information in the save file"""
    for item_pos in range(len(game_information_list)):
        if (item_pos % 2) == 0:
            try:
                game_information[coord] = entity
            except:
                pass
            coord = eval(game_information_list[item_pos])
        else:
            if game_information_list[item_pos] == "Wall('#')":
                entity = Wall()
            elif game_information_list[item_pos] == "Key('K')":
                entity = Key()
            elif game_information_list[item_pos] == "MoveIncrease('M')":
                entity = MoveIncrease()
            elif game_information_list[item_pos] == "Door('D')":
                entity = Door()
            else:
                pass
        item_pos = item_pos + 1
    game_information[coord] = entity

    """This section determines the size of the loaded dungeon"""
    x_values = []
    for item in game_information:
        x = item[0]
        x_values.append(x)
    x_max = max(x_values)
    print(x_max)

    """This section sets variables as values derived from the save file"""
    moves_remaining = int(save_data[1])
    elapsed_time = eval((save_data[2]))[2]
    player_position = list(eval((save_data[3])))

    """Destroys existing GameApp instance"""
    root.destroy()
    root = tkinter.Tk()

    """Loads new GameApp instance"""
    gameapp = GameApp(root, size=(x_max + 1))
    gameapp._gamelogic._game_information = game_information
    gameapp._gamelogic.get_player()._moves = moves_remaining
    gameapp._statusbar._time_seconds = elapsed_time
    gameapp._gamelogic.get_player()._position = player_position

    """Displays dialog prompting user to move player to update map"""
    gameapp._loaded_dialog = tkinter.Tk()
    gameapp._loaded_dialog.title("Game loaded")
    gameapp._loaded_label = tkinter.Label(gameapp._loaded_dialog,
                                          text="Game loaded! Please move the player to update the map.")
    gameapp._loaded_label.grid(row=0, sticky="nwse")
    gameapp._restart_button = tkinter.Button(gameapp._loaded_dialog, text="Continue",
                                             command=lambda: [gameapp._loaded_dialog.destroy()])
    gameapp._restart_button.grid(row=1)

    gameapp._loaded_dialog.mainloop()

    root.mainloop()

def restart():
    """This function destroys and recreates the GameApp instance"""
    global root, gameapp
    root.destroy()
    root = tkinter.Tk()
    gameapp = GameApp(root)
    root.mainloop()


def quit():
    """This function destroys the GameApp instance"""
    root.destroy()


main()  # This initiates the game
