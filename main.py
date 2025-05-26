import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image # Added for background image
from kivy.core.window import Window # Added to potentially set background color

from kivy.uix.floatlayout import FloatLayout # Added for better background and content layering
from kivy.uix.scrollview import ScrollView # For StoryScreen and RewardsScreen
from kivy.properties import StringProperty # For binding Label text size in ScrollView
from kivy.uix.gridlayout import GridLayout # For RewardsScreen
from kivy.uix.screenmanager import SlideTransition # For screen transitions

kivy.require('2.0.0') # Ensure Kivy version compatibility

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        
        # Root layout for StartScreen: FloatLayout for layering
        root_layout = FloatLayout()

        # --- Background Image ---
        # FUTURE_INTEGRATION: Consider animated or themed backgrounds based on game progress.
        try:
            background_image = Image(source='placeholder_background.png', 
                                     allow_stretch=True, 
                                     keep_ratio=False,
                                     size_hint=(1, 1)) # Cover the whole screen
            root_layout.add_widget(background_image)
        except Exception as e:
            print(f"Error loading background image 'placeholder_background.png': {e}")
            # Fallback: set window background color if image fails
            Window.clearcolor = (0.1, 0.1, 0.1, 1) # Dark fallback color

        # --- Content Layout (BoxLayout for title and buttons) ---
        content_layout = BoxLayout(orientation='vertical', 
                                   padding=20, 
                                   spacing=15,
                                   size_hint=(None, None), 
                                   width=300, # Fixed width for the content box
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        # Manually calculate height based on children, or set a fixed height
        # For this example, let's give it a height that accommodates its children.
        content_layout.height = 250 # Adjusted height

        # Game Title
        title = Label(text='Time Traveler', 
                      font_size='32sp', 
                      bold=True,
                      size_hint_y=None,
                      height=60) # Increased height for title
        content_layout.add_widget(title)

        # Buttons
        button_height = 50 # Standard button height
        start_button = Button(text='Start Game', size_hint_y=None, height=button_height)
        start_button.bind(on_press=self.start_game)
        content_layout.add_widget(start_button)

        how_to_play_button = Button(text='How to Play', size_hint_y=None, height=button_height)
        how_to_play_button.bind(on_press=self.how_to_play)
        content_layout.add_widget(how_to_play_button)

        exit_button = Button(text='Exit', size_hint_y=None, height=button_height)
        exit_button.bind(on_press=self.exit_app)
        content_layout.add_widget(exit_button)
        
        root_layout.add_widget(content_layout) # Add content on top of the background
        self.add_widget(root_layout) # Add the root layout to the screen

    def start_game(self, instance):
        print("Start Game button pressed")
        self.manager.current = 'ar_camera_view' # Navigate to ARCameraViewScreen

    def how_to_play(self, instance):
        print("How to Play button pressed, navigating to HowToPlayScreen.")
        self.manager.current = 'how_to_play_screen'

    def exit_app(self, instance):
        print("Exit button pressed")
        App.get_running_app().stop()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Main Screen'))
        # Button to switch to SettingsScreen
        settings_button = Button(text='Go to Settings')
        settings_button.bind(on_press=self.switch_to_settings)
        layout.add_widget(settings_button)
        self.add_widget(layout)

    def switch_to_settings(self, instance):
        self.manager.current = 'settings'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding='20dp', spacing='10dp')
        title_label = Label(text='Settings', font_size='24sp', bold=True, size_hint_y=None, height='50dp')
        layout.add_widget(title_label)
        
        # Placeholder for actual settings content
        # FUTURE_INTEGRATION: Populate this screen with actual game settings widgets,
        # e.g., volume controls, notification preferences, accessibility options.
        settings_content_label = Label(text='(Placeholder for future game settings, e.g., sound, notifications)',
                                       font_size='16sp',
                                       halign='center',
                                       valign='top')
        layout.add_widget(settings_content_label)

        # Button to switch back to StartScreen
        back_button = Button(text='Back to Start', size_hint_y=None, height='50dp')
        back_button.bind(on_press=self.go_to_start_screen) 
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_to_start_screen(self, instance):
        # Renamed method for clarity, navigates back to Start Screen.
        print("SettingsScreen: Navigating back to Start Screen.")
        self.manager.current = 'start'

