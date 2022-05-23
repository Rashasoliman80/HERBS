import os
from os.path import dirname, realpath, join
import sys
from sys import argv, exit
from pathlib import Path
import queue
import requests

import pickle
import csv
import nibabel as nib
import tifffile as tiff
from aicspylibczi import CziFile


import numpy as np
import pandas as pd
import math
import scipy
import scipy.io
import scipy.ndimage as ndi
from scipy.ndimage import map_coordinates
from natsort import natsorted, ns

import cv2
opencv_ver = (cv2.__version__).split('.')
from numba import jit
import colorsys


import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtMultimedia import QSound
# from PyQt5 import uic
from PyQt5.uic import loadUiType
import pyqtgraph as pg
pg.setConfigOption('imageAxisOrder', 'row-major')
pg.setConfigOption('useNumba', True)
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph import metaarray

import warnings


from .uuuuuu import *
from .czi_reader import CZIReader

from .atlas_downloader import AtlasDownloader
from .atlas_processor import AtlasProcessor
from .atlas_loader import AtlasLoader
from .atlas_view import AtlasView

from .image_reader import ImageReader, ImagesReader
from .image_curves import *
from .image_view import ImageView

from .layers_control import *
from .object_control import *
from .toolbox import ToolBox
from .wtiles import LayerSettingDialog, SliceSettingDialog
from .styles import Styles


herbs_style = '''
QMainWindow {
    background-color: rgb(50, 50, 50);
    color: white;
    font-size: 12px;
}

/*---------------------- QComboBox -----------------------*/
QComboBox {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    selection-background-color: transparent;
    color: white;
    background-color: #656565;
    border: None;
    border-radius: 5px;
    padding: 0px 0px 0px 5px;
    margin: 0px;
}


QComboBox:item {
    background: #656565;
    color: white;
    height: 20px;
    margin: 0px;
    padding: 3px;
}

QComboBox:item:selected
{
    border: 3px solid #656565;
    background: #232323;
    margin: 0px;
    color: white;
    padding: 3px;
}


QComboBox:editable {
    background: #656565;
    margin: 0px;
}

QComboBox:!editable, QComboBox::drop-down:editable {
     background: #656565;
}

QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    background: #656565;
    margin: 0px;
    padding: 0px;
}

QComboBox:on { /* shift the text when the popup opens */
    margin: 0px;
    padding: 0px;
    color: white;
    background-color: transparent;
    selection-background-color: transparent;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-top: None;
    border-bottom: None;
    border-left-width: 1px;
    border-left-color: transparent;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
    margin: 0px;
}

QComboBox::down-arrow {
    image: url(icons/tdown.svg);
    width: 13px;
    height: 14px;
    padding-right: 3px;
}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
    top: 1px;
    left: 1px;
}



/*---------------------- Slider -----------------------*/
QSlider {
    min-height: 20px;
    max-height: 20px;
    background: transparent;
    border: None;
}

QSlider::groove:horizontal {
    border: None;
    height: 2px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
    margin: 2px 0px;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
    border: 1px solid #5c5c5c;
    width: 10px;
    height: 30px;
    margin: -4px -2px; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
    border-radius: 0px;
}

/*---------------------- LineEdit -----------------------*/
QLineEdit { 
    background-color: transparent;
    color: white;
}

/*---------------------- SpinBox -----------------------*/
QSpinBox {
    padding-right: 0px; /* make room for the arrows */
    border: 1px solid #242424;
    background: transparent;
    color: white;
}

QSpinBox::up-button {
    background: transparent;
    subcontrol-origin: border;
    subcontrol-position: top right; /* position at the top right corner */
    width: 15px; 
    border-width: 0px;
}

QSpinBox::down-button {
    background: transparent;
    subcontrol-origin: border;
    subcontrol-position: bottom right; /* position at bottom right corner */
    width: 15px;
    border-width: 0px;
}

QSpinBox::up-button:hover {
    background-color: #282828;
}

QSpinBox::down-button:hover {
    background-color: #282828;
}

QSpinBox::up-button:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #282828, stop: 1 #323232);
}

QSpinBox::down-button:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #323232, stop: 1 #282828);
}

QSpinBox::up-arrow {
    image: url(icons/up-arrow.svg);
    width: 7px;
    height: 7px;
}

QSpinBox::down-arrow {
    image: url(icons/down-arrow.svg);
    width: 7px;
    height: 7px;
}

/*---------------------- DoubleSpinBox -----------------------*/
QDoubleSpinBox {
    padding-right: 0px; 
    border: 1px solid #242424;
    background: transparent;
    color: white;
    
}

QDoubleSpinBox::up-button {
    background: transparent;
    subcontrol-origin: border;
    subcontrol-position: top right; /* position at the top right corner */
    width: 15px; 
    border: None;
}

QDoubleSpinBox::down-button {
    background: transparent;
    subcontrol-origin: border;
    subcontrol-position: bottom right; /* position at bottom right corner */
    width: 15px;
    border: None;
}

QDoubleSpinBox::up-button:hover {
    background-color: #282828;
}

QDoubleSpinBox::down-button:hover {
    background-color: #282828;
}

QDoubleSpinBox::up-button:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #282828, stop: 1 #000000);
}

QDoubleSpinBox::down-button:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #000000, stop: 1 #282828);
}

QDoubleSpinBox::up-arrow {
    image: url(icons/up-arrow.svg);
    width: 7px;
    height: 7px;
}

QDoubleSpinBox::down-arrow {
    image: url(icons/down-arrow.svg);
    width: 7px;
    height: 7px;
}



/*---------------------- QSplitter -----------------------*/
QSplitter::handle {
    image: url(icons/dot.svg);
}

QSplitter::handle:horizontal {
    width: 5px;
}

QSplitter::handle:vertical {
    height: 5px;
}

'''


toolbar_style = '''
QToolBar::separator { 
    color: white;
    background-color: gray;
    width: 1px;
    height: 10px;
    border: 5px solid rgb(50, 50, 50);
}


QToolBar {
    color: rgb(255, 255, 255);
    background-color: rgb(50, 50, 50);
    border: None;
    selection-color: rgb(50, 50, 50);
    selection-background-color: #27292a;
    spacing: 0px;
}

QToolButton {
    border-top: 2px solid rgb(50, 50, 50);
    border-bottom: 2px solid rgb(50, 50, 50);
}

QRadioButton {
    color: white;
}


QToolButton:hover {
    background-color: #27292a;
    border-top: 2px solid #27292a;
    border-bottom: 2px solid #27292a;
}

QToolButton:checked {
    border-bottom: 2px solid gray;
}

QPushButton {
    background-color: rgb(50, 50, 50);
    border: 0px solid gray;
    width: 32px;
    height: 32px;
    margin: 0px;
    padding: 0px;
}

QPushButton:hover {
    background-color: #27292a;
}

QLabel {
    color: #d6d6d6;
    background-color: rgb(50, 50, 50);
}

QLineEdit { 
    border: 1px solid gray;
}



QSlider::groove:horizontal {
    border: 1px solid #999999;
    height: 2px; 
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
    margin: 2px 0;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
    border: 1px solid #5c5c5c;
    width: 18px;
    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
    border-radius: 3px;
}

'''

sidebar_button_style = '''
QPushButton{
    background: #656565;
    border-radius: 5px;
    color: white;
    border-style: outset;
    border-bottom: 1px solid rgb(30, 30, 30);
    height: 24px;
    margin: 0px;
}

QPushButton:hover{
    background-color: #323232;
    border: 1px solid #656565;
}

QPushButton:checked{
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #17bb00, stop: 1 #0e6900);
    border-bottom: 1px solid rgb(30, 30, 30);
    border-top: None;
    border-left: None;
    border-right: None;  
}
'''

menubar_style = '''
QMenuBar {
    background-color: rgb(25, 27, 29);
    color: rgb(254, 252, 255);
    border-bottom-color: rgb(37, 37, 37);
}

QMenuBar::item {
    spacing: 50px;
    background-color: rgb(25, 27, 29);
    color: rgb(254, 252, 255);
    border-bottom-color: rgb(37, 37, 37);
}

QMenuBar::item:selected {
    background-color: red;
    color: rgb(254, 252, 255);
    border-bottom-color: rgb(37, 37, 37);
}
 
QMenu {
    border: None; 
    color: rgb(255, 255, 255);
    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgb(42, 49, 53), stop:1 rgb(85, 85, 88));
}

QMenu:hover {
    border: None; 
    color: rgb(255, 255, 255);
    background-color: red;
}
 
QMenu::item{
    Background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(42, 49, 53, 255), stop:1 rgba(85, 85, 88, 255));
    Border: 2px solid transparent; // border
    Padding: 20 25 20 20px;
}

QMenu::item:selected{
    color: rgb(255, 255, 255);
    background-color: rgb(63, 124, 234);
    
}

'''

script_dir = dirname(realpath(__file__))
FORM_Main, _ = loadUiType((join(dirname(__file__), "main_window.ui")))


