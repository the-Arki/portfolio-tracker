import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDToolbar

from src.main import Portfolios

portfolios = Portfolios()
main_kv_file = "main.kv"


class NewPortfolio(MDBoxLayout):
    name = ObjectProperty("init")

    def get_name(self):
        print(self.name)

class Tracker(MDApp):
    dialog = None
    def build(self):
        self.load_kv(main_kv_file)
        return self.root

    # it has to be deleted (in .kv file as well)
    def test(self):
        print('button has been pushed')

    def add_portfolio(self):
        new = NewPortfolio()
        self.dialog = MDDialog(
            title="Add new portfolio",
            type="custom",
            content_cls=new,
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=self.close_dialog),
                MDFlatButton(
                    text="Add",
                    on_release=self.get_text
                    )
            ]
            )
        self.dialog.open()

    def get_text(self, inst):
        textfield = self.dialog.content_cls.name
        name = textfield.text
        if name:
            print(self.dialog.content_cls.name.text)
            if name in portfolios.instances.keys():
                textfield.error=True
                textfield.helper_text="{} has already been created".format(name)
            else:
                portfolios.create_instance(name)
                self.close_dialog(inst)

    def close_dialog(self, inst):
        self.dialog.dismiss()
        self.dialog = None


if __name__ == "__main__":
    Tracker().run()