# How To Play Screen
class HowToPlayScreen(Screen):
    def __init__(self, **kwargs):
        super(HowToPlayScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding='20dp', spacing='10dp')

        title_label = Label(text='How to Play Time Traveler', 
                            font_size='24sp', 
                            bold=True,
                            size_hint_y=None,
                            height='50dp')
        layout.add_widget(title_label)

        instructions_text = """
Welcome, Time Traveler!

1.  **Start Your Journey**: From the main menu, tap "Start Game".
2.  **Explore in AR**: You'll see the world through your camera. Look for historical characters or anomalies!
3.  **Navigate the Map**: Tap "Next Scene" to open the Map. This shows your location and historical points of interest (goals).
4.  **Visit Goals**: Physically travel to the goal locations marked on your map.
5.  **Check In**: Once at a goal, tap "Check In" on the map.
6.  **Uncover Stories**: Checking in successfully will reveal a piece of history or a story about that location.
7.  **Collect Rewards**: After reading the story, tap "Collect Reward" to add treasures to your inventory.
8.  **View Your Treasures**: Access your collected items from the "Rewards" screen.

Have fun exploring the past!
        """
        instructions_label = Label(text=instructions_text,
                                   font_size='16sp',
                                   halign='left',
                                   valign='top',
                                   text_size=(Window.width - 60, None)) # For word wrap
        instructions_label.bind(texture_size=instructions_label.setter('size')) # Adjust size for text

        # Add instructions to a ScrollView in case they get too long
        scroll_view_instructions = ScrollView(size_hint=(1, 1))
        scroll_view_instructions.add_widget(instructions_label)
        layout.add_widget(scroll_view_instructions)

        back_button = Button(text='Back to Start', size_hint_y=None, height='50dp')
        back_button.bind(on_press=self.back_to_start)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def back_to_start(self, instance):
        self.manager.current = 'start'

# AR Camera View Screen
class ARCameraViewScreen(Screen):
    def __init__(self, **kwargs):
        super(ARCameraViewScreen, self).__init__(**kwargs)
        
        # Root layout for AR screen: FloatLayout for layering
        ar_root_layout = FloatLayout()

        # --- Camera Feed Simulation ---
        # AR_RENDERING_POINT: Live Camera Feed Integration
        # The Image widget below (camera_feed_image) is a placeholder.
        # This should be replaced with a Kivy widget capable of displaying a live camera feed
        # (e.g., Kivy's `Camera` widget or a custom solution using OpenCV).
        # The actual AR rendering (placing virtual objects onto the feed) would happen
        # either by overlaying widgets on this feed or by manipulating the camera texture directly.
        try:
            camera_feed_image = Image(source='camera_feed_placeholder.png',
                                      allow_stretch=True,
                                      keep_ratio=False,
                                      size_hint=(1, 1))
            ar_root_layout.add_widget(camera_feed_image)
        except Exception as e:
            print(f"Error loading camera_feed_placeholder.png: {e}")
            with ar_root_layout.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(0.15, 0.15, 0.2, 1) 
                self.rect = Rectangle(size=Window.size) 
                Window.bind(on_resize=self._update_rect_size)

        # --- Character Interaction Overlay ---
        # AR_RENDERING_POINT: AR Objects & Character Rendering
        # This `character_overlay` FloatLayout is intended to hold AR elements.
        # Virtual characters, clues, or other AR objects would be added as widgets to this layout.
        # Their positions could be determined by AR tracking libraries (e.g., ARCore, ARKit) via Python bindings,
        # or by simpler logic if not using full SLAM.
        character_overlay = FloatLayout(size_hint=(1, 1))
        
        # CHARACTER_DIALOGUE_SYSTEM: Character Appearance & Animation
        # The character_image below is a static placeholder.
        # Future logic should dynamically set the character's image, position, and animations.
        # This could involve:
        # - A state machine for character behavior.
        # - Animation sequences (e.g., using Kivy's Atlas for sprite sheets or `ImageSequence`).
        # - Logic to trigger appearances based on game events, location, or story progress.
        try:
            character_image = Image(source='character_placeholder.png',
                                    size_hint=(None, None),
                                    size=('150dp', '200dp'), 
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5}) 
            character_overlay.add_widget(character_image)
        except Exception as e:
            print(f"Error loading character_placeholder.png: {e}")
            character_image = Label(text="Character\nPlaceholder",
                                    size_hint=(None, None), size=('150dp', '200dp'),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.5})
            character_overlay.add_widget(character_image)

        # CHARACTER_DIALOGUE_SYSTEM: Dialogue Text & Logic
        # The dialogue_bubble's text is static.
        # Future logic should:
        # - Fetch dialogue lines from a script or database.
        # - Update the text dynamically based on game state or player interaction.
        # - Potentially include branching dialogues or player choices.
        dialogue_bubble = Button(text="Hello, Traveler! Welcome to the past.", # Placeholder text
                                 size_hint=(None, None),
                                 width='300dp',
                                 height='60dp',
                                 pos_hint={'center_x': 0.5, 'y': 0.25}, 
                                 background_color=(0.2, 0.6, 0.8, 0.8), 
                                 color=(1,1,1,1)) 
        character_overlay.add_widget(dialogue_bubble)
        
        ar_root_layout.add_widget(character_overlay)

        # --- Navigation Buttons ---
        nav_layout = BoxLayout(orientation='horizontal',
                               size_hint=(1, None),
                               height='50dp',
                               pos_hint={'center_x': 0.5, 'bottom': 1}, # Anchor to bottom
                               spacing='10dp',
                               padding='10dp')

        back_button = Button(text='Back to Start') # Or 'Previous Scene'
        back_button.bind(on_press=self.go_back)
        nav_layout.add_widget(back_button)

        next_button = Button(text='Next Scene')
        next_button.bind(on_press=self.go_next)
        nav_layout.add_widget(next_button)
        
        ar_root_layout.add_widget(nav_layout) # Add nav buttons on top of everything

        self.add_widget(ar_root_layout)

    def _update_rect_size(self, instance, width, height):
        if hasattr(self, 'rect'):
            self.rect.size = (width, height)

    def go_back(self, instance):
        print("ARCameraView: Back button pressed")
        # Example: Navigate back to StartScreen or a previous AR scene
        self.manager.current = 'start' 

    def go_next(self, instance):
        print("ARCameraView: Next button pressed, navigating to MapViewScreen")
        self.manager.current = 'map_view'

