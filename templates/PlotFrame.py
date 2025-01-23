# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 22/ene/2025  at 21:03 $"

import ttkbootstrap as ttk
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pyslm.visualise


class PlotSTL(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.type_plot = kwargs.get("type_plot", "mesh_3d")
        match self.type_plot:
            case "mesh_3d":
                solid_trimesh_part = kwargs.get("solid_trimesh_part")
                self.figure = Figure(figsize=(5, 5), dpi=150)
                self.axes = self.figure.add_subplot(111, projection="3d")
                self.canvas = FigureCanvasTkAgg(self.figure, self)
                toolbar = NavigationToolbar2Tk(self.canvas, self)
                toolbar.update()
                self.canvas.get_tk_widget().pack(side=ttk.TOP, fill=ttk.BOTH, expand=1)
                if solid_trimesh_part is not None:
                    self.axes.plot_trisurf(
                        solid_trimesh_part.vertices[:, 0],
                        solid_trimesh_part.vertices[:, 1],
                        triangles=solid_trimesh_part.faces,
                        Z=solid_trimesh_part.vertices[:, 2],
                        cmap="viridis",
                    )
                    self.axes.set_xlabel("X")
                    self.axes.set_ylabel("Y")
                    self.axes.set_zlabel("Z")
                    self.axes.set_title("3D Part")
            case "layer":
                layer = kwargs.get("layer")
                if layer is None:
                    return
                self.figure = Figure(figsize=(5, 5), dpi=150)
                self.axes = self.figure.add_subplot(111)
                self.figure, self.axes = pyslm.visualise.plot(
                    layer,
                    plot3D=False,
                    plotOrderLine=True,
                    plotArrows=False,
                )
                self.canvas = FigureCanvasTkAgg(self.figure, self)
                toolbar = NavigationToolbar2Tk(self.canvas, self)
                toolbar.update()
                self.canvas.get_tk_widget().pack(side=ttk.TOP, fill=ttk.BOTH, expand=1)
            case _:
                print("No type plot")
