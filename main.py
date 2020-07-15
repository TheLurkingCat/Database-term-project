from datetime import date
from functools import partial
from os import remove
from os.path import exists

import matplotlib.pyplot as plt
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from query.draw import draw
from query.query import TableType, TempType
from query.user import create, log, login, register, retrieve

create()

username = None


class LoginTable(GridLayout):
    def __init__(self,  ** kwargs):
        super(LoginTable, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='Username: '))
        self.username = TextInput(multiline=False)
        self.ids['Username'] = self.username
        self.add_widget(self.username)

        self.add_widget(Label(text='Password: '))
        self.password = TextInput(multiline=False, password=True)
        self.ids['Password'] = self.password
        self.add_widget(self.password)

        self.register = Button(text='Register')
        self.ids['Register'] = self.register
        self.add_widget(self.register)

        self.login = Button(text='Login')
        self.ids['Login'] = self.login
        self.add_widget(self.login)


class DateSelect(GridLayout):

    def __init__(self, **kwargs):
        super(DateSelect, self).__init__(**kwargs)
        self.cols = 4

        self.add_widget(Label(text='Start: Year'))
        self.start_year = TextInput(multiline=False)
        self.ids['StartYear'] = self.start_year
        self.add_widget(self.start_year)

        self.add_widget(Label(text='Month'))
        self.start_month = TextInput(multiline=False)
        self.ids['StartMonth'] = self.start_month
        self.add_widget(self.start_month)

        self.add_widget(Label(text='Date 2: Year'))
        self.end_year = TextInput(multiline=False)
        self.ids['EndYear'] = self.end_year
        self.add_widget(self.end_year)

        self.add_widget(Label(text='Month'))
        self.end_month = TextInput(multiline=False)
        self.ids['EndMonth'] = self.end_month
        self.add_widget(self.end_month)


class MyPop(Popup):
    def __init__(self, **kwargs):
        super(MyPop, self).__init__(**kwargs)
        self.isreg = False
        self.logintable = LoginTable()
        self.title = 'Login or Register?'
        self.content = self.logintable
        self.auto_dismiss = False
        self.logintable.ids['Register'].bind(
            on_press=partial(self.new_dismiss))
        self.logintable.ids['Login'].bind(on_press=partial(self.new_dismiss))
        self.bind(on_dismiss=self.save_data)

    def new_dismiss(self, instance):
        if instance.text == 'Register':
            self.isreg = True
        else:
            self.isreg = False
        self.dismiss()

    @staticmethod
    def save_data(instance):
        user = instance.logintable.ids['Username'].text
        password = instance.logintable.ids['Password'].text

        try:
            if instance.isreg:
                register(user, password)
            else:
                login(user, password)
        except KeyError as err:
            print(str(err)[1:-1])
        else:
            global username
            username = user
        instance.logintable.ids['Username'].text = ''
        instance.logintable.ids['Password'].text = ''


class GraphSelect(GridLayout):

    def __init__(self, **kwargs):
        super(GraphSelect, self).__init__(**kwargs)
        self.cols = 6
        self.rows = 4
        self.linegraph = CheckBox()
        self.linegraph.group = 'graph'
        self.linegraph.active = True
        self.add_widget(self.linegraph)
        self.ids['useline'] = self.linegraph

        self.add_widget(Label(text='Line graph'))
        self.bargraph = CheckBox()
        self.bargraph.group = 'graph'
        self.ids['usebar'] = self.bargraph
        self.add_widget(self.bargraph)
        self.add_widget(Label(text='Bar graph'))
        self.add_widget(Label())
        self.add_widget(Label())

        self.month = CheckBox()
        self.month.group = 'time'
        self.month.active = True
        self.ids['usemonth'] = self.month
        self.add_widget(self.month)
        self.add_widget(Label(text='Month data'))
        self.year = CheckBox()
        self.year.group = 'time'
        self.add_widget(self.year)
        self.ids['useyear'] = self.year
        self.add_widget(Label(text='Year data'))
        self.add_widget(Label())
        self.add_widget(Label())

        self.avg = CheckBox()
        self.add_widget(self.avg)
        self.add_widget(Label(text='Average'))
        self.ids['avg'] = self.avg

        self.max = CheckBox()
        self.add_widget(self.max)
        self.add_widget(Label(text='Max'))
        self.ids['max'] = self.max

        self.min = CheckBox()
        self.add_widget(self.min)
        self.add_widget(Label(text='Min'))
        self.ids['min'] = self.min

        self.add_widget(Label())
        self.login = Button(text='Login')
        self.add_widget(self.login)
        self.ids['login'] = self.login
        self.add_widget(Label())

        self.add_widget(Label())
        self.retrieve = Button(text='retrieve')
        self.add_widget(self.retrieve)
        self.ids['retrieve'] = self.retrieve
        self.add_widget(Label())