# Map View Screen
class MapViewScreen(Screen):
    def __init__(self, **kwargs):
        super(MapViewScreen, self).__init__(**kwargs)
        
        # Root layout for Map screen: FloatLayout for layering map and markers
        map_root_layout = FloatLayout()

        # --- Map Background ---
        # FUTURE_INTEGRATION: Could use an interactive map library (e.g., Kivy Garden mapview)
        # or allow pinch-to-zoom and panning on a large map image.
        try:
            map_image = Image(source='map_placeholder.png',
                              allow_stretch=True,
                              keep_ratio=True, 
                              size_hint=(1, 1))
            map_root_layout.add_widget(map_image)
        except Exception as e:
            print(f"Error loading map_placeholder.png: {e}")
            with map_root_layout.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(0.7, 0.8, 0.5, 1) 
                self.rect = Rectangle(size=Window.size)
                Window.bind(on_resize=self._update_rect_size)
        
        # --- Player Marker ---
        # GPS_TRACKING: Player Position Update
        # The `player_marker` position is static.
        # Future logic should:
        # - Interface with a GPS module (e.g., using `plyer` on mobile).
        # - Continuously update `player_marker.pos_hint` based on real-time GPS coordinates,
        #   translating lat/lon to map coordinates.
        try:
            player_marker = Image(source='player_marker.png',
                                  size_hint=(None, None),
                                  size=('30dp', '30dp'), 
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5}) # Placeholder position
            map_root_layout.add_widget(player_marker)
        except Exception as e:
            print(f"Error loading player_marker.png: {e}")
            player_marker = Label(text="P", pos_hint={'center_x': 0.5, 'center_y': 0.5}) 
            map_root_layout.add_widget(player_marker)

        # --- Goal Markers ---
        # GPS_TRACKING: Dynamic Goal Loading & Proximity
        # Goal markers are currently hardcoded.
        # Future logic should:
        # - Load goal locations (lat/lon, story data, etc.) from a database or configuration file.
        # - Dynamically create and place `goal_marker` widgets on the map.
        # - The `check_in_location` method will use GPS data to verify proximity to these goals.
        goal_positions = [ # Placeholder goal data
            {'center_x': 0.3, 'center_y': 0.7, 'id': 'goal1'},
            {'center_x': 0.7, 'center_y': 0.3, 'id': 'goal2'},
            {'center_x': 0.8, 'center_y': 0.8, 'id': 'goal3'}
        ]
        for i, pos_data in enumerate(goal_positions):
            try:
                goal_marker = Image(source='goal_marker.png',
                                    size_hint=(None, None),
                                    size=('25dp', '25dp'), 
                                    pos_hint={'center_x': pos_data['center_x'], 'center_y': pos_data['center_y']})
                # FUTURE_INTEGRATION: Store goal_id or related data with the marker widget for interaction.
                # goal_marker.goal_id = pos_data['id'] 
                map_root_layout.add_widget(goal_marker)
            except Exception as e:
                print(f"Error loading goal_marker.png for goal {i}: {e}")
                goal_marker = Label(text=f"G{i+1}", pos_hint={'center_x': pos_data['center_x'], 'center_y': pos_data['center_y']})
                map_root_layout.add_widget(goal_marker)

        # --- UI Elements (Buttons) ---
        ui_layout = BoxLayout(orientation='vertical', # Changed to vertical for easier stacking
                              size_hint=(None, None), # Give specific size
                              width='200dp',
                              height='120dp', # Accommodate two buttons
                              pos_hint={'center_x': 0.5, 'y': 0.02}, # Bottom center
                              spacing='10dp')

        check_in_button = Button(text='Check In')
        check_in_button.bind(on_press=self.check_in_location)
        ui_layout.add_widget(check_in_button)
        
        back_to_ar_button = Button(text='Back to AR View')
        back_to_ar_button.bind(on_press=self.back_to_ar)
        ui_layout.add_widget(back_to_ar_button)
        
        map_root_layout.add_widget(ui_layout)
        self.add_widget(map_root_layout)

    def _update_rect_size(self, instance, width, height):
        if hasattr(self, 'rect'): # Check if self.rect exists (for fallback background)
            self.rect.size = (width, height)

    def check_in_location(self, instance):
        print("MapViewScreen: Check In button pressed. Navigating to StoryScreen.")
        # CHECK_IN_LOGIC: Proximity Verification & Event Triggering
        # This function is called when the "Check In" button is pressed.
        # Future logic should:
        # 1. Get current player GPS coordinates.
        # 2. Identify the nearest active goal marker (or a specific target goal).
        # 3. Calculate distance to the goal.
        # 4. If within a defined radius (e.g., 10-20 meters):
        #    a. Trigger the story event: self.manager.current = 'story_screen'
        #       (Potentially pass goal_id to StoryScreen to load specific content).
        #    b. Mark the goal as completed or update game state.
        # 5. Else (not close enough):
        #    a. Provide feedback to the player (e.g., "You are not close enough to check in.").
        self.manager.current = 'story_screen' # Placeholder: navigates directly

    def back_to_ar(self, instance):
        print("MapViewScreen: Navigating back to AR Camera View.")
        self.manager.current = 'ar_camera_view'

