# -*- coding: utf-8 -*-
__author__ = "Edisson A. Naula"
__date__ = "$ 05/feb/2025  at 21:20 $"

from werkzeug.datastructures import FileStorage

from templates.static.constants import api

expected_files_almacen = api.parser()
expected_files_almacen.add_argument(
    "file", type=FileStorage, location="files", required=True
)
