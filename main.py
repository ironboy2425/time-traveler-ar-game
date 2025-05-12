from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MainLayout(BoxLayout):
    pass

class TimeTravelerApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    TimeTravelerApp().run()
