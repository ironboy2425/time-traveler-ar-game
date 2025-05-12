from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window

class DrawingWidget(Widget):
    def on_touch_down(self, touch):
        if touch.button == 'right':  # Right click draws red dot
            with self.canvas:
                Color(0.8, 0.1, 0.1)  # Red
                d = 20
                Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))

class TimeTravelerApp(App):
    def build(self):
        root = FloatLayout()

        # Set background image
        background = Image(source='A_digital_painting_depicts_an_enchanting_forest_ba.png',
                           allow_stretch=True,
                           keep_ratio=False,
                           size_hint=(1, 1),
                           pos_hint={'x': 0, 'y': 0})
        root.add_widget(background)

        # Drawing layer on top
        drawing_layer = DrawingWidget()
        root.add_widget(drawing_layer)

        return root

if __name__ == '__main__':
    TimeTravelerApp().run()
