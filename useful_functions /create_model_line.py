# -*- coding: utf-8 -*-
# Copyright (c) Volkov Andrey,  2021
# 7771080@gmail.com
__title__ = 'Model line'
__doc__ = 'Создание модельной линии'
__autor__ = 'Volkov Andrey'

import clr
import os
import sys
from math import pi

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference("RevitServices")

from Autodesk.Revit.DB import XYZ, Transaction, FilteredElementCollector, BuiltInParameter, Plane, SketchPlane, Line, Arc
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.UI import Selection, TaskDialog, TaskDialogCommonButtons, TaskDialogResult, TaskDialogIcon
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
selection = uidoc.Selection
active_view = doc.ActiveView
T = Transaction(doc, "Split rectangle")

def multiply(a, b):
    new_x = a.Y * b.Z - a.Z * b.Y
    new_y = a.Z * b.Z - a.X * b.Z
    new_z = a.X * b.Y - a.Y * b.X
    return XYZ(new_x, new_y, new_z)


def create_line(p1, p2, plane=None):
    """Создание модельных линий"""
    if not plane:
        vector = p2-p1
        p3 = p1 + multiply(active_view.ViewDirection, vector).Normalize()
        plane = Plane.CreateByThreePoints(p1, p2, p3)
    sketch_plane = SketchPlane.Create(doc, plane)  # специальная плоскость на которой мы создаем линию
    new_line = Line.CreateBound(p1, p2)  # новая линия  
    m_line = doc.Create.NewModelCurve(new_line, sketch_plane) # создаем модельную линию
    return m_line


def create_arc(point, plane=None, radius = 0.3):
    """Создание окружности"""
    if not plane:
        plane = Plane.CreateByNormalAndOrigin(active_view.ViewDirection, point)
    sketch_plane = SketchPlane.Create(doc, plane)
    new_arc = Arc.Create(point, radius, 0, pi * 2, plane.XVec, plane.YVec)
    m_line = doc.Create.NewModelCurve(new_arc, sketch_plane)
    return m_line


def main():
    T.Start ("Создание модельной линии")
    line_1 = create_line(XYZ(0,0,0), XYZ(10,10,10))
    line_2 = create_arc(XYZ(0,0,0))
    T.Commit()


if __name__ == "__main__":
    main()
