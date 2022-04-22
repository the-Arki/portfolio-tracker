import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDToolbar

from src.main import Portfolios

portfolios = Portfolios()
main_kv_file = "main.kv"


class Main(MDApp):
    def build(self):
        self.load_kv(main_kv_file)
        return Builder.load_file(main_kv_file)

Main().run()