class HERBS(QMainWindow, FORM_Main):
    """
    easier for me to trace:
    connect all menu actions
    Menu Bar ---- Edit ----- related
    Menubar - View - Window Control
    Menu Bar ---- Image ----- related
    Menu Bar ---- Atlas ----- related

    ToolBar layout and connections
    ToolBar checkable btn clicked

    SideBar layout and connections : init_side_bar()

    ToolBar ruler btn related
    ToolBar lasso btn related
    ToolBar probe btn related
    ToolBar pencil btn related
    ToolBar eraser btn related
    ToolBar loc btn related
    ToolBar magic wand btn related
    ToolBar triangle btn related
    ToolBar transform btn clicked

    Image window - Image Processing

    Sidebar - Atlas panel related

    Atlas window related: coronal_slice_stacks_hovered ...
    Atlas 3D control

    Sidebar - Layer Panel, all layer related functions
    Sidebar - Object Control

    Atlas Loader
    Image Loader

    Menu Bar ---- File ----- related
    """
    def __init__(self, parent=FORM_Main):
        super(HERBS, self).__init__()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("HERBS - A toolkit for Histological E-data Registration in Brain Space")

        self.num_windows = 1

        self.styles = Styles()

        self.atlas_folder = None
        self.current_img_path = None
        self.current_img_name = None

        self.atlas_img_path = None

        self.small_mesh_list = {}

        self.img_lasso_is_closure = False
        self.atlas_lasso_is_closure = False
        self.eraser_is_on = False
        self.is_pencil_allowed = False
        self.pencil_size = 3

        self.probe_type = 0
        self.tip_length = 175
        self.channel_size = 20
        self.channel_number_in_banks = (384, 384, 192)

        self.np_onside = None
        self.atlas_rect = None
        self.histo_rect = None
        self.small_atlas_rect = None
        self.small_histo_rect = None

        self.atlas_corner_points = None
        self.atlas_side_lines = None
        self.atlas_tri_data = []
        self.atlas_tri_inside_data = []
        self.atlas_tri_onside_data = []

        self.histo_corner_points = None
        self.histo_side_lines = None
        self.histo_tri_data = []
        self.histo_tri_inside_data = []
        self.histo_tri_onside_data = []

        self.drawing_allowed = False

        self.working_img_data = {'img-overlay': None,
                                 'img-mask': None,
                                 'img-probe': [],
                                 'img-cells': [],
                                 'img-contour': [],
                                 'img-virus': None,
                                 'img-drawing': [],
                                 'img-blob': [],
                                 'cell_count': [0 for i in range(5)],
                                 'cell_size': [],
                                 'cell_symbol': [],
                                 'cell_layer_index': [],
                                 'lasso_path': [],
                                 'ruler_path': []}
        self.working_img_type = {'img-overlay': 'image',
                                 'img-mask': 'image',
                                 'img-probe': 'vector',
                                 'img-cells': 'vector',
                                 'img-contour': 'vector',
                                 'img-virus': 'image',
                                 'img-drawing': 'vector',
                                 'img-blob': 'vector',
                                 'cell_size': 'vector',
                                 'cell_symbol': 'vector',
                                 'cell_layer_index': 'vector',
                                 'lasso_path': 'vector',
                                 'ruler_path': 'vector'}

        self.working_atlas_data = {'atlas-overlay': None,
                                   'atlas-mask': None,
                                   'atlas-probe': [],
                                   'atlas-cells': [],
                                   'atlas-contour': [],
                                   'atlas-virus': [],
                                   'atlas-drawing': [],
                                   'atlas-slice': None,
                                   'cell_count': [0 for i in range(5)],
                                   'cell_size': [],
                                   'cell_symbol': [],
                                   'cell_layer_index': [],
                                   'lasso_path': [],
                                   'ruler_path': []}
        self.working_atlas_type = {'atlas-overlay': 'image',
                                   'atlas-mask': 'image',
                                   'atlas-probe': 'vector',
                                   'atlas-cells': 'vector',
                                   'atlas-contour': 'vector',
                                   'atlas-virus': 'vector',
                                   'atlas-drawing': 'vector',
                                   'atlas-slice': 'image',
                                   'cell_size': 'vector',
                                   'cell_symbol': 'vector',
                                   'cell_layer_index': 'vector',
                                   'lasso_path': 'vector',
                                   'ruler_path': 'vector'}

        self.cell_base_symbol = ['+', '+', 'x', 't', 's']

        self.working_atlas_text = []
        self.working_img_text = []

        self.a2h_transferred = False
        self.h2a_transferred = False
        self.project_method = 'pre plan'
        self.register_method = 0

        self.action_list = []
        self.layer_action_after_matching = []

        self.probe_lines_2d_list = []

        self.object_3d_list = []

        self.previous_checked_label = []
        self.atlas_display = 'coronal'
        self.show_child_mesh = False
        self.warning_status = False

        self.current_checked_tool = None

        self.drawing_img = None
        self.cell_img = None
        self.probe_img = None

        self.processing_img = None
        self.processing_img_size = None
        self.processing_tb_size = None

        self.processing_slice_is_allowed = False

        self.overlay_img = None

        self.error_message_color = '#ff6e6e'
        self.reminder_color = 'gray'
        self.normal_color = 'white'

        self.layer_shift_val = 1
        self.layer_rotate_val = 1
        self.action_id = 0
        self.undo_count = 0
        self.redo_count = -1

        self.current_atlas = 'volume'
        self.slice_tb_size = None
        self.slice_cut = 'Coronal'
        self.slice_width = 0
        self.slice_height = 0
        self.slice_distance = 0
        self.slice_bregma = []
        self.slice_boundary_points = []
        self.slice_info_ready = False

        self.kernel = None

        # ---------------------
        self.tool_box = ToolBox()
        self.toolbar_wrap_action_dict = {}
        self.pencil_color = (255, 102, 0)
        self.probe_color = (0, 0, 255)
        self.cell_color = (0, 255, 0)
        self.lasso_color = (0, 255, 255)
        self.magic_wand_lut = np.array([[0, 0, 0, 0], [255, 0, 255, 255]])
        self.magic_wand_lut[1] = np.ravel(self.tool_box.magic_color_btn.color().getRgb()).astype(int)
        self.contour_color = self.magic_wand_lut[1].copy()
        self.triangle_color = np.ravel(self.tool_box.triang_color_btn.color().getRgb()).astype(int)
        self.virus_lut = self.magic_wand_lut.copy()

        # ---------------------------- load controls, views, panels
        self.layer_ctrl = LayersControl()
        self.layer_ctrl.sig_opacity_changed.connect(self.layers_opacity_changed)
        self.layer_ctrl.sig_visible_changed.connect(self.layers_visible_changed)
        self.layer_ctrl.sig_layer_deleted.connect(self.layers_exist_changed)
        self.layer_ctrl.sig_blend_mode_changed.connect(self.layers_blend_mode_changed)

        self.object_ctrl = ObjectControl()
        self.object_ctrl.sig_delete_object.connect(self.object_deleted)
        self.object_ctrl.sig_color_changed.connect(self.obj_color_changed)
        self.object_ctrl.sig_visible_changed.connect(self.obj_vis_changed)
        self.object_ctrl.sig_size_changed.connect(self.obj_size_changed)
        self.object_ctrl.sig_opacity_changed.connect(self.obj_opacity_changed)
        self.object_ctrl.sig_blend_mode_changed.connect(self.obj_blend_mode_changed)
        self.object_ctrl.add_object_btn.clicked.connect(self.make_object_pieces)
        self.object_ctrl.merge_probe_btn.clicked.connect(self.merge_probes)
        self.object_ctrl.merge_virus_btn.clicked.connect(self.merge_virus)
        self.object_ctrl.merge_cell_btn.clicked.connect(self.merge_cells)
        self.object_ctrl.merge_contour_btn.clicked.connect(self.merge_contour)
        self.object_ctrl.merge_drawing_btn.clicked.connect(self.merge_drawings)

        self.image_view = ImageView()
        self.image_view.sig_image_changed.connect(self.update_histo_tri_onside_data)
        self.image_view.img_stacks.sig_mouse_clicked.connect(self.img_stacks_clicked)
        self.image_view.img_stacks.sig_mouse_hovered.connect(self.img_stacks_hovered)
        self.image_view.img_stacks.sig_key_pressed.connect(self.img_stacks_key_pressed)
        self.image_view.img_stacks.image_dict['tri_pnts'].mouseDragged.connect(self.hist_window_tri_pnts_moving)
        self.image_view.img_stacks.image_dict['tri_pnts'].mouseClicked.connect(self.hist_window_tri_pnts_clicked)
        self.image_view.img_stacks.image_dict['lasso_path'].sigPointsClicked.connect(self.lasso_points_clicked)
        self.image_view.img_stacks.image_dict['ruler_path'].sigPointsClicked.connect(self.img_ruler_points_clicked)
        # self.image_view.img_stacks.image_dict['img-cells'].sigClicked.connect(self.img_cell_pnts_clicked)
        # self.image_view.img_stacks.image_dict['img-probe'].sigClicked.connect(self.img_probe_pnts_clicked)
        # self.image_view.img_stacks.image_dict['img-drawing'].sigClicked.connect(self.img_drawing_pnts_clicked)

        self.atlas_view = AtlasView()
        self.atlas_view.show_boundary_btn.clicked.connect(self.vis_atlas_boundary)
        self.atlas_view.section_rabnt1.toggled.connect(self.display_changed)
        self.atlas_view.section_rabnt2.toggled.connect(self.display_changed)
        self.atlas_view.section_rabnt3.toggled.connect(self.display_changed)
        self.atlas_view.label_tree.labels_changed.connect(self.sig_label_changed)
        # hovered
        self.atlas_view.cimg.sig_mouse_hovered.connect(self.coronal_slice_stacks_hovered)
        self.atlas_view.simg.sig_mouse_hovered.connect(self.sagital_slice_stacks_hovered)
        self.atlas_view.himg.sig_mouse_hovered.connect(self.horizontal_slice_stacks_hovered)
        # clicked
        self.atlas_view.cimg.sig_mouse_clicked.connect(self.atlas_stacks_clicked)
        self.atlas_view.simg.sig_mouse_clicked.connect(self.atlas_stacks_clicked)
        self.atlas_view.himg.sig_mouse_clicked.connect(self.atlas_stacks_clicked)
        # ruler points
        self.atlas_view.cimg.image_dict['ruler_path'].sigPointsClicked.connect(self.atlas_ruler_points_clicked)
        self.atlas_view.simg.image_dict['ruler_path'].sigPointsClicked.connect(self.atlas_ruler_points_clicked)
        self.atlas_view.himg.image_dict['ruler_path'].sigPointsClicked.connect(self.atlas_ruler_points_clicked)
        # triangle points moving and clicked
        self.atlas_view.cimg.image_dict['tri_pnts'].mouseDragged.connect(self.atlas_window_tri_pnts_moving)
        self.atlas_view.cimg.image_dict['tri_pnts'].mouseClicked.connect(self.atlas_window_tri_pnts_clicked)
        self.atlas_view.himg.image_dict['tri_pnts'].mouseDragged.connect(self.atlas_window_tri_pnts_moving)
        self.atlas_view.himg.image_dict['tri_pnts'].mouseClicked.connect(self.atlas_window_tri_pnts_clicked)
        self.atlas_view.simg.image_dict['tri_pnts'].mouseDragged.connect(self.atlas_window_tri_pnts_moving)
        self.atlas_view.simg.image_dict['tri_pnts'].mouseClicked.connect(self.atlas_window_tri_pnts_clicked)
        # probe clicked
        self.atlas_view.cimg.image_dict['atlas-probe'].sigClicked.connect(self.atlas_probe_pnts_clicked)
        self.atlas_view.simg.image_dict['atlas-probe'].sigClicked.connect(self.atlas_probe_pnts_clicked)
        self.atlas_view.himg.image_dict['atlas-probe'].sigClicked.connect(self.atlas_probe_pnts_clicked)
        # contour clicked
        # self.atlas_view.cimg.image_dict['atlas-contour'].sigClicked.connect(self.atlas_contour_pnts_clicked)
        # self.atlas_view.simg.image_dict['atlas-contour'].sigClicked.connect(self.atlas_contour_pnts_clicked)
        # self.atlas_view.himg.image_dict['atlas-contour'].sigClicked.connect(self.atlas_contour_pnts_clicked)
        # slice_stack
        self.atlas_view.slice_stack.sig_mouse_clicked.connect(self.atlas_stacks_clicked)
        self.atlas_view.slice_stack.sig_mouse_hovered.connect(self.slice_stack_hovered)
        self.atlas_view.slice_stack.sig_key_pressed.connect(self.slice_stack_key_pressed)
        self.atlas_view.slice_stack.image_dict['lasso_path'].sigPointsClicked.connect(
            self.slice_window_lasso_points_clicked)
        self.atlas_view.slice_stack.image_dict['ruler_path'].sigPointsClicked.connect(
            self.atlas_ruler_points_clicked)

        # set color to mask layer
        self.image_view.img_stacks.image_dict['img-mask'].setLookupTable(self.magic_wand_lut)
        self.atlas_view.cimg.image_dict['atlas-mask'].setLookupTable(self.magic_wand_lut)
        self.atlas_view.himg.image_dict['atlas-mask'].setLookupTable(self.magic_wand_lut)
        self.atlas_view.simg.image_dict['atlas-mask'].setLookupTable(self.magic_wand_lut)

        # --------------------------------------------------------
        #                 connect all menu actions
        # --------------------------------------------------------
        # self.menuBar.setStyleSheet(menubar_style)
        # file menu related
        self.actionAtlas.triggered.connect(self.load_atlas_clicked)
        self.actionSingle_Image.triggered.connect(self.load_image)
        # self.actionSave_Processed_Image.triggered.connect(lambda: self.save_image('Processed'))
        # self.actionSave_Overlay_Image.triggered.connect(lambda: self.save_image('Overlay'))
        # self.actionSave_Mask_Image.triggered.connect(lambda: self.save_image('Mask'))
        self.actionSave_Project.triggered.connect(self.save_project)
        # self.actionCurrent_Layer.triggered.connect(self.save_current_layer)
        # self.actionAll_Layer.triggered.connect(self.save_all_layer)
        self.actionSave_Current.triggered.connect(self.save_current_object)
        self.actionSave_Probes.triggered.connect(lambda: self.save_merged_object('probe'))
        self.actionSave_Cells.triggered.connect(lambda: self.save_merged_object('cell'))
        self.actionSave_Virus.triggered.connect(lambda: self.save_merged_object('virus'))
        self.actionSave_Drawings.triggered.connect(lambda: self.save_merged_object('drawing'))
        self.actionSave_Contours.triggered.connect(lambda: self.save_merged_object('contour'))
        self.actionLoad_Project.triggered.connect(self.load_project)
        self.actionLoad_Objects.triggered.connect(self.load_object)
        # self.actionLoad_Layers.triggered.connect(self.load_layers)

        # edit menu related
        self.actionDistance.triggered.connect(self.shift_setting_changed)
        self.actionAngle.triggered.connect(self.rotate_setting_changed)
        self.actionUp.triggered.connect(lambda: self.vertical_translation_pressed('up'))
        self.actionDown.triggered.connect(lambda: self.vertical_translation_pressed('down'))
        self.actionLeft.triggered.connect(lambda: self.horizontal_translation_pressed('left'))
        self.actionRight.triggered.connect(lambda: self.horizontal_translation_pressed('right'))
        self.actionClockwise.triggered.connect(lambda: self.layer_rotation_pressed('clockwise'))
        self.actionCounter_Clockwise.triggered.connect(lambda: self.layer_rotation_pressed('counter_clock'))
        self.actionUndo.triggered.connect(self.undo_called)
        self.actionRedo.triggered.connect(self.redo_called)

        # atlas menu related
        self.actionDownload.triggered.connect(self.download_waxholm_rat_atlas)
        self.actionAtlas_Processor.triggered.connect(self.process_raw_atlas_data)
        self.actionLoad_Image_Atlas.triggered.connect(self.load_atlas_slice)
        self.actionCrop.triggered.connect(self.crop_slice)
        self.actionRegister_Slice_Info.triggered.connect(self.register_slice_info)
        self.actionSave_Slice.triggered.connect(self.save_processed_slice)
        self.actionSwitch_Atlas.triggered.connect(self.switch_atlas)
        self.actionBregma_Picker.setCheckable(True)
        self.actionBregma_Picker.triggered.connect(self.pick_bregma)
        self.actionCreate_Slice_Layer.triggered.connect(self.process_slice)
        self.actionSave_Triangulation_Points.triggered.connect(self.save_triangulation_points)
        self.actionLoad_Triangulation_Points.triggered.connect(self.load_triangulation_points)

        # view menu related
        self.actionCoronal_Window.triggered.connect(self.show_only_coronal_window)
        self.actionSagital_Window.triggered.connect(self.show_only_sagital_window)
        self.actionHorizontal_Window.triggered.connect(self.show_only_horizontal_window)
        self.action3D_Window.triggered.connect(self.show_only_3d_window)
        self.actionImage_Window.triggered.connect(self.show_only_image_window)
        self.actionVolume_Histology.triggered.connect(self.show_2_windows)
        self.action4_Windows.triggered.connect(self.show_4_windows)
        self.actionSlice_Histology.triggered.connect(self.show_slice_and_histology)

        self.actionShow_Grids.triggered.connect(lambda: self.show_grids(True))
        self.actionHide_Grids.triggered.connect(lambda: self.show_grids(False))

        # image menu related
        self.actionFlip_Horizontal.triggered.connect(self.image_view.image_horizon_flip)
        self.actionFlip_Vertical.triggered.connect(self.image_view.image_vertical_flip)
        self.action180.triggered.connect(self.image_view.image_180_rotate)
        self.action90_Clockwise.triggered.connect(self.image_view.image_90_rotate)
        self.action90_Counter_Clockwise.triggered.connect(self.image_view.image_90_counter_rotate)
        self.actionProcess_Image.triggered.connect(self.turn_current_to_process)
        self.actionReset_Image.triggered.connect(self.reset_current_image)
        self.action1_Clockwise.triggered.connect(lambda: self.image_view.image_1_rotate('clockwise'))
        self.action1_Counter_Clockwise.triggered.connect(lambda: self.image_view.image_1_rotate('counter'))
        self.actionCut.triggered.connect(self.cut_image)
        self.actionHide.setCheckable(True)
        self.actionHide.triggered.connect(self.hide_image)

        # about menu related

        self.init_tool_bar()
        self.init_side_bar()
        # --------------------------------------------------------
        # --------------------------------------------------------
        #
        #                 windows setting up
        #
        # --------------------------------------------------------
        # --------------------------------------------------------
        # ------------------ coronal
        coronal_layout = QGridLayout(self.coronalframe)
        coronal_layout.setSpacing(0)
        coronal_layout.setContentsMargins(0, 0, 0, 0)
        coronal_layout.addWidget(self.atlas_view.cimg, 0, 0, 1, 1)
        coronal_layout.addWidget(self.atlas_view.clut, 0, 1, 1, 1)
        coronal_layout.addWidget(self.atlas_view.cpage_ctrl, 1, 0, 1, 2)

        # ------------------ sagital / image sagital
        self.sagital_layout = QGridLayout(self.sagitalframe)
        self.sagital_layout.setSpacing(0)
        self.sagital_layout.setContentsMargins(0, 0, 0, 0)
        self.sagital_layout.addWidget(self.atlas_view.simg, 0, 0, 1, 1)
        self.sagital_layout.addWidget(self.atlas_view.slut, 0, 1, 1, 1)
        self.sagital_layout.addWidget(self.atlas_view.spage_ctrl, 1, 0, 1, 2)

        # ------------------ horizontal
        horizontal_layout = QGridLayout(self.horizontalframe)
        horizontal_layout.setSpacing(0)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.addWidget(self.atlas_view.himg, 0, 0, 1, 1)
        horizontal_layout.addWidget(self.atlas_view.hlut, 0, 1, 1, 1)
        horizontal_layout.addWidget(self.atlas_view.hpage_ctrl, 1, 0, 1, 2)

        # ------------------ sagital copy / atlas sagital
        self.sagital_copy_layout = QGridLayout(self.sagitalcopyframe)
        self.sagital_copy_layout.setSpacing(0)
        self.sagital_copy_layout.setContentsMargins(0, 0, 0, 0)

        # ------------------ image
        self.image_view_layout = QGridLayout(self.histview)
        self.image_view_layout.setSpacing(0)
        self.image_view_layout.setContentsMargins(0, 0, 0, 0)
        self.image_view_layout.addWidget(self.image_view.img_stacks, 0, 0, 1, 1)

        # ------------------ slice view
        self.aslice_view_layout = QGridLayout(self.sliceframe)
        self.aslice_view_layout.setSpacing(0)
        self.aslice_view_layout.setContentsMargins(0, 0, 0, 0)
        self.aslice_view_layout.addWidget(self.atlas_view.slice_stack, 0, 0, 1, 1)

        # -------------------- 3D view
        self.view3d.opts['distance'] = 200  # distance of camera from center
        self.view3d.opts['elevation'] = 50  # camera's angle of elevation in degrees
        self.view3d.opts['azimuth'] = 45    # camera's azimuthal angle in degrees
        self.view3d.opts['fov'] = 60        # horizontal field of view in degrees
        # self.view3d.setBackgroundColor(pg.mkColor(50, 50, 50))
        self.view3d.addItem(self.atlas_view.axis)
        self.view3d.addItem(self.atlas_view.grid)
        self.view3d.addItem(self.atlas_view.mesh)
        self.view3d.addItem(self.atlas_view.ap_plate_mesh)
        self.view3d.addItem(self.atlas_view.dv_plate_mesh)
        self.view3d.addItem(self.atlas_view.ml_plate_mesh)

        # -------------------- initial window
        self.coronalframe.show()
        self.sagitalframe.hide()
        self.horizontalframe.hide()
        self.sagitalcopyframe.hide()
        self.view3d.hide()
        self.histview.hide()
        self.sliceframe.setVisible(False)

        self.sidebar.setCurrentIndex(0)
        tab1_shortcut = QShortcut(QKeySequence('Ctrl+1'), self)
        tab1_shortcut.activated.connect(lambda: self.sidebar_tab_state(0))
        tab2_shortcut = QShortcut(QKeySequence('Ctrl+2'), self)
        tab2_shortcut.activated.connect(lambda: self.sidebar_tab_state(1))
        tab3_shortcut = QShortcut(QKeySequence('Ctrl+3'), self)
        tab3_shortcut.activated.connect(lambda: self.sidebar_tab_state(2))
        tab4_shortcut = QShortcut(QKeySequence('Ctrl+4'), self)
        tab4_shortcut.activated.connect(lambda: self.sidebar_tab_state(3))
        tab5_shortcut = QShortcut(QKeySequence('Ctrl+5'), self)
        tab5_shortcut.activated.connect(lambda: self.sidebar_tab_state(4))

        undo_shortcut = QShortcut(QKeySequence('Ctrl+Z'), self)
        undo_shortcut.activated.connect(self.undo_called)
        redo_shortcut = QShortcut(QKeySequence('Ctrl+Shift+Z'), self)
        redo_shortcut.activated.connect(self.redo_called)


        self.print_message('Ready', self.normal_color, 0)

    def sidebar_tab_state(self, tab_num):
        self.sidebar.setCurrentIndex(tab_num)

    # ------------------------------------------------------------------
    #
    #               Menubar - View - Window Control
    #
    # ------------------------------------------------------------------
    def show_only_slice_window(self):
        self.num_windows = 1
        self.atlas_view.radio_group.setVisible(True)
        self.coronalframe.setVisible(False)
        self.sagitalframe.setVisible(False)
        self.horizontalframe.setVisible(False)
        self.sagitalcopyframe.setVisible(False)
        self.view3d.setVisible(False)
        self.histview.setVisible(False)
        self.sliceframe.setVisible(True)

    def show_only_coronal_window(self):
        if self.atlas_view.atlas_data is None:
            return
        if self.num_windows == 4:
            self.sagital_copy_layout.removeWidget(self.atlas_view.simg)
            self.sagital_copy_layout.removeWidget(self.atlas_view.slut)
            self.sagital_copy_layout.removeWidget(self.atlas_view.spage_ctrl)
            self.sagital_layout.addWidget(self.atlas_view.simg, 0, 0, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.slut, 0, 1, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.spage_ctrl, 1, 0, 1, 2)
        self.num_windows = 1
        self.atlas_view.radio_group.setVisible(True)
        self.coronalframe.setVisible(True)
        self.sagitalframe.setVisible(False)
        self.horizontalframe.setVisible(False)
        self.sagitalcopyframe.setVisible(False)
        self.view3d.setVisible(False)
        self.histview.setVisible(False)
        self.sliceframe.setVisible(False)

    def show_only_sagital_window(self):
        if self.atlas_view.atlas_data is None:
            return
        if self.num_windows == 4:
            self.sagital_copy_layout.removeWidget(self.atlas_view.simg)
            self.sagital_copy_layout.removeWidget(self.atlas_view.slut)
            self.sagital_copy_layout.removeWidget(self.atlas_view.spage_ctrl)
            self.sagital_layout.addWidget(self.atlas_view.simg, 0, 0, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.slut, 0, 1, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.spage_ctrl, 1, 0, 1, 2)
        self.num_windows = 1
        self.atlas_view.radio_group.setVisible(True)
        self.coronalframe.setVisible(False)
        self.sagitalframe.setVisible(True)
        self.horizontalframe.setVisible(False)
        self.sagitalcopyframe.setVisible(False)
        self.view3d.setVisible(False)
        self.histview.setVisible(False)
        self.sliceframe.setVisible(False)

    def show_only_horizontal_window(self):
        if self.atlas_view.atlas_data is None:
            return
        if self.num_windows == 4:
            self.sagital_copy_layout.removeWidget(self.atlas_view.simg)
            self.sagital_copy_layout.removeWidget(self.atlas_view.slut)
            self.sagital_copy_layout.removeWidget(self.atlas_view.spage_ctrl)
            self.sagital_layout.addWidget(self.atlas_view.simg, 0, 0, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.slut, 0, 1, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.spage_ctrl, 1, 0, 1, 2)
        self.num_windows = 1
        self.atlas_view.radio_group.setVisible(True)
        self.coronalframe.setVisible(False)
        self.sagitalframe.setVisible(False)
        self.horizontalframe.setVisible(True)
        self.sagitalcopyframe.setVisible(False)
        self.view3d.setVisible(False)
        self.histview.setVisible(False)
        self.sliceframe.setVisible(False)

    def show_only_image_window(self):
        self.atlas_view.radio_group.setVisible(True)
        self.coronalframe.setVisible(False)
        self.sagitalframe.setVisible(False)
        self.horizontalframe.setVisible(False)
        self.sagitalcopyframe.setVisible(False)
        self.view3d.setVisible(False)
        self.histview.setVisible(True)
        self.sliceframe.setVisible(False)

    def show_only_3d_window(self):
        if self.atlas_view.atlas_data is None:
            return
        if self.num_windows == 4:
            self.sagital_copy_layout.removeWidget(self.atlas_view.simg)
            self.sagital_copy_layout.removeWidget(self.atlas_view.slut)
            self.sagital_copy_layout.removeWidget(self.atlas_view.spage_ctrl)
            self.sagital_layout.addWidget(self.atlas_view.simg, 0, 0, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.slut, 0, 1, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.spage_ctrl, 1, 0, 1, 2)
        self.num_windows = 1
        self.atlas_view.radio_group.setVisible(True)
        self.coronalframe.setVisible(False)
        self.sagitalframe.setVisible(False)
        self.horizontalframe.setVisible(False)
        self.sagitalcopyframe.setVisible(False)
        self.view3d.setVisible(True)
        self.histview.setVisible(False)
        self.sliceframe.setVisible(False)

    def show_2_windows(self):
        if self.atlas_view.atlas_data is None:
            return
        if self.num_windows == 4:
            self.sagital_copy_layout.removeWidget(self.atlas_view.simg)
            self.sagital_copy_layout.removeWidget(self.atlas_view.slut)
            self.sagital_copy_layout.removeWidget(self.atlas_view.spage_ctrl)
            self.sagital_layout.addWidget(self.atlas_view.simg, 0, 0, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.slut, 0, 1, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.spage_ctrl, 1, 0, 1, 2)
        self.num_windows = 2
        self.atlas_view.radio_group.setVisible(True)
        if self.atlas_display == 'coronal':
            self.coronalframe.setVisible(True)
            self.sagitalframe.setVisible(False)
            self.horizontalframe.setVisible(False)
        elif self.atlas_display == 'sagittal':
            self.coronalframe.setVisible(False)
            self.sagitalframe.setVisible(True)
            self.horizontalframe.setVisible(False)
        else:
            self.coronalframe.setVisible(False)
            self.sagitalframe.setVisible(False)
            self.horizontalframe.setVisible(True)

        self.sagitalcopyframe.setVisible(False)
        self.view3d.setVisible(False)
        self.histview.setVisible(True)
        self.sliceframe.setVisible(False)

    def show_slice_and_histology(self):
        if self.atlas_view.slice_image_data is None:
            return
        self.coronalframe.setVisible(False)
        self.sagitalframe.setVisible(False)
        self.horizontalframe.setVisible(False)
        self.sagitalcopyframe.setVisible(False)
        self.view3d.setVisible(False)
        self.histview.setVisible(True)
        self.sliceframe.setVisible(True)

    def show_3_windows(self):
        if self.atlas_view.atlas_data is None:
            return
        if self.num_windows == 4:
            self.sagital_copy_layout.removeWidget(self.atlas_view.simg)
            self.sagital_copy_layout.removeWidget(self.atlas_view.slut)
            self.sagital_copy_layout.removeWidget(self.atlas_view.spage_ctrl)
            self.sagital_layout.addWidget(self.atlas_view.simg, 0, 0, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.slut, 0, 1, 1, 1)
            self.sagital_layout.addWidget(self.atlas_view.spage_ctrl, 1, 0, 1, 2)
        self.num_windows = 3
        self.atlas_view.radio_group.setVisible(True)
        if self.atlas_display == 'coronal':
            self.coronalframe.setVisible(True)
            self.sagitalframe.setVisible(False)
            self.horizontalframe.setVisible(False)
        elif self.atlas_display == 'sagittal':
            self.coronalframe.setVisible(False)
            self.sagitalframe.setVisible(True)
            self.horizontalframe.setVisible(False)
        else:
            self.coronalframe.setVisible(False)
            self.sagitalframe.setVisible(False)
            self.horizontalframe.setVisible(True)

        self.sagitalcopyframe.setVisible(False)
        self.view3d.setVisible(True)
        self.histview.setVisible(True)
        self.sliceframe.setVisible(False)

    def show_4_windows(self):
        if self.atlas_view.atlas_data is None:
            return
        if self.num_windows != 4:
            self.sagital_layout.removeWidget(self.atlas_view.simg)
            self.sagital_layout.removeWidget(self.atlas_view.slut)
            self.sagital_layout.removeWidget(self.atlas_view.spage_ctrl)
            self.sagital_copy_layout.addWidget(self.atlas_view.simg, 0, 0, 1, 1)
            self.sagital_copy_layout.addWidget(self.atlas_view.slut, 0, 1, 1, 1)
            self.sagital_copy_layout.addWidget(self.atlas_view.spage_ctrl, 1, 0, 1, 2)
        self.num_windows = 4
        self.atlas_view.radio_group.setVisible(False)
        self.coronalframe.setVisible(True)
        self.sagitalframe.setVisible(False)
        self.horizontalframe.setVisible(True)
        self.sagitalcopyframe.setVisible(True)
        self.view3d.setVisible(True)
        self.histview.setVisible(False)
        self.sliceframe.setVisible(False)

    def show_grids(self, vis):
        self.atlas_view.cimg.image_dict['grid_lines'].setVisible(vis)
        self.atlas_view.simg.image_dict['grid_lines'].setVisible(vis)
        self.atlas_view.himg.image_dict['grid_lines'].setVisible(vis)
        self.atlas_view.slice_stack.image_dict['grid_lines'].setVisible(vis)
        self.image_view.img_stacks.image_dict['grid_lines'].setVisible(vis)

    #
    # def clear_layout(self, layout):
    #     while layout.count() > 0:
    #         item = layout.takeAt(0)
    #         if not item:
    #             continue
    #         w = item.widget()
    #         if w:
    #             w.deleteLater()
    #

    # ------------------------------------------------------------------
    #
    #                   Sidebar - Atlas panel related
    #
    # ------------------------------------------------------------------
    def display_changed(self):
        rbtn = self.sender()
        if rbtn.isChecked():
            if rbtn.text() == "Coronal":
                self.coronalframe.setVisible(True)
                self.sagitalframe.setVisible(False)
                self.horizontalframe.setVisible(False)
                self.atlas_display = 'coronal'
            elif rbtn.text() == "Sagittal":
                self.coronalframe.setVisible(False)
                self.sagitalframe.setVisible(True)
                self.horizontalframe.setVisible(False)
                self.atlas_display = 'sagittal'
            else:
                self.coronalframe.setVisible(False)
                self.sagitalframe.setVisible(False)
                self.horizontalframe.setVisible(True)
                self.atlas_display = 'horizontal'
        if self.atlas_view.atlas_data is None or self.atlas_view.atlas_label is None:
            return
        self.atlas_view.working_cut_changed(self.atlas_display)
        self.reset_corners_atlas()
        self.working_atlas_data['atlas-mask'] = np.ones(self.atlas_view.slice_size).astype('uint8')

    def reset_corners_atlas(self):
        self.atlas_rect = (0, 0, int(self.atlas_view.slice_size[1]), int(self.atlas_view.slice_size[0]))
        self.atlas_tri_inside_data = []  # renew tri_inside data to empty
        inds = np.arange(len(self.working_atlas_text))[::-1]
        for da_ind in inds:
            self.atlas_view.working_atlas.vb.removeItem(self.working_atlas_text[da_ind])
            self.working_atlas_text[da_ind].deleteLater()
            del self.working_atlas_text[da_ind]
        self.working_atlas_text = []
        self.atlas_corner_points = self.atlas_view.corner_points.copy()
        self.atlas_side_lines = self.atlas_view.side_lines.copy()
        self.atlas_tri_onside_data = num_side_pnt_changed(self.np_onside, self.atlas_corner_points, self.atlas_side_lines)
        self.atlas_tri_data = self.atlas_tri_onside_data + self.atlas_tri_inside_data
        self.atlas_view.working_atlas.image_dict['tri_pnts'].setData(pos=np.asarray(self.atlas_tri_data))
        if self.tool_box.checkable_btn_dict['triang_btn'].isChecked():
            self.atlas_view.working_atlas.image_dict['tri_pnts'].setVisible(True)
        else:
            self.atlas_view.working_atlas.image_dict['tri_pnts'].setVisible(False)
        if self.tool_box.triang_vis_btn.isChecked():
            self.update_atlas_tri_lines()
        self.small_atlas_rect = None
        self.small_histo_rect = None

    def reset_corners_hist(self):
        self.histo_tri_inside_data = []  # renew tri_inside data to empty
        for da_item in self.working_img_text:
            self.image_view.img_stacks.vb.removeItem(da_item)
            da_item.deleteLater()
            del da_item
        self.working_img_text = []
        # if self.processing_img is not None:
        #     self.histo_rect = (0, 0, int(self.processing_img_size[1]), int(self.processing_img_size[0]))
        #     self.histo_corner_points, self.histo_side_lines = get_corner_line_from_rect(self.histo_rect)
        # else:
        print(self.image_view.img_size)
        self.histo_rect = (0, 0, int(self.image_view.img_size[1]), int(self.image_view.img_size[0]))
        self.histo_corner_points = self.image_view.corner_points.copy()
        self.histo_side_lines = self.image_view.side_lines.copy()
        self.histo_tri_onside_data = num_side_pnt_changed(self.np_onside, self.histo_corner_points, self.histo_side_lines)

        self.histo_tri_data = self.histo_tri_onside_data + self.histo_tri_inside_data
        self.image_view.img_stacks.image_dict['tri_pnts'].setData(pos=np.asarray(self.histo_tri_data))
        if self.tool_box.checkable_btn_dict['triang_btn'].isChecked():
            self.image_view.img_stacks.image_dict['tri_pnts'].setVisible(True)
        else:
            self.image_view.img_stacks.image_dict['tri_pnts'].setVisible(False)
        if self.tool_box.triang_vis_btn.isChecked():
            self.update_histo_tri_lines()
        self.small_atlas_rect = None
        self.small_histo_rect = None

        self.white_img = np.ones(self.image_view.img_size).astype('uint8')

    def vis_atlas_boundary(self):
        if self.atlas_view.atlas_data is None:
            return
        if self.atlas_view.show_boundary_btn.isChecked():
            self.atlas_view.cimg.boundary.setVisible(True)
            self.atlas_view.simg.boundary.setVisible(True)
            self.atlas_view.himg.boundary.setVisible(True)
        else:
            self.atlas_view.cimg.boundary.setVisible(False)
            self.atlas_view.simg.boundary.setVisible(False)
            self.atlas_view.himg.boundary.setVisible(False)

    # ------------------------------------------------------------------
    #
    #                  Menu Bar ---- Edit ----- related
    #
    # ------------------------------------------------------------------
    def clear_all_layers(self):
        if not self.layer_ctrl.layer_link:
            self.print_message('No layer data can be removed.', self.reminder_color, 0)
            return
        self.layer_ctrl.clear_all()
        for da_key in list(self.working_img_type.keys()):
            if self.working_img_type[da_key] == 'vector':
                self.working_img_data[da_key] = []
            else:
                self.working_img_data[da_key] = None
        for da_key in list(self.working_atlas_type.keys()):
            # if da_key == 'atlas-slice':
            #     continue
            if self.working_atlas_type[da_key] == 'vector':
                self.working_atlas_data[da_key] = []
            else:
                self.working_atlas_data[da_key] = None
        self.working_img_data['cell_count'] = [0 for i in range(5)]
        self.working_atlas_data['cell_count'] = [0 for i in range(5)]

    def shift_setting_changed(self):
        shift_setting = LayerSettingDialog('Layer Shifting Setting', 0, 100, self.layer_shift_val)
        shift_setting.exec()
        self.layer_shift_val = shift_setting.val

    def rotate_setting_changed(self):
        rotate_setting = LayerSettingDialog('Layer Rotating Setting', 0, 50, self.layer_rotate_val)
        rotate_setting.exec()
        self.layer_rotate_val = rotate_setting.val

    def get_valid_layer(self):
        if not self.layer_ctrl.current_layer_index or not self.h2a_transferred:
            self.print_message('Translation only works for layers on atlas window.', self.reminder_color, 0)
            return []
        selected_links = [self.layer_ctrl.layer_link[ind] for ind in self.layer_ctrl.current_layer_index]
        valid_links = [da_link for da_link in selected_links if 'atlas' in da_link]
        return valid_links

    def move_layers(self, da_link, moving_vec):
        if da_link in ['img-process', 'atlas-slice']:
            self.print_message('Transform only works on overlay and transferred layers.', self.reminder_color, 0)
            return
        if 'img-' in da_link:
            if self.working_img_type[da_link] == 'vector':
                temp = np.asarray(self.working_img_data[da_link]).copy()
                temp = temp + moving_vec
                self.working_img_data[da_link] = temp.tolist()
                self.image_view.img_stacks.image_dict[da_link].setData(
                    pos=np.asarray(self.working_img_data[da_link]))
            else:
                shift_mat = np.float32([[1, 0, moving_vec[0]], [0, 1, moving_vec[1]]])
                da_img = self.working_img_data[da_link].copy()
                self.working_img_data[da_link] = cv2.warpAffine(da_img, shift_mat, da_img.shape[:2])
                self.image_view.img_stacks.image_dict[da_link].setImage(self.working_img_data[da_link])
        else:
            if self.working_atlas_type[da_link] == 'vector':
                temp = np.asarray(self.working_atlas_data[da_link]).copy()
                temp = temp + moving_vec
                self.working_atlas_data[da_link] = temp.tolist()
                self.atlas_view.working_atlas.image_dict[da_link].setData(
                    pos=np.asarray(self.working_atlas_data[da_link]))
            else:
                shift_mat = np.float32([[1, 0, moving_vec[0]], [0, 1, moving_vec[1]]])
                da_img = self.working_atlas_data[da_link].copy()
                self.working_atlas_data[da_link] = cv2.warpAffine(da_img, shift_mat, da_img.shape[:2])
                self.atlas_view.working_atlas.image_dict[da_link].setImage(self.working_atlas_data[da_link])
        if da_link == 'atlas-overlay':
            print('record after transferred action for later accept.')

    def rotate_layers(self, da_link, rotate_angle):
        theta = np.radians(rotate_angle)
        rot_mat = np.array(((np.cos(theta), -np.sin(theta)), (np.sin(theta), np.cos(theta))))

        if da_link in ['img-process', 'atlas-slice']:
            self.print_message('Transform only works on overlay and transferred layers.', self.reminder_color, 0)
            return
        else:
            if 'img-' in da_link:
                img_rect = cv2.boundingRect(self.histo_tri_onside_data)
                img_center = np.array([img_rect[0] + 0.5 * img_rect[2], img_rect[1] + 0.5 * img_rect[3]]).astype(int)
                if self.working_img_type[da_link] == 'vector':
                    temp = np.asarray(self.working_img_data[da_link]).copy() - img_center
                    temp = np.dot(rot_mat, temp) + img_center
                    self.working_img_data[da_link] = temp.tolist()
                    self.image_view.img_stacks.image_dict[da_link].setData(
                        pos=np.asarray(self.working_img_data[da_link]))
                else:
                    temp = rotate(self.working_img_data[da_link], rotate_angle, img_center)
                    self.working_img_data[da_link] = temp.copy()
                    self.image_view.img_stacks.image_dict[da_link].setImage(self.working_img_data[da_link])
            else:
                atlas_rect = cv2.boundingRect(self.histo_tri_onside_data)
                atlas_center = np.array([atlas_rect[0] + 0.5 * atlas_rect[2], atlas_rect[1] + 0.5 * atlas_rect[3]])
                atlas_center = atlas_center.astype(int)
                if self.working_atlas_type[da_link] == 'vector':
                    temp = np.asarray(self.working_atlas_data[da_link]).copy() - atlas_center
                    temp = np.dot(rot_mat, temp) + atlas_center
                    self.working_atlas_data[da_link] = temp.tolist()
                    self.atlas_view.working_atlas.image_dict[da_link].setData(
                        pos=np.asarray(self.working_atlas_data[da_link]))
                else:
                    temp = rotate(self.working_atlas_data[da_link], rotate_angle, atlas_center)
                    self.working_atlas_data[da_link] = temp.copy()
                    self.atlas_view.working_atlas.image_dict[da_link].setImage(self.working_atlas_data[da_link])

    def vertical_translation_pressed(self, moving_direction):
        valid_links = self.get_valid_layer()

        if moving_direction == 'up':
            moving_vec = np.array([0, - self.layer_shift_val])
        else:
            moving_vec = np.array([0, self.layer_shift_val])

        for da_link in valid_links:
            self.move_layers(da_link, moving_vec)

        if self.a2h_transferred or self.h2a_transferred:
            self.layer_action_after_matching.append({'action': 'shift', 'val': moving_vec})

    def horizontal_translation_pressed(self, moving_direction):
        valid_links = self.get_valid_layer()

        if moving_direction == 'right':
            moving_vec = np.array([self.layer_shift_val, 0])
        else:
            moving_vec = np.array([- self.layer_shift_val, 0])

        for da_link in valid_links:
            self.move_layers(da_link, moving_vec)

        if self.a2h_transferred or self.h2a_transferred:
            self.layer_action_after_matching.append({'action': 'shift', 'val': moving_vec})

    def layer_rotation_pressed(self, rotating_direction):
        valid_links = self.get_valid_layer()

        if rotating_direction == 'clockwise':
            rotating_val = self.rotating_step_val
        else:
            rotating_val = - self.rotating_step_val

        for da_link in valid_links:
            self.rotate_layers(da_link, rotating_val)

        if self.a2h_transferred or self.h2a_transferred:
            self.layer_action_after_matching.append({'action': 'rotate', 'val': rotating_val})

    def save_current_action(self, current_tool, layer_link, data, layer_tb):
        if self.action_id != 0:
            del_index = np.arange(len(self.action_list) + self.action_id, len(self.action_list))[::-1]
            for da_ind in del_index:
                del self.action_list[da_ind]
            self.action_id = 0
        current_action = {'tool': current_tool, 'link': layer_link, 'data': data, 'layer': layer_tb}
        self.action_list.append(current_action)
        if len(self.action_list) > 6:
            del self.action_list[0]

    def redo_called(self):
        self.action_id += 1
        if self.action_id > 0:
            self.action_id -= 1
            return
        self.set_undo_redo_data()

    def undo_called(self):
        self.action_id -= 1
        if abs(self.action_id) >= len(self.action_list):
            self.action_id += 1
            return
        self.set_undo_redo_data()

    def set_undo_redo_data(self):
        current_action = self.action_list[self.action_id - 1]
        current_data = current_action['data']
        layer_link = current_action['link']
        current_tool = current_action['tool']
        da_layer = current_action['layer']
        if current_tool != 'delete':
            self.tool_box.checkable_btn_dict[current_tool].setChecked(True)
        if 'img' in layer_link:
            if layer_link == 'img-process':
                self.processing_img = current_data['data']
                self.image_view.img_stacks.set_data(self.processing_img)
            elif layer_link in ['img-mask', 'img-virus']:
                self.working_img_data[layer_link] = current_data['data']
                self.image_view.img_stacks.image_dict[layer_link].setImage(self.working_img_data[layer_link])
            elif layer_link == 'img-cells':
                self.working_img_data[layer_link] = current_data['data']
                self.working_img_data['cell_size'] = current_data['size']
                self.working_img_data['cell_symbol'] = current_data['symbol']
                self.working_img_data['cell_layer_index'] = current_data['index']
                self.working_img_data['cell_count'] = current_data['count']
                self.image_view.img_stacks.image_dict[layer_link].setData(
                    pos=np.asarray(self.working_img_data[layer_link]), symbol=self.working_img_data['cell_symbol'])
                for i in range(5):
                    self.tool_box.cell_count_val_list[i].setText(str(self.working_img_data['cell_count'][i]))
            elif layer_link == 'img-drawing':
                self.working_img_data[layer_link] = current_data['data']
                if current_data['closed']:
                    self.set_img_pencil_closed_style()
                else:
                    self.clear_img_pencil_closed_style()
                self.image_view.img_stacks.image_dict[layer_link].setData(
                    np.asarray(self.working_img_data[layer_link]))
            elif layer_link == 'img-contour':
                self.working_img_data[layer_link] = current_data['data']
                self.image_view.img_stacks.image_dict[layer_link].setData(
                    np.asarray(self.working_img_data[layer_link]))
            elif layer_link == 'img-probe':
                self.working_img_data[layer_link] = current_data['data']
                self.image_view.img_stacks.image_dict[layer_link].setData(
                    pos=np.asarray(self.working_img_data[layer_link]))
        elif 'atlas' in layer_link:
            if layer_link == 'atlas_slice':
                print('process')
            elif layer_link == 'atlas-mask':
                print('mask')
            elif layer_link == 'atlas-probe':
                print('cells')
            else:
                print('others')
        else:
            return
        da_index = np.where(np.ravel(self.layer_ctrl.layer_link) == layer_link)[0][0]
        self.layer_ctrl.layer_list[da_index].set_thumbnail_data(da_layer)

    # ------------------------------------------------------------------
    #
    #                  Menu Bar ---- Image ----- related
    #
    # ------------------------------------------------------------------
    def hide_image(self):
        if self.image_view.image_file is None:
            self.print_message('No histological image file is loaded.', self.error_message_color, 0)
            return
        if self.actionHide.isChecked():
            for i in range(self.image_view.image_file.n_channels):
                self.image_view.img_stacks.image_list[i].setVisible(False)
        else:
            for i in range(self.image_view.image_file.n_channels):
                self.image_view.img_stacks.image_list[i].setVisible(True)

    def turn_current_to_process(self):
        if self.image_view.image_file is None:
            self.print_message('No histological image file is loaded.', self.error_message_color, 0)
            return
        self.processing_img = self.image_view.current_img.copy()
        if self.image_view.image_file.pixel_type == 'rgb24':
            input_img = self.image_view.current_img.copy()
        else:
            channel_hsv = self.image_view.image_file.hsv_colors
            img_temp = merge_channels_into_single_img(self.processing_img, channel_hsv)
            input_img = cv2.normalize(img_temp, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        temp = gamma_correction(input_img, 1.45)
        res = cv2.resize(temp, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
        self.master_layers(res, layer_type='img-process', color=[])
        self.sidebar_tab_state(3)
        self.print_message('Processing image is created.', self.normal_color, 0)

    def reset_current_image(self):
        if self.image_view.image_file is None or not self.image_view.image_file.is_rgb:
            return
        if self.processing_img is None:
            return
        self.image_view.set_data_to_img_stacks()
        self.processing_img = None
        remove_index = np.where(np.ravel(self.layer_ctrl.layer_link) == 'img-process')[0][0]
        self.layer_ctrl.delete_layer(remove_index)
        self.reset_corners_hist()
        self.print_message('Processing image is deleted.', 'white', 0)
        self.action_list = []
        self.action_id = 0

    def cut_image(self):
        if self.image_view.image_file is None:
            self.print_message('Please load histological image.', self.reminder_color, 0)
            return
        if self.img_lasso_is_closure:
            cut_rect = cv2.boundingRect(np.asarray(self.working_img_data['lasso_path']).astype('int'))
            temp = self.image_view.current_img.copy()
            self.processing_img = temp[cut_rect[1]:(cut_rect[1] + cut_rect[3]), cut_rect[0]:(cut_rect[0] + cut_rect[2])]
            for i in range(self.image_view.image_file.n_channels):
                self.image_view.img_stacks.image_list[i].clear()
            self.image_view.set_data_and_size(self.processing_img)
            self.reset_corners_hist()
            if self.image_view.image_file.pixel_type == 'rgb24':
                input_img = self.processing_img.copy()
            else:
                channel_hsv = self.image_view.image_file.hsv_colors
                img_temp = merge_channels_into_single_img(self.processing_img, channel_hsv)
                input_img = cv2.normalize(img_temp, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            temp = gamma_correction(input_img, 1.45)
            res = cv2.resize(temp, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='img-process', color=[])
            self.inactive_lasso()
            self.action_list = []
            self.action_id = 0

    # ------------------------------------------------------------------
    #
    #                  Menu Bar ---- Atlas ----- related
    #
    # ------------------------------------------------------------------
    def download_waxholm_rat_atlas(self):
        download_waxholm_rat_window = AtlasDownloader()
        download_waxholm_rat_window.exec()

    def process_raw_atlas_data(self):
        process_atlas_window = AtlasProcessor()
        process_atlas_window.exec()

    def load_atlas_slice(self):
        self.print_message('Load Atlas Slice ... This process will clear the current Atlas (if any).',
                           self.normal_color, 0)
        file_title = "Select Atlas Slice File"
        file_filter = "JPEG (*.jpg);;PNG (*.png);;Pickle File (*.pkl)"
        if self.atlas_img_path is None:
            file_path = str(Path.home())
        else:
            file_path = self.atlas_img_path
        file_options = QFileDialog.Options()
        file_options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        image_file_path = file_dialog.getOpenFileName(self, file_title, file_path, file_filter, options=file_options)

        if image_file_path[0] != '':
            if self.atlas_view.slice_image_data is not None:
                self.slice_cut = 'Coronal'
                self.slice_width = 0
                self.slice_height = 0
                self.slice_distance = 0
                self.slice_bregma = []
                self.slice_info_ready = False

            if image_file_path[0][-4:] in ['.jpg', '.png']:
                img_data = cv2.imread(image_file_path[0])
                img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2RGBA)
            else:
                infile = open(image_file_path[0], 'rb')
                slice_data = pickle.load(infile)
                infile.close()
                img_data = slice_data['data'].copy()
                self.slice_cut = slice_data['cut']
                self.slice_width = slice_data['width']
                self.slice_height = slice_data['height']
                self.slice_distance = slice_data['distance']
                self.slice_bregma = slice_data['Bregma']

            self.atlas_view.set_slice_data(img_data)
            self.reset_corners_atlas()

            self.actionSwitch_Atlas.setText('Switch Atlas: Slice')
            self.current_atlas = 'slice'
            self.atlascontrolpanel.setEnabled(False)
            self.treeviewpanel.setEnabled(False)
            self.actionBregma_Picker.setEnabled(True)
            self.actionCreate_Slice_Layer.setEnabled(True)
            self.delete_all_atlas_layer()

            if self.image_view.image_file is not None:
                self.show_slice_and_histology()
            else:
                self.show_only_slice_window()

        else:
            self.print_message('', self.normal_color, 0)

    def register_slice_info(self):
        if self.atlas_view.slice_image_data is None:
            self.print_message('No Slice Data is loaded.  Please load Slice through <Atlas Menu>.',
                               self.error_message_color, 0)
            return
        slice_info = SliceSettingDialog()
        slice_info.exec()
        self.slice_cut = slice_info.cut
        self.slice_width = slice_info.width
        self.slice_height = slice_info.height
        self.slice_distance = slice_info.distance
        if self.slice_height == 0 or self.slice_width == 0 or self.slice_distance == 0 or not self.slice_bregma:
            self.slice_info_ready = False
        else:
            self.slice_info_ready = True

    def crop_slice(self):
        if self.atlas_view.slice_image_data is None:
            self.print_message('Please load Atlas Slice image.', self.reminder_color, 0)
            return
        if self.atlas_lasso_is_closure:
            cut_rect = cv2.boundingRect(np.asarray(self.working_atlas_data['lasso_path']).astype('int'))
            temp = self.atlas_view.slice_image_data.copy()
            cut_img = temp[cut_rect[1]:(cut_rect[1] + cut_rect[3]), cut_rect[0]:(cut_rect[0] + cut_rect[2])]
            self.working_atlas_data['atlas-slice'] = cut_img
            self.atlas_view.set_slice_data(self.working_atlas_data['atlas-slice'])
            self.reset_corners_atlas()
            res = cv2.resize(self.working_atlas_data['atlas-slice'][:, :, :3], self.atlas_view.slice_tb_size,
                             interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='atlas-slice', color=[])
            self.inactive_slice_window_lasso()

    def process_slice(self):
        if self.atlas_view.slice_image_data is None:
            self.print_message('Please load Atlas Slice image.', self.reminder_color, 0)
            return
        self.inactive_slice_window_lasso()
        self.working_atlas_data['atlas-slice'] = self.atlas_view.slice_image_data.copy()
        res = cv2.resize(self.working_atlas_data['atlas-slice'][:, :, :3], self.atlas_view.slice_tb_size,
                         interpolation=cv2.INTER_AREA)
        self.master_layers(res, layer_type='atlas-slice', color=[])

    def pick_bregma(self):
        if self.actionBregma_Picker.isChecked():
            self.set_all_toolbox_btns_unchecked()
            self.current_checked_tool = None
            self.show_triangle_points('triang')
            self.vis_eraser_symbol(False)

    def save_processed_slice(self):
        if self.atlas_view.slice_image_data is None:
            self.print_message('No Atlas Slice to save.', self.error_message_color, 0)
            return
        if not self.slice_info_ready:
            self.print_message('No Slice information is given.', self.error_message_color, 0)
            return
        path = QFileDialog.getSaveFileName(self, "Save Processed Slice", str(Path.home()), "Pickle File (*.pkl)")
        if path[0] != '':
            if self.working_atlas_data['atlas-slice'] is None:
                img_data = self.atlas_view.slice_image_data
            else:
                img_data = self.working_atlas_data['atlas-slice']
            data = {'data': img_data,
                    'cut': self.slice_cut,
                    'width': self.slice_width,
                    'height': self.slice_height,
                    'distance': self.slice_distance,
                    'Bregma': self.slice_bregma}
            with open(path[0], 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            self.print_message('Current Slice is saved successfully.', 'white', 0.1)

    def switch_atlas(self):
        if self.atlas_view.atlas_data is None or self.atlas_view.slice_image_data is None:
            msg = 'Atlas can be switched only after both two types of Atlas are loaded.'
            self.print_message(msg, self.error_message_color, 0)
            return
        self.delete_all_atlas_layer()

        if self.current_atlas == 'volume':
            self.actionSwitch_Atlas.setText('Switch Atlas: Slice')
            self.current_atlas = 'slice'
            self.atlascontrolpanel.setEnabled(False)
            self.treeviewpanel.setEnabled(False)
            self.atlas_view.set_slice_data(self.atlas_view.slice_image_data)
            self.reset_corners_atlas()
            self.actionBregma_Picker.setEnabled(True)
            self.actionCreate_Slice_Layer.setEnabled(True)
        else:
            self.actionSwitch_Atlas.setText('Switch Atlas: Volume')
            self.current_atlas = 'volume'
            self.atlascontrolpanel.setEnabled(True)
            self.treeviewpanel.setEnabled(True)
            self.atlas_view.working_cut_changed(self.atlas_display)
            self.reset_corners_atlas()
            self.actionBregma_Picker.setEnabled(False)
            self.actionCreate_Slice_Layer.setEnabled(False)

    def reset_atlas_slice(self):
        self.atlas_view.slice_stack.set_data(self.atlas_view.slice_image_data)
        self.working_atlas_data['atlas-slice'] = None

    # save triangle points for the atlas
    def save_triangulation_points(self):
        path = QFileDialog.getSaveFileName(self, "Save Triangulation Points Data",
                                           str(Path.home()), "Pickle File (*.pkl)")
        if path[0] != '':
            data = {'atlas_corner_points': self.atlas_corner_points,
                    'atlas_side_lines': self.atlas_side_lines,
                    'atlas_tri_data': self.atlas_tri_data,
                    'atlas_tri_inside_data': self.atlas_tri_inside_data,
                    'atlas_tri_onside_data': self.atlas_tri_onside_data,
                    'working_atlas_text': self.working_atlas_text,
                    'atlas_display': self.atlas_display}
            with open(path[0], 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # load triangulation points
    def load_triangulation_points(self):
        if self.atlas_view.atlas_data is None:
            self.print_message('Atlas need to be loaded first.', 'gray', 0)
            return
        filter = "Pickle File (*.pkl)"
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        pnt_path = dlg.getOpenFileName(self, "Load Triangulation Points", str(Path.home()), filter)
        print(pnt_path)

        if pnt_path[0] != '':
            infile = open(pnt_path[0], 'rb')
            tri_data = pickle.load(infile)
            infile.close()

            if 'atlas_corner_points' not in list(tri_data.keys()):
                self.print_message('Loaded data is not triangulation points data !!!', self.error_message_color, 0.1)
                return

            self.atlas_display = tri_data['atlas_display']
            self.atlas_corner_points = tri_data['atlas_corner_points']
            self.atlas_side_lines = tri_data['atlas_side_lines']
            self.atlas_tri_data = tri_data['atlas_tri_data']
            self.atlas_tri_inside_data = tri_data['atlas_tri_inside_data']
            self.atlas_tri_onside_data = tri_data['atlas_tri_onside_data']
            self.working_atlas_text = tri_data['working_atlas_text']

            if tri_data['atlas_display'] == 'coronal':
                self.atlas_view.section_rabnt1.setChecked(True)
            elif tri_data['atlas_display'] == 'sagittal':
                self.atlas_view.section_rabnt2.setChecked(True)
            else:
                self.atlas_view.section_rabnt3.setChecked(True)
            if self.atlas_tri_data:
                self.atlas_view.working_atlas.image_dict['tri_pnts'].setData(self.atlas_tri_data)
                for i in range(len(self.atlas_tri_data)):
                    self.atlas_view.working_atlas.vb.addItem(self.working_atlas_text[i])

    # ------------------------------------------------------------------
    #
    #                      ToolBar layout and connections
    #
    # -----------------------------------------------------------------
    def init_tool_bar(self):
        self.toolbar.setStyleSheet(toolbar_style)
        # -------------- ToolBar layout and functions -------------- #
        self.tool_box.add_atlas.triggered.connect(self.load_previous_atlas)
        self.tool_box.add_image_stack.triggered.connect(self.load_image)
        #     add_cell_act = QAction(QIcon('icons/neuron.png'), 'upload recorded cell activities', self)
        self.tool_box.vis2.triggered.connect(self.show_2_windows)
        self.tool_box.vis3.triggered.connect(self.show_3_windows)
        self.tool_box.vis4.triggered.connect(self.show_4_windows)
        self.tool_box.toh_btn.triggered.connect(self.transfer_to_hist_clicked)
        self.tool_box.toa_btn.triggered.connect(self.transfer_to_atlas_clicked)
        self.tool_box.check_btn.triggered.connect(self.transform_accept)

        self.tool_box.checkable_btn_dict['lasso_btn'].triggered.connect(self.lasso_btn_clicked)
        self.tool_box.checkable_btn_dict['magic_wand_btn'].triggered.connect(self.magic_wand_btn_clicked)
        self.tool_box.checkable_btn_dict['pencil_btn'].triggered.connect(self.pencil_btn_clicked)
        self.tool_box.checkable_btn_dict['eraser_btn'].triggered.connect(self.eraser_btn_clicked)
        self.tool_box.checkable_btn_dict['probe_btn'].triggered.connect(self.probe_btn_clicked)
        self.tool_box.checkable_btn_dict['triang_btn'].triggered.connect(self.triang_btn_clicked)
        self.tool_box.checkable_btn_dict['loc_btn'].triggered.connect(self.loc_btn_clicked)
        self.tool_box.checkable_btn_dict['ruler_btn'].triggered.connect(self.ruler_btn_clicked)
        # magic_wand related
        self.tool_box.magic_color_btn.sigColorChanged.connect(self.change_magic_wand_color)
        self.tool_box.magic_wand_virus_register.clicked.connect(self.get_virus_img)
        self.tool_box.magic_wand_bnd_register.clicked.connect(self.get_contour_img)
        self.tool_box.magic_wand_kernel.currentTextChanged.connect(self.kernel_changed)
        self.tool_box.magic_wand_ksize.valueChanged.connect(self.kernel_changed)
        # triangle related
        self.tool_box.triang_color_btn.sigColorChanged.connect(self.change_triangle_color)
        self.tool_box.bound_pnts_num.textEdited.connect(self.number_of_side_points_changed)
        self.tool_box.triang_vis_btn.clicked.connect(self.vis_tri_lines_btn_clicked)
        self.tool_box.triang_match_bnd.clicked.connect(self.matching_tri_bnd)
        # cell related
        self.tool_box.cell_color_btn.sigColorChanged.connect(self.change_cell_color)
        self.tool_box.cell_radar_btn.clicked.connect(self.cell_detect_btn_clicked)
        self.tool_box.cell_selector_btn.clicked.connect(self.cell_select_btn_clicked)
        self.tool_box.cell_aim_btn.clicked.connect(self.cell_aim_btn_clicked)
        # pencil related
        self.tool_box.pencil_color_btn.sigColorChanged.connect(self.change_pencil_color)
        self.tool_box.pencil_size_valt.textChanged.connect(self.change_pencil_size)
        # ruler related
        self.tool_box.ruler_color_btn.sigColorChanged.connect(self.change_ruler_color)
        self.tool_box.ruler_size_valt.textChanged.connect(self.change_ruler_size)
        # probe_related
        self.tool_box.probe_color_btn.sigColorChanged.connect(self.probe_color_changed)
        self.tool_box.probe_type1.toggled.connect(lambda: self.probe_type_changed(0))
        self.tool_box.probe_type2.toggled.connect(lambda: self.probe_type_changed(1))
        self.tool_box.probe_type3.toggled.connect(lambda: self.probe_type_changed(2))
        # eraser_related
        self.tool_box.eraser_color_btn.sigColorChanged.connect(self.change_eraser_color)
        # lasso related
        self.tool_box.lasso_color_btn.sigColorChanged.connect(self.lasso_color_changed)

        self.toolbar.addAction(self.tool_box.add_atlas)
        self.toolbar.addAction(self.tool_box.add_image_stack)
        #     self.toolBar.addAction(add_cell_act)
        self.toolbar.addAction(self.tool_box.vis2)
        self.toolbar.addAction(self.tool_box.vis3)
        self.toolbar.addAction(self.tool_box.vis4)
        self.toolbar.addSeparator()
        for da_key in self.tool_box.toolbox_btn_keys:
            self.toolbar.addAction(self.tool_box.checkable_btn_dict[da_key])
        # self.toolbar.addAction(self.tool_box.boundary_btn)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.tool_box.toa_btn)
        self.toolbar.addAction(self.tool_box.check_btn)
        self.toolbar.addAction(self.tool_box.toh_btn)
        self.toolbar.addWidget(self.tool_box.sep_label)

        magic_wand_action = self.toolbar.addWidget(self.tool_box.magic_wand_wrap)
        pencil_action = self.toolbar.addWidget(self.tool_box.pencil_wrap)
        eraser_action = self.toolbar.addWidget(self.tool_box.eraser_wrap)
        lasso_action = self.toolbar.addWidget(self.tool_box.lasso_wrap)
        probe_action = self.toolbar.addWidget(self.tool_box.probe_wrap)
        triang_action = self.toolbar.addWidget(self.tool_box.triang_wrap)
        loc_action = self.toolbar.addWidget(self.tool_box.cell_count_wrap)
        ruler_action = self.toolbar.addWidget(self.tool_box.ruler_wrap)

        self.toolbar_wrap_action_dict['pencil_act'] = pencil_action
        self.toolbar_wrap_action_dict['eraser_act'] = eraser_action
        self.toolbar_wrap_action_dict['lasso_act'] = lasso_action
        self.toolbar_wrap_action_dict['magic_wand_act'] = magic_wand_action
        self.toolbar_wrap_action_dict['probe_act'] = probe_action
        self.toolbar_wrap_action_dict['triang_act'] = triang_action
        self.toolbar_wrap_action_dict['loc_act'] = loc_action
        self.toolbar_wrap_action_dict['ruler_act'] = ruler_action

        toolbar_wrap_action_keys = list(self.toolbar_wrap_action_dict.keys())
        for da_key in toolbar_wrap_action_keys:
            self.toolbar_wrap_action_dict[da_key].setVisible(False)

        self.np_onside = int(self.tool_box.bound_pnts_num.text())

    # ------------------------------------------------------------------
    #              ToolBar checkable btn clicked
    # ------------------------------------------------------------------
    def ruler_btn_clicked(self):
        self.inactive_lasso()
        self.inactive_slice_window_lasso()
        self.set_toolbox_btns_unchecked('ruler')
        self.show_triangle_points('triang')
        self.vis_eraser_symbol(False)

    def lasso_btn_clicked(self):
        self.set_toolbox_btns_unchecked('lasso')
        self.show_triangle_points('triang')
        self.vis_eraser_symbol(False)

    def magic_wand_btn_clicked(self):
        self.inactive_lasso()
        self.inactive_slice_window_lasso()
        self.set_toolbox_btns_unchecked('magic_wand')
        self.show_triangle_points('triang')
        self.vis_eraser_symbol(False)

    def pencil_btn_clicked(self):
        self.inactive_lasso()
        self.inactive_slice_window_lasso()
        self.set_toolbox_btns_unchecked('pencil')
        self.show_triangle_points('triang')
        self.vis_eraser_symbol(False)

    def eraser_btn_clicked(self):
        self.inactive_lasso()
        self.inactive_slice_window_lasso()
        self.set_toolbox_btns_unchecked('eraser')
        if self.tool_box.checkable_btn_dict['eraser_btn'].isChecked():
            self.vis_eraser_symbol(True)
        else:
            self.vis_eraser_symbol(False)

    def rotation_btn_clicked(self):
        self.inactive_lasso()
        self.inactive_slice_window_lasso()
        self.set_toolbox_btns_unchecked('rotation')
        self.show_triangle_points('triang')
        self.vis_eraser_symbol(False)

    def triang_btn_clicked(self):
        self.inactive_lasso()
        self.inactive_slice_window_lasso()
        self.set_toolbox_btns_unchecked('triang')
        self.show_triangle_points('triang')
        self.vis_eraser_symbol(False)

    def probe_btn_clicked(self):
        self.inactive_lasso()
        self.inactive_slice_window_lasso()
        self.set_toolbox_btns_unchecked('probe')
        self.show_triangle_points('triang')
        self.vis_eraser_symbol(False)

    def loc_btn_clicked(self):
        self.inactive_lasso()
        self.inactive_slice_window_lasso()
        self.set_toolbox_btns_unchecked('loc')
        self.show_triangle_points('triang')
        self.vis_eraser_symbol(False)

    def set_all_toolbox_btns_unchecked(self):
        for da_key in self.tool_box.toolbox_btn_keys:
            self.tool_box.checkable_btn_dict[da_key].setChecked(False)
        for da_key in list(self.toolbar_wrap_action_dict.keys()):
            self.toolbar_wrap_action_dict[da_key].setVisible(False)

    def set_toolbox_btns_unchecked(self, current_btn):
        self.actionBregma_Picker.setChecked(False)
        btn_checked = self.tool_box.checkable_btn_dict['{}_btn'.format(current_btn)].isChecked()
        if btn_checked:
            self.current_checked_tool = current_btn
            for da_key in self.tool_box.toolbox_btn_keys:
                if current_btn in da_key:
                    continue
                else:
                    self.tool_box.checkable_btn_dict[da_key].setChecked(False)
            for da_key in list(self.toolbar_wrap_action_dict.keys()):
                if current_btn in da_key:
                    self.toolbar_wrap_action_dict[da_key].setVisible(True)
                else:
                    self.toolbar_wrap_action_dict[da_key].setVisible(False)
        else:
            self.current_checked_tool = None
            self.toolbar_wrap_action_dict['{}_act'.format(current_btn)].setVisible(False)

    def vis_eraser_symbol(self, vis):
        self.image_view.img_stacks.image_dict['circle_follow'].setVisible(vis)
        self.atlas_view.slice_stack.image_dict['circle_follow'].setVisible(vis)

    # ------------------------------------------------------------------
    #
    #                      SideBar layout and connections
    #
    # ------------------------------------------------------------------
    def init_side_bar(self):
        self.sidebar.setStyleSheet(self.styles.tab_style)
        self.sidebar.setIconSize(QSize(24, 24))
        self.sidebar.setTabIcon(0, QIcon('icons/sidebar/atlascontrol.svg'))
        self.sidebar.setTabIcon(1, QIcon('icons/sidebar/treeview.svg'))
        self.sidebar.setTabIcon(2, QIcon('icons/sidebar/tool.svg'))
        self.sidebar.setTabIcon(3, QIcon('icons/sidebar/layers.svg'))
        self.sidebar.setTabIcon(4, QIcon('icons/sidebar/object.svg'))

        # ---------------------------- atlas control panel
        atlas_panel_layout = QVBoxLayout(self.atlascontrolpanel)
        atlas_panel_layout.setContentsMargins(0, 0, 0, 0)
        atlas_panel_layout.setAlignment(Qt.AlignTop)
        atlas_control_label = QLabel('Atlasing Controller')
        atlas_control_label.setStyleSheet(self.styles.sidebar_title_label_style)

        atlas_panel_layout.addWidget(atlas_control_label)
        atlas_panel_layout.addWidget(self.atlas_view.sidebar_wrap)

        # ---------------------------- Label Panel
        label_panel_layout = QVBoxLayout(self.treeviewpanel)
        label_panel_layout.setContentsMargins(0, 0, 0, 0)
        label_panel_layout.setAlignment(Qt.AlignTop)
        label_control_label = QLabel('Segmentation View Controller')
        label_control_label.setStyleSheet(self.styles.sidebar_title_label_style)

        label_tree_container = QFrame()
        label_container_layout = QVBoxLayout(label_tree_container)
        # label_container_layout.setContentsMargins(0, 0, 0, 0)
        label_container_layout.setSpacing(0)
        label_container_layout.setAlignment(Qt.AlignTop)
        show_3d_button = QPushButton()
        show_3d_button.setStyleSheet(sidebar_button_style)
        show_3d_button.setCheckable(True)
        show_3d_button.setText('Show in 3D view')
        show_3d_button.clicked.connect(self.show_small_area_in_3d)

        composition_label = QLabel('Composition: ')
        self.composition_combo = QComboBox()
        self.composition_combo.setFixedHeight(22)
        self.composition_combo.addItems(['opaque', 'translucent', 'additive'])
        self.composition_combo.currentIndexChanged.connect(self.composition_3d_changed)

        label_container_layout.addWidget(show_3d_button)
        label_container_layout.addSpacing(10)
        label_container_layout.addWidget(self.composition_combo)
        label_container_layout.addSpacing(10)
        label_container_layout.addWidget(self.atlas_view.label_tree)

        label_panel_layout.addWidget(label_control_label)
        label_panel_layout.addWidget(label_tree_container)

        # ---------------------------- image panel
        image_panel_layout = QVBoxLayout(self.imagecontrolpanel)
        image_panel_layout.setContentsMargins(0, 0, 0, 0)
        image_panel_layout.setSpacing(0)
        image_panel_layout.setAlignment(Qt.AlignTop)
        image_control_label = QLabel('Image View Controller')
        image_control_label.setStyleSheet(self.styles.sidebar_title_label_style)

        image_panel_layout.addWidget(image_control_label)

        space_item = QSpacerItem(300, 10, QSizePolicy.Expanding)

        image_container = QFrame()
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setSpacing(5)
        image_container_layout.setAlignment(Qt.AlignTop)
        image_container_layout.addWidget(self.image_view.outer_frame)
        # image_container_layout.addSpacerItem(space_item)
        # image_container_layout.addWidget(self.image_view.chn_widget_wrap)

        image_panel_layout.addWidget(image_container)
        image_panel_layout.insertStretch(-1, 1)

        # ---------------------------- layer panel
        layer_panel_layout = QVBoxLayout(self.layerpanel)
        layer_panel_layout.setContentsMargins(0, 0, 0, 0)
        layer_panel_layout.setSpacing(0)
        layer_panel_layout.setAlignment(Qt.AlignTop)
        layer_control_label = QLabel('Layer View Controller')
        layer_control_label.setStyleSheet(self.styles.sidebar_title_label_style)

        layer_btm_ctrl = QFrame()
        layer_btm_ctrl.setStyleSheet('background-color:rgb(65, 65, 65);')
        layer_btm_ctrl.setFixedHeight(24)
        layer_btm_layout = QHBoxLayout(layer_btm_ctrl)
        layer_btm_layout.setContentsMargins(0, 0, 0, 0)
        layer_btm_layout.setSpacing(5)
        layer_btm_layout.setAlignment(Qt.AlignRight)
        layer_btm_layout.addWidget(self.layer_ctrl.add_layer_btn)
        layer_btm_layout.addWidget(self.layer_ctrl.delete_layer_btn)

        layer_panel_layout.addWidget(layer_control_label)
        layer_panel_layout.addWidget(self.layer_ctrl)
        # layer_panel_layout.addWidget(layer_btm_ctrl)
        # self.layerpanel.setEnabled(False)

        # ---------------------------- object panel
        object_panel_layout = QVBoxLayout(self.probecontrolpanel)
        object_panel_layout.setContentsMargins(0, 0, 0, 0)
        object_panel_layout.setSpacing(0)
        object_panel_layout.setAlignment(Qt.AlignTop)
        object_control_label = QLabel('Object View Controller')
        object_control_label.setStyleSheet(self.styles.sidebar_title_label_style)

        object_btm_ctrl = QFrame()
        object_btm_ctrl.setStyleSheet('background-color:rgb(65, 65, 65);')
        object_btm_ctrl.setFixedHeight(24)
        object_btm_layout = QHBoxLayout(object_btm_ctrl)
        object_btm_layout.setContentsMargins(0, 0, 0, 0)
        object_btm_layout.setSpacing(5)
        object_btm_layout.setAlignment(Qt.AlignRight)

        object_btm_layout.addWidget(self.object_ctrl.merge_probe_btn)
        object_btm_layout.addWidget(self.object_ctrl.merge_virus_btn)
        object_btm_layout.addWidget(self.object_ctrl.merge_cell_btn)
        object_btm_layout.addWidget(self.object_ctrl.merge_drawing_btn)
        object_btm_layout.addWidget(self.object_ctrl.merge_contour_btn)
        object_btm_layout.addWidget(self.object_ctrl.add_object_btn)
        object_btm_layout.addWidget(self.object_ctrl.delete_object_btn)

        object_panel_layout.addWidget(object_control_label)
        object_panel_layout.addWidget(self.object_ctrl.outer_frame)
        object_panel_layout.addWidget(object_btm_ctrl)

    # ------------------------------------------------------------------
    #
    #               ToolBar ruler btn related
    #
    # ------------------------------------------------------------------
    def change_ruler_color(self, ev):
        color = np.ravel(ev.color().getRgb())
        width = self.tool_box.ruler_width_slider.value()
        self.image_view.img_stacks.image_dict['ruler_path'].setPen(pg.mkPen(color, width=width, style=Qt.DashLine))
        self.atlas_view.cimg.image_dict['ruler_path'].setPen(pg.mkPen(color, width=width, style=Qt.DashLine))
        self.atlas_view.himg.image_dict['ruler_path'].setPen(pg.mkPen(color, width=width, style=Qt.DashLine))
        self.atlas_view.simg.image_dict['ruler_path'].setPen(pg.mkPen(color, width=width, style=Qt.DashLine))
        self.atlas_view.slice_stack.image_dict['ruler_path'].setPen(pg.mkPen(color, width=width, style=Qt.DashLine))
        self.image_view.img_stacks.image_dict['ruler_path'].setSymbolPen(color=color)
        self.atlas_view.cimg.image_dict['ruler_path'].setSymbolPen(color=color)
        self.atlas_view.himg.image_dict['ruler_path'].setSymbolPen(color=color)
        self.atlas_view.simg.image_dict['ruler_path'].setSymbolPen(color=color)
        self.atlas_view.slice_stack.image_dict['ruler_path'].setSymbolPen(color=color)
        self.image_view.img_stacks.image_dict['ruler_path'].setSymbolBrush(color=color)
        self.atlas_view.cimg.image_dict['ruler_path'].setSymbolBrush(color=color)
        self.atlas_view.himg.image_dict['ruler_path'].setSymbolBrush(color=color)
        self.atlas_view.simg.image_dict['ruler_path'].setSymbolBrush(color=color)
        self.atlas_view.slice_stack.image_dict['ruler_path'].setSymbolBrush(color=color)

    def change_ruler_size(self):
        width = int(self.tool_box.ruler_size_valt.text())
        self.tool_box.ruler_width_slider.setValue(width)
        color = np.ravel(self.tool_box.ruler_color_btn.color().getRgb())
        self.image_view.img_stacks.image_dict['ruler_path'].setPen(pg.mkPen(color, width=width, style=Qt.DashLine))
        self.atlas_view.cimg.image_dict['ruler_path'].setPen(pg.mkPen(color, width=width, style=Qt.DashLine))
        self.atlas_view.himg.image_dict['ruler_path'].setPen(pg.mkPen(color, width=width, style=Qt.DashLine))
        self.atlas_view.simg.image_dict['ruler_path'].setPen(pg.mkPen(color, width=width, style=Qt.DashLine))
        self.atlas_view.slice_stack.image_dict['ruler_path'].setPen(pg.mkPen(color, width=width, style=Qt.DashLine))
        self.image_view.img_stacks.image_dict['ruler_path'].setSymbolSize(width)
        self.atlas_view.cimg.image_dict['ruler_path'].setSymbolSize(width)
        self.atlas_view.himg.image_dict['ruler_path'].setSymbolSize(width)
        self.atlas_view.simg.image_dict['ruler_path'].setSymbolSize(width)
        self.atlas_view.slice_stack.image_dict['ruler_path'].setSymbolSize(width)

    def inactive_atlas_ruler(self):
        self.atlas_view.working_atlas.image_dict['ruler_path'].clear()
        self.atlas_view.working_atlas.image_dict['ruler_path'].updateItems()
        self.working_atlas_data['ruler_path'] = []

    def atlas_ruler_points_clicked(self, points, ev):
        clicked_ind = ev[0].index()
        pos = ev[0].pos()
        if clicked_ind != 0 and len(self.working_atlas_data['ruler_path']) == 1:
            self.working_atlas_data['ruler_path'].append([pos.x(), pos.y()])
            self.atlas_view.working_atlas.image_dict['ruler_path'].setData(
                np.asarray(self.working_atlas_data['ruler_path']))
            self.set_ruler_length()
        else:
            self.inactive_atlas_ruler()

    def set_ruler_length(self):
        if len(self.working_atlas_data['ruler_path']) == 2:
            data = np.asarray(self.working_atlas_data['ruler_path'])
            if self.current_atlas == 'volume':
                dist = np.sqrt(np.sum((data[0] - data[1]) ** 2))
                self.tool_box.ruler_length_label.setText('Length: {} um'.format(
                    round(dist * self.atlas_view.vox_size_um, 2)))
            else:
                if not self.slice_info_ready:
                    dist = np.sqrt(np.sum((data[0] - data[1]) ** 2))
                    self.tool_box.ruler_length_label.setText('Length: {} px'.format(int(dist)))
                else:
                    xv, yv, zv = get_slice_atlas_coord(data,
                                                       self.slice_cut, self.atlas_view.slice_image_data.shape[:2],
                                                       self.slice_width, self.slice_height, self.slice_distance,
                                                       self.slice_bregma)
                    dist = np.sqrt((xv[0] - xv[1]) ** 2 + (yv[0] - yv[1]) ** 2 + (zv[0] - zv[1]) ** 2)
                    self.tool_box.ruler_length_label.setText('Length: {} um'.format(round(dist, 2)))

    def inactive_img_ruler(self):
        self.image_view.img_stacks.image_dict['ruler_path'].clear()
        self.image_view.img_stacks.image_dict['ruler_path'].updateItems()
        self.working_img_data['ruler_path'] = []

    def img_ruler_points_clicked(self, points, ev):
        clicked_ind = ev[0].index()
        pos = ev[0].pos()
        if clicked_ind != 0 and len(self.working_img_data['ruler_path']) == 1:
            self.working_img_data['ruler_path'].append([pos.x(), pos.y()])
            self.image_view.img_stacks.image_dict['ruler_path'].setData(
                np.asarray(self.working_img_data['ruler_path']))
            self.set_img_ruler_length()
        else:
            self.inactive_img_ruler()

    def set_img_ruler_length(self):
        if len(self.working_img_data['ruler_path']) == 2:
            data = np.asarray(self.working_img_data['ruler_path'])
            dist = np.sqrt(np.sum((data[0] - data[1]) ** 2))
            if self.image_view.image_file.scaling_val is None:
                self.tool_box.ruler_length_label.setText('Length: {} px'.format(int(dist)))
            else:
                self.tool_box.ruler_length_label.setText('Length: {} um'.format(
                    round(dist * self.image_view.image_file.scaling_val / self.image_view.current_scale, 2)))

    # ------------------------------------------------------------------
    #
    #               ToolBar lasso btn related
    #
    # ------------------------------------------------------------------
    def lasso_color_changed(self, ev):
        lasso_color = np.ravel(ev.color().getRgb())
        self.lasso_color = (int(lasso_color[0]), int(lasso_color[1]), int(lasso_color[2]))
        if self.img_lasso_is_closure:
            self.image_view.img_stacks.image_dict['lasso_path'].setPen(
                pg.mkPen(color=self.lasso_color, width=3, style=Qt.SolidLine))
        else:
            self.image_view.img_stacks.image_dict['lasso_path'].setPen(
                pg.mkPen(color=self.lasso_color, width=3, style=Qt.DashLine))
        self.image_view.img_stacks.image_dict['lasso_path'].setSymbolPen(color=self.lasso_color)
        if self.atlas_lasso_is_closure:
            self.atlas_view.slice_stack.image_dict['lasso_path'].setPen(
                pg.mkPen(color=self.lasso_color, width=3, style=Qt.SolidLine))
        else:
            self.atlas_view.slice_stack.image_dict['lasso_path'].setPen(
                pg.mkPen(color=self.lasso_color, width=3, style=Qt.DashLine))
        self.atlas_view.working_atlas.image_dict['lasso_path'].setSymbolPen(color=self.lasso_color)

    def inactive_lasso(self):
        self.working_img_data['lasso_path'] = []
        self.image_view.img_stacks.image_dict['lasso_path'].clear()
        self.image_view.img_stacks.image_dict['lasso_path'].updateItems()
        self.image_view.img_stacks.image_dict['lasso_path'].setPen(
            pg.mkPen(color=self.lasso_color, width=3, style=Qt.DashLine))
        self.img_lasso_is_closure = False

    def lasso_points_clicked(self, points, ev):
        clicked_ind = ev[0].index()
        if clicked_ind == 0 and len(self.working_img_data['lasso_path']) >= 3:
            self.working_img_data['lasso_path'].append(self.working_img_data['lasso_path'][0])
            self.image_view.img_stacks.image_dict['lasso_path'].setData(np.asarray(self.working_img_data['lasso_path']))
            self.img_lasso_is_closure = True
            self.image_view.img_stacks.image_dict['lasso_path'].setPen(
                pg.mkPen(color=self.lasso_color, width=3, style=Qt.SolidLine))
        else:
            self.inactive_lasso()

    def inactive_slice_window_lasso(self):
        self.working_atlas_data['lasso_path'] = []
        self.atlas_view.slice_stack.image_dict['lasso_path'].clear()
        self.atlas_view.slice_stack.image_dict['lasso_path'].updateItems()
        self.atlas_view.slice_stack.image_dict['lasso_path'].setPen(
            pg.mkPen(color=self.lasso_color, width=3, style=Qt.DashLine))
        self.atlas_lasso_is_closure = False

    def slice_window_lasso_points_clicked(self, points, ev):
        clicked_ind = ev[0].index()
        if clicked_ind == 0 and len(self.working_atlas_data['lasso_path']) >= 3:
            self.working_atlas_data['lasso_path'].append(self.working_atlas_data['lasso_path'][0])
            self.atlas_view.slice_stack.image_dict['lasso_path'].setData(
                np.asarray(self.working_atlas_data['lasso_path']))
            self.atlas_lasso_is_closure = True
            self.atlas_view.slice_stack.image_dict['lasso_path'].setPen(
                pg.mkPen(color=self.lasso_color, width=3, style=Qt.SolidLine))
        else:
            self.inactive_slice_window_lasso()

    # ------------------------------------------------------------------
    #
    #               ToolBar probe btn related
    #
    # ------------------------------------------------------------------
    def probe_type_changed(self, type):
        self.probe_type = type
        if type == 0:
            self.tip_length = 175
            self.channel_size = 20
            self.channel_number_in_banks = (384, 384, 192)
        elif type == 1:
            self.tip_length = 175
            self.channel_size = 15
            self.channel_number_in_banks = (384, 384, 192)
        else:
            self.tip_length = 0
            self.channel_size = None
            self.channel_number_in_banks = None

    def probe_color_changed(self, ev):
        probe_color = np.ravel(ev.color().getRgb())
        self.probe_color = (int(probe_color[0]), int(probe_color[1]), int(probe_color[2]))
        self.image_view.img_stacks.image_dict['img-probe'].setPen(pen=self.probe_color)
        self.atlas_view.cimg.image_dict['atlas-probe'].setPen(pen=self.probe_color)
        self.atlas_view.himg.image_dict['atlas-probe'].setPen(pen=self.probe_color)
        self.atlas_view.simg.image_dict['atlas-probe'].setPen(pen=self.probe_color)
        self.atlas_view.slice_stack.image_dict['atlas-probe'].setPen(pen=self.probe_color)
        self.image_view.img_stacks.image_dict['img-probe'].setBrush(pen=self.probe_color)
        self.atlas_view.cimg.image_dict['atlas-probe'].setBrush(pen=self.probe_color)
        self.atlas_view.himg.image_dict['atlas-probe'].setBrush(pen=self.probe_color)
        self.atlas_view.simg.image_dict['atlas-probe'].setBrush(pen=self.probe_color)
        self.atlas_view.slice_stack.image_dict['atlas-probe'].setBrush(pen=self.probe_color)

    # ------------------------------------------------------------------
    #
    #               ToolBar moving btn related
    #
    # ------------------------------------------------------------------
    # def moving_left_btn_clicked(self):
    #     if not self.layer_ctrl.current_layer_id:
    #         return
    #     self.moving_layers(-self.tool_box.moving_px, 0)
    #
    # def moving_right_btn_clicked(self):
    #     if not self.layer_ctrl.current_layer_id:
    #         return
    #     self.moving_layers(self.tool_box.moving_px, 0)
    #
    # def moving_up_btn_clicked(self):
    #     if not self.layer_ctrl.current_layer_id:
    #         return
    #     self.moving_layers(0, -self.tool_box.moving_px)
    #
    # def moving_down_btn_clicked(self):
    #     if not self.layer_ctrl.current_layer_id:
    #         return
    #     self.moving_layers(0, self.tool_box.moving_px)

    # ------------------------------------------------------------------
    #
    #               ToolBar pencil btn related
    #
    # ------------------------------------------------------------------
    def change_pencil_color(self, ev):
        pencil_color = ev.color()
        self.pencil_color = np.ravel(pencil_color.getRgb())
        self.image_view.img_stacks.image_dict['img-drawing'].setPen(
            pg.mkPen(color=self.pencil_color, width=self.pencil_size))
        self.atlas_view.cimg.image_dict['atlas-drawing'].setPen(
            pg.mkPen(color=self.pencil_color, width=self.pencil_size))
        self.atlas_view.simg.image_dict['atlas-drawing'].setPen(
            pg.mkPen(color=self.pencil_color, width=self.pencil_size))
        self.atlas_view.himg.image_dict['atlas-drawing'].setPen(
            pg.mkPen(color=self.pencil_color, width=self.pencil_size))
        self.atlas_view.slice_stack.image_dict['atlas-drawing'].setPen(
            pg.mkPen(color=self.pencil_color, width=self.pencil_size))
        if self.working_img_data['img-drawing'] and self.tool_box.is_closed:
            self.image_view.img_stacks.image_dict['img-drawing'].setFillBrush(color=self.pencil_color)
        if self.working_atlas_data['atlas-drawing'] and self.tool_box.is_closed:
            self.atlas_view.working_atlas.image_dict['img-drawing'].setFillBrush(color=self.pencil_color)

    def set_img_pencil_closed_style(self):
        if not self.working_img_data['img-drawing']:
            return
        mid_line = np.mean(np.asarray(self.working_img_data['img-drawing'])[:, 1])
        self.image_view.img_stacks.image_dict['img-drawing'].setFillLevel(level=mid_line)
        self.image_view.img_stacks.image_dict['img-drawing'].setFillBrush(color=self.pencil_color)

    def clear_img_pencil_closed_style(self):
        self.image_view.img_stacks.image_dict['img-drawing'].setFillLevel(None)
        self.image_view.img_stacks.image_dict['img-drawing'].setFillBrush(None)

    def set_atlas_pencil_closed_style(self):
        if not self.working_atlas_data['atlas-drawing']:
            return
        mid_line = np.mean(np.asarray(self.working_atlas_data['atlas-drawing'])[:, 1])
        self.atlas_view.working_atlas.image_dict['atlas-drawing'].setFillLevel(level=mid_line)
        self.atlas_view.working_atlas.image_dict['atlas-drawing'].setFillBrush(color=self.pencil_color)

    def clear_atlas_pencil_closed_style(self):
        self.atlas_view.working_atlas.image_dict['atlas-drawing'].setFillLevel(None)
        self.atlas_view.working_atlas.image_dict['atlas-drawing'].setFillBrush(None)

    def change_pencil_size(self):
        val = int(self.tool_box.pencil_size_valt.text())
        self.pencil_size = val
        self.tool_box.pencil_size_slider.setValue(val)
        self.image_view.img_stacks.image_dict['img-drawing'].setPen(
            pg.mkPen(color=self.pencil_color, width=self.pencil_size))
        self.atlas_view.cimg.image_dict['atlas-drawing'].setPen(
            pg.mkPen(color=self.pencil_color, width=self.pencil_size))
        self.atlas_view.simg.image_dict['atlas-drawing'].setPen(
            pg.mkPen(color=self.pencil_color, width=self.pencil_size))
        self.atlas_view.himg.image_dict['atlas-drawing'].setPen(
            pg.mkPen(color=self.pencil_color, width=self.pencil_size))

    def inactive_drawing(self):
        self.working_img_data['img-drawing'] = []
        self.image_view.img_stacks.image_dict['img-drawing'].clear()
        self.image_view.img_stacks.image_dict['img-drawing'].updateItems()
        self.drawing_img = np.zeros((self.image_view.img_size[0], self.image_view.img_size[1], 3))

    def img_drawing_pnts_clicked(self, points, ev):  # check mark
        clicked_ind = ev[0].index()
        pos = ev[0].pos()
        if self.tool_box.checkable_btn_dict['eraser_btn'].isChecked():
            del self.working_img_data['img-drawing'][clicked_ind]
            if not self.working_img_data['img-drawing']:
                self.inactive_drawing()
        else:
            if clicked_ind == 0:
                print('first point clicked')
                self.inactive_drawing()
            elif clicked_ind == len(self.working_img_data['img-drawing']) - 1:
                print('last point clicked')
                self.is_pencil_allowed = False
                self.working_img_data['img-drawing'].append([pos.x(), pos.y()])
                if self.tool_box.is_closed:
                    self.working_img_data['img-drawing'].append([self.working_img_data['img-drawing'][0][0],
                                                                 self.working_img_data['img-drawing'][0][1]])
                self.image_view.img_stacks.image_dict['img-drawing'].setData(
                    np.asarray(self.working_img_data['img-drawing']))
                da_img = create_vis_img(self.image_view.img_size, self.working_img_data['img-drawing'],
                                        self.pencil_color, 'l', self.tool_box.is_closed)
                res = cv2.resize(da_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                self.master_layers(res, layer_type='img-drawing', color=self.pencil_color)
                current_data = {'data': self.working_img_data['img-drawing'].copy(),
                                'closed': self.tool_box.is_closed}
                self.save_current_action('pencil_btn', 'img-drawing', current_data, res)
            else:
                print('other point clicked')
                if not self.is_pencil_allowed:
                    self.inactive_drawing()

    # ------------------------------------------------------------------
    #
    #               ToolBar eraser btn related
    #
    # ------------------------------------------------------------------
    def change_eraser_color(self, ev):
        eraser_color = ev.color()
        self.image_view.img_stacks.image_dict['circle_follow'].setPen(pg.mkPen(color=eraser_color))
        self.atlas_view.working_atlas.image_dict['circle_follow'].setPen(pg.mkPen(color=eraser_color))

    # ------------------------------------------------------------------
    #
    #               ToolBar loc btn related
    #
    # ------------------------------------------------------------------
    def change_cell_color(self, ev):
        cell_color = np.ravel(ev.color().getRgb())
        self.cell_color = (int(cell_color[0]), int(cell_color[1]), int(cell_color[2]))
        self.image_view.img_stacks.image_dict['img-cells'].setPen(color=self.cell_color)
        self.image_view.img_stacks.image_dict['img-cells'].setBrush(color=self.cell_color)
        self.atlas_view.cimg.image_dict['atlas-cells'].setPen(color=self.cell_color)
        self.atlas_view.himg.image_dict['atlas-cells'].setPen(color=self.cell_color)
        self.atlas_view.simg.image_dict['atlas-cells'].setPen(color=self.cell_color)
        self.atlas_view.cimg.image_dict['atlas-cells'].setBrush(color=self.cell_color)
        self.atlas_view.himg.image_dict['atlas-cells'].setBrush(color=self.cell_color)
        self.atlas_view.simg.image_dict['atlas-cells'].setBrush(color=self.cell_color)

    def cell_select_btn_clicked(self):
        if self.tool_box.cell_aim_btn.isChecked():
            self.tool_box.cell_aim_btn.setChecked(False)

    def cell_aim_btn_clicked(self):
        if self.tool_box.cell_selector_btn.isChecked():
            self.tool_box.cell_selector_btn.setChecked(False)

    def cell_detect_btn_clicked(self):   # ??????????
        if not self.working_img_data['img-blob']:
            return

        locs = np.asarray(self.working_img_data['img-blob']).astype(int)
        da_width = np.max(locs[:, 0]) - np.min(locs[:, 0]) + 1
        da_height = np.max(locs[:, 1]) - np.min(locs[:, 1]) + 1
        small_img = np.zeros((da_height, da_width), 'uint8')
        small_locs = locs - np.array([np.min(locs[:, 0]), np.min(locs[:, 1])])
        small_img[small_locs[:, 1], small_locs[:, 0]] = 1
        ct, ht = cv2.findContours(small_img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        cnt = ct[0]
        da_moment = cv2.moments(cnt)
        center_x = int(da_moment["m10"] / da_moment["m00"])
        center_y = int(da_moment["m01"] / da_moment["m00"])
        da_area = cv2.contourArea(cnt)
        da_perimeter = cv2.arcLength(cnt, True)

        da_circularity = 4 * np.pi * da_area / (da_perimeter ** 2)

        params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        params.filterByArea = True
        params.minArea = da_area - 1
        params.maxArea = da_area + 1
        params.filterByCircularity = True
        params.minCircularity = da_circularity
        params.filterByConvexity = True
        params.minConvexity = 0.87
        params.filterByInertia = True
        params.minInertiaRatio = 0.01

        temp = self.image_view.current_img.copy()
        if self.image_view.image_file.is_rgb:
            if self.image_view.current_mode == 'rgb':
                temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
                layer_ind = 0
        else:
            da_layer = [ind for ind in range(4) if self.image_view.channel_visible[ind]]
            n_layers = len(da_layer)
            if n_layers == 0:
                return
            if n_layers > 1:
                return
            temp = temp[:, :, da_layer[0]]
            layer_ind = da_layer[0] + 1

        da_colors = temp[locs[:, 1], locs[:, 0]]
        params.minThreshold = np.min(da_colors)
        params.maxThreshold = np.max(da_colors)

        if int(opencv_ver[0]) < 3:
            detector = cv2.SimpleBlobDetector(params)
        else:
            detector = cv2.SimpleBlobDetector_create(params)

        keypoints = detector.detect(temp)
        n_keypoints = len(keypoints)
        if n_keypoints == 0:
            return

        for i in range(n_keypoints):
            x = keypoints[i].pt[0]
            y = keypoints[i].pt[1]
            size = keypoints[i].size
            self.working_img_data['img-cells'].append([x, y])
            self.working_img_data['cell_layer_index'].append(layer_ind)
            self.working_img_data['cell_symbol'].append(self.cell_base_symbol[layer_ind])
            self.working_img_data['cell_size'].append(size)
        self.working_img_data['cell_count'][layer_ind] = self.working_img_data['cell_count'][layer_ind] + n_keypoints
        self.tool_box.cell_count_val_list[layer_ind].setText(str(self.working_img_data['cell_count'][layer_ind]))

        self.image_view.img_stacks.image_dict['img-cells'].setData(
            pos=np.asarray(self.working_img_data['img-cells']), symbol=self.working_img_data['cell_symbol'])

        self.working_img_data['img-blob'] = []
        self.image_view.img_stacks.image_dict['img-blob'].clear()

    # ------------------------------------------------------------------
    #
    #               ToolBar magic wand btn related
    #
    # ------------------------------------------------------------------
    def change_magic_wand_color(self, ev):
        if self.image_view.image_file is None:
            return
        self.magic_wand_lut[1] = np.ravel(ev.color().getRgb())
        self.image_view.img_stacks.image_dict['img-mask'].setLookupTable(self.magic_wand_lut)
        self.atlas_view.cimg.image_dict['atlas-mask'].setLookupTable(self.magic_wand_lut)
        self.atlas_view.himg.image_dict['atlas-mask'].setLookupTable(self.magic_wand_lut)
        self.atlas_view.simg.image_dict['atlas-mask'].setLookupTable(self.magic_wand_lut)
        self.atlas_view.slice_stack.image_dict['atlas-mask'].setLookupTable(self.magic_wand_lut)
        self.image_view.img_stacks.image_dict['img-mask'].updateImage()
        self.atlas_view.cimg.image_dict['atlas-mask'].updateImage()
        self.atlas_view.himg.image_dict['atlas-mask'].updateImage()
        self.atlas_view.simg.image_dict['atlas-mask'].updateImage()
        self.atlas_view.slice_stack.image_dict['atlas-mask'].updateImage()

    def get_virus_img(self):
        if 'img-mask' not in self.layer_ctrl.layer_link:
            self.print_message('Need Mask Data to transfer to Virus Data.', self.reminder_color, 0)
            return
        self.virus_lut = self.magic_wand_lut.copy()
        self.atlas_view.working_atlas.image_dict['atlas-virus'].setPen(color=self.virus_lut[1])
        self.atlas_view.working_atlas.image_dict['atlas-virus'].setBrush(color=self.virus_lut[1])
        self.image_view.img_stacks.image_dict['img-virus'].setLookupTable(self.virus_lut)
        self.working_img_data['img-virus'] = self.working_img_data['img-mask'].copy()
        self.image_view.img_stacks.image_dict['img-virus'].setImage(self.working_img_data['img-virus'])
        temp = color_vis_img(self.working_img_data['img-virus'], self.virus_lut[1])
        res = cv2.resize(temp, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
        self.master_layers(res, layer_type='img-virus', color=self.virus_lut[1])
        self.remove_single_link_related('img-mask')

    def get_contour_img(self):
        if 'img-mask' not in self.layer_ctrl.layer_link:
            self.print_message('Need Mask Data to transfer to Contour Data.', self.reminder_color, 0)
            return
        self.contour_color = self.magic_wand_lut[1].copy()
        self.image_view.img_stacks.image_dict['img-contour'].setPen(color=self.contour_color)
        self.image_view.img_stacks.image_dict['img-contour'].setBrush(color=self.contour_color)
        self.atlas_view.working_atlas.image_dict['atlas-contour'].setPen(color=self.contour_color)
        self.atlas_view.working_atlas.image_dict['atlas-contour'].setBrush(color=self.contour_color)
        temp = self.working_img_data['img-mask'].astype('uint8')
        contour_length = 0
        contour_points = None
        ct, hc = cv2.findContours(image=temp, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        for j in range(len(ct)):
            da_contour = ct[j].copy()
            da_shp = da_contour.shape
            da_contour = np.reshape(da_contour, (da_shp[0], da_shp[2]))
            if len(da_contour) > contour_length:
                contour_points = da_contour
                contour_length = len(da_contour)
        if contour_points is None:
            self.print_message('No contour can be created.', self.error_message_color, 0)
            return
        self.working_img_data['img-contour'] = contour_points.tolist()
        self.image_view.img_stacks.image_dict['img-contour'].setData(contour_points)
        # make showing img
        contour_img = create_vis_img(self.image_view.img_size, contour_points, self.contour_color, 'l')
        res = cv2.resize(contour_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
        self.master_layers(res, layer_type='img-contour', color=self.contour_color)
        self.remove_single_link_related('img-mask')

    def kernel_changed(self):
        ksize = self.tool_box.magic_wand_ksize.value()
        kernel_shape = self.tool_box.magic_wand_kernel.currentText()
        if ksize != 0 and kernel_shape != "Kernel":
            if kernel_shape == "Rectangular":
                self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
            elif kernel_shape == "Elliptical":
                self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
            else:
                self.kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (ksize, ksize))
        else:
            self.kernel = None

    # ------------------------------------------------------------------
    #
    #               ToolBar triangle btn related
    #
    # ------------------------------------------------------------------
    def show_triangle_points(self, current_btn):
        if self.tool_box.checkable_btn_dict['{}_btn'.format(current_btn)].isChecked():
            if self.atlas_tri_data:
                if not self.atlas_view.working_atlas.image_dict['tri_pnts'].isVisible():
                    self.atlas_view.working_atlas.image_dict['tri_pnts'].setVisible(True)
                if self.atlas_tri_inside_data and not self.working_atlas_text[0].isVisible():
                    for i in range(len(self.working_atlas_text)):
                        self.working_atlas_text[i].setVisible(True)
            if self.histo_tri_data:
                if not self.image_view.img_stacks.image_dict['tri_pnts'].isVisible():
                    self.image_view.img_stacks.image_dict['tri_pnts'].setVisible(True)
                if self.histo_tri_inside_data and not self.working_img_text[0].isVisible():
                    for i in range(len(self.working_img_text)):
                        self.working_img_text[i].setVisible(True)
        else:
            if self.atlas_tri_data:
                if self.atlas_view.working_atlas.image_dict['tri_pnts'].isVisible():
                    self.atlas_view.working_atlas.image_dict['tri_pnts'].setVisible(False)
                if self.atlas_tri_inside_data and self.working_atlas_text[0].isVisible():
                    for i in range(len(self.working_atlas_text)):
                        self.working_atlas_text[i].setVisible(False)
            if self.histo_tri_data:
                if self.image_view.img_stacks.image_dict['tri_pnts'].isVisible():
                    self.image_view.img_stacks.image_dict['tri_pnts'].setVisible(False)
                if self.histo_tri_inside_data and self.working_img_text[0].isVisible():
                    for i in range(len(self.working_img_text)):
                        self.working_img_text[i].setVisible(False)

    def number_of_side_points_changed(self):
        self.np_onside = int(self.tool_box.bound_pnts_num.text())
        if self.atlas_view.atlas_data is not None:
            self.atlas_tri_onside_data = num_side_pnt_changed(self.np_onside, self.atlas_corner_points,
                                                              self.atlas_side_lines)
            self.atlas_tri_data = self.atlas_tri_onside_data + self.atlas_tri_inside_data
            self.atlas_view.working_atlas.image_dict['tri_pnts'].setData(pos=np.asarray(self.atlas_tri_data))
            if self.tool_box.triang_vis_btn.isChecked():
                self.update_atlas_tri_lines()
        if self.image_view.image_file is not None:
            self.histo_tri_onside_data = num_side_pnt_changed(self.np_onside, self.histo_corner_points,
                                                              self.histo_side_lines)
            self.histo_tri_data = self.histo_tri_onside_data + self.histo_tri_inside_data
            self.image_view.img_stacks.image_dict['tri_pnts'].setData(pos=np.asarray(self.histo_tri_data))
            if self.tool_box.triang_vis_btn.isChecked():
                self.update_histo_tri_lines()

    def remove_histo_tri_lines(self):
        if self.image_view.img_stacks.tri_lines_list:
            for da_item in self.image_view.img_stacks.tri_lines_list:
                self.image_view.img_stacks.vb.removeItem(da_item)
            self.image_view.img_stacks.tri_lines_list = []

    def update_histo_tri_lines(self):
        self.remove_histo_tri_lines()
        histo_tri_lines = get_tri_lines(self.histo_rect, self.histo_tri_data)
        for el in histo_tri_lines:
            pt1 = [el[0], el[1]]
            pt2 = [el[2], el[3]]
            self.image_view.img_stacks.tri_lines_list.append(pg.PlotDataItem(pen=self.tool_box.tri_line_style))
            self.image_view.img_stacks.tri_lines_list[-1].setData(np.asarray([pt1, pt2]))
            self.image_view.img_stacks.vb.addItem(self.image_view.img_stacks.tri_lines_list[-1])

    def remove_atlas_tri_lines(self):
        if self.atlas_view.working_atlas.tri_lines_list:
            for da_item in self.atlas_view.working_atlas.tri_lines_list:
                self.atlas_view.working_atlas.vb.removeItem(da_item)
            self.atlas_view.working_atlas.tri_lines_list = []

    def update_atlas_tri_lines(self):
        self.remove_atlas_tri_lines()
        point_data = self.atlas_view.working_atlas.image_dict['tri_pnts'].data['pos'].copy()
        point_data = list(point_data)
        atlas_tri_lines = get_tri_lines(self.atlas_rect, point_data)
        for el in atlas_tri_lines:
            pt1 = [el[0], el[1]]
            pt2 = [el[2], el[3]]
            self.atlas_view.working_atlas.tri_lines_list.append(pg.PlotDataItem(pen=self.tool_box.tri_line_style))
            self.atlas_view.working_atlas.tri_lines_list[-1].setData(np.asarray([pt1, pt2]))
            self.atlas_view.working_atlas.vb.addItem(self.atlas_view.working_atlas.tri_lines_list[-1])

    def vis_tri_lines_btn_clicked(self):
        if self.tool_box.triang_vis_btn.isChecked():
            if self.atlas_tri_data:
                self.update_atlas_tri_lines()
            if self.histo_tri_data:
                self.update_histo_tri_lines()
        else:
            if self.atlas_tri_data:
                self.remove_atlas_tri_lines()
            if self.histo_tri_data:
                self.remove_histo_tri_lines()

    def matching_tri_bnd(self):
        if self.image_view.image_file is None:
            self.print_message('No histological image is loaded.', self.error_message_color, 0)
            return
        if self.atlas_view.atlas_data is None and self.atlas_view.slice_image_data is None:
            self.print_message('No Atlas is loaded.', self.error_message_color, 0)
            return
        if not self.histo_tri_inside_data:
            self.print_message('No in-image triangulation points are selected.', self.error_message_color, 0)
            return
        if self.current_atlas == 'slice':
            if not self.slice_boundary_points and not self.atlas_tri_inside_data:
                self.print_message('No in-slice triangulation points are selected.', self.error_message_color, 0)
                return
        print('matching bnd')
        slice_size = self.atlas_view.slice_size
        image_size = self.image_view.img_size

        histo_pnts = np.asarray(self.histo_tri_inside_data)
        rect_img = cv2.boundingRect(histo_pnts.astype(np.float32))

        if not self.atlas_tri_inside_data:
            label_img = self.atlas_view.working_atlas.label_img.image.copy()
            none_zero_label = np.where(label_img != 0)
            if len(none_zero_label) == 0:
                return
            atlas_pnts = np.vstack([none_zero_label[1], none_zero_label[0]]).T
        else:
            atlas_pnts = np.asarray(self.atlas_tri_inside_data)
        rect_atlas = cv2.boundingRect(atlas_pnts.astype(np.float32))

        self.small_atlas_rect = rect_atlas
        self.small_histo_rect = rect_img

        self.atlas_corner_points, self.atlas_side_lines, self.histo_corner_points, self.histo_side_lines = \
            match_sides_points(rect_atlas, slice_size, rect_img, image_size)

        self.atlas_tri_onside_data = num_side_pnt_changed(self.np_onside, self.atlas_corner_points, self.atlas_side_lines)
        self.atlas_tri_data = self.atlas_tri_onside_data + self.atlas_tri_inside_data
        self.atlas_view.working_atlas.image_dict['tri_pnts'].setData(pos=np.asarray(self.atlas_tri_data))

        self.histo_tri_onside_data = num_side_pnt_changed(self.np_onside, self.histo_corner_points, self.histo_side_lines)
        self.histo_tri_data = self.histo_tri_onside_data + self.histo_tri_inside_data
        self.image_view.img_stacks.image_dict['tri_pnts'].setData(pos=np.asarray(self.histo_tri_data))
        if self.tool_box.triang_vis_btn.isChecked():
            self.update_histo_tri_lines()
            self.update_atlas_tri_lines()

    # change color for triangle points and text
    def change_triangle_color(self, ev):
        self.triangle_color = ev.color()
        # triang_color = np.ravel(triang_color.getRgb())
        self.image_view.img_stacks.image_dict['tri_pnts'].scatter.setPen(color=self.triangle_color)
        self.image_view.img_stacks.image_dict['tri_pnts'].scatter.setBrush(color=self.triangle_color)
        if self.working_img_text:
            for i in range(len(self.working_img_text)):
                self.working_img_text[i].setColor(self.triangle_color)
        self.atlas_view.cimg.image_dict['tri_pnts'].scatter.setPen(color=self.triangle_color)
        self.atlas_view.simg.image_dict['tri_pnts'].scatter.setPen(color=self.triangle_color)
        self.atlas_view.himg.image_dict['tri_pnts'].scatter.setPen(color=self.triangle_color)
        self.atlas_view.cimg.image_dict['tri_pnts'].scatter.setBrush(color=self.triangle_color)
        self.atlas_view.simg.image_dict['tri_pnts'].scatter.setBrush(color=self.triangle_color)
        self.atlas_view.himg.image_dict['tri_pnts'].scatter.setBrush(color=self.triangle_color)
        if self.working_atlas_text:
            for i in range(len(self.working_atlas_text)):
                self.working_atlas_text[i].setColor(self.triangle_color)

    # ------------------------------------------------------------------
    #
    #               ToolBar transform btn clicked
    #
    # ------------------------------------------------------------------
    def transfer_to_hist_clicked(self):
        if self.image_view.image_file is None:
            self.print_message('No histological image data is loaded.', self.error_message_color, 0)
            return
        if self.atlas_view.atlas_data is None and self.atlas_view.slice_image_data is None:
            self.print_message('No Atlas data is loaded.', self.error_message_color, 0)
            return
        self.print_message('Transfer atlas brain region segmentation to histological window.', 'white', 0)
        if not self.a2h_transferred:
            if self.current_atlas == 'volume':
                label_img = self.atlas_view.working_atlas.label_img.image.copy()
                lut = self.atlas_view.label_tree.current_lut.copy()
                self.overlay_img = make_label_rgb_img(label_img, lut)
            else:
                self.overlay_img = self.atlas_view.slice_stack.img_layer.image.copy()

            input_img = self.overlay_img.copy()

            img_wrap = np.zeros((self.image_view.img_size[0], self.image_view.img_size[1], 3), np.float32)

            if self.histo_tri_inside_data and self.atlas_tri_inside_data:
                a_temp = len(self.histo_tri_data)
                b_temp = len(self.atlas_tri_data)
                if a_temp != b_temp:
                    self.print_message('Number of points in two windows are not matching.', self.error_message_color, 0)
                    return

                subdiv = cv2.Subdiv2D(self.histo_rect)
                for p in self.histo_tri_data:
                    subdiv.insert(p)

                tri_vet_inds = get_vertex_ind_in_triangle(subdiv)
                for i in range(len(tri_vet_inds)):
                    da_inds = tri_vet_inds[i]
                    t1 = [self.atlas_tri_data[da_inds[0]], self.atlas_tri_data[da_inds[1]], self.atlas_tri_data[da_inds[2]]]
                    t2 = [self.histo_tri_data[da_inds[0]], self.histo_tri_data[da_inds[1]], self.histo_tri_data[da_inds[2]]]
                    t1 = np.reshape(t1, (3, 2))
                    t2 = np.reshape(t2, (3, 2))
                    warp_triangle(input_img, img_wrap, t1, t2, True)
                self.project_method = 'match to hist'
                self.register_method = 2
            else:
                if self.small_atlas_rect is not None:
                    atlas_rect = self.small_atlas_rect
                    histo_rect = self.small_histo_rect
                    self.project_method = 'match to hist'
                    self.register_method = 2
                else:
                    atlas_rect = self.atlas_rect
                    histo_rect = self.histo_rect
                    self.project_method = 'match to atlas'
                    self.register_method = 1
                src_xrange = (atlas_rect[0], atlas_rect[0] + atlas_rect[2])
                src_yrange = (atlas_rect[1], atlas_rect[1] + atlas_rect[3])
                src_img = input_img[src_yrange[0]:src_yrange[1], src_xrange[0]:src_xrange[1], :].copy()

                da_dim = (histo_rect[2], histo_rect[3])
                resized_des = cv2.resize(src_img, da_dim, interpolation=cv2.INTER_LINEAR)

                des_xrange = (histo_rect[0], histo_rect[0] + histo_rect[2])
                des_yrange = (histo_rect[1], histo_rect[1] + histo_rect[3])
                img_wrap[des_yrange[0]:des_yrange[1], des_xrange[0]:des_xrange[1]] = resized_des

            self.working_img_data['img-overlay'] = img_wrap
            self.image_view.img_stacks.image_dict['img-overlay'].setImage(img_wrap)
            res = cv2.resize(img_wrap, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='img-overlay', color=[])
            self.a2h_transferred = True
            self.tool_box.toh_btn.setIcon(self.tool_box.toh_btn_on_icon)
            self.tool_box.toa_btn.setEnabled(False)
            self.print_message('Transfer finished.', 'white', 0)
        else:
            self.overlay_img = None
            self.remove_single_link_related('img-overlay')
            self.a2h_transferred = False
            self.tool_box.toa_btn.setEnabled(True)
            self.tool_box.toh_btn.setIcon(self.tool_box.toh_btn_off_icon)
            self.project_method = 'pre plan'
            self.register_method = 0
            self.print_message('Transfer deleted.', 'white', 0)

    #
    def transfer_to_atlas_clicked(self):
        if self.image_view.image_file is None:
            self.print_message('No histological image data is loaded.', self.error_message_color, 0)
            return
        if self.atlas_view.atlas_data is None and self.atlas_view.slice_image_data is None:
            self.print_message('No Atlas data is loaded.', self.error_message_color, 0)
            return
        self.print_message('Transfer histological image to atlas window.', 'white', 0)
        if not self.h2a_transferred:
            if self.processing_img is not None:
                input_img = self.processing_img.copy()
            else:
                input_img = self.image_view.current_img.copy()

            if self.image_view.image_file.pixel_type == 'rgb24':
                self.overlay_img = input_img.copy()
            else:
                czi_img = input_img.copy()
                channel_hsv = self.image_view.image_file.hsv_colors
                img_temp = merge_channels_into_single_img(czi_img, channel_hsv)
                self.overlay_img = cv2.normalize(img_temp, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

            working_img = self.overlay_img.copy()

            img_wrap = np.zeros((self.atlas_view.slice_size[0], self.atlas_view.slice_size[1], 3), np.float32)

            if self.histo_tri_inside_data and self.atlas_tri_inside_data:
                a_temp = len(self.histo_tri_data)
                b_temp = len(self.atlas_tri_data)
                if a_temp != b_temp:
                    self.print_message('Number of points in two windows are not matching.', self.error_message_color, 0)
                    return
                subdiv = cv2.Subdiv2D(self.atlas_rect)
                for p in self.atlas_tri_data:
                    subdiv.insert(p)

                tri_vet_inds = get_vertex_ind_in_triangle(subdiv)

                for i in range(len(tri_vet_inds)):
                    da_inds = tri_vet_inds[i]
                    t2 = [self.atlas_tri_data[da_inds[0]], self.atlas_tri_data[da_inds[1]],
                          self.atlas_tri_data[da_inds[2]]]
                    t1 = [self.histo_tri_data[da_inds[0]], self.histo_tri_data[da_inds[1]],
                          self.histo_tri_data[da_inds[2]]]
                    t1 = np.reshape(t1, (3, 2))
                    t2 = np.reshape(t2, (3, 2))
                    warp_triangle(working_img, img_wrap, t1, t2, True)
            else:
                if self.small_atlas_rect is not None:
                    atlas_rect = self.small_atlas_rect
                    histo_rect = self.small_histo_rect
                else:
                    atlas_rect = self.atlas_rect
                    histo_rect = self.histo_rect
                src_xrange = (histo_rect[0], histo_rect[0] + histo_rect[2])
                src_yrange = (histo_rect[1], histo_rect[1] + histo_rect[3])
                src_img = working_img[src_yrange[0]:src_yrange[1], src_xrange[0]:src_xrange[1], :].copy()

                da_dim = (atlas_rect[2], atlas_rect[3])
                resized_des = cv2.resize(src_img, da_dim, interpolation=cv2.INTER_LINEAR)

                des_xrange = (atlas_rect[0], atlas_rect[0] + atlas_rect[2])
                des_yrange = (atlas_rect[1], atlas_rect[1] + atlas_rect[3])
                img_wrap[des_yrange[0]:des_yrange[1], des_xrange[0]:des_xrange[1]] = resized_des

            self.working_atlas_data['atlas-overlay'] = img_wrap.astype('uint8')
            self.atlas_view.working_atlas.image_dict['atlas-overlay'].setImage(img_wrap)
            res = cv2.resize(img_wrap, self.atlas_view.slice_tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='atlas-overlay', color=[])
            self.h2a_transferred = True
            self.tool_box.toa_btn.setIcon(self.tool_box.toa_btn_on_icon)
            self.project_method = 'match to atlas'
            self.register_method = 0
            self.tool_box.toh_btn.setEnabled(False)
            self.print_message('Transfer finished.', 'white', 0)
        else:
            self.overlay_img = None
            self.remove_single_link_related('atlas-overlay')
            self.h2a_transferred = False
            self.tool_box.toa_btn.setIcon(self.tool_box.toa_btn_off_icon)
            self.project_method = 'pre plan'
            self.register_method = 0
            self.tool_box.toh_btn.setEnabled(True)
            self.atlas_tri_data = self.atlas_view.working_atlas.image_dict['tri_pnts'].data['pos'].tolist()
            self.print_message('Transfer deleted.', self.normal_color, 0)

    # ---------------------------
    #          Accept
    # ---------------------------
    def transfer_pnt(self, pnt, tri_vet_inds):
        res_pnts = np.zeros((len(pnt), 2))
        res_pnts[:] = np.nan
        loc = get_pnts_triangle_ind(tri_vet_inds, self.histo_tri_data, self.image_view.img_size, pnt)
        loc = np.ravel(loc)
        if np.any(np.isnan(loc)):
            self.print_message('Some of the selected points are out of triangles, the points are deleted.',
                               self.reminder_color, 0)
        for i in range(len(tri_vet_inds)):
            da_inds = tri_vet_inds[i]
            t2 = [self.atlas_tri_data[da_inds[0]], self.atlas_tri_data[da_inds[1]],
                  self.atlas_tri_data[da_inds[2]]]
            t1 = [self.histo_tri_data[da_inds[0]], self.histo_tri_data[da_inds[1]],
                  self.histo_tri_data[da_inds[2]]]
            t1 = np.reshape(t1, (3, 2))
            t2 = np.reshape(t2, (3, 2))
            inds = np.where(loc == i)
            if len(inds) > 0:
                pnts_inside = pnt[inds[0]]
                res = warp_points(pnts_inside, t1, t2)
                res_pnts[inds[0]] = res
        res_pnts = res_pnts[~np.isnan(res_pnts[:, 0])]
        return res_pnts

    def transfer_vox_to_pnt(self, img_data, tri_vet_inds):
        temp_pnts = np.where(img_data != 0)
        data = np.stack([temp_pnts[1], temp_pnts[0]], axis=1) + 0.5
        res_pnts = self.transfer_pnt(data, tri_vet_inds)
        return res_pnts

    def transform_accept(self):
        if not self.h2a_transferred:
            self.print_message('Please transfer image to atlas first', self.error_message_color, 0)
            return
        self.print_message('Transform accepted, start transferring...', self.normal_color, 0)
        self.sidebar_tab_state(3)
        subdiv = cv2.Subdiv2D(self.atlas_rect)
        self.atlas_tri_data = list(self.atlas_view.working_atlas.image_dict['tri_pnts'].data['pos'].astype(int))
        for p in self.atlas_tri_data:
            subdiv.insert((int(p[0]), int(p[1])))

        tri_vet_inds = get_vertex_ind_in_triangle(subdiv)

        if self.working_img_data['img-contour']:
            self.print_message('Transferring contour...', self.normal_color, 0)
            res_pnts = self.transfer_pnt(np.asarray(self.working_img_data['img-contour']), tri_vet_inds)
            self.working_atlas_data['atlas-contour'] = res_pnts.tolist()
            self.atlas_view.working_atlas.image_dict['atlas-contour'].setData(
                np.asarray(self.working_atlas_data['atlas-contour']))
            vis_img = create_vis_img(self.atlas_view.slice_size, res_pnts, self.contour_color, vis_type='l')
            res = cv2.resize(vis_img, self.atlas_view.slice_tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='atlas-contour', color=self.contour_color)
            self.remove_single_link_related('img-contour')
            self.print_message('Contour transferred.', self.normal_color, 0)

        if self.working_img_data['img-probe']:
            res_pnts = self.transfer_pnt(np.asarray(self.working_img_data['img-probe']), tri_vet_inds)
            self.working_atlas_data['atlas-probe'] = res_pnts.tolist()
            self.atlas_view.working_atlas.image_dict['atlas-probe'].setData(
                pos=np.asarray(self.working_atlas_data['atlas-probe']))
            vis_img = create_vis_img(self.atlas_view.slice_size, res_pnts, self.probe_color, vis_type='p')
            res = cv2.resize(vis_img, self.atlas_view.slice_tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='atlas-probe', color=self.probe_color)
            self.remove_single_link_related('img-probe')
            self.print_message('Probe transferred.', self.normal_color, 0)

        if self.working_img_data['img-drawing']:
            res_pnts = self.transfer_pnt(np.asarray(self.working_img_data['img-drawing']), tri_vet_inds)
            self.working_atlas_data['atlas-drawing'] = res_pnts.tolist()
            if self.tool_box.is_closed:
                self.set_atlas_pencil_closed_style()
            else:
                self.clear_atlas_pencil_closed_style()
            self.atlas_view.working_atlas.image_dict['atlas-drawing'].setData(
                np.asarray(self.working_atlas_data['atlas-drawing']))
            vis_img = create_vis_img(self.atlas_view.slice_size, res_pnts, self.pencil_color, 'l',
                                     self.tool_box.is_closed)
            res = cv2.resize(vis_img, self.atlas_view.slice_tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='atlas-drawing', color=self.pencil_color)
            self.remove_single_link_related('img-drawing')
            self.print_message('Drawing transferred.', self.normal_color, 0)

        if self.working_img_data['img-cells']:
            res_pnts = self.transfer_pnt(np.asarray(self.working_img_data['img-cells']), tri_vet_inds)
            self.working_atlas_data['atlas-cells'] = res_pnts.tolist()
            self.atlas_view.working_atlas.image_dict['atlas-cells'].setData(
                pos=np.asarray(self.working_atlas_data['atlas-cells']), symbol=self.working_img_data['cell_symbol'])
            vis_img = create_vis_img(self.atlas_view.slice_size, res_pnts, self.cell_color, vis_type='p')
            res = cv2.resize(vis_img, self.atlas_view.slice_tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='atlas-cells', color=self.cell_color)
            self.remove_single_link_related('img-cells')
            self.print_message('Cells transferred.', self.normal_color, 0)

        if self.working_img_data['img-virus'] is not None:
            input_virus_img = self.working_img_data['img-virus'].copy()
            img_wrap = np.zeros((self.atlas_view.slice_size[0], self.atlas_view.slice_size[1]), np.float32)

            for i in range(len(tri_vet_inds)):
                da_inds = tri_vet_inds[i]
                t2 = [self.atlas_tri_data[da_inds[0]], self.atlas_tri_data[da_inds[1]],
                      self.atlas_tri_data[da_inds[2]]]
                t1 = [self.histo_tri_data[da_inds[0]], self.histo_tri_data[da_inds[1]],
                      self.histo_tri_data[da_inds[2]]]
                t1 = np.reshape(t1, (3, 2))
                t2 = np.reshape(t2, (3, 2))
                warp_triangle(input_virus_img, img_wrap, t1, t2, False)

            temp_pnts = np.where(img_wrap != 0)
            res_pnts = np.stack([temp_pnts[1], temp_pnts[0]], axis=1) + 0.5

            self.working_atlas_data['atlas-virus'] = res_pnts.tolist()
            self.atlas_view.working_atlas.image_dict['atlas-virus'].setData(
                pos=np.asarray(self.working_atlas_data['atlas-virus']))
            vis_img = create_vis_img(self.atlas_view.slice_size, res_pnts, self.virus_lut[1], 'p')
            res = cv2.resize(vis_img, self.atlas_view.slice_tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='atlas-virus', color=self.virus_lut[1])
            self.remove_single_link_related('img-virus')
            self.print_message('Virus transferred.', self.normal_color, 0)

        self.print_message('All objects transferred.', self.normal_color, 0)

    # ------------------------------------------------------------------
    #
    #              Image window - Image Processing
    #
    # ------------------------------------------------------------------
    def update_histo_tri_onside_data(self):
        print('image_changed')
        self.white_img = np.ones(self.image_view.img_size).astype('uint8')
        if self.processing_img is not None:
            self.processing_img = None
        self.reset_corners_hist()
        self.drawing_img = np.zeros((self.image_view.img_size[0], self.image_view.img_size[1], 3))
        self.cell_img = np.zeros((self.image_view.img_size[0], self.image_view.img_size[1], 3))
        self.probe_img = np.zeros((self.image_view.img_size[0], self.image_view.img_size[1], 3))
        self.clear_all_layers()
        self.action_list = []
        self.action_id = 0

    def img_stacks_clicked(self, pos):
        x = pos[0]
        y = pos[1]
        if self.image_view.image_file is None:
            return
        # ------------------------- pencil
        if self.tool_box.checkable_btn_dict['pencil_btn'].isChecked():
            if not self.working_img_data['img-drawing']:
                self.is_pencil_allowed = True
                self.working_img_data['img-drawing'].append([x, y])
                self.image_view.img_stacks.image_dict['img-drawing'].setData(
                    np.asarray(self.working_img_data['img-drawing']))
                da_img = create_vis_img(self.image_view.img_size, self.working_img_data['img-drawing'],
                                        self.pencil_color, 'p', False)
                self.drawing_img = da_img
                res = cv2.resize(self.drawing_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                self.master_layers(res, layer_type='img-drawing', color=self.pencil_color)
                # save action
                current_data = {'data': self.working_img_data['img-drawing'].copy(),
                                'closed': self.tool_box.is_closed}
                self.save_current_action('pencil_btn', 'img-drawing', current_data, res)
            else:
                if self.is_pencil_allowed:
                    print('not click on ')
                    self.working_img_data['img-drawing'].append([x, y])
                    if self.tool_box.is_closed:
                        self.working_img_data['img-drawing'].append([self.working_img_data['img-drawing'][0][0],
                                                                     self.working_img_data['img-drawing'][0][1]])
                        self.set_img_pencil_closed_style()
                    self.image_view.img_stacks.image_dict['img-drawing'].setData(
                        np.asarray(self.working_img_data['img-drawing']))
                    self.is_pencil_allowed = False
                    da_img = create_vis_img(self.image_view.img_size, self.working_img_data['img-drawing'],
                                            self.pencil_color, 'l', self.tool_box.is_closed)
                    res = cv2.resize(da_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                    self.master_layers(res, layer_type='img-drawing', color=self.pencil_color)
                    # save action
                    current_data = {'data': self.working_img_data['img-drawing'].copy(),
                                    'closed': self.tool_box.is_closed}
                    self.save_current_action('pencil_btn', 'img-drawing', current_data, res)
                else:
                    self.inactive_drawing()
                    self.clear_img_pencil_closed_style()

        # ------------------------- ruler
        if self.tool_box.checkable_btn_dict['ruler_btn'].isChecked():
            if len(self.working_img_data['ruler_path']) == 2:
                self.inactive_img_ruler()
                self.tool_box.ruler_length_label.setText('Length:')
            else:
                self.working_img_data['ruler_path'].append([x, y])
                self.image_view.img_stacks.image_dict['ruler_path'].setData(
                    np.asarray(self.working_img_data['ruler_path']))
        # ------------------------- eraser
        elif self.tool_box.checkable_btn_dict['eraser_btn'].isChecked():
            if not self.layer_ctrl.layer_id or len(self.layer_ctrl.current_layer_index) > 1:
                self.print_message('Eraser only works on one single layer.', self.error_message_color, 0.1)
                return
            else:
                r = self.tool_box.eraser_size_slider.value()
                mask_img = np.zeros(self.image_view.img_size, dtype=np.uint8)
                cv2.circle(mask_img, center=(int(x), int(y)), radius=r, color=255, thickness=-1)
                mask_img = 255 - mask_img

                da_link = self.layer_ctrl.layer_link[self.layer_ctrl.current_layer_index[0]]
                if da_link in ['img-mask', 'img-virus']:
                    temp = self.working_img_data[da_link].astype(np.uint8)
                    dst = cv2.bitwise_and(temp, temp, mask=mask_img)
                    self.image_view.img_stacks.image_dict[da_link].setImage(dst)
                    self.working_img_data[da_link] = dst
                    vis_img = color_vis_img(dst, self.layer_ctrl.layer_color[self.layer_ctrl.current_layer_index[0]])
                    res = cv2.resize(vis_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                    self.layer_ctrl.layer_list[self.layer_ctrl.current_layer_index[0]].set_thumbnail_data(res)
                    # save action
                    current_data = {'data': self.working_img_data[da_link].copy()}
                    self.save_current_action('eraser_btn', da_link, current_data, res)
                elif da_link == 'img-process':
                    temp = self.processing_img.copy()
                    dst = cv2.bitwise_and(temp, temp, mask=mask_img)
                    if self.image_view.image_file.pixel_type != 'rgb24':
                        channel_hsv = self.image_view.image_file.hsv_colors
                        img_temp = merge_channels_into_single_img(dst, channel_hsv)
                        input_img = cv2.normalize(img_temp, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                    else:
                        input_img = dst.copy()
                    res = cv2.resize(input_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                    self.layer_ctrl.layer_list[self.layer_ctrl.current_layer_index[0]].set_thumbnail_data(res)
                    self.image_view.img_stacks.set_data(dst)
                    self.processing_img = dst
                    current_data = {'data': self.processing_img.copy()}
                    self.save_current_action('eraser_btn', da_link, current_data, res)
                else:
                    if not self.working_img_data[da_link]:
                        return
                    temp = np.asarray(self.working_img_data[da_link])
                    remain_points, del_indexes = delete_points_inside_eraser(temp, np.array([x, y]), r)
                    if remain_points is None:
                        return
                    self.working_img_data[da_link] = remain_points.tolist()
                    if self.working_img_data[da_link]:
                        if da_link == 'img-contour':
                            self.image_view.img_stacks.image_dict[da_link].setData(remain_points)
                            da_color = self.layer_ctrl.layer_color[self.layer_ctrl.current_layer_index[0]]
                            vis_img = create_vis_img(self.image_view.img_size, self.working_img_data[da_link],
                                                     da_color, 'l')
                            res = cv2.resize(vis_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                            self.layer_ctrl.layer_list[self.layer_ctrl.current_layer_index[0]].set_thumbnail_data(res)
                        elif da_link == 'img-drawing':
                            self.image_view.img_stacks.image_dict[da_link].setData(remain_points)
                            da_color = self.layer_ctrl.layer_color[self.layer_ctrl.current_layer_index[0]]
                            vis_img = create_vis_img(self.image_view.img_size, self.working_img_data[da_link],
                                                     da_color, 'l', self.tool_box.is_closed)
                            res = cv2.resize(vis_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                            self.layer_ctrl.layer_list[self.layer_ctrl.current_layer_index[0]].set_thumbnail_data(res)
                        else:
                            if da_link == 'img-cells':
                                del_inds = np.sort(del_indexes)[::-1]
                                for da_ind in del_inds:
                                    del self.working_img_data['cell_size'][da_ind]
                                    del self.working_img_data['cell_symbol'][da_ind]
                                    del self.working_img_data['cell_layer_index'][da_ind]
                                for i in range(5):
                                    self.working_img_data['cell_count'][i] = \
                                        np.sum(np.ravel(self.working_img_data['cell_layer_index']) == i)
                                for i in range(5):
                                    self.tool_box.cell_count_val_list[i].setText(
                                        str(self.working_img_data['cell_count'][i]))
                                self.image_view.img_stacks.image_dict[da_link].setData(
                                    pos=remain_points, symbol=self.working_img_data['cell_symbol'])
                            else:
                                self.image_view.img_stacks.image_dict[da_link].setData(pos=remain_points)
                            da_color = self.layer_ctrl.layer_color[self.layer_ctrl.current_layer_index[0]]
                            vis_img = create_vis_img(self.image_view.img_size, self.working_img_data[da_link],
                                                     da_color, 'p')
                            res = cv2.resize(vis_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                            self.layer_ctrl.layer_list[self.layer_ctrl.current_layer_index[0]].set_thumbnail_data(res)
                    else:
                        return
                    # save action
                    if da_link == 'img-cells':
                        current_data = {'data': self.working_img_data[da_link].copy(),
                                        'size': self.working_img_data['cell_size'],
                                        'symbol': self.working_img_data['cell_symbol'],
                                        'index': self.working_img_data['cell_layer_index'],
                                        'count': self.working_img_data['cell_count']}
                    elif da_link == 'img-drawing':
                        current_data = {'data': self.working_img_data[da_link].copy(),
                                        'closed': self.tool_box.is_closed}
                    else:
                        current_data = {'data': self.working_img_data[da_link].copy()}
                    self.save_current_action('eraser_btn', da_link, current_data, res)
        # ------------------------- magic wand
        elif self.tool_box.checkable_btn_dict['magic_wand_btn'].isChecked():
            tol_val = float(self.tool_box.magic_tol_val.text())
            if self.processing_img is None:
                src_img = self.image_view.current_img.copy()
            else:
                src_img = self.processing_img.copy()

            # if self.image_view.image_file.is_rgb:
            #     da_color = src_img[int(y), int(x)]
            #     lower_val, upper_val = get_bound_color(da_color, tol_val, self.image_view.image_file.level, 'rgb')
            #     print(lower_val, upper_val)
            #
            #     mask_img = cv2.inRange(src_img[:, :, :3], tuple(lower_val), tuple(upper_val))
            # else:
            mask_img = self.white_img.copy()
            for i in range(self.image_view.image_file.n_channels):
                if not self.image_view.channel_visible[i]:
                    continue
                temp = src_img[:, :, i]
                selected_color = temp[int(y), int(x)]
                print(selected_color)
                lower_val, upper_val = get_bound_color(selected_color, tol_val, self.image_view.image_file.level,
                                                       'gray')
                ret, thresh = cv2.threshold(temp, lower_val, upper_val, cv2.THRESH_BINARY)
                mask_img = cv2.bitwise_and(mask_img, mask_img, mask=thresh.astype(np.uint8))
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ShiftModifier:
                if self.working_img_data['img-mask'] is None:
                    self.working_img_data['img-mask'] = cv2.bitwise_or(mask_img, mask_img, mask=self.white_img)
                else:
                    self.working_img_data['img-mask'] = cv2.bitwise_or(self.working_img_data['img-mask'],
                                                                       mask_img, mask=self.white_img)
            else:
                self.working_img_data['img-mask'] = mask_img.copy()

            if self.kernel is not None:
                temp = self.working_img_data['img-mask'].copy()
                open_img = cv2.morphologyEx(temp, cv2.MORPH_OPEN, self.kernel)
                close_img = cv2.morphologyEx(open_img, cv2.MORPH_CLOSE, self.kernel)
                self.working_img_data['img-mask'] = close_img.copy()
            self.image_view.img_stacks.image_dict['img-mask'].setImage(self.working_img_data['img-mask'])
            temp = color_vis_img(self.working_img_data['img-mask'], self.magic_wand_lut[1])
            res = cv2.resize(temp, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='img-mask', color=self.magic_wand_lut[1])
            # save action
            current_data = {'data': self.working_img_data['img-mask'].copy()}
            self.save_current_action('magic_wand_btn', 'img-mask', current_data, res)

        # ------------------------- lasso
        elif self.tool_box.checkable_btn_dict['lasso_btn'].isChecked():
            if self.working_atlas_data['lasso_path']:
                self.inactive_slice_window_lasso()
            if self.img_lasso_is_closure:
                self.inactive_lasso()
                return
            new_pnt = np.array([x, y])
            if len(self.working_img_data['lasso_path']) > 1:
                dists = np.sum((np.asarray(self.working_img_data['lasso_path'][0]) - new_pnt) ** 2)
            else:
                dists = 1e5
            if dists < np.min(self.image_view.img_size) * 0.05:
                self.working_img_data['lasso_path'].append(self.working_img_data['lasso_path'][0])
                self.image_view.img_stacks.image_dict['lasso_path'].setPen(
                    pg.mkPen(color='r', width=3, style=Qt.SolidLine))
                self.img_lasso_is_closure = True
            else:
                self.working_img_data['lasso_path'].append([x, y])
            drawing_pnts = np.asarray(self.working_img_data['lasso_path'])
            self.image_view.img_stacks.image_dict['lasso_path'].setData(drawing_pnts)
            # save action
            current_data = {'data': self.working_img_data['lasso_path']}
            self.save_current_action('lasso_btn', 'lasso_path', current_data, None)
        # ------------------------- triang -- triangulation pnts
        elif self.tool_box.checkable_btn_dict['triang_btn'].isChecked():
            if self.a2h_transferred or self.h2a_transferred:
                return
            self.histo_tri_inside_data.append([int(x), int(y)])
            self.histo_tri_data = self.histo_tri_onside_data + self.histo_tri_inside_data
            self.image_view.img_stacks.image_dict['tri_pnts'].setData(pos=np.asarray(self.histo_tri_data))
            self.working_img_text.append(pg.TextItem(str(len(self.histo_tri_data) - (self.np_onside - 1) * 4)))
            self.working_img_text[-1].setColor(self.triangle_color)
            self.image_view.img_stacks.vb.addItem(self.working_img_text[-1])
            self.working_img_text[-1].setPos(x, y)
            if self.tool_box.triang_vis_btn.isChecked():
                self.update_histo_tri_lines()
        # ------------------------- loc -- cell
        elif self.tool_box.checkable_btn_dict['loc_btn'].isChecked():
            if self.tool_box.cell_selector_btn.isChecked():
                if 'rgb' in self.image_view.image_file.pixel_type:
                    layer_ind = 0
                else:
                    # only one layer is allowed to work on
                    da_layer = [ind for ind in range(4) if self.image_view.channel_visible[ind]]
                    n_layers = len(da_layer)
                    if n_layers == 0:
                        self.print_message('No image layer is visualised.', self.error_message_color, 0)
                        return
                    if n_layers > 1:
                        self.print_message('Only one image layer is allowed to select cells.',
                                           self.error_message_color, 0)
                        return
                    layer_ind = da_layer[0] + 1

                self.working_img_data['img-cells'].append([x, y])
                self.working_img_data['cell_size'].append(1)
                self.working_img_data['cell_symbol'].append(self.cell_base_symbol[layer_ind])
                self.working_img_data['cell_layer_index'].append(layer_ind)
                self.working_img_data['cell_count'][layer_ind] += 1
                self.tool_box.cell_count_val_list[layer_ind].setText(
                    str(self.working_img_data['cell_count'][layer_ind]))

                self.image_view.img_stacks.image_dict['img-cells'].setData(
                    pos=np.asarray(self.working_img_data['img-cells']), symbol=self.working_img_data['cell_symbol'])

                cv2.circle(self.cell_img, (int(x), int(y)), radius=2, color=self.cell_color, thickness=-1)
                res = cv2.resize(self.cell_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                self.master_layers(res, layer_type='img-cells', color=self.cell_color)

                current_data = {'data': self.working_img_data['img-cells'].copy(),
                                'size': self.working_img_data['cell_size'].copy(),
                                'symbol': self.working_img_data['cell_symbol'].copy(),
                                'index': self.working_img_data['cell_layer_index'].copy(),
                                'count': self.working_img_data['cell_count'].copy()}
                self.save_current_action('loc_btn', 'img-cells', current_data, res)
            if self.tool_box.cell_aim_btn.isChecked():
                self.working_img_data['img-blob'].append([x, y])
                self.image_view.img_stacks.image_dict['img-blob'].setData(
                    pos=np.asarray(self.working_img_data['img-blob']))
        # ------------------------- probe
        elif self.tool_box.checkable_btn_dict['probe_btn'].isChecked():
            self.working_img_data['img-probe'].append([x, y])
            self.image_view.img_stacks.image_dict['img-probe'].setData(
                pos=np.asarray(self.working_img_data['img-probe']))
            vis_img = create_vis_img(self.image_view.img_size, self.working_img_data['img-probe'], self.probe_color, 'p')
            res = cv2.resize(vis_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='img-probe', color=self.probe_color)
            current_data = {'data': self.working_img_data['img-probe'].copy()}
            self.save_current_action('probe_btn', 'img-probe', current_data, res)
        else:
            return

    def img_stacks_hovered(self, event):
        if event.isExit():
            return
        try:
            pos = (event.pos())
        except (IndexError, AttributeError):
            return
        y = pos.y()
        x = pos.x()
        if self.tool_box.checkable_btn_dict['eraser_btn'].isChecked():
            r = self.tool_box.eraser_size_slider.value()
            shp = self.image_view.current_img.shape
            if x - r > 0 and x + r < shp[1] and y - r > 0 and y + r < shp[0]:
                if not self.image_view.img_stacks.image_dict['circle_follow'].isVisible():
                    self.vis_eraser_symbol(True)
                data = self.tool_box.circle.copy()
                data[:, 0] = data[:, 0] + x
                data[:, 1] = data[:, 1] + y
                self.image_view.img_stacks.image_dict['circle_follow'].setData(data)
            else:
                if self.image_view.img_stacks.image_dict['circle_follow'].isVisible():
                    self.vis_eraser_symbol(False)
        # ------------------------- ruler
        elif self.tool_box.checkable_btn_dict['ruler_btn'].isChecked():
            if len(self.working_img_data['ruler_path']) == 1:
                temp = self.working_img_data['ruler_path'].copy()
                temp.append([x, y])
                self.image_view.img_stacks.image_dict['ruler_path'].setData(np.asarray(temp))
        # ------------------------ pencil
        elif self.tool_box.checkable_btn_dict['pencil_btn'].isChecked():
            if self.is_pencil_allowed:
                self.working_img_data['img-drawing'].append([x, y])
                self.image_view.img_stacks.image_dict['img-drawing'].setData(
                    np.asarray(self.working_img_data['img-drawing']))
        msg = 'Histological image coordinates: {}, {}'.format(round(x, 3), round(y, 3))
        self.print_message(msg, self.normal_color, 0)

    def img_stacks_key_pressed(self, action):
        if len(self.layer_ctrl.current_layer_index) != 1:
            self.print_message('Delete only works on single layer. Multiple or No layer is selected.',
                               self.reminder_color, 0)
            return
        da_link = self.layer_ctrl.layer_link[self.layer_ctrl.current_layer_index[0]]

        if action == 'delete':
            if self.img_lasso_is_closure:
                mask = np.zeros(self.image_view.img_size, dtype=np.uint8)
                pts = np.int32(self.working_img_data['lasso_path'])
                cv2.fillPoly(mask, pts=[pts], color=255)
                if not self.tool_box.remove_inside:
                    mask = 255 - mask
                if da_link == 'img-mask':
                    dst = cv2.bitwise_and(self.working_img_data[da_link], self.working_img_data[da_link], mask=mask)
                    self.image_view.img_stacks.image_dict[da_link].setImage(dst)
                    self.working_img_data[da_link] = dst
                    vis_img = color_vis_img(dst, self.layer_ctrl.layer_color[self.layer_ctrl.current_layer_index[0]])
                    res = cv2.resize(vis_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                    current_data = {'data': self.working_img_data[da_link].copy()}
                    self.save_current_action('delete', da_link, current_data, res)
                elif da_link == 'img-process':
                    dst = cv2.bitwise_and(self.processing_img, self.processing_img, mask=mask)
                    self.image_view.img_stacks.set_data(dst)
                    self.processing_img = dst
                    if self.image_view.image_file.pixel_type != 'rgb24':
                        channel_hsv = self.image_view.image_file.hsv_colors
                        img_temp = merge_channels_into_single_img(dst, channel_hsv)
                        input_img = cv2.normalize(img_temp, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                    else:
                        input_img = dst.copy()
                    res = cv2.resize(input_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                    current_data = {'data': self.processing_img.copy()}
                    self.save_current_action('delete', da_link, current_data, res)
                else:
                    msg = 'Lasso Tool only works on process layer, slice layer and mask layer.'
                    self.print_message(msg, self.reminder_color, 0)
                    return
            else:
                if self.working_img_data['img-mask'] is None or da_link != 'img-process':
                    return
                print('ttt')
                mask = self.working_img_data['img-mask'].copy()
                mask = 255 - mask * 255
                temp = self.processing_img.copy()
                print(temp.shape)
                dst = cv2.bitwise_and(temp, temp, mask=mask)
                input_img = dst.copy()
                print(np.max(dst))
                print(np.min(dst))
                self.image_view.img_stacks.set_data(dst)
                self.processing_img = dst
                if self.image_view.image_file.pixel_type != 'rgb24':
                    channel_hsv = self.image_view.image_file.hsv_colors
                    img_temp = merge_channels_into_single_img(dst, channel_hsv)
                    input_img = cv2.normalize(img_temp, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                res = cv2.resize(input_img, self.image_view.tb_size, interpolation=cv2.INTER_AREA)
                self.remove_single_link_related('img-mask')
                current_data = {'data': self.processing_img.copy()}
                self.save_current_action('delete', da_link, current_data, res)

            self.layer_ctrl.layer_list[self.layer_ctrl.current_layer_index[0]].set_thumbnail_data(res)

    def hist_window_tri_pnts_moving(self, ev_obj):
        ev = ev_obj[0]
        ind = ev_obj[1]
        da_num = (self.np_onside - 1) * 4
        if ind < da_num:
            return

        if self.a2h_transferred:
            old_pnts = self.histo_tri_data.copy()
            new_pnts = self.histo_tri_data.copy()
            da_new_pnt = self.image_view.img_stacks.image_dict['tri_pnts'].data['pos'][ind].copy()
            new_pnts[ind] = [int(da_new_pnt[0]), int(da_new_pnt[1])]

            img_overlay = self.image_view.img_stacks.image_dict['img-overlay'].image.copy()
            img_wrap = img_overlay.copy()

            img_size = img_wrap.shape[:2]
            rect = (0, 0, img_size[1], img_size[0])

            subdiv = cv2.Subdiv2D(rect)
            for p in new_pnts:
                subdiv.insert(p)

            tri_vet_inds = get_vertex_ind_in_triangle(subdiv)
            for i in range(len(tri_vet_inds)):
                da_inds = tri_vet_inds[i]
                # if ind not in da_inds:
                #     continue
                t1 = [old_pnts[da_inds[0]], old_pnts[da_inds[1]], old_pnts[da_inds[2]]]
                t2 = [new_pnts[da_inds[0]], new_pnts[da_inds[1]], new_pnts[da_inds[2]]]
                t1 = np.reshape(t1, (3, 2))
                t2 = np.reshape(t2, (3, 2))
                warp_triangle(img_overlay, img_wrap,  t1, t2, True)
            self.image_view.img_stacks.image_dict['img-overlay'].setImage(img_wrap)
            self.histo_tri_data = new_pnts
        else:
            da_new_pnt = self.image_view.img_stacks.image_dict['tri_pnts'].data['pos'][ind].copy()
            self.histo_tri_data[ind] = [int(da_new_pnt[0]), int(da_new_pnt[1])]
        self.histo_tri_inside_data[ind - da_num] = [int(da_new_pnt[0]), int(da_new_pnt[1])]
        self.working_img_text[ind - da_num].setPos(da_new_pnt[0], da_new_pnt[1])
        if self.tool_box.triang_vis_btn.isChecked():
            self.update_histo_tri_lines()

    def img_probe_pnts_clicked(self, points, ev):
        if not self.tool_box.checkable_btn_dict['eraser_btn'].isChecked() or not self.working_img_data['img-probe']:
            return
        clicked_ind = ev[0].index()
        del self.working_img_data['img-probe'][clicked_ind]
        self.image_view.img_stacks.image_dict['img-probe'].setData(np.asarray(self.working_img_data['img-probe']))


    def img_cell_pnts_clicked(self, points, ev):
        if not self.tool_box.checkable_btn_dict['eraser_btn'].isChecked() or not self.working_img_data['img-cells']:
            return
        clicked_ind = ev[0].index()
        layer_ind = self.working_img_data['cell_layer_index'][clicked_ind]
        self.working_img_data['cell_count'][layer_ind] -= 1
        self.tool_box.cell_count_val_list[layer_ind].setText(str(self.working_img_data['cell_count'][layer_ind]))
        del self.working_img_data['img-cells'][clicked_ind]
        del self.working_img_data['cell_symbol'][clicked_ind]
        del self.working_img_data['cell_size'][clicked_ind]
        del self.working_img_data['cell_layer_index'][clicked_ind]
        self.image_view.img_stacks.image_dict['img-cells'].setData(pos=np.asarray(self.working_img_data['img-cells']),
                                                     symbol=self.working_img_data['cell_symbol'])

    def hist_window_tri_pnts_clicked(self, ev):
        if not self.tool_box.checkable_btn_dict['eraser_btn'].isChecked() or not self.histo_tri_data:
            return
        if self.a2h_transferred or self.h2a_transferred:
            return
        self.inactive_lasso()
        clicked_ind = ev[1]
        num = (self.np_onside - 1) * 4
        if clicked_ind < num:
            return
        self.image_view.img_stacks.vb.removeItem(self.working_img_text[-1])
        del self.working_img_text[-1]
        del self.histo_tri_data[clicked_ind]
        del self.histo_tri_inside_data[clicked_ind - num]
        self.image_view.img_stacks.image_dict['tri_pnts'].setData(pos=np.asarray(self.histo_tri_data))
        for i in range(len(self.working_img_text)):
            pnt_id = i + num
            self.working_img_text[i].setPos(self.histo_tri_data[pnt_id][0], self.histo_tri_data[pnt_id][1])
        if self.tool_box.triang_vis_btn.isChecked():
            self.update_histo_tri_lines()

    # ------------------------------------------------------------------
    #
    #                       Atlas window related
    #
    # ------------------------------------------------------------------
    def slice_stack_hovered(self, event):
        if event.isExit():
            return
        try:
            pos = (event.pos())
        except (IndexError, AttributeError):
            return
        y = pos.y()
        x = pos.x()
        if self.tool_box.checkable_btn_dict['eraser_btn'].isChecked():
            r = self.tool_box.eraser_size_slider.value()
            shp = self.working_atlas_data['atlas-slice'].shape
            if x - r > 0 and x + r < shp[1] and y - r > 0 and y + r < shp[0]:
                if not self.atlas_view.slice_stack.image_dict['circle_follow'].isVisible():
                    self.vis_eraser_symbol(True)
                data = self.tool_box.circle.copy()
                data[:, 0] = data[:, 0] + x
                data[:, 1] = data[:, 1] + y
                self.atlas_view.slice_stack.image_dict['circle_follow'].setData(data)
            else:
                if self.atlas_view.slice_stack.image_dict['circle_follow'].isVisible():
                    self.vis_eraser_symbol(False)
        elif self.tool_box.checkable_btn_dict['ruler_btn'].isChecked():
            if len(self.working_atlas_data['ruler_path']) == 1:
                temp = self.working_atlas_data['ruler_path'].copy()
                temp.append([x, y])
                self.atlas_view.slice_stack.image_dict['ruler_path'].setData(np.asarray(temp))

        if not self.slice_bregma or self.slice_height == 0 or self.slice_distance == 0 or self.slice_width == 0:
            msg = 'Atlas Slice Image coordinates: {} px, {} px'.format(int(x), int(y))
        else:
            xc, yc, zc = get_slice_atlas_coord(np.asarray([[x, y]]), self.slice_cut, self.atlas_view.slice_size,
                                               self.slice_width, self.slice_height, self.slice_distance,
                                               self.slice_bregma)
            msg = 'Atlas Slice Image coordinates: {} um, {} um, {} um w.r.t. Bregma.'.format(
                round(xc[0], 2), round(yc[0], 2), round(zc[0], 2))
        self.print_message(msg, self.normal_color, 0)

    def coronal_slice_stacks_hovered(self, pos):
        y = pos.y()
        x = pos.x()

        if self.tool_box.checkable_btn_dict['ruler_btn'].isChecked() and self.num_windows != 4:
            if len(self.working_atlas_data['ruler_path']) == 1:
                temp = self.working_atlas_data['ruler_path'].copy()
                temp.append([x, y])
                self.atlas_view.cimg.image_dict['ruler_path'].setData(np.asarray(temp))

        c_id = self.atlas_view.current_coronal_index
        s_id = self.atlas_view.current_sagital_index
        h_id = self.atlas_view.atlas_size[0] - self.atlas_view.current_horizontal_index

        o_rot = np.array([h_id, s_id, c_id])
        da_pnt = np.array([y, x, c_id])

        if self.atlas_view.coronal_rotated:
            da_pnt = np.dot(self.atlas_view.c_rotm_2d, (da_pnt - o_rot)) + o_rot

        da_label = self.atlas_view.cimg.label_img.image.copy()
        da_id = da_label[int(y), int(x)]

        vox_val = self.atlas_view.cimg.img.image[int(y), int(x)]

        if vox_val != 0:
            coords = np.round((da_pnt - np.ravel(self.atlas_view.Bregma)) * self.atlas_view.vox_size_um, 2)
            da_vec = self.atlas_view.cimg.img.image[:, int(da_pnt[1])]
            valid_inds = np.where(da_vec != 0)[0]
            # self.atlas_view.cimg.image_dict['atlas-probe'].setData(pos=[[x, valid_inds[0]]])
            dv_val = np.round((valid_inds[0] - da_pnt[0]) * self.atlas_view.vox_size_um, 2)
            pstr = 'Atlas voxel:({}, {}, {}), ML:{}um, AP:{}um, DV:{}um w.r.t Bregma, DV:{}um w.r.t Surface: {} '.format(
                int(da_pnt[1]), int(da_pnt[2]), int(self.atlas_view.atlas_size[0] - da_pnt[0]),
                coords[1], coords[2], -coords[0], dv_val, self.atlas_view.label_tree.describe(da_id))
            self.print_message(pstr, self.normal_color, 0)

            if self.atlas_view.navigation_btn.isChecked():
                self.atlas_view.cimg.v_line.setPos(x)
                self.atlas_view.cimg.h_line.setPos(y)
                self.atlas_view.simg.v_line.setPos(c_id)
                self.atlas_view.simg.h_line.setPos(y)
                self.atlas_view.himg.v_line.setPos(c_id)
                self.atlas_view.himg.h_line.setPos(x)

                self.atlas_view.spage_ctrl.set_val(x)
                self.atlas_view.hpage_ctrl.set_val(self.atlas_view.atlas_size[0] - int(y))
        else:
            self.print_message('', self.normal_color, 0)

    def sagital_slice_stacks_hovered(self, pos):
        y = pos.y()
        x = pos.x()

        if self.tool_box.checkable_btn_dict['ruler_btn'].isChecked() and self.num_windows != 4:
            if len(self.working_atlas_data['ruler_path']) == 1:
                temp = self.working_atlas_data['ruler_path'].copy()
                temp.append([x, y])
                self.atlas_view.simg.image_dict['ruler_path'].setData(np.asarray(temp))

        c_id = self.atlas_view.current_coronal_index
        s_id = self.atlas_view.current_sagital_index
        h_id = self.atlas_view.atlas_size[0] - self.atlas_view.current_horizontal_index

        o_rot = np.array([h_id, s_id, c_id])
        da_pnt = np.array([y, s_id, x])

        if self.atlas_view.sagital_rotated:
            da_pnt = o_rot + np.dot(self.atlas_view.s_rotm_2d, (da_pnt - o_rot))

        da_label = self.atlas_view.simg.label_img.image.copy()
        da_id = da_label[int(y), int(x)]

        vox_val = self.atlas_view.simg.img.image[int(y), int(x)]

        if vox_val != 0:
            coords = np.round((da_pnt - np.ravel(self.atlas_view.Bregma)) * self.atlas_view.vox_size_um, 2)
            da_vec = self.atlas_view.simg.img.image[:, int(da_pnt[2])]
            valid_inds = np.where(da_vec != 0)[0]
            # self.atlas_view.simg.image_dict['atlas-probe'].setData(pos=[[x, valid_inds[0]]])
            dv_val = np.round((valid_inds[0] - da_pnt[0]) * self.atlas_view.vox_size_um, 2)
            pstr = 'Atlas voxel:({}, {}, {}), ML:{}um, AP:{}um, DV:{}um w.r.t Bregma, DV:{}um w.r.t Surface: {} '.format(
                int(da_pnt[1]), int(da_pnt[2]), int(self.atlas_view.atlas_size[0] - da_pnt[0]),
                coords[1], coords[2], -coords[0], dv_val, self.atlas_view.label_tree.describe(da_id))
            self.print_message(pstr, self.normal_color, 0)

            if self.atlas_view.navigation_btn.isChecked():
                self.atlas_view.simg.v_line.setPos(x)
                self.atlas_view.simg.h_line.setPos(y)
                self.atlas_view.cimg.v_line.setPos(s_id)
                self.atlas_view.cimg.h_line.setPos(y)
                self.atlas_view.himg.v_line.setPos(x)
                self.atlas_view.himg.h_line.setPos(s_id)

                self.atlas_view.cpage_ctrl.set_val(x)
                self.atlas_view.hpage_ctrl.set_val(self.atlas_view.atlas_size[0] - int(y))
        else:
            self.print_message('', self.normal_color, 0)

    def horizontal_slice_stacks_hovered(self, pos):
        y = pos.y()
        x = pos.x()

        if self.tool_box.checkable_btn_dict['ruler_btn'].isChecked() and self.num_windows != 4:
            if len(self.working_atlas_data['ruler_path']) == 1:
                temp = self.working_atlas_data['ruler_path'].copy()
                temp.append([x, y])
                self.atlas_view.himg.image_dict['ruler_path'].setData(np.asarray(temp))

        c_id = self.atlas_view.current_coronal_index
        s_id = self.atlas_view.current_sagital_index
        h_id = self.atlas_view.atlas_size[0] - self.atlas_view.current_horizontal_index

        o_rot = np.array([h_id, s_id, c_id])
        da_pnt = np.array([h_id, y, x])

        if self.atlas_view.horizontal_rotated:
            da_pnt = o_rot + np.dot(self.atlas_view.h_rotm_2d, (da_pnt - o_rot))

        da_label = self.atlas_view.himg.label_img.image.copy()
        da_id = da_label[int(y), int(x)]

        vox_val = self.atlas_view.himg.img.image[int(y), int(x)]

        if vox_val != 0:
            coords = np.round((da_pnt - np.ravel(self.atlas_view.Bregma)) * self.atlas_view.vox_size_um, 2)
            da_vec = self.atlas_view.atlas_data[:, int(da_pnt[1]), int(da_pnt[2])]
            valid_inds = np.where(da_vec != 0)[0]
            # self.atlas_view.cimg.image_dict['atlas-probe'].setData(pos=[[int(y), valid_inds[0]]])
            # self.atlas_view.simg.image_dict['atlas-probe'].setData(pos=[[int(x), valid_inds[0]]])
            dv_val = np.round((valid_inds[0] - h_id) * self.atlas_view.vox_size_um, 2)
            pstr = 'Atlas voxel:({}, {}, {}), ML:{}um, AP:{}um, DV:{}um w.r.t. Bregma, DV:{}um w.r.t Surface: {} '.format(
                int(da_pnt[1]), int(da_pnt[2]), int(self.atlas_view.atlas_size[0] - da_pnt[0]),
                coords[1], coords[2], -coords[0], dv_val, self.atlas_view.label_tree.describe(da_id))
            self.print_message(pstr, self.normal_color, 0)

            if self.atlas_view.navigation_btn.isChecked():
                self.atlas_view.himg.v_line.setPos(x)
                self.atlas_view.himg.h_line.setPos(y)
                self.atlas_view.cimg.v_line.setPos(y)
                self.atlas_view.cimg.h_line.setPos(h_id)
                self.atlas_view.simg.v_line.setPos(x)
                self.atlas_view.simg.h_line.setPos(h_id)

                self.atlas_view.cpage_ctrl.set_val(int(x))
                self.atlas_view.spage_ctrl.set_val(int(y))
        else:
            self.print_message('', self.normal_color, 0)

    def atlas_stacks_clicked(self, pos):
        # print('atlas clicked')
        x = pos[0]
        y = pos[1]
        if self.current_atlas == 'volume':
            if self.atlas_view.atlas_data is None or self.num_windows == 4:
                return
        else:
            if self.atlas_view.slice_image_data is None:
                return
        # ------------------------- ruler
        if self.tool_box.checkable_btn_dict['ruler_btn'].isChecked():
            if len(self.working_atlas_data['ruler_path']) == 2:
                self.inactive_atlas_ruler()
                self.tool_box.ruler_length_label.setText('Length:')
            else:
                self.working_atlas_data['ruler_path'].append([x, y])
                self.atlas_view.working_atlas.image_dict['ruler_path'].setData(
                    np.asarray(self.working_atlas_data['ruler_path']))

        # ------------------------- triangle
        elif self.tool_box.checkable_btn_dict['triang_btn'].isChecked():
            if self.a2h_transferred or self.h2a_transferred:
                return
            self.atlas_tri_inside_data.append([int(x), int(y)])
            self.atlas_tri_data = self.atlas_tri_onside_data + self.atlas_tri_inside_data
            self.atlas_view.working_atlas.image_dict['tri_pnts'].setData(pos=np.asarray(self.atlas_tri_data))
            self.working_atlas_text.append(pg.TextItem(str(len(self.atlas_tri_inside_data))))
            self.working_atlas_text[-1].setColor(self.triangle_color)
            self.working_atlas_text[-1].setPos(x, y)
            self.atlas_view.working_atlas.vb.addItem(self.working_atlas_text[-1])
            if self.tool_box.triang_vis_btn.isChecked():
                self.update_atlas_tri_lines()
        # ------------------------- eraser
        elif self.tool_box.checkable_btn_dict['eraser_btn'].isChecked():
            if not self.layer_ctrl.layer_id or len(self.layer_ctrl.current_layer_index) > 1:
                self.print_message('Eraser only works on one single layer.', self.error_message_color, 0.1)
                return
            else:
                da_link = self.layer_ctrl.layer_link[self.layer_ctrl.current_layer_index[0]]
                if da_link == 'atlas-probe':
                    if self.h2a_transferred:
                        return
                    if not self.working_atlas_data[da_link]:
                        return
                    r = self.tool_box.eraser_size_slider.value()
                    temp = np.asarray(self.working_atlas_data[da_link])
                    remain_points, del_indexes = delete_points_inside_eraser(temp, np.array([x, y]), r)
                    if remain_points is None:
                        return
                    self.working_atlas_data[da_link] = remain_points.tolist()
                    if self.working_atlas_data[da_link]:
                        self.atlas_view.working_atlas.image_dict[da_link].setData(pos=remain_points)
                        da_color = self.layer_ctrl.layer_color[self.layer_ctrl.current_layer_index[0]]
                        vis_img = create_vis_img(self.atlas_view.slice_size, self.working_atlas_data[da_link],
                                                 da_color, 'p')
                        res = cv2.resize(vis_img, self.atlas_view.slice_tb_size, interpolation=cv2.INTER_AREA)
                        self.layer_ctrl.layer_list[self.layer_ctrl.current_layer_index[0]].set_thumbnail_data(res)
                    else:
                        return
                else:
                    if self.current_atlas == 'volume':
                        return
                    r = self.tool_box.eraser_size_slider.value()
                    mask_img = np.zeros(self.working_atlas_data[da_link].shape[:2], dtype=np.uint8)
                    cv2.circle(mask_img, center=(int(x), int(y)), radius=r, color=255, thickness=-1)
                    mask_img = 255 - mask_img
                    if da_link in ['atlas-mask', 'atlas-slice']:
                        temp = self.working_atlas_data[da_link].astype(np.uint8)
                        dst = cv2.bitwise_and(temp, temp, mask=mask_img)
                        res = cv2.resize(dst, self.slice_tb_size, interpolation=cv2.INTER_AREA)
                        self.atlas_view.slice_stack.image_dict[da_link].setImage(dst)
                        self.working_atlas_data[da_link] = dst
                    else:
                        return
                self.layer_ctrl.layer_list[self.layer_ctrl.current_layer_index[0]].set_thumbnail_data(res)
                current_data = {'data': self.working_atlas_data[da_link].copy()}
                self.save_current_action('eraser_btn', da_link, current_data, res)
        # ------------------------- lasso
        elif self.tool_box.checkable_btn_dict['lasso_btn'].isChecked():
            if self.working_img_data['lasso_path']:
                self.inactive_lasso()
            if self.atlas_lasso_is_closure:
                self.inactive_slice_window_lasso()
                return
            if self.current_atlas == 'volume':
                return
            new_pnt = np.array([x, y])
            if len(self.working_atlas_data['lasso_path']) > 1:
                dists = np.sum((np.asarray(self.working_atlas_data['lasso_path'][0]) - new_pnt) ** 2)
            else:
                dists = 1e5
            if dists < 5:
                self.working_atlas_data['lasso_path'].append(self.working_atlas_data['lasso_path'][0])
                self.atlas_view.slice_stack.image_dict['lasso_path'].setPen(
                    pg.mkPen(color='r', width=3, style=Qt.SolidLine))
                self.atlas_lasso_is_closure = True
            else:
                self.working_atlas_data['lasso_path'].append([x, y])
            drawing_pnts = np.asarray(self.working_atlas_data['lasso_path'])
            self.atlas_view.slice_stack.image_dict['lasso_path'].setData(drawing_pnts)
            current_data = {'data': self.working_atlas_data['lasso_path'].copy()}
            self.save_current_action('lasso_btn', 'lasso_path', current_data, None)
        # ------------------------- probe
        elif self.tool_box.checkable_btn_dict['probe_btn'].isChecked():
            self.working_atlas_data['atlas-probe'].append([x, y])
            self.atlas_view.working_atlas.image_dict['atlas-probe'].setData(
                pos=np.asarray(self.working_atlas_data['atlas-probe']))  #??
            current_data = {'data': self.working_atlas_data['atlas-probe'].copy()}
            self.save_current_action('probe_btn', 'atlas-probe', current_data, None)
        # ------------------------- magic wand -- mask
        elif self.tool_box.checkable_btn_dict['magic_wand_btn'].isChecked():
            if self.current_atlas == 'volume':
                if not self.h2a_transferred:
                    return
                src_img = self.atlas_view.working_atlas.image_dict['atlas-overlay'].image.copy()
            else:
                src_img = self.atlas_view.slice_image_data.copy()
            white_img = np.ones(self.atlas_view.slice_size).astype('uint8')
            tol_val = int(self.tool_box.magic_tol_val.text())
            da_color = src_img[int(y), int(x), :3]
            lower_val, upper_val = get_bound_color(da_color, tol_val, 255, 'rgb')
            mask_img = cv2.inRange(src_img[:, :, :3], np.array(lower_val, dtype='float'),
                                   np.array(upper_val, dtype='float'))

            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ShiftModifier:
                if self.working_atlas_data['atlas-mask'] is None:
                    self.working_atlas_data['atlas-mask'] = cv2.bitwise_or(mask_img, mask_img, mask=white_img)
                else:
                    self.working_atlas_data['atlas-mask'] = cv2.bitwise_or(self.working_atlas_data['atlas-mask'],
                                                                           mask_img, mask=white_img)
            else:
                self.working_atlas_data['atlas-mask'] = mask_img.copy()

            if self.kernel is not None:
                temp = self.working_atlas_data['atlas-mask'].copy()
                open_img = cv2.morphologyEx(temp, cv2.MORPH_OPEN, self.kernel)
                close_img = cv2.morphologyEx(open_img, cv2.MORPH_CLOSE, self.kernel)
                self.working_atlas_data['atlas-mask'] = close_img.copy()

            self.atlas_view.working_atlas.image_dict['atlas-mask'].setImage(self.working_atlas_data['atlas-mask'])
            res = cv2.resize(self.working_atlas_data['atlas-mask'],
                             self.atlas_view.slice_tb_size, interpolation=cv2.INTER_AREA)
            self.master_layers(res, layer_type='atlas-mask', color=self.magic_wand_lut[1])
            current_data = {'data': self.working_atlas_data['atlas-mask'].copy()}
            self.save_current_action('magic_wand_btn', 'atlas-mask', current_data, res)
        # ------------------------- bregma picker
        elif self.actionBregma_Picker.isChecked():
            self.slice_bregma = [x, y]
            self.atlas_view.slice_stack.image_dict['bregma_pnt'].setData(pos=np.array([self.slice_bregma]))
            self.actionBregma_Picker.setChecked(False)
            if self.slice_height == 0 or self.slice_width == 0 or self.slice_distance == 0:
                self.slice_info_ready = False
            else:
                self.slice_info_ready = True
        else:
            return

    def slice_stack_key_pressed(self, action):
        if len(self.layer_ctrl.current_layer_index) != 1:
            self.print_message('Delete only works on single layer. Multiple or No layer is selected.',
                               self.reminder_color, 0)
            return
        da_link = self.layer_ctrl.layer_link[self.layer_ctrl.current_layer_index[0]]

        if action == 'delete':
            if self.atlas_lasso_is_closure:
                mask = np.zeros(self.atlas_view.slice_size, dtype=np.uint8)
                pts = np.int32(self.working_atlas_data['lasso_path'])
                cv2.fillPoly(mask, pts=[pts], color=255)
                if not self.tool_box.remove_inside:
                    mask = 255 - mask
                if da_link == 'atlas-mask':
                    dst = cv2.bitwise_and(self.working_atlas_data['atlas-mask'], self.working_atlas_data['atlas-mask'],
                                          mask=mask)
                    self.atlas_view.slice_stack.image_dict['atlas-mask'].setImage(dst)
                    self.working_atlas_data['atlas-mask'] = dst
                    res = cv2.resize(self.working_atlas_data['atlas-mask'], self.atlas_view.slice_tb_size,
                                     interpolation=cv2.INTER_AREA)
                elif da_link == 'atlas-slice':
                    dst = cv2.bitwise_and(self.working_atlas_data[da_link], self.working_atlas_data[da_link], mask=mask)
                    self.atlas_view.slice_stack.set_data(dst)
                    self.working_atlas_data[da_link] = dst
                    res = cv2.resize(dst, self.atlas_view.slice_tb_size, interpolation=cv2.INTER_AREA)
                else:
                    return
            else:
                if self.working_atlas_data['atlas-mask'] is None or da_link != 'atlas-slice':
                    return
                mask = self.working_atlas_data['atlas-mask'].copy()
                mask = 255 - mask
                temp = self.working_atlas_data['atlas-slice'].copy()
                dst = cv2.bitwise_and(temp, temp, mask=mask)
                self.atlas_view.slice_stack.set_data(dst)
                self.working_atlas_data['atlas-slice'] = dst
                res = cv2.resize(dst, self.atlas_view.slice_tb_size, interpolation=cv2.INTER_AREA)
            self.layer_ctrl.layer_list[self.layer_ctrl.current_layer_index[0]].set_thumbnail_data(res)
            current_data = {'data': self.working_atlas_data[da_link].copy()}
            self.save_current_action('delete', da_link, current_data, res)
        else:
            return

    #
    def atlas_window_tri_pnts_moving(self, ev_obj):
        ev = ev_obj[0]
        ind = ev_obj[1]
        da_num = (self.np_onside - 1) * 4
        if ind < da_num:
            return
        if self.h2a_transferred:
            old_pnts = self.atlas_tri_data.copy()
            new_pnts = self.atlas_tri_data.copy()
            da_new_pnt = self.atlas_view.working_atlas.image_dict['tri_pnts'].data['pos'][ind].copy()
            new_pnts[ind] = [int(da_new_pnt[0]), int(da_new_pnt[1])]
            print(self.atlas_tri_data[ind])
            print(da_new_pnt)


            input_img = self.overlay_img.copy()
            img_wrap = np.zeros((self.atlas_view.slice_size[0], self.atlas_view.slice_size[1], input_img.shape[2]),
                                np.float32)

            subdiv = cv2.Subdiv2D(self.atlas_rect)
            for p in self.atlas_tri_data:
                subdiv.insert(p)

            tri_vet_inds = get_vertex_ind_in_triangle(subdiv)
            for i in range(len(tri_vet_inds)):
                da_inds = tri_vet_inds[i]
                t1 = [self.atlas_tri_data[da_inds[0]], self.atlas_tri_data[da_inds[1]],
                      self.atlas_tri_data[da_inds[2]]]
                t2 = [new_pnts[da_inds[0]], new_pnts[da_inds[1]],
                      new_pnts[da_inds[2]]]
                t1 = np.reshape(t1, (3, 2))
                t2 = np.reshape(t2, (3, 2))
                warp_triangle(input_img, img_wrap, t1, t2, True)

            #

            # # img_overlay = self.atlas_view.working_atlas.overlay_img.image.copy()
            # img_wrap = img_overlay.copy()
            #
            # img_size = img_wrap.shape[:2]
            # rect = (0, 0, img_size[1], img_size[0])
            #
            # subdiv = cv2.Subdiv2D(rect)
            # for p in new_pnts:
            #     subdiv.insert(p)
            #
            # tri_vet_inds = get_vertex_ind_in_triangle(subdiv)
            # for i in range(len(tri_vet_inds)):
            #     da_inds = tri_vet_inds[i]
            #     if ind not in da_inds:
            #         continue
            #     t1 = [old_pnts[da_inds[0]], old_pnts[da_inds[1]], old_pnts[da_inds[2]]]
            #     t2 = [new_pnts[da_inds[0]], new_pnts[da_inds[1]], new_pnts[da_inds[2]]]
            #     t1 = np.reshape(t1, (3, 2))
            #     t2 = np.reshape(t2, (3, 2))
            #     warp_triangle(img_overlay, img_wrap,  t1, t2, True)
            self.atlas_view.working_atlas.image_dict['atlas-overlay'].setImage(img_wrap)
            # self.atlas_tri_data = new_pnts
        else:
            da_new_pnt = self.atlas_view.working_atlas.image_dict['tri_pnts'].data['pos'][ind].copy()
            self.atlas_tri_data[ind] = [int(da_new_pnt[0]), int(da_new_pnt[1])]
        self.atlas_tri_inside_data[ind - da_num] = [int(da_new_pnt[0]), int(da_new_pnt[1])]
        self.working_atlas_text[ind - da_num].setPos(da_new_pnt[0], da_new_pnt[1])
        if self.tool_box.triang_vis_btn.isChecked():
            self.update_atlas_tri_lines()

    def atlas_window_tri_pnts_clicked(self, ev):
        print(self.atlas_tri_data)
        if not self.tool_box.checkable_btn_dict['eraser_btn'].isChecked():
            return
        if self.a2h_transferred or self.h2a_transferred:
            return
        self.inactive_lasso()
        clicked_ind = ev[1]
        num = (self.np_onside - 1) * 4
        if clicked_ind < num:
            return
        self.atlas_view.working_atlas.vb.removeItem(self.working_atlas_text[-1])
        del self.working_atlas_text[-1]
        del self.atlas_tri_inside_data[clicked_ind - num]
        self.atlas_tri_data = self.atlas_tri_onside_data + self.atlas_tri_inside_data
        self.atlas_view.working_atlas.image_dict['tri_pnts'].setData(pos=np.asarray(self.atlas_tri_data))
        for i in range(len(self.working_atlas_text)):
            pnt_id = i + num
            self.working_atlas_text[i].setPos(self.atlas_tri_data[pnt_id][0], self.atlas_tri_data[pnt_id][1])
        if self.tool_box.triang_vis_btn.isChecked():
            self.update_atlas_tri_lines()

    def atlas_probe_pnts_clicked(self, points, ev):
        if self.num_windows == 4 or not self.working_atlas_data['atlas-probe']:
            return
        if not self.tool_box.checkable_btn_dict['eraser_btn'].isChecked():
            return
        clicked_ind = ev[0].index()
        del self.working_atlas_data['atlas-probe'][clicked_ind]
        if self.working_atlas_data['atlas-probe']:
            self.atlas_view.working_atlas.image_dict['atlas-probe'].setData(
                pos=np.asarray(self.working_atlas_data['atlas-probe']))
        else:
            self.atlas_view.working_atlas.image_dict['atlas-probe'].clear()

    def atlas_contour_pnts_clicked(self, points, ev):
        if self.num_windows == 4 or not self.working_atlas_data['atlas-contour']:
            return
        if not self.tool_box.checkable_btn_dict['eraser_btn'].isChecked():
            return
        clicked_ind = ev[0].index()
        del self.working_atlas_data['atlas-contour'][clicked_ind]
        if self.working_atlas_data['atlas-contour']:
            self.atlas_view.working_atlas.image_dict['atlas-contour'].setData(
                pos=np.asarray(self.working_atlas_data['atlas-contour']))
        else:
            self.atlas_view.working_atlas.image_dict['atlas-contour'].clear()

    # ------------------------------------------------------------------
    #
    #                       Atlas 3D control
    #
    # ------------------------------------------------------------------
    def show_small_area_in_3d(self):
        if self.show_child_mesh:
            self.show_child_mesh = False
        else:
            self.show_child_mesh = True

    def composition_3d_changed(self):
        if self.atlas_view.atlas_data is None:
            return
        all_keys = list(self.small_mesh_list.keys())
        for da_key in all_keys:
            self.small_mesh_list[da_key].setGLOptions(self.composition_combo.currentText())

    def sig_label_changed(self):
        if self.atlas_view.atlas_data is None or self.atlas_view.atlas_label is None:
            return
        lut = self.atlas_view.label_tree.lookup_table()

        self.atlas_view.cimg.label_img.setLookupTable(lut=lut)
        self.atlas_view.simg.label_img.setLookupTable(lut=lut)
        self.atlas_view.himg.label_img.setLookupTable(lut=lut)

        if len(self.small_mesh_list) == 0:
            return
        valid_id = list(self.small_mesh_list.keys())
        current_checked_label = list(self.atlas_view.label_tree.checked)
        n_current_label = len(current_checked_label)
        n_previous_label = len(self.previous_checked_label)
        if self.show_child_mesh:
            if n_current_label > n_previous_label:
                label_to_show = [id for id in current_checked_label if id not in self.previous_checked_label]
                label_to_show = list(np.ravel(label_to_show).astype(str))
                for id in label_to_show:
                    if id in valid_id:
                        self.small_mesh_list[id].setVisible(True)
            else:
                label_to_hide = [id for id in self.previous_checked_label if id not in current_checked_label]
                label_to_hide = list(np.ravel(label_to_hide).astype(str))
                for id in label_to_hide:
                    if id in valid_id:
                        self.small_mesh_list[id].setVisible(False)
        self.previous_checked_label = current_checked_label

        check_id = list(self.atlas_view.label_tree.checked)

        if self.show_child_mesh:
            if len(check_id) != 0:
                for id in check_id:
                    if id in valid_id:
                        if not self.small_mesh_list[id].visible():
                            self.small_mesh_list[id].setVisible(True)
            else:
                for id in valid_id:
                    if self.small_mesh_list[id].visible():
                        self.small_mesh_list[id].setVisible(False)
        #
        # # lut = self.label_tree.lookup_table()
        # lut = self.acontrols.atlas_view.label_tree.lookup_table()
        # check_id = list(self.acontrols.atlas_view.label_tree.checked)
        # check_id = np.ravel(check_id).astype(str)
        # if len(self.working_mesh) != 0:
        #     print(len(self.working_mesh))
        #     print(self.working_mesh[0])
        #     for i in range(len(self.working_mesh)):
        #         self.view3d.removeItem(self.working_mesh[i])
        #     self.working_mesh = {}
        # print(check_id)
        # valid_id = list(self.small_mesh_list.keys())
        # # valid_id = np.ravel(valid_id).astype(int)
        # print(valid_id)
        # if len(check_id) != 0:
        #     valid_mesh_count = 0
        #     for id in check_id:
        #         if id in valid_id:
        #             col_to_set = np.ravel(lut[int(id)]) / 255
        #             self.small_mesh_list[id].setColor((col_to_set[0], col_to_set[1], col_to_set[2], 0.3))
        #             self.working_mesh[valid_mesh_count] = self.small_mesh_list[id]
        #             self.view3d.addItem(self.working_mesh[valid_mesh_count])
        #             valid_mesh_count += 1

    # ------------------------------------------------------------------
    #
    #                      Sidebar - Layer Panel
    #
    # ------------------------------------------------------------------
    def remove_single_link_related(self, link_type):
        del_index = np.where(np.ravel(self.layer_ctrl.layer_link) == link_type)[0][0]
        self.layer_ctrl.delete_layer(del_index)
        self.layers_exist_changed(link_type)

    def delete_all_atlas_layer(self):
        if not self.layer_ctrl.layer_link:
            return
        for da_link in self.layer_ctrl.layer_link:
            if 'atlas' not in da_link:
                continue
            da_index = np.where(np.ravel(self.layer_ctrl.layer_link) == da_link)[0][0]
            self.layer_ctrl.delete_layer(da_index)
            self.layers_exist_changed(da_link)
        if self.h2a_transferred:
            self.h2a_transferred = False
            self.tool_box.toa_btn.setIcon(self.tool_box.toa_btn_off_icon)
            self.project_method = 'pre plan'
            self.register_method = 0
            self.tool_box.toh_btn.setEnabled(True)

    def master_layers(self, res, layer_type, color):
        if layer_type not in self.layer_ctrl.layer_link:
            self.layer_ctrl.add_layer(layer_type, color)
            self.layer_ctrl.layer_list[-1].set_thumbnail_data(res)
        else:
            da_ind = np.where(np.ravel(self.layer_ctrl.layer_link) == layer_type)[0][0]
            self.layer_ctrl.layer_list[da_ind].set_thumbnail_data(res)

    def layers_opacity_changed(self, ev):
        da_link = ev[0]
        da_color = ev[1]
        val = ev[2]
        if da_link == 'img-process':
            for i in range(self.image_view.image_file.n_channels):
                self.image_view.img_stacks.image_list[i].setOpts(opacity=val * 0.01)
        elif da_link == 'atlas-slice':
            self.atlas_view.slice_stack.img_layer.setOpts(opacity=val * 0.01)
        else:
            if 'img' in da_link:
                if self.working_img_type[da_link] == 'image':
                    self.image_view.img_stacks.image_dict[da_link].setOpts(opacity=val * 0.01)
                else:
                    self.image_view.img_stacks.image_dict[da_link].setPen((da_color[0], da_color[1], da_color[2],
                                                                           int(val * 255 * 0.01)))
            else:
                if self.working_atlas_type[da_link] == 'image':
                    self.atlas_view.working_atlas.image_dict[da_link].setOpts(opacity=val * 0.01)
                else:
                    self.atlas_view.working_atlas.image_dict[da_link].setPen((da_color[0], da_color[1], da_color[2],
                                                                              int(val * 255 * 0.01)))

    def layers_visible_changed(self, event):
        da_link = event[1]
        vis = event[2]
        if da_link == 'img-process':
            for i in range(self.image_view.image_file.n_channels):
                self.image_view.img_stacks.image_list[i].setVisible(vis)
        elif da_link == 'atlas-slice':
            self.atlas_view.slice_stack.img_layer.setVisible(vis)
        else:
            if 'img' in da_link:
                self.image_view.img_stacks.image_dict[da_link].setVisible(vis)
            else:
                self.atlas_view.working_atlas.image_dict[da_link].setVisible(vis)

    def layers_exist_changed(self, da_link):  # delete
        if da_link == 'img-process':
            self.reset_current_image()
        elif da_link == 'atlas-slice':
            self.reset_atlas_slice()
        else:
            if 'img' in da_link:
                self.image_view.img_stacks.image_dict[da_link].clear()
                if self.working_img_type[da_link] == 'image':
                    self.working_img_data[da_link] = None
                else:
                    self.working_img_data[da_link] = []
                    if 'drawing' in da_link:
                        self.image_view.img_stacks.image_dict[da_link].updateItems()
            else:
                self.atlas_view.working_atlas.image_dict[da_link].clear()
                if self.working_atlas_type[da_link] == 'image':
                    self.working_atlas_data[da_link] = None
                else:
                    self.working_atlas_data[da_link] = []
                    if 'drawing' in da_link:
                        self.atlas_view.working_atlas.image_dict[da_link].updateItems()

            if da_link == 'img-cells':
                for da_key in ['cell_count', 'cell_size', 'cell_symbol', 'cell_layer_index']:
                    self.working_img_data[da_key] = []
                self.working_img_data['cell_count'] = [0 for i in range(5)]
                if self.a2h_transferred or not self.h2a_transferred:
                    for i in range(5):
                        self.tool_box.self.cell_count_val_list[i].setText('0')

            if da_link == 'atlas-cells':
                for da_key in ['cell_count', 'cell_size', 'cell_symbol', 'cell_layer_index']:
                    self.working_atlas_data[da_key] = []
                for i in range(5):
                    self.tool_box.self.cell_count_val_list[i].setText('0')

    def layers_blend_mode_changed(self, ev):
        da_link = ev[0]
        blend_mode = ev[1]
        if blend_mode == 'Plus':
            da_mode = QPainter.CompositionMode_Plus
        elif blend_mode == 'Multiply':
            da_mode = QPainter.CompositionMode_Multiply
        elif blend_mode == 'Overlay':
            da_mode = QPainter.CompositionMode_Overlay
        elif blend_mode == 'SourceOver':
            da_mode = QPainter.CompositionMode_SourceOver
        else:
            return
        if da_link == 'img-process':
            for i in range(self.image_view.image_file.n_channels):
                self.image_view.img_stacks.image_list[i].setCompositionMode(da_mode)
        elif da_link == 'atlas-slice':
            self.atlas_view.slice_stack.img_layer.setCompositionMode(da_mode)
        else:
            if 'img' in da_link:
                if self.working_img_type[da_link] == 'image':
                    self.image_view.img_stacks.image_dict[da_link].setCompositionMode(da_mode)
            else:
                if self.working_atlas_type[da_link] == 'image':
                    self.atlas_view.working_atlas.image_dict[da_link].setCompositionMode(da_mode)

    # ------------------------------------------------------------------
    #
    #              Sidebar - Object Control
    #
    # ------------------------------------------------------------------
    def get_coronal_3d(self, points2):
        da_y = np.ones(len(points2)) * self.atlas_view.current_coronal_index
        points3 = np.vstack([points2[:, 0], da_y, self.atlas_view.atlas_size[0] - points2[:, 1]]).T
        points3 = points3 - self.atlas_view.origin_3d
        if self.atlas_view.coronal_rotated:
            rot_mat = self.atlas_view.c_rotm_3d
            rotation_origin = self.atlas_view.rotate_origin_3d
            points3 = np.dot(rot_mat, (points3 - rotation_origin).T).T + rotation_origin
            print('p3', points3)

        return points3

    def get_sagital_3d(self, points2):
        da_x = np.ones(len(points2)) * self.atlas_view.current_sagital_index
        points3 = np.vstack([da_x, points2[:, 0], self.atlas_view.atlas_size[0] - points2[:, 1]]).T
        points3 = points3 - self.atlas_view.origin_3d
        if self.atlas_view.sagital_rotated:
            rot_mat = self.atlas_view.s_rotm_3d
            rotation_origin = self.atlas_view.rotate_origin_3d
            points3 = np.dot(rot_mat, (points3 - rotation_origin).T).T + rotation_origin
        return points3

    def get_horizontal_3d(self, points2):
        da_z = np.ones(len(points2)) * self.atlas_view.current_horizontal_index
        points3 = np.vstack([points2[:, 1], points2[:, 0], self.atlas_view.atlas_size[0] - da_z]).T
        points3 = points3 - self.atlas_view.origin_3d
        if self.atlas_view.horizontal_rotated:
            rot_mat = self.atlas_view.h_rotm_3d
            rotation_origin = self.atlas_view.rotate_origin_3d
            points3 = np.dot(rot_mat, (points3 - rotation_origin).T).T + rotation_origin
        return points3

    def get_3d_pnts(self, processing_data):
        if self.register_method == 0:
            if self.atlas_display == 'coronal':
                data = self.get_coronal_3d(processing_data)
            elif self.atlas_display == 'sagittal':
                data = self.get_sagital_3d(processing_data)
            else:
                data = self.get_horizontal_3d(processing_data)
        elif self.register_method == 1:
            print('need to be considered later')
            data = None
        else:
            data = processing_data   # ??????????
        return data

    def make_probe_piece(self):
        if self.a2h_transferred:
            data_tobe_registered = self.working_img_data['img-probe']
        else:
            data_tobe_registered = self.working_atlas_data['atlas-probe']
        if data_tobe_registered:
            data_2d = np.asarray(data_tobe_registered)
            data_3d = self.get_3d_pnts(data_2d)
            self.object_ctrl.add_object(object_type='probe - piece', object_data=data_3d)
            self.object_3d_list.append([])
            self.working_atlas_data['atlas-probe'] = []

    def make_virus_piece(self):
        if self.h2a_transferred:
            if not self.working_atlas_data['atlas-virus']:
                return
            processing_pnt = np.asarray(self.working_atlas_data['atlas-virus'])
        else:
            if self.working_img_data['img-virus'] is None:
                return
            inds = np.where(self.working_img_data['img-virus'] != 0)
            processing_pnt = np.vstack([inds[0], inds[1]]).T

        data = self.get_3d_pnts(processing_pnt)
        self.object_ctrl.add_object(object_type='virus - piece', object_data=data)
        self.object_3d_list.append([])
        self.working_atlas_data['atlas-virus'] = []

    def make_contour_piece(self):
        if self.h2a_transferred:
            if not self.working_atlas_data['atlas-contour']:
                return
            processing_pnt = np.asarray(self.working_atlas_data['atlas-contour'])
        else:
            if self.working_img_data['img-contour'] is None:
                return
            inds = np.where(self.working_img_data['img-contour'] != 0)
            processing_pnt = np.vstack([inds[0], inds[1]]).T

        data = self.get_3d_pnts(processing_pnt)
        self.object_ctrl.add_object(object_type='contour - piece', object_data=data)
        self.object_3d_list.append([])
        self.working_atlas_data['atlas-contour'] = []

    def make_drawing_piece(self):
        if self.a2h_transferred:
            data_tobe_registered = self.working_img_data['img-drawing']
        else:
            data_tobe_registered = self.working_atlas_data['atlas-drawing']
        if not data_tobe_registered:
            return
        processing_data = np.asarray(data_tobe_registered)
        data = self.get_3d_pnts(processing_data)
        self.object_ctrl.add_object(object_type='drawing - piece', object_data=data)
        self.object_3d_list.append([])
        self.working_atlas_data['atlas-drawing'] = []

    def make_cell_piece(self):
        if self.a2h_transferred:
            data_tobe_registered = self.working_img_data['img-cells']
        else:
            data_tobe_registered = self.working_atlas_data['atlas-cells']
        if not data_tobe_registered:
            return
        processing_data = np.asarray(data_tobe_registered)
        data = self.get_3d_pnts(processing_data)
        for i in range(5):
            if i == 0:
                object_type = 'cell - piece'
            else:
                object_type = 'cell {} - piece'.format(i)
            if self.working_atlas_data['cell_count'][i] != 0:
                piece_data = data[np.where(np.ravel(self.working_atlas_data['cell_layer_index']) == i)[0], :]
                self.object_ctrl.add_object(object_type=object_type, object_data=piece_data)
                self.object_3d_list.append([])
        self.working_atlas_data['atlas-cells'] = []

    def make_object_pieces(self):
        self.make_probe_piece()
        self.make_virus_piece()
        self.make_cell_piece()
        self.make_drawing_piece()
        self.make_contour_piece()

    def add_3d_probe_lines(self, data_dict):
        pos = np.stack([data_dict['new_insertion_coords_3d'], data_dict['new_terminus_coords_3d']], axis=0)
        vis_color = get_object_vis_color(data_dict['vis_color'])
        probe_line = gl.GLLinePlotItem(pos=pos, color=vis_color, width=2, mode='line_strip')
        probe_line.setGLOptions('opaque')
        self.object_3d_list.append(probe_line)
        self.view3d.addItem(self.object_3d_list[-1])

    def add_3d_drawing_lines(self, data_dict):
        pos = np.asarray(data_dict['data'])
        vis_color = get_object_vis_color(data_dict['vis_color'])
        drawing_line = gl.GLLinePlotItem(pos=pos, color=vis_color, width=2, mode='line_strip')
        drawing_line.setGLOptions('opaque')
        self.object_3d_list.append(drawing_line)
        self.view3d.addItem(self.object_3d_list[-1])

    # probe related functions
    def merge_probes(self):
        if self.object_ctrl.probe_piece_count == 0:
            return
        data = self.object_ctrl.get_merged_data('probe')
        print(data)
        label_data = np.transpose(self.atlas_view.atlas_label, (1, 2, 0))[:, :, ::-1]

        for i in range(len(data)):
            info_dict = calculate_probe_info(data[i], label_data, self.atlas_view.label_info,
                                             self.atlas_view.vox_size_um, self.tip_length, self.channel_size,
                                             self.atlas_view.origin_3d)
            self.object_ctrl.add_object('merged probe', object_data=info_dict)

            self.add_3d_probe_lines(info_dict)

    # virus related functions
    def merge_virus(self):
        if self.object_ctrl.virus_piece_count == 0:
            return
        data = self.object_ctrl.get_merged_data('virus')
        label_data = np.transpose(self.atlas_view.atlas_label, (1, 2, 0))[:, :, ::-1]

        for i in range(len(data)):
            info_dict = calculate_virus_info(data[i], label_data, self.atlas_view.label_info, self.atlas_view.origin_3d)
            self.object_ctrl.add_object('merged virus', object_data=info_dict)

            virus_points = create_plot_points_in_3d(info_dict)
            self.object_3d_list.append(virus_points)
            self.view3d.addItem(self.object_3d_list[-1])

    # cell related functions
    def merge_cells(self):
        if self.object_ctrl.cell_piece_count == 0:
            return
        data = self.object_ctrl.get_merged_data('cell')
        print(data)
        label_data = np.transpose(self.atlas_view.atlas_label, (1, 2, 0))[:, :, ::-1]

        for i in range(len(data)):
            info_dict = calculate_cells_info(data[i], label_data, self.atlas_view.label_info,
                                             self.atlas_view.origin_3d)
            self.object_ctrl.add_object('merged cell', object_data=info_dict)

            cell_points = create_plot_points_in_3d(info_dict)
            self.object_3d_list.append(cell_points)
            self.view3d.addItem(self.object_3d_list[-1])

    # drawing related functions
    def merge_drawings(self):
        if self.object_ctrl.drawing_piece_count == 0:
            return
        data = self.object_ctrl.get_merged_data('drawing')
        # label_data = np.transpose(self.atlas_view.atlas_label, (1, 2, 0))[:, :, ::-1]

        for i in range(len(data)):
            info_dict = {'object_type': 'drawing', 'data': data[i]}
            self.object_ctrl.add_object('merged drawing', object_data=info_dict)
            self.add_3d_drawing_lines(info_dict)

    # contour related functions
    def merge_contour(self):
        if self.object_ctrl.contour_piece_count == 0:
            return
        data = self.object_ctrl.get_merged_data('contour')

        for i in range(len(data)):
            info_dict = {'object_type': 'contour', 'data': data[i]}
            self.object_ctrl.add_object('merged contour', object_data=info_dict)

            contour_points = create_plot_points_in_3d(info_dict)
            self.object_3d_list.append(contour_points)
            self.view3d.addItem(self.object_3d_list[-1])

    # common functions
    def obj_color_changed(self, ev):
        clicked_index = ev[0]
        color = ev[1]
        self.object_ctrl.obj_data[clicked_index]['vis_color'] = color
        vis_color = get_object_vis_color(color)
        self.object_3d_list[clicked_index].setData(color=vis_color)

    def obj_opacity_changed(self, val):
        col = self.object_ctrl.obj_data[self.object_ctrl.current_obj_index]['vis_color']
        vis_color = (col[0] / 255, col[1] / 255, col[2] / 255, val / 100)
        self.object_3d_list[self.object_ctrl.current_obj_index].setData(color=vis_color)

    def obj_blend_mode_changed(self, blend_mode):
        self.object_3d_list[self.object_ctrl.current_obj_index].setGLOptions(blend_mode)

    def obj_vis_changed(self, ev):
        clicked_index = ev[0]
        vis = ev[1]
        self.object_3d_list[clicked_index].setVisible(vis)

    def object_deleted(self, ind):
        if not isinstance(self.object_3d_list[ind], list):
            self.view3d.removeItem(self.object_3d_list[ind])
            self.object_3d_list[ind].deleteLater()
        del self.object_3d_list[ind]

    def obj_size_changed(self, ev):
        obj_type = ev[0]
        val = ev[1]
        if 'probe' in obj_type or 'drawing' in obj_type:
            self.object_3d_list[self.object_ctrl.current_obj_index].setData(width=val)
        else:
            self.object_3d_list[self.object_ctrl.current_obj_index].setData(size=val)

    # ------------------------------------------------------------------
    #
    #                       Image Loader
    #
    # ------------------------------------------------------------------
    def load_image(self):
        self.print_message('Load Image ...', self.normal_color, 0)
        file_title = "Select Histological Image File"
        file_filter = "CZI (*.czi);;JPEG (*.jpg);;PNG (*.png);;TIFF (*.tif);;BMP (*.bmp)"
        if self.current_img_path is None:
            file_path = str(Path.home())
        else:
            file_path = self.current_img_path
        file_options = QFileDialog.Options()
        file_options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        image_file_path = file_dialog.getOpenFileName(self, file_title, file_path, file_filter, options=file_options)

        if image_file_path[0] != '':

            image_file_type = image_file_path[0][-4:].lower()
            self.current_img_path = image_file_path[0]
            self.current_img_name = os.path.basename(os.path.realpath(image_file_path[0]))
            self.load_single_image_file(self.current_img_path, image_file_type)
            # change sidebar focus
            self.sidebar.setCurrentIndex(2)
            if self.atlas_view.atlas_data is None:
                self.show_only_image_window()
            else:
                self.show_2_windows()
        else:
            if self.image_view.image_file is None:
                self.statusbar.showMessage('No image file is selected.')
            else:
                self.statusbar.showMessage('No new image file is selected.')
            return

    def load_single_image_file(self, image_file_path, image_file_type):
        with pg.BusyCursor():
            with warnings.catch_warnings():
                warnings.filterwarnings("error")
                if image_file_type == '.czi':
                    image_file = CZIReader(image_file_path)
                    scale = self.image_view.scale_slider.value()
                    scale = 0.01 if scale == 0 else scale * 0.01
                    if self.image_view.check_scenes.isChecked():
                        image_file.read_data(scale, scene_index=None)
                    else:
                        image_file.read_data(scale, scene_index=0)
                    if image_file.is_rgb:
                        self.tool_box.cell_count_label_list[0].setVisible(True)
                        self.tool_box.cell_count_val_list[0].setVisible(True)
                    else:
                        for i in range(image_file.n_channels):
                            self.tool_box.cell_count_label_list[i + 1].setVisible(True)
                            self.tool_box.cell_count_val_list[i + 1].setVisible(True)
                else:
                    image_file = ImageReader(image_file_path)
                    self.tool_box.cell_count_label_list[0].setVisible(True)
                    self.tool_box.cell_count_val_list[0].setVisible(True)
            self.image_view.set_data(image_file)
            self.reset_corners_hist()
        self.layerpanel.setEnabled(True)
        self.statusbar.showMessage('Image file loaded.')

    # load multiple images
    def load_images(self):
        self.statusbar.showMessage('Selecte folder to load multiple images, files can not be .czi format ...')
        images_folder = str(QFileDialog.getExistingDirectory(self, "Select Images Folder"))
        if images_folder != '':
            # image_files_list = os.listdir(images_folder)
            # image_files_list = natsorted(image_files_list)

            with pg.BusyCursor():
                with warnings.catch_warnings():
                    warnings.filterwarnings("error")
                    image_file = ImagesReader(images_folder)
                    self.image_view.set_data(image_file)

            self.sidebar.setCurrentIndex(3)
            self.statusbar.showMessage('Image files loaded.')
        else:
            return

    # ------------------------------------------------------------------
    #
    #              Menu Bar ---- File ----- related
    #
    # ------------------------------------------------------------------
    def load_volume_atlas(self, atlas_folder):
        self.atlascontrolpanel.setEnabled(True)
        self.treeviewpanel.setEnabled(True)
        self.actionSwitch_Atlas.setText('Switch Atlas: Volume')
        self.current_atlas = 'volume'
        self.actionBregma_Picker.setEnabled(False)
        self.actionCreate_Slice_Layer.setEnabled(False)
        self.atlas_folder = atlas_folder

        if self.atlas_view.atlas_data is not None:
            self.delete_all_atlas_layer()


        with pg.BusyCursor():
            da_atlas = AtlasLoader(atlas_folder)

        if not da_atlas.success:
            # self.print_message(da_atlas.msg)
            self.statusbar.showMessage(da_atlas.msg)
            return
        else:
            self.print_message('Atlas loaded successfully.', self.normal_color, 0.1)

        atlas_data = np.transpose(da_atlas.atlas_data, [2, 0, 1])[::-1, :, :]
        segmentation_data = np.transpose(da_atlas.segmentation_data, [2, 0, 1])[::-1, :, :]

        s_boundary = np.transpose(da_atlas.boundary['s_contour'], [2, 0, 1])[::-1, :, :]
        c_boundary = np.transpose(da_atlas.boundary['c_contour'], [2, 0, 1])[::-1, :, :]
        h_boundary = np.transpose(da_atlas.boundary['h_contour'], [2, 0, 1])[::-1, :, :]

        boundary = {'s_contour': s_boundary, 'c_contour': c_boundary, 'h_contour': h_boundary}

        self.atlas_view.set_data(atlas_data, segmentation_data, da_atlas.atlas_info,
                                 da_atlas.label_info, boundary)
        self.atlas_view.working_cut_changed(self.atlas_display)
        self.reset_corners_atlas()

        if self.image_view.image_file is None:
            if self.atlas_display == 'coronal':
                self.show_only_coronal_window()
            elif self.atlas_display == 'sagittal':
                self.show_only_sagital_window()
            else:
                self.show_only_horizontal_window()
        else:
            self.show_2_windows()

        msg = 'Successfully set atlas data to view. Checking rendering for 3D visualisation...'
        self.print_message(msg, self.normal_color, 0.1)

        # load mesh data
        pre_made_meshdata_path = os.path.join(atlas_folder, 'atlas_meshdata.pkl')
        pre_made_small_meshdata_path = os.path.join(atlas_folder, 'atlas_small_meshdata.pkl')

        if not os.path.exists(pre_made_meshdata_path) or not os.path.exists(pre_made_small_meshdata_path):
            msg = 'Brain mesh is not found! Please pre-process the atlas.'
            self.print_message(msg, self.error_message_color, 0)

        try:
            infile = open(pre_made_meshdata_path, 'rb')
            self.meshdata = pickle.load(infile)
            infile.close()
        except ValueError:
            msg = 'Please pre-process mesh for the whole brain.'
            self.print_message(msg, self.error_message_color, 0)
            return

        self.atlas_view.mesh.setMeshData(meshdata=self.meshdata)
        self.mesh_origin = np.ravel(da_atlas.atlas_info[3]['Bregma'])
        self.atlas_view.mesh.translate(-self.mesh_origin[0], -self.mesh_origin[1], -self.mesh_origin[2])

        self.print_message('Brain mesh is Loaded.', self.normal_color, 0)

        return

        try:
            infile = open(pre_made_small_meshdata_path, 'rb')
            self.small_meshdata_list = pickle.load(infile)
            infile.close()
        except ValueError:
            self.statusbar.showMessage('Please re-process meshes for each brain region.')
            return

        for id in np.unique(da_atlas.segmentation_data):
            id = int(id)
            if id == 0:
                continue
            if id in self.atlas_view.label_info['index']:
                color_to_set = self.atlas_view.label_info['color'][(self.atlas_view.label_info['index'] == id)][0] / 255
                mesh = gl.GLMeshItem(meshdata=self.small_meshdata_list[str(id)], smooth=True,
                                     color=(color_to_set[0], color_to_set[1], color_to_set[2], 0.8), shader='balloon')
                mesh.setGLOptions('opaque')
                mesh.translate(-self.mesh_origin[0], -self.mesh_origin[1], -self.mesh_origin[2])
                # mesh.setVisible(False)
                self.small_mesh_list[str(id)] = mesh
                self.small_mesh_list[str(id)].setVisible(False)

        mesh_keys = list(self.small_mesh_list.keys())
        for i in range(len(self.small_mesh_list)):
            self.view3d.addItem(self.small_mesh_list[mesh_keys[i]])

        self.sidebar.setCurrentIndex(0)

        self.statusbar.showMessage('Brain region mesh is Loaded.  Atlas loaded successfully.')

    # ------------------------------------------------------------------
    #
    #                       Atlas Loader
    #
    # ------------------------------------------------------------------
    def load_atlas_clicked(self):
        self.print_message('Loading Brain Atlas...', self.normal_color, 0.1)

        atlas_folder = str(QFileDialog.getExistingDirectory(self, "Select Atlas Folder"))
        with open('data/atlas_path.txt', 'w') as f:
            f.write(atlas_folder)

        if atlas_folder != '':
            self.load_volume_atlas(atlas_folder)
        else:
            if self.atlas_view.atlas_data is not None:
                self.statusbar.showMessage('No new atlas is selected.')
            else:
                self.statusbar.showMessage('No valid path for atlas.')

    def load_previous_atlas(self):
        self.print_message('Loading Brain Atlas...', self.normal_color, 0.1)

        if os.path.exists('data/atlas_path.txt'):
            with open('data/atlas_path.txt') as f:
                lines = f.readlines()
            atlas_folder = lines[0]
            if not os.path.exists(atlas_folder):
                atlas_folder = str(QFileDialog.getExistingDirectory(self, "Select Atlas Folder"))
                with open('data/atlas_path.txt', 'w') as f:
                    f.write(atlas_folder)
        else:
            atlas_folder = str(QFileDialog.getExistingDirectory(self, "Select Atlas Folder"))
            with open('data/atlas_path.txt', 'w') as f:
                f.write(atlas_folder)

        if atlas_folder != '':
            self.load_volume_atlas(atlas_folder)
        else:
            if self.atlas_view.atlas_data is not None:
                self.statusbar.showMessage('No new atlas is selected.')
            else:
                self.statusbar.showMessage('No valid path for atlas.')


    def save_image(self, image_type):
        if image_type == 'Processed':
            da_img = self.processing_img
        elif image_type == 'Overlay':
            if self.h2a_transferred:
                da_img = self.working_atlas_data['atlas-overlay']
            if self.a2h_transferred:
                da_img = self.working_atlas_data['img-overlay']
        else:
            da_img = self.working_img_data['img-mask']
        if da_img is None:
            self.print_message('No required {} image is created.'.format(image_type), self.error_message_color, 0.1)
            return
        if image_type in ['Processed', 'Overlay']:
            da_img = cv2.cvtColor(da_img, cv2.COLOR_RGB2BGR)
        self.print_message('Save {} Image ...'.format(image_type), 'white', 0.1)
        path = QFileDialog.getSaveFileName(self, "Save Image", self.current_img_path, "JPEG (*.jpg)")
        if path[0] != '':
            cv2.imwrite(path[0], da_img)
            self.print_message('{} Image is saved successfully ...'.format(image_type), 'white', 0.1)
        else:
            self.print_message('No file name is given to save.', self.error_message_color, 0.1)

    # save merged object
    def save_merged_object(self, object_type):
        if not self.object_ctrl.obj_list:
            self.print_message('No object is created ...', 'gray', 0)
            return

        otype = self.object_ctrl.obj_type
        valid_index = [ind for ind in range(len(otype)) if object_type in otype[ind] and 'merged' in otype[ind]]

        if not valid_index:
            self.print_message('No merged object is created ...', 'gray', 0)
            return

        save_path = str(QFileDialog.getExistingDirectory(self, "Select Folder to Save Objects"))
        if save_path != '':
            self.print_message('Saving {} objects ...'.format(object_type), 'white', 0.1)
            for da_ind in valid_index:
                data = {'type': self.object_ctrl.obj_type[da_ind],
                        'data': self.object_ctrl.obj_data[da_ind],
                        'widget3d': self.object_3d_list[da_ind]}
                s_name = self.object_ctrl.obj_name[da_ind]
                s_path = os.path.join(save_path, s_name)
                with open('{}.pkl'.format(s_path), 'wb') as handle:
                    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            return

    def save_current_object(self):
        if self.object_ctrl.current_obj_index is None:
            self.statusbar.showMessage('No object is created ...')
            return
        file_name = QFileDialog.getSaveFileName(self, 'Save Current Object File', self.current_img_path, "Pickle File (*.pkl)")
        if file_name[0] != '':
            if 'merged' not in self.object_ctrl.obj_type[self.object_ctrl.current_obj_index]:
                self.statusbar.showMessage('Only merged object can be saved ...')
                return
            da_data = self.object_ctrl.obj_data[self.object_ctrl.current_obj_index]
            with open(file_name[0], 'wb') as handle:
                pickle.dump(da_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            self.statusbar.showMessage('Current merged object is saved successfully.')

    # load object
    def load_object(self):
        if self.atlas_view.atlas_data is None:
            self.print_message('Atlas need to be loaded first.', 'gray', 0)
            return
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        object_file_path = dlg.getOpenFileNames(self, "Load Object Files", str(Path.home()), "Pickle File (*.pkl)")

        if object_file_path[0]:
            n_files = len(object_file_path[0])
            for i in range(n_files):
                infile = open(object_file_path[0][i], 'rb')
                object_dict = pickle.load(infile)
                infile.close()

                self.object_ctrl.add_object(object_dict['type'], object_data=object_dict['data'])
                self.object_3d_list.append(object_dict['widget3d'])
                self.view3d.addItem(self.object_3d_list[-1])
            self.print_message('Objects loaded successfully.', 'white', 0)

    def save_project(self):
        if self.overlay_img is None:
            msg = 'Project can be saved only after that histological image and atlas are matched.'
            self.print_message(msg, self.reminder_color, 0)
            return
        self.statusbar.showMessage('Saving Project ...')

        file_name = QFileDialog.getSaveFileName(self, 'Save Project')
        if file_name != '':
            img_ctrl_data = self.image_view.get_image_control_data()

            object_data = self.object_ctrl.get_obj_data()
            object_data['object_3d_list'] = self.object_3d_list

            layer_data = self.layer_ctrl.get_layer_data()

            setting_data = self.get_setting_data()

            if self.current_atlas == 'slice':
                atlas_ctrl_data = {'data': self.atlas_view.slice_image_data,
                                   'slice_cut': self.slice_cut,
                                   'slice_width': self.slice_width,
                                   'slice_height': self.slice_height,
                                   'slice_distance': self.slice_distance,
                                   'slice_bregma': self.slice_bregma}
            else:
                atlas_rotation = self.atlas_view.get_atlas_angles()
                atlas_ctrl_data = {'atlas_display': self.atlas_display,
                                   'coronal_index': self.atlas_view.current_coronal_index,
                                   'sagittal_index': self.atlas_view.current_sagital_index,
                                   'horizontal_index': self.atlas_view.current_horizontal_index,
                                   'slice_rotation': atlas_rotation}

            project_data = {'current_atlas': self.current_atlas,
                            'atlas_ctrl_data': atlas_ctrl_data,
                            'current_img_name': self.current_img_name,
                            'img_ctrl_data': img_ctrl_data,
                            'layers': layer_data,
                            'objects': object_data,
                            'setting_data': setting_data,
                            'probe_type': self.probe_type,
                            'is_project_data': True}

            with open(file_name[0], 'wb') as handle:
                pickle.dump(project_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            self.print_message('Project saved successfully.', 'white', 0)

    def get_setting_data(self):
        data = {'np_onside': self.np_onside,
                'atlas_rect': self.atlas_rect,
                'histo_rect': self.histo_rect,
                'small_atlas_rect': self.small_atlas_rect,
                'small_histo_rect': self.small_histo_rect,
                'atlas_corner_points': self.atlas_corner_points,
                'atlas_side_lines': self.atlas_side_lines,
                'atlas_tri_data': self.atlas_tri_data,
                'atlas_tri_inside_data': self.atlas_tri_inside_data,
                'atlas_tri_onside_data': self.atlas_tri_onside_data,
                'histo_corner_points': self.histo_corner_points,
                'histo_side_lines': self.histo_side_lines,
                'histo_tri_data': self.histo_tri_data,
                'histo_tri_inside_data': self.histo_tri_inside_data,
                'histo_tri_onside_data': self.histo_tri_onside_data,
                'working_img_text': self.working_img_text,
                'working_atlas_text': self.working_atlas_text,
                'a2h_transferred': self.a2h_transferred,
                'h2a_transferred': self.h2a_transferred,
                'project_method': self.project_method,
                'register_method': self.register_method,
                'processed_img': self.processing_img,
                'overlay_img': self.overlay_img,
                'working_img_data': self.working_img_data,
                'working_atlas_data': self.working_atlas_data,
                'drawing_is_closed': self.tool_box.is_closed}
        return data

    # load project
    def load_project(self):
        if self.atlas_view.atlas_data is None and self.atlas_view.slice_image_data is None:
            self.print_message('Please upload atlas first.', self.reminder_color, 0.1)
            return

        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.ExistingFiles)
        project_path = dlg.getOpenFileName(self, "Load Project", str(Path.home()), "Pickle File (*.pkl)")

        if project_path[0] != '':
            infile = open(project_path[0], 'rb')
            project_dict = pickle.load(infile)
            infile.close()

            if 'is_project_data' not in list(project_dict.keys()):
                self.print_message('Loaded data is not a project data !!!', self.error_message_color, 0.1)
                return

            self.current_atlas = project_dict['current_atlas']
            atlas_ctrl_data = project_dict['atlas_ctrl_data']
            img_data = atlas_ctrl_data['data']
            if img_data is not None:
                self.atlas_view.set_slice_data(img_data)
            self.slice_cut = atlas_ctrl_data['slice_cut']
            self.slice_width = atlas_ctrl_data['slice_width']
            self.slice_height = atlas_ctrl_data['slice_height']
            self.slice_distance = atlas_ctrl_data['slice_distance']
            self.slice_bregma = atlas_ctrl_data['slice_bregma']
            if self.current_atlas == 'slice':
                self.actionSwitch_Atlas.setText('Switch Atlas: Slice')
                self.atlascontrolpanel.setEnabled(False)
                self.treeviewpanel.setEnabled(False)
                self.actionBregma_Picker.setEnabled(True)
                self.actionCreate_Slice_Layer.setEnabled(True)
            else:
                if self.atlas_view.atlas_data is None:
                    msg = 'Please load {} atlas for the loaded project.'.format(project_dict['atlas_type'])
                    self.print_message(msg, self.error_message_color, 0.1)
                # load volume atlas related
                if atlas_ctrl_data['atlas_display'] == 'coronal':
                    self.atlas_view.section_rabnt1.setChecked(True)
                elif atlas_ctrl_data['atlas_display'] == 'sagittal':
                    self.atlas_view.section_rabnt2.setChecked(True)
                else:
                    self.atlas_view.section_rabnt3.setChecked(True)
                self.atlas_view.cpage_ctrl.page_slider.setValue(atlas_ctrl_data['coronal_index'])
                self.atlas_view.spage_ctrl.page_slider.setValue(atlas_ctrl_data['sagittal_index'])
                self.atlas_view.hpage_ctrl.page_slider.setValue(atlas_ctrl_data['horizontal_index'])
                atlas_rotation = atlas_ctrl_data['atlas_rotation']
                self.atlas_view.crotation_ctrl.h_spinbox.setValue(atlas_rotation[0][0])
                self.atlas_view.crotation_ctrl.v_spinbox.setValue(atlas_rotation[0][1])
                self.atlas_view.srotation_ctrl.h_spinbox.setValue(atlas_rotation[1][0])
                self.atlas_view.srotation_ctrl.v_spinbox.setValue(atlas_rotation[1][1])
                self.atlas_view.hrotation_ctrl.h_spinbox.setValue(atlas_rotation[2][0])
                self.atlas_view.hrotation_ctrl.v_spinbox.setValue(atlas_rotation[2][1])

            self.current_img_name = project_dict['current_img_name']
            img_ctrl_data = project_dict['img_ctrl_data']
            self.image_view.corner_points = img_ctrl_data['corner_points']
            self.image_view.side_lines = img_ctrl_data['side_lines']
            self.image_view.scene_slider.setValue(img_ctrl_data['scene_index'])
            self.image_view.scale_slider.setValue(img_ctrl_data['scale_val'])
            image_file = project_dict['image_file']
            self.image_view.set_data(image_file)

            self.image_view.current_img = img_ctrl_data['current_img'].copy()
            self.image_view.channel_color = img_ctrl_data['channel_color']
            self.image_view.set_data_to_img_stacks()
            for i in range(4):
                if self.image_view.channel_color[i] is not None:
                    self.image_view.channel_color_changed(self.image_view.channel_color[i], i)

            self.probe_type = project_dict['probe_type']
            self.probe_type_changed(self.probe_type)

            setting_data = project_dict['setting_data']
            self.np_onside = setting_data['np_onside']
            self.atlas_rect = setting_data['atlas_rect']
            self.histo_rect = setting_data['histo_rect']
            self.small_atlas_rect = setting_data['small_atlas_rect']
            self.small_histo_rect = setting_data['small_histo_rect']
            self.atlas_corner_points = setting_data['atlas_corner_points']
            self.atlas_side_lines = setting_data['atlas_side_lines']
            self.atlas_tri_data = setting_data['atlas_tri_data']
            self.atlas_tri_inside_data = setting_data['atlas_tri_inside_data']
            self.atlas_tri_onside_data = setting_data['atlas_tri_onside_data']
            self.histo_corner_points = setting_data['histo_corner_points']
            self.histo_side_lines = setting_data['histo_side_lines']
            self.histo_tri_data = setting_data['histo_tri_data']
            self.histo_tri_inside_data = setting_data['histo_tri_inside_data']
            self.histo_tri_onside_data = setting_data['histo_tri_onside_data']
            self.working_img_text = setting_data['working_img_text']
            self.working_atlas_text = setting_data['working_atlas_text']
            self.a2h_transferred = setting_data['a2h_transferred']
            self.h2a_transferred = setting_data['h2a_transferred']
            self.project_method = setting_data['project_method']
            self.register_method = setting_data['register_method']
            self.processing_img = setting_data['processed_img']
            self.overlay_img = setting_data['overlay_img']
            self.working_img_data = setting_data['working_img_data']
            self.working_atlas_data = setting_data['working_atlas_data']

            self.tool_box.is_closed = setting_data['drawing_is_closed']

            if self.tool_box.is_closed:
                self.tool_box.pencil_path_btn.setChecked(True)
            else:
                self.tool_box.pencil_path_btn.setChecked(False)

            self.tool_box.bound_pnts_num.setText(str(self.np_onside))

            layer_data = project_dict['layers']
            self.layer_ctrl.set_layer_data(layer_data)

            for da_link in self.layer_ctrl.layer_link:
                if 'img' in da_link:
                    if da_link == 'img-process':
                        self.processing_img = self.working_img_data[da_link]
                        self.image_view.img_stacks.set_data(self.processing_img)
                    elif da_link in ['img-overlay', 'img-mask', 'img-virus']:
                        self.image_view.img_stacks.image_dict[da_link].setImage(self.working_img_data[da_link])
                    elif da_link in ['img-drawing', 'img-contour']:
                        self.image_view.img_stacks.image_dict[da_link].setData(
                            np.asarray(self.working_img_data[da_link]))
                    elif da_link == 'img-cells':
                        self.image_view.img_stacks.image_dict[da_link].setData(
                            pos=np.asarray(self.working_img_data[da_link]), symbol=self.working_img_data['cell_symbol'])
                    else:
                        self.image_view.img_stacks.image_dict[da_link].setData(
                            pos=np.asarray(self.working_img_data[da_link]))
                elif 'atlas' in da_link:
                    if da_link == 'atlas-slice':
                        self.atlas_view.slice_stack.set_data(self.working_atlas_data[da_link])
                    elif da_link == 'atlas-mask':
                        self.atlas_view.working_atlas.image_dict[da_link].setImage(self.working_atlas_data[da_link])
                    elif da_link == 'atlas-cells':
                        self.atlas_view.working_atlas.image_dict[da_link].setData(
                            pos=np.asarray(self.working_atlas_data[da_link]),
                            symbol=self.working_atlas_data['cell_symbol'])
                    elif da_link == 'atlas-drawing':
                        if self.tool_box.is_closed:
                            self.set_atlas_pencil_closed_style()
                        else:
                            self.clear_atlas_pencil_closed_style()
                        self.atlas_view.working_atlas.image_dict[da_link].setData(
                            np.asarray(self.working_atlas_data[da_link]))
                    elif da_link == 'atlas-contour':
                        self.atlas_view.working_atlas.image_dict[da_link].setData(
                            np.asarray(self.working_atlas_data[da_link]))
                    else:
                        self.atlas_view.working_atlas.image_dict[da_link].setData(
                            pos=np.asarray(self.working_atlas_data[da_link]))
                else:
                    return





            obj_data = project_dict['objects']
            self.object_ctrl.set_layer_data(obj_data)
            self.object_3d_list = obj_data['object_3d_list']
            for i in range(len(self.object_3d_list)):
                self.view3d.addItem(self.object_3d_list[i])



    # status
    def print_message(self, msg, col, sec):
        self.statusbar.setStyleSheet(get_statusbar_style(col))
        self.statusbar.showMessage('  ' + msg)
        time.sleep(sec)


def main():
    app = QApplication(argv)
    app.setStyleSheet(herbs_style)
    print(sys.flags.interactive)  # 0
    print(hasattr(QtCore, 'PYQT_VERSION'))
    # if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #     app.instance().exec_()
    window = HERBS()
    window.show()
    exit(app.exec_())








