# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 18:56 $"

import ttkbootstrap as ttk

from templates.FrameSliceFile import SliceFile
from templates.Frame_ReadFile import ReadFile


class MainGUI(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("PySLM")
        self.geometry("800x600")
        self.resizable(True, True)
        self.configure(bg="#f0f0f0")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # --------------------notebook-------------------
        self.frame_content = ttk.Frame(self)
        self.frame_content.grid(row=0, column=0, sticky="nsew")
        self.frame_content.columnconfigure(0, weight=1)
        self.frame_content.rowconfigure(0, weight=1)
        self.notebook = ttk.Notebook(self.frame_content)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)
        tab1 = ReadFile(self.notebook)
        self.notebook.add(tab1, text="Leer archivo")
        tab2 = SliceFile(self.notebook)
        self.notebook.add(tab2, text="Slicer")
