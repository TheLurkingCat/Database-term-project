from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class MainPage(GridLayout):

    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.cols = 4

        self.add_widget(Label(text='Date 1: Year'))
        self.year1 = TextInput(multiline=False)
        self.add_widget(self.year1)
        self.add_widget(Label(text='Month'))
        self.month1 = TextInput(password=True, multiline=False)
        self.add_widget(self.month1)

        self.add_widget(Label(text='Date 2: Year'))
        self.year2 = TextInput(multiline=False)
        self.add_widget(self.year2)
        self.add_widget(Label(text='Month'))
        self.month2 = TextInput(multiline=False)
        self.add_widget(self.month2)


class FinalProject(App):

    def build(self):
        return MainPage()


if __name__ == '__main__':
    FinalProject().run()