# Story Screen
class StoryScreen(Screen):
    story_text_content = StringProperty("""
A long time ago, in a bustling city that is now your quiet park, lived a famous inventor named Alistair Finch. 
Alistair was known for his peculiar gadgets and his even more peculiar theories about time. 
One day, he vanished without a trace, leaving behind only a cryptic journal filled with diagrams of a strange device.

Legend says Alistair discovered a way to create small pockets in time, allowing him to observe the past. 
He wasn't trying to change history, only to learn from its forgotten moments. His journal speaks of 'Echoes of Time' – 
locations where significant events left a strong temporal residue.

Your mission, should you choose to accept it, is to find these Echoes. 
By visiting the locations marked on your map, you'll unlock fragments of Alistair's story and perhaps discover what became of him.

The first Echo is said to be near the old oak tree, the oldest in the park. 
Alistair believed it was a silent witness to centuries of change. Go there, activate your scanner (the AR view), 
and see if you can perceive the whispers of the past.

Remember, time is a river; we are merely travelers on its currents. Observe, learn, and respect the flow.
This is a very long text to ensure that scrolling is actually needed. 
Kivy's ScrollView requires its child's size_hint_y to be None and its height to be set explicitly. 
The Label's text_size property is also important for word wrapping. 
By binding the Label's height to its texture_size[1], it will grow as tall as its text content.
Let's add more lines. And more. And more.
This should be enough to demonstrate scrolling functionality within the Kivy application.
Ancient tales speak of a hidden artifact, the Chronos Shard, which Alistair sought. 
It was said to stabilize these time pockets.
Perhaps clues to its whereabouts are hidden within these Echoes.
The city archives mention a great fire in 1888 that ravaged this part of the town. Alistair was fascinated by it.
Could one of the Echoes be related to this event?
Be wary, some say that lingering too long in these Echoes can have... side effects.
But that's just superstition, right?
Keep exploring!
    """)

    def __init__(self, **kwargs):
        super(StoryScreen, self).__init__(**kwargs)
        
        screen_layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')

        # --- Story Text Area ---
        # FUTURE_INTEGRATION: Story text could be loaded dynamically based on game progress or goal_id.
        # Consider using Kivy's markup for richer text formatting if needed.
        scroll_view = ScrollView(size_hint=(1, 0.7)) 
        
        story_label = Label(text=self.story_text_content, # Current placeholder text
                            font_size='16sp',
                            text_size=(Window.width - 40, None), 
                            size_hint_y=None,
                            markup=True) 
        story_label.bind(texture_size=story_label.setter('height')) 
        
        scroll_view.add_widget(story_label)
        screen_layout.add_widget(scroll_view)

        # --- Buttons ---
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), height='50dp', spacing='10dp')

        read_aloud_button = Button(text='Read Aloud')
        read_aloud_button.bind(on_press=self.read_aloud)
        button_layout.add_widget(read_aloud_button)

        collect_reward_button = Button(text='Collect Reward')
        collect_reward_button.bind(on_press=self.collect_reward)
        button_layout.add_widget(collect_reward_button)
        
        screen_layout.add_widget(button_layout)

        # --- Navigation ---
        back_to_map_button = Button(text='Back to Map', size_hint=(1, 0.15), height='50dp')
        back_to_map_button.bind(on_press=self.back_to_map)
        screen_layout.add_widget(back_to_map_button)
        
        self.add_widget(screen_layout)

    def read_aloud(self, instance):
        print("StoryScreen: Read Aloud button pressed.")
        # TEXT_TO_SPEECH: TTS Integration
        # This function is the entry point for Text-to-Speech.
        # Future logic should:
        # 1. Check if a TTS engine is available (e.g., using `plyer.tts` or other libraries).
        # 2. Pass `self.story_text_content` (or selected parts) to the TTS engine.
        # 3. Provide controls for play/pause/stop if necessary.
        # Example (using plyer):
        # try:
        #     from plyer import tts
        #     tts.speak(self.story_text_content)
        # except ImportError:
        #     print("Plyer TTS not available on this platform.")
        # except Exception as e:
        #     print(f"TTS Error: {e}")
        pass

    def collect_reward(self, instance):
        print("StoryScreen: Collect Reward button pressed. Navigating to RewardsScreen.")
        # REWARD_SYSTEM: Granting and Persisting Rewards
        # This function is called after the player reads the story.
        # Future logic should:
        # 1. Determine the reward associated with the current story/goal.
        # 2. Add the reward to the player's inventory (which needs a data structure, e.g., a list or dict).
        # 3. Persist the updated inventory (e.g., save to a file using JSON/pickle, or a database).
        #    This ensures rewards are not lost when the app closes.
        # 4. Provide feedback to the player (e.g., "You collected [Reward Name]!").
        # Example:
        # current_goal_id = self.manager.get_screen('map_view').current_goal_id # Hypothetical
        # reward_to_grant = game_data.get_reward_for_goal(current_goal_id)
        # player_inventory.add_item(reward_to_grant)
        # player_inventory.save() # Save the inventory state
        self.manager.current = 'rewards_screen'

    def back_to_map(self, instance):
        print("StoryScreen: Navigating back to Map View.")
        self.manager.current = 'map_view'

