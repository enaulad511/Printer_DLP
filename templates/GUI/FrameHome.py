# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 20/feb/2025  at 14:21 $"

import json

import ttkbootstrap as ttk

from files.constants import font_buttons, font_title
from templates.AuxiliarFunctions import (
    read_projects,
    update_settings,
    create_new_project,
)


class HomePage(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.current_data_p = None
        self.frame_new_project = None
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)
        self.master = master
        self.callbacks = kwargs.get("callbacks")
        # ------------------------ProjectFilesSelector----------------------
        self.frame_new = ttk.Frame(self)
        self.frame_new.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.frame_new.columnconfigure(0, weight=1)
        ttk.Button(
            self.frame_new,
            text="New Project",
            command=self.new_project_callback,
            style="success.TButton",
        ).grid(row=0, column=0, sticky="e", padx=10, pady=10)

        self.frame_previous = ttk.Frame(self)
        self.frame_previous.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.frame_previous.columnconfigure(0, weight=1)
        projects = read_projects()
        data_lists = [
            [
                k,
                v.get("name"),
                v.get("timestamp"),
                v.get("user"),
                v.get("status"),
                json.dumps(v),
            ]
            for k, v in projects.items()
        ]
        data_lists.sort(key=lambda x: x[2], reverse=True)
        self.current_project_key = data_lists[0][0]
        self.current_p_text = ttk.StringVar(
            value=f"Current Project: {data_lists[0][1]}"
        )
        ttk.Label(
            self.frame_previous,
            textvariable=self.current_p_text,
            font=font_buttons,
            style="Custom.TLabel",
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ttk.Label(
            self.frame_previous,
            text="Previous Projects",
            font=font_buttons,
            style="Custom.TLabel",
        ).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.tv_projects = ttk.Treeview(
            self.frame_previous,
            columns=("name", "timestamp"),
            show="headings",
            style="Custom.Treeview",
        )
        self.tv_projects.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.tv_projects.configure(
            columns=("key", "name", "Last modified", "User", "Status", "data")
        )
        for col in self.tv_projects["columns"]:
            self.tv_projects.heading(col, text=col.title(), anchor="w")
        # hide data column
        self.tv_projects.column("data", stretch=False, width=0)
        self.tv_projects.column("key", stretch=False, width=0)
        # insert data
        for item in data_lists:
            self.tv_projects.insert("", "end", values=item)
        self.tv_projects.bind("<Double-1>", self.item_selected_treeview)

    def new_project_callback(self):
        if self.frame_new_project is None:
            self.frame_new_project = NewProjectWindow(self)

    def item_selected_treeview(self, event):
        values = event.widget.item(event.widget.selection()[0], "values")
        data = json.loads(values[-1])
        self.current_project_key = values[0]
        self.current_p_text.set(f"Current Project: {data.get('name')}")
        self.callbacks["change_title"](f"Project: {data.get('name')}")
        update_settings(**data.get("settings", {}))
        self.current_data_p = data
        self.callbacks["change_tab_text"](
            data.get("settings", {"status_frames"}).get("status_frames", [0, 0, 0, 0])
        )
        self.callbacks["init_tabs"]()


class NewProjectWindow(ttk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("New Project")
        self.attributes("-topmost", True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frame = NewProjectForm(self)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.frame.on_close(from_parent=True)
        self.destroy()


def create_widgets_form_new_project(master):
    ttk.Label(master, text="Project Data", font=font_title).grid(
        row=0, column=0, sticky="n", padx=10, pady=10
    )

    frame_widgets = ttk.Frame(master)
    frame_widgets.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    frame_widgets.columnconfigure(0, weight=1)

    entries = []
    ttk.Label(frame_widgets, text="Project Name", style="Custom.TLabel").grid(
        row=0, column=0, sticky="n", padx=10, pady=10
    )
    entry_name = ttk.StringVar()
    ttk.Entry(frame_widgets, textvariable=entry_name, style="Custom.TEntry").grid(
        row=1, column=0, sticky="n", padx=10, pady=10
    )
    entries.append(entry_name)

    ttk.Label(frame_widgets, text="Project user", style="Custom.TLabel").grid(
        row=2, column=0, sticky="n", padx=10, pady=10
    )
    entry_user = ttk.StringVar()
    ttk.Entry(frame_widgets, textvariable=entry_user, style="Custom.TEntry").grid(
        row=3, column=0, sticky="n", padx=10, pady=10
    )
    entries.append(entry_user)

    return entries


class NewProjectForm(ttk.Frame):
    def __init__(self, master, *kwargs):
        super().__init__(master)
        self.master = master
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Project Data", font=font_title).grid(
            row=0, column=0, sticky="n", padx=10, pady=10
        )

        self.frame_widgets = ttk.Frame(self)
        self.frame_widgets.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.entries = create_widgets_form_new_project(self.frame_widgets)

        self.frame_buttons = ttk.Frame(self)
        self.frame_buttons.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.frame_buttons.columnconfigure(0, weight=1)
        ttk.Button(
            self.frame_buttons,
            text="Create",
            command=self.on_close,
            style="success.TButton",
        ).grid(row=0, column=0, sticky="e", padx=10, pady=10)

    def on_close(self, from_parent=False):
        data = [entry.get() for entry in self.entries]
        print(data)
        create_new_project(
            {
                "name": data[0],
                "user": data[1],
                "status": 0,
            }
        )
        if not from_parent:
            self.master.destroy()
