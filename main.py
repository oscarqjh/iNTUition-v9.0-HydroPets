from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from dbfunctions import authenticate, set_interval,check_drink_time
from hydropetsSM import main_store, first_time_toggle_action
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty
)
Config.set('graphics', 'width', 340)
Config.write()

class Bounds(RelativeLayout):
    pass


class Background(Image):
    offset = ListProperty()
    magnification = NumericProperty(0)
    
class PlantRoomBackground(Image):
    offset = ListProperty()
    magnification = NumericProperty(0)

#hydropetsSM functions
def bye_mapper(state,widget):
    #Maps bye
    widget.bye = state.get('saying_bye')

def bye_dispatcher(dispatch, widget):
    #Dispatches bye action
    return {
        'bind':{
            'bye':lambda *largs, **kwargs: dispatch(bye_action)
        },
        'init':{
            'bye':True
        }
    }

def ByeFunction(*largs):
    '''
        Functional component which returns nothing, changes state
    '''
    return

ByeFunction = main_store.connect(bye_mapper, bye_dispatcher, ByeFunction)

####

class PetScreen(Screen):
    def backPress(self):
        self.ids.backButton_image.source = 'assets/back_pressed.png'

    def backOff(self):
        self.ids.backButton_image.source = 'assets/back.png'

class WindowManager(ScreenManager):
    pass

class PlantScreen(Screen):
    growth = 0
    stage = 0
    text = StringProperty("0")
    harvest_count = 0


    def change_image(self):
        self.growth += 1
        if self.growth == 3:
            self.growth = 0
            self.stage += 1
        elif self.stage == 2:
            self.stage += 1
        
        if self.stage == 0:
            # Change the image source
            self.ids.plant_image.source = 'assets/stage1.webp'
            # Reload the image
            self.ids.plant_image.reload()

        if self.stage == 1:
            # Change the image source
            self.ids.plant_image.source = 'assets/stage2.webp'
            # Reload the image
            self.ids.plant_image.reload()

        if self.stage == 2:
            # Change the image source
            self.ids.plant_image.source = 'assets/stage3.webp'
            # Reload the image
            self.ids.plant_image.reload()

        if self.stage == 3:
            self.ids.hydrate_button.source = 'assets/newHarvest.png'
            
    def press(self):
        if self.stage == 2:
            self.ids.hydrate_button.source = 'assets/newHarvest_pressed.png'
            self.growth = -1
            self.stage = 0  
            self.harvestCounter()
        else:
            self.ids.hydrate_button.source = 'assets/newHydrate_pressed.png'
        self.change_image()

    def off(self):
        if self.stage == 2:
            self.ids.hydrate_button.source = 'assets/newHarvest.png' 
        else:
            self.ids.hydrate_button.source = 'assets/newHydrate.png'
    
    def harvestCounter(self):
        self.harvest_count += 1
        self.text = str(self.harvest_count)
        
    def petPress(self):
        self.ids.petButton_image.source = 'assets/pets_pressed.png'

    def petOff(self):
        self.ids.petButton_image.source = 'assets/pets.png'
    
        
kv = Builder.load_file('Main.kv')

class MainApp(App):
    def on_start(self):
        authenticated = authenticate()
        #authenticated 0 is not authenticated, 1 is first time, 2 is existing user
        if authenticated:
            set_interval(check_drink_time,60)
            if authenticated==1:
                pass
            elif authenticated==2:
                pass
        else:
            pass
        return super().on_start()
    def build(self):
        return kv

if __name__ == '__main__':
    app = MainApp()
    app.run()