# Rewards / Inventory Screen
class RewardsScreen(Screen):
    def __init__(self, **kwargs):
        super(RewardsScreen, self).__init__(**kwargs)
        
        screen_layout = BoxLayout(orientation='vertical', padding='10dp', spacing='10dp')

        # --- Title ---
        title_label = Label(text='Collected Treasures', 
                            font_size='24sp', 
                            size_hint_y=None, 
                            height='40dp',
                            bold=True)
        screen_layout.add_widget(title_label)

        # --- Inventory Display ---
        scroll_view = ScrollView(size_hint=(1, 1)) # Takes available vertical space
        
        # GridLayout for items
        inventory_layout = GridLayout(cols=3, 
                                      spacing='10dp', 
                                      padding='10dp',
                                      size_hint_y=None)
        inventory_layout.bind(minimum_height=inventory_layout.setter('height')) 

        # REWARD_SYSTEM: Displaying Collected Rewards
        # The `placeholder_items` list is static.
        # Future logic should:
        # 1. Load the player's actual collected items from the persisted inventory data.
        # 2. Dynamically populate `inventory_layout` with widgets for each collected item.
        #    - Each item might have properties like name, image, description, date_collected.
        # Example:
        # player_items = player_inventory.load_items() # Load from save file/database
        # for item_data in player_items:
        #    # Create item_box, item_image, item_label as below
        #    inventory_layout.add_widget(item_box)
        # If no items, display a message like "No treasures collected yet."

        placeholder_items = [ # Placeholder data
            {"name": "Ancient Badge", "image": "badge_placeholder.png"},
            {"name": "Mystic Scroll", "image": "scroll_placeholder.png"},
            {"name": "Time Crystal", "image": "artifact_placeholder.png"},
            {"name": "Old Compass", "image": "badge_placeholder.png"}, # Reusing for demo
            {"name": "Faded Map", "image": "scroll_placeholder.png"},  # Reusing for demo
            {"name": "Lost Diary Page", "image": "artifact_placeholder.png"}, # Reusing for demo
            {"name": "Roman Coin", "image": "badge_placeholder.png"},
            {"name": "Victorian Locket", "image": "artifact_placeholder.png"},
            {"name": "WWII Medal", "image": "badge_placeholder.png"},
        ]

        for item_data in placeholder_items:
            item_box = BoxLayout(orientation='vertical', size_hint_y=None, height='120dp', spacing='5dp')
            try:
                item_image = Image(source=item_data["image"], 
                                   size_hint_y=None, 
                                   height='80dp', 
                                   allow_stretch=True, 
                                   keep_ratio=True)
            except Exception as e:
                print(f"Error loading reward image {item_data['image']}: {e}")
                item_image = Label(text="Img\nError", size_hint_y=None, height='80dp')
            
            item_label = Label(text=item_data["name"], 
                               font_size='14sp', 
                               size_hint_y=None, 
                               height='20dp',
                               halign='center')
            
            item_box.add_widget(item_image)
            item_box.add_widget(item_label)
            inventory_layout.add_widget(item_box)
        
        scroll_view.add_widget(inventory_layout)
        screen_layout.add_widget(scroll_view)

        # --- Navigation ---
        back_to_game_button = Button(text='Back to Map', 
                                   size_hint_y=None, 
                                   height='50dp')
        back_to_game_button.bind(on_press=self.back_to_game)
        screen_layout.add_widget(back_to_game_button)
        
        self.add_widget(screen_layout)

    def back_to_game(self, instance):
        print("RewardsScreen: Navigating back to Map View.")
        # Or could navigate to AR view, or a main game hub screen
        self.manager.current = 'map_view'