class Graph(Image):

    def __init__(self, **kwargs):
        super(Graph, self).__init__(**kwargs)
        self.source = 'figure.png'


class SearchInfo(GridLayout):

    def __init__(self, **kwargs):
        super(SearchInfo, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 2

        self.add_widget(Label(text='Country/City/State/Global'))

        self.qtype = TextInput(multiline=False)
        self.ids['qtype'] = self.qtype
        self.add_widget(self.qtype)

        self.add_widget(Label(text='Place (If not choose global)'))

        self.place = TextInput(multiline=False)
        self.ids['place'] = self.place
        self.add_widget(self.place)


class MainPage(GridLayout):

    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 2

        self.dateselect = DateSelect()
        self.ids['DateSelect'] = self.dateselect
        self.add_widget(self.dateselect)

        self.graph = Graph()
        self.ids['Graph'] = self.graph
        self.add_widget(self.graph)

        self.searchinfo = SearchInfo()
        self.ids['Search'] = self.searchinfo
        self.add_widget(self.searchinfo)

        self.graph_select = GraphSelect()
        self.ids['GraphSelect'] = self.graph_select
        self.add_widget(self.graph_select)


class FinalProject(App):

    def __init__(self, **kwargs):
        super(FinalProject, self).__init__(**kwargs)
        self.page = MainPage()
        self.style = ('solid', 'dashed', 'dashdot', 'dotted')
        self.loginpop = MyPop()
        self.page.ids['GraphSelect'].ids['login'].bind(
            on_press=self.loginpop.open)
        self.page.ids['GraphSelect'].ids['retrieve'].bind(
            on_press=partial(self.retrieve))

    def build(self):
        Window.bind(on_key_down=self.key_action)
        return self.page

    def retrieve(self, instance):
        if username is not None:
            try:
                meta, history = retrieve(username)
            except ValueError:
                print("No record")
            else:
                self.page.ids['GraphSelect'].ids['usebar'].active = meta['use_bar']
                self.page.ids['GraphSelect'].ids['useline'].active = not meta['use_bar']

                self.page.ids['GraphSelect'].ids['usemonth'].active = meta['use_month']
                self.page.ids['GraphSelect'].ids['useyear'].active = not meta['use_month']

                self.page.ids['GraphSelect'].ids['avg'].active = meta['avg']
                self.page.ids['GraphSelect'].ids['min'].active = meta['min']
                self.page.ids['GraphSelect'].ids['max'].active = meta['max']

                self.page.ids['Search'].ids['qtype'].text = history['search_type']
                self.page.ids['Search'].ids['place'].text = history['keyword']
                self.page.ids['DateSelect'].ids['StartYear'].text = str(
                    meta['year_start']
                )
                self.page.ids['DateSelect'].ids['StartMonth'].text = str(
                    meta['month_start']
                )
                self.page.ids['DateSelect'].ids['EndYear'].text = str(
                    meta['year_end']
                )
                self.page.ids['DateSelect'].ids['EndMonth'].text = str(
                    meta['month_end']
                )

    def key_action(self, *args):
        if args[1] == 13 or args[1] == 271:
            use_bar = self.page.ids['GraphSelect'].ids['usebar'].active
            use_month = self.page.ids['GraphSelect'].ids['usemonth'].active
            isavg = self.page.ids['GraphSelect'].ids['avg'].active
            ismin = self.page.ids['GraphSelect'].ids['min'].active
            ismax = self.page.ids['GraphSelect'].ids['max'].active

            qtype = self.page.ids['Search'].ids['qtype'].text
            place = self.page.ids['Search'].ids['place'].text
            try:
                start_date = date(
                    int(self.page.ids['DateSelect'].ids['StartYear'].text),
                    int(self.page.ids['DateSelect'].ids['StartMonth'].text),
                    1
                )
                end_date = date(
                    int(self.page.ids['DateSelect'].ids['EndYear'].text),
                    int(self.page.ids['DateSelect'].ids['EndMonth'].text),
                    1
                )
            except Exception as error:
                print("Error: " + str(error))

            if username is not None:
                meta = {
                    'username': username,
                    'year_start': int(self.page.ids['DateSelect'].ids['StartYear'].text),
                    'month_start': int(self.page.ids['DateSelect'].ids['StartMonth'].text),
                    'year_end': int(self.page.ids['DateSelect'].ids['EndYear'].text),
                    'month_end': int(self.page.ids['DateSelect'].ids['EndMonth'].text),
                    'use_bar': use_bar,
                    'use_month': use_month,
                    'avg': isavg,
                    'max': ismax,
                    'min': ismin
                }
                compare = {
                    'username': username,
                    'search_type': qtype,
                    'keyword': place
                }
                log(username, meta, compare)

            try:
                if qtype.lower() == 'global':
                    if isavg and not ismin and not ismax:
                        draw(start_date, end_date, True,
                             TempType.LANDAVG, None, use_bar, use_month, 'k', 'solid', 111)
                    elif ismin and not ismax and not isavg:
                        draw(start_date, end_date, True,
                             TempType.LANDMIN, None, use_bar, use_month, 'b', 'solid', 111)
                    elif ismax and not isavg and not ismin:
                        draw(start_date, end_date, True,
                             TempType.LANDMAX, None, use_bar, use_month, 'r', 'solid', 111)
                    elif ismin and ismax and not isavg:
                        draw(start_date, end_date, True,
                             TempType.LANDMIN, None, use_bar, use_month, 'b', 'solid', 211)
                        draw(start_date, end_date, True,
                             TempType.LANDMAX, None, use_bar, use_month, 'r', 'solid', 212)
                    elif ismax and isavg and not ismin:
                        draw(start_date, end_date, True,
                             TempType.LANDAVG, None, use_bar, use_month, 'k', 'solid', 211)
                        draw(start_date, end_date, True,
                             TempType.LANDMAX, None, use_bar, use_month, 'r', 'solid', 212)
                    elif isavg and ismin and not ismax:
                        draw(start_date, end_date, True,
                             TempType.LANDAVG, None, use_bar, use_month, 'k', 'solid', 211)
                        draw(start_date, end_date, True,
                             TempType.LANDMIN, None, use_bar, use_month, 'b', 'solid', 212)
                    elif ismin and ismax and isavg:
                        draw(start_date, end_date, True,
                             TempType.LANDAVG, None, use_bar, use_month, 'k', 'solid', 211)
                        draw(start_date, end_date, True,
                             TempType.LANDMAX, None, use_bar, use_month, 'r', 'solid', 223)
                        draw(start_date, end_date, True,
                             TempType.LANDMIN, None, use_bar, use_month, 'b', 'solid', 224)
                    else:
                        print("No selection")
                elif qtype.lower() == 'city':
                    draw(start_date, end_date, False,
                         TableType.CITY, place, use_bar, use_month, 'k', 'solid', 111)
                elif qtype.lower() == 'country':
                    draw(start_date, end_date, False,
                         TableType.COUNTRY, place, use_bar, use_month, 'k', 'solid', 111)
                elif qtype.lower() == 'state':
                    draw(start_date, end_date, False,
                         TableType.STATE, place, use_bar, use_month, 'k', 'solid', 111)

                else:
                    print("No position")
            except Exception:
                pass
            else:
                plt.savefig('figure.png')
                self.page.ids['Graph'].reload()
            finally:
                plt.close()


if __name__ == '__main__':
    FinalProject().run()
    if exists('figure.png'):
        remove('figure.png')
