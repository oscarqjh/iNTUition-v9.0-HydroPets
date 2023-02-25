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
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
)

Window.size = (360, 640)
Config.set('graphics', 'resizable', False)

# class MainPage(Screen):
#     pass

class PetScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

# class AppWidget(Widget):
#     pass

class Plant(Screen):
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
            self.image.source = 'assets/stage1.webp'
            # Reload the image
            self.image.reload()

        if self.stage == 1:
            # Change the image source
            self.image.source = 'assets/stage2.webp'
            # Reload the image
            self.image.reload()

        if self.stage == 2:
            # Change the image source
            self.image.source = 'assets/stage3.webp'
            # Reload the image
            self.image.reload()

        if self.stage == 3:
            self.ids.image.source = 'assets/newHarvest.png'
            
    def press(self):
        if self.stage == 2:
            self.ids.image.source = 'assets/newHarvest_pressed.png'
            self.growth = -1
            self.stage = 0  
            self.harvestCounter()
            print(self.harvest_count) 
        else:
            self.ids.image.source = 'assets/newHydrate_pressed.png'
        self.change_image()

    def off(self):
        if self.stage == 2:
            self.ids.image.source = 'assets/newHarvest.png' 
        else:
            self.ids.image.source = 'assets/newHydrate.png'
    
    def harvestCounter(self):
        self.harvest_count += 1
        self.text = str(self.harvest_count)
        
    def petPress(self):
        self.ids.petButton_image.source = 'assets/pets_pressed.png'

    def petOff(self):
        self.ids.petButton_image.source = 'assets/pets.png'
        
kv = Builder.load_file('Main.kv')

class MainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    app = MainApp()
    app.run()