class TimeTravelerApp(App):
    # FUTURE_INTEGRATION: Consider implementing app lifecycle events (on_start, on_pause, on_resume, on_stop)
    # for tasks like:
    # - Initializing game state or loading saved data (on_start).
    # - Saving game state (on_pause, on_stop).
    # - Releasing resources like camera or GPS (on_pause, on_stop).
    # - Restoring camera or GPS (on_resume).

    def build(self):
        # Create the screen manager with a default transition
        sm = ScreenManager(transition=SlideTransition(direction="left"))
        
        # Add all screens
        # FUTURE_INTEGRATION: Game data (player inventory, story progress, settings) could be
        # managed by a central class/object accessible by all screens, passed during init or via App instance.
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(MainScreen(name='main')) 
        sm.add_widget(SettingsScreen(name='settings')) 
        sm.add_widget(HowToPlayScreen(name='how_to_play_screen')) 
        sm.add_widget(ARCameraViewScreen(name='ar_camera_view'))
        sm.add_widget(MapViewScreen(name='map_view'))
        sm.add_widget(StoryScreen(name='story_screen'))
        sm.add_widget(RewardsScreen(name='rewards_screen'))
        
        sm.current = 'start' 
        return sm

if __name__ == '__main__':
    TimeTravelerApp().run()
