#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math
import os
import sys

from PyQt5.QtCore import Qt, QSize, pyqtSignal, QPoint, QRegExp, QModelIndex, QTimer
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import *


PICTURES_FOLDER = 'Pictures'

FACILITIES = {
    '制造台': '制造台MK.II',
    '采矿机': '采矿机',
    '冶炼设备': '电弧熔炉',
    '抽水站': '抽水站',
    '原油萃取站': '原油萃取站',
    '化工设备': '化工厂',
    '精炼设备': '原油精炼厂',
    '分馏塔': '分馏塔',
    '粒子对撞机': '微型粒子对撞机',
    '科研设备': '矩阵研究站'
}

STYLE_SHEET = '''
    * {
        font-family: Microsoft YaHei;
    }
    MainWindow {
        background-color: #222C3C;
    }
    MPushButton, MTipsButton, RequirementTableItem {
        border: 0px;
    }
    TopButton:hover {
        border-radius: 5px;
        background-color: #33435b;
    }
    ThingsTableItem {
        border: 1px solid #030404;
        background-color: #162226;
    }
    ThingsTableWindow {
        gridline-color: #030404;
        background-color: #030404; 
        border: 1px solid #030404;
    }
    FormulaWidget, FacilityPowerWidget {
        background-color: transparent;
    }
    ThingTooltipWindow {
        border: 1px solid #415E68;
        border-radius: 5px;
        padding: 10px 10px 10px 10px;
        background-color: #101D27;
    }
    QLineEdit {
        border: 1px solid #415E68;
        border-radius: 4px;
        background-color: transparent;
        color: #557b88;
    }
    QLineEdit:hover {
        border: 1px solid #557b88;
    }
    QGroupBox {
        border: 1px solid #585858;
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 10px;
    }
    QGroupBox::title {
        color: #989898;
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 10px;
    }
    QComboBox {
        border: 1px solid #415E68;
        border-radius: 4px;
        background-color: transparent;
        color: #557b88;
    }
    FormulaSelectWidget {
        min-width: 100px;
        min-height: 50px;
    }
    QComboBox:hover {
        border: 1px solid #557b88;
    }
    QComboBox QAbstractItemView {
        border: 1px solid #415E68;
        background-color: #222C3C;
        color: #557b88;
        selection-background-color: #133555;
        selection-color: #557b88;
    }
    FormulaListWidget {
        border: 1px solid #415E68; 
        background-color: #222C3C;
    }
    RequirementTableWidget {
        border: 1px solid #415E68;
        border-radius: 5px;
        gridline-color: #415E68; 
    }
    SettingsWidget, RequirementTableItem, RequirementTableWidget, RequirementPowerWidget {
        background-color: transparent;
    }
    CalculateWindow {
        background-color: #222C3C;
    }
    QHeaderView::section {
        border: none; 
        background-color: #415E68;
        color: #989898
    }
    QScrollBar {
        background-color: transparent;
        border-radius: 5px;
        padding: 1px;
        height: 10px;
        width: 10px;
    }
    QScrollBar::handle {
        border-radius: 3px;
        background: #686868;
        min-width: 16px;
        min-height: 16px;
    }
    QScrollBar::handle:hover {
        background: #989898;
    }
    QScrollBar::add-line, QScrollBar::sub-line,
    QScrollBar::add-page, QScrollBar::sub-page {
        width: 0px;
        background: transparent;
    }
'''


class MainWindow(QWidget):
    inst = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)  # 窗体大小固定
        self.setWindowIcon(QIcon('Logo.png'))
        self.things_mgr = ThingsMgr.create_inst()
        self.product_mgr = ProductMgr.create_inst()
        self.btn_component = TopButton(self, '物品.png')
        self.btn_building = TopButton(self, '建筑.png')
        self.btn_other = TopButton(self, '杂项.png')
        self.wnd_components = ThingsTableWindow(self)
        self.wnd_buildings = ThingsTableWindow(self)
        self.wnd_others = ThingsTableWindow(self)

        self.hbl_button = QHBoxLayout()
        self.hbl_button.addWidget(self.btn_component)
        self.hbl_button.addWidget(self.btn_building)
        self.hbl_button.addWidget(self.btn_other)
        self.hbl_button.addStretch(1)

        self.vbl_main = QVBoxLayout()
        self.vbl_main.addLayout(self.hbl_button)
        self.vbl_main.addWidget(self.wnd_components)
        self.vbl_main.addWidget(self.wnd_buildings)
        self.vbl_main.addWidget(self.wnd_others)
        self.vbl_main.setContentsMargins(0, 0, 0, 0)

        self.hbl_main = QHBoxLayout(self)
        self.hbl_main.addLayout(self.vbl_main)
        self.hbl_main.setContentsMargins(20, 10, 20, 20)
        self.wnd_buildings.setVisible(False)
        self.wnd_others.setVisible(False)
        self.setFixedSize(self.hbl_main.sizeHint())

        self.init_things_window()
        self.show_components()
        self.btn_component.clicked.connect(self.show_components)
        self.btn_building.clicked.connect(self.show_buildings)
        self.btn_other.clicked.connect(self.show_others)

    def init_things_window(self):
        self.wnd_components.show_items(self.things_mgr.components())
        self.wnd_buildings.show_items(self.things_mgr.buildings())
        self.wnd_others.show_items(self.things_mgr.others())

    def show_components(self):
        self.wnd_components.setVisible(True)
        self.wnd_buildings.setVisible(False)
        self.wnd_others.setVisible(False)

    def show_buildings(self):
        self.wnd_components.setVisible(False)
        self.wnd_buildings.setVisible(True)
        self.wnd_others.setVisible(False)

    def show_others(self):
        self.wnd_components.setVisible(False)
        self.wnd_buildings.setVisible(False)
        self.wnd_others.setVisible(True)

    def closeEvent(self, event):
        sys.exit()

    @classmethod
    def create_inst(cls):
        if cls.inst is None:
            cls.inst = cls()
        return cls.inst


class MPushButton(QPushButton):
    def __init__(self, parent=None):
        super(MPushButton, self).__init__(parent)

    def set_icon(self, picture):
        self.setIcon(QIcon(os.path.join(PICTURES_FOLDER, picture or '')))


class MTipsButton(QPushButton):
    def __init__(self, parent=None):
        super(MTipsButton, self).__init__(parent)
        self.name = None
        self.count = None
        self.clicked.connect(ThingTooltipWindow.inst.on_hide)

    def set_name(self, name):
        self.name = name

    def set_count(self, count):
        self.count = count

    def set_icon(self, picture):
        self.setIcon(QIcon(os.path.join(PICTURES_FOLDER, picture or '')))

    def enterEvent(self, event):
        x = event.globalPos().x() - event.localPos().x() + self.width() / 2
        y = event.globalPos().y() - event.localPos().y() + self.height() + 5
        ThingTooltipWindow.inst.delay_show(self.name, QPoint(int(x), int(y)), self.count)

    def leaveEvent(self, event):
        ThingTooltipWindow.inst.on_hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.right_pressed = True
        super(MTipsButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self.right_pressed:
            x = event.globalPos().x() - event.localPos().x() + self.width() / 2
            y = event.globalPos().y() - event.localPos().y() + self.height() + 5
            ThingTooltipWindow.inst.show_relevant_formula(self.name, QPoint(x, y))
        self.right_pressed = False
        super(MTipsButton, self).mouseReleaseEvent(event)


class MTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(MTableWidget, self).__init__(parent)
        self.setShowGrid(False)
        self.horizontalHeader().setVisible(False)  # 行列表头不显示
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionsClickable(False)  # 表头不可点击
        self.verticalHeader().setSectionsClickable(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # 自动大小
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑
        self.setSelectionMode(QAbstractItemView.NoSelection)  # 不可选中
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

    def set_min_section(self, size):
        self.horizontalHeader().setMinimumSectionSize(size.width())
        self.verticalHeader().setMinimumSectionSize(size.height())


class MHLine1(QFrame):
    line_style = '''
        QFrame {
            border-top: 1px solid #0B151D;
            border-bottom: 1px solid #182C3B;
            border-left: none;
            border-right: none;
        }
    '''

    def __init__(self, parent=None):
        super(MHLine1, self).__init__(parent)
        self.setStyleSheet(self.line_style)
        self.setFrameShadow(QFrame.Plain)
        self.setFrameShape(QFrame.HLine)


class MHLine2(QFrame):
    line_style = '''
        QFrame {
            border-top: 1px solid #1C2532;
            border-bottom: 1px solid #303F55;
            border-left: none;
            border-right: none;
        }
    '''

    def __init__(self, parent=None):
        super(MHLine2, self).__init__(parent)
        self.setStyleSheet(self.line_style)
        self.setFrameShadow(QFrame.Plain)
        self.setFrameShape(QFrame.HLine)


class TopButton(MPushButton):
    size = QSize(70, 70)
    image_size = QSize(60, 60)

    def __init__(self, parent=None, picture=None):
        super(TopButton, self).__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        self.set_icon(picture)


class ThingsTableItem(MTipsButton):
    size = QSize(60, 60)
    image_size = QSize(50, 50)

    def __init__(self, name=None, picture=None, parent=None):
        super(ThingsTableItem, self).__init__(parent)
        self.name = name
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        if picture:
            self.set_icon(picture)
        self.clicked.connect(self.open_calculation)

    def open_calculation(self):
        if self.name:
            CalculateWindow.new_window(self.name)


class ThingsTableWindow(MTableWidget):
    def __init__(self, parent=None):
        super(ThingsTableWindow, self).__init__(parent)
        self.set_min_section(ThingsTableItem.size)
        self.init_items()

    def init_items(self):
        self.setRowCount(8)
        self.setColumnCount(14)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = ThingsTableItem()
                self.setCellWidget(row, col, item)
        self.horizontalHeader().resizeSections()
        self.resize(self.sizeHint())

    def clear_items(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.cellWidget(row, col)
                item.set_icon(None)
                item.set_name(None)
                item.setCursor(Qt.ArrowCursor)

    def show_items(self, data):
        for name, it in data.items():
            if it['row'] >= 0 and it['col'] >= 0:
                item = self.cellWidget(it['row'], it['col'])
                item.set_name(name)
                item.set_icon(it['icon'])
                item.setCursor(Qt.PointingHandCursor)


class FormulaListWidget(QListWidget):
    def __init__(self, parent=None):
        super(FormulaListWidget, self).__init__(parent)

    def add_formulas(self, formulas):
        for formula in formulas:
            item = FormulaWidget(formula, True)
            list_item = QListWidgetItem(self)
            list_item.setSizeHint(item.sizeHint())
            self.setItemWidget(list_item, item)
            item.clicked.connect(self.item_clicked(list_item))

    def item_clicked(self, list_item):
        def func():
            self.itemClicked.emit(list_item)
        return func


class FormulaSelectWidget(QComboBox):
    def __init__(self, name, parent=None):
        super(FormulaSelectWidget, self).__init__(parent)
        self.name = name
        self.list_widget = FormulaListWidget(self)
        self.setModel(self.list_widget.model())
        self.setView(self.list_widget)
        self.vbl_widget = QVBoxLayout()
        self.vbl_widget.setSpacing(0)
        self.hbl_widget = QHBoxLayout(self)
        self.hbl_widget.addLayout(self.vbl_widget)
        self.hbl_widget.setSpacing(0)
        self.hbl_widget.setContentsMargins(0, 0, 18, 0)
        self.list_widget.itemClicked.connect(self.selected)
        self.currentIndexChanged.connect(self.current_index_changed_event)

    def add_formulas(self, formulas):
        self.list_widget.add_formulas(formulas)
        for formula in formulas:
            item = FormulaWidget(formula, True)
            item.clicked.connect(self.showPopup)
            self.vbl_widget.addWidget(item)
        self.show_item(self.currentIndex())
    #    self.setMinimumWidth(self.list_widget.sizeHintForColumn(0))

    def show_item(self, index):
        for i in range(self.vbl_widget.count()):
            self.vbl_widget.itemAt(i).widget().setVisible(False)
        if index < self.vbl_widget.count():
            self.vbl_widget.itemAt(index).widget().setVisible(True)

    def selected(self, event):
        self.hidePopup()
        self.setCurrentIndex(self.list_widget.row(event))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.showPopup()

    def current_index_changed_event(self, event):
        self.show_item(self.currentIndex())

    def wheelEvent(self, event):
        pass


class RequirementThingWidget(QWidget):
    size = QSize(60, 50)
    image_size = QSize(38, 38)
    value_style = '''
        QLabel {
            color: #99FFFF; 
            font-size: 12px; 
            qproperty-alignment: "AlignHCenter | AlignBottom";
        }
    '''

    def __init__(self, name=None, picture=None, value=None, parent=None):
        super(RequirementThingWidget, self).__init__(parent)
        self.setFixedSize(self.size)
        self.name = name
        self.value = value
        self.btn_image = MTipsButton(self)
        self.lbl_value = QLabel(self)
        count_text = '%.2f' % value if value >= 0 else '不定'
        self.lbl_value.setStyleSheet(self.value_style)
        self.lbl_value.setText(count_text)
        self.btn_image.setFixedSize(self.image_size)
        self.btn_image.setIconSize(self.image_size)
        self.btn_image.set_name(name)
        self.btn_image.set_count(count_text)
        self.btn_image.set_icon(picture)

        self.hbl_widget = QHBoxLayout()
        self.hbl_widget.setSpacing(0)
        self.hbl_widget.addStretch(1)
        self.hbl_widget.addWidget(self.btn_image)
        self.hbl_widget.addStretch(1)
        self.hbl_widget.setContentsMargins(0, 0, 0, 0)

        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.setSpacing(0)
        self.vbl_widget.addLayout(self.hbl_widget)
        self.vbl_widget.addWidget(self.lbl_value)
        self.vbl_widget.setContentsMargins(0, 0, 0, 0)

        self.btn_image.clicked.connect(self.open_calculation)

    def open_calculation(self):
        if self.name:
            wnd_cal = CalculateWindow.new_window(self.name, round(self.value, 2))
        #    wnd_cal.start_calculate()


class RequirementTableItem(MTableWidget):
    def __init__(self, col_count, data, parent=None):
        super(RequirementTableItem, self).__init__(parent)
        row_count = math.ceil(len(data) / col_count) or 1
        self.setRowCount(row_count)
        self.setColumnCount(col_count)
        self.set_min_section(RequirementThingWidget.size)
        row = 0
        col = 0
        for name, value in data:
            picture = ThingsMgr.create_inst().get_icon(name)
            item = RequirementThingWidget(name, picture, value)
            self.setCellWidget(row, col, item)
            col += 1
            if col >= col_count:
                row += 1
                col = 0
        self.horizontalHeader().resizeSections()
        self.resize(self.sizeHint())

    def currentChanged(self, *event):
        self.setCurrentIndex(QModelIndex())


class RequirementPowerWidget(QWidget):
    style_sheet = '''
        QLabel {
            color: #99FFFF;
            font-size: 9pt;
            qproperty-alignment: "AlignCenter";
        }
    '''

    def __init__(self, power, parent=None):
        super(RequirementPowerWidget, self).__init__(parent)
        self.setStyleSheet(self.style_sheet)
        self.lbl_power = QLabel(trans_power(power), self)
        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.addWidget(self.lbl_power)
        self.resize(self.vbl_widget.sizeHint())


class RequirementTableWidget(MTableWidget):
    def __init__(self, material_count, facility_count, byproduct_count, parent=None):
        super(RequirementTableWidget, self).__init__(parent)
        self.setShowGrid(True)
        self.setColumnCount(4)
        self.horizontalHeader().setVisible(True)
        self.setHorizontalHeaderLabels(('所需原料', '所需设备', '副产物', '工作功率'))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.set_min_section(RequirementThingWidget.size)
        self.setRowCount(10)
        self.setCellWidget(0, 0, RequirementTableItem(material_count, []))
        self.setCellWidget(0, 1, RequirementTableItem(facility_count, []))
        self.setCellWidget(0, 2, RequirementTableItem(byproduct_count, []))
        self.setCellWidget(0, 3, RequirementPowerWidget(99999))
        self.horizontalHeader().resizeSections()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setStretchLastSection(True)
        self.setFixedSize(self.sizeHint())
        self.setRowCount(0)


class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self.formulas_mgr = FormulasMgr.create_inst()
        self.things_mgr = ThingsMgr.create_inst()
        self.lbl_mineral_utilization = QLabel('矿物利用等级：', self)
        self.ldt_utilization_level = QLineEdit(self)
        self.lbl_assembler_level = QLabel('制造台：', self)
        self.cbb_assembler = QComboBox(self)
        self.gpb_select_group = QGroupBox(self)
        self.gpb_select_group.setTitle('设置特定合成公式')
        self.ldt_utilization_level.setFixedWidth(60)
        self.ldt_utilization_level.setValidator(QRegExpValidator(QRegExp(r"[0-9]+")))
        self.ldt_utilization_level.setText(str(self.things_mgr.utilization_level))
        self.cbb_assembler.setFixedWidth(120)
        self.cbb_assembler.addItems(['制造台MK.I', '制造台MK.II', '制造台MK.III'])
        self.cbb_assembler.setView(QListView())
        self.cbb_assembler.setCurrentText(self.things_mgr.assembler_level)
        self.gdl_select = QGridLayout(self.gpb_select_group)
        self.add_select_widget()
        self.hbl_settings = QHBoxLayout()
        self.hbl_settings.setSpacing(0)
        self.hbl_settings.addSpacing(13)
        self.hbl_settings.addWidget(self.lbl_mineral_utilization)
        self.hbl_settings.addWidget(self.ldt_utilization_level)
        self.hbl_settings.addSpacing(40)
        self.hbl_settings.addWidget(self.lbl_assembler_level)
        self.hbl_settings.addWidget(self.cbb_assembler)
        self.hbl_settings.addStretch(1)
        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.setContentsMargins(0, 0, 0, 0)
        self.vbl_widget.addWidget(MHLine2(self))
        self.vbl_widget.addLayout(self.hbl_settings)
        self.vbl_widget.addWidget(self.gpb_select_group)
        self.resize(self.vbl_widget.sizeHint())
        self.ldt_utilization_level.textChanged.connect(self.utilization_level_changed_event)
        self.cbb_assembler.currentTextChanged.connect(self.assembler_level_changed_event)

    def add_select_widget(self):
        row = 0
        col = 0
        for name, formulas in self.formulas_mgr.all_multi_formulas():
            if self.things_mgr.is_exclude_product(name):
                continue
            select_widget = FormulaSelectWidget(name, self)
            select_widget.add_formulas(formulas)
            selected_index = self.formulas_mgr.get_selected_formula(name)
            select_widget.setCurrentIndex(selected_index)
            select_widget.currentIndexChanged.connect(self.selected_changed_event)
            self.gdl_select.addWidget(select_widget, row, col)
            col += 1
            if col >= 3:
                row += 1
                col = 0
        self.gpb_select_group.resize(self.gdl_select.totalSizeHint())

    def utilization_level_changed_event(self, event):
        self.things_mgr.utilization_level = int(event or 0)

    def assembler_level_changed_event(self, event):
        self.things_mgr.assembler_level = event

    def selected_changed_event(self, event):
        select_widget = self.sender()
        self.formulas_mgr.set_selected_formula(select_widget.name, select_widget.currentIndex())


class CalculateWindow(QDialog):
    material_count = 6
    facility_count = 5
    byproduct_count = 1
    win_id = 0
    all_windows = {}
    style_sheet = '''
         QLabel {
            color: #989898;
            font-size: 9pt;
            qproperty-alignment: "AlignCenter";
        }
    '''
    button_style = '''
         QPushButton {
            border: 1px solid #415E68;
            border-radius: 4px;
            background-color: transparent;
            color: #557b88;
            padding: 5px 5px 5px 5px;
        }
        QPushButton:hover {
            border: 1px solid #557b88;
            background-color: #33435b;
    }   
    '''

    def __init__(self, parent=None):
        super(CalculateWindow, self).__init__(parent)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # 无帮助按钮
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)  # 窗体大小固定
        self.setStyleSheet(self.style_sheet)
        self.formulas_mgr = FormulasMgr.create_inst()
        self.things_mgr = ThingsMgr.create_inst()
        self.product_mgr = ProductMgr.create_inst()
        self.btn_product = MTipsButton(self)
        self.lbl_unit = QLabel('/min', self)
        self.ldt_production_speed = QLineEdit(self)
        self.btn_calculate = QPushButton('计算', self)
        self.btn_calculate.setStyleSheet(self.button_style)
        self.btn_settings = QPushButton('设置', self)
        self.btn_settings.setStyleSheet(self.button_style)
        self.wgt_settings = SettingsWidget(self)
        self.wgt_requirements = QWidget(self)
        self.tbw_result_table = RequirementTableWidget(
            self.material_count, self.facility_count, self.byproduct_count, self)

        self.btn_product.setFixedSize(QSize(50, 50))
        self.btn_product.setIconSize(QSize(50, 50))
        self.ldt_production_speed.setFixedWidth(60)
        self.ldt_production_speed.setValidator(QRegExpValidator(QRegExp(r"[0-9.]+")))
        self.btn_calculate.setDefault(True)
        self.btn_calculate.setCursor(Qt.PointingHandCursor)
        self.btn_settings.setCursor(Qt.PointingHandCursor)

        self.hbl_topbar = QHBoxLayout()
        self.hbl_topbar.addWidget(self.btn_product)
        self.hbl_topbar.addWidget(self.ldt_production_speed)
        self.hbl_topbar.addWidget(self.lbl_unit)
        self.hbl_topbar.addSpacing(10)
        self.hbl_topbar.addWidget(self.btn_calculate)
        self.hbl_topbar.addStretch(1)
        self.hbl_topbar.addWidget(self.btn_settings)

        self.vbl_requirements = QVBoxLayout(self.wgt_requirements)
        self.vbl_requirements.setContentsMargins(0, 0, 0, 0)
        self.vbl_requirements.addWidget(MHLine2(self))
        self.vbl_requirements.addWidget(self.tbw_result_table)
        self.wgt_requirements.resize(self.vbl_requirements.sizeHint())

        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.addLayout(self.hbl_topbar)
        self.vbl_widget.addWidget(self.wgt_settings)
        self.vbl_widget.addWidget(self.wgt_requirements)
        self.resize(self.vbl_widget.sizeHint())

        self.name = None
        self.w_id = self.win_id
        self.btn_calculate.clicked.connect(self.start_calculate)
        self.btn_settings.clicked.connect(self.show_select_group_event)

    @classmethod
    def new_window(cls, name, value=60, parent=None):
        if not isinstance(value, (int, float)) or value < 0:
            value = 60
        new_win = cls(parent)
        cls.all_windows[cls.win_id] = new_win
        cls.win_id += 1
        new_win.on_show(name, value)
        return new_win

    def on_show(self, name, value=60):
        self.name = name
        picture = ThingsMgr.create_inst().get_icon(name)
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon(os.path.join(PICTURES_FOLDER, picture)))
        self.btn_product.set_name(name)
        self.btn_product.set_icon(picture)
        self.ldt_production_speed.setText(str(value))
        self.tbw_result_table.setRowCount(0)
        self.wgt_requirements.setVisible(False)
        self.wgt_settings.setVisible(True)
        self.setFixedHeight(self.vbl_widget.sizeHint().height())
        self.show()

    def start_calculate(self):
        try:
            speed = float(self.ldt_production_speed.text() or 0)
        except Exception as exc:
            speed = 0
        try:
            requirements, result = self.product_mgr.calculate(self.name, speed)
            self.show_requirements(requirements, result)
        except Exception as exc:
            print(str(exc))
        self.wgt_requirements.setVisible(True)
        self.wgt_settings.setVisible(False)
        self.setFixedHeight(self.vbl_widget.sizeHint().height())

    def show_materials(self, row_index, materials):
        table_widget = RequirementTableItem(self.material_count, materials)
        self.tbw_result_table.setCellWidget(row_index, 0, table_widget)

    def show_facilities(self, row_index, facilities):
        table_widget = RequirementTableItem(self.facility_count, facilities)
        self.tbw_result_table.setCellWidget(row_index, 1, table_widget)

    def show_byproducts(self, row_index, byproducts):
        table_widget = RequirementTableItem(self.byproduct_count, byproducts)
        self.tbw_result_table.setCellWidget(row_index, 2, table_widget)

    def show_power(self, row_index, power):
        widget = RequirementPowerWidget(power)
        self.tbw_result_table.setCellWidget(row_index, 3, widget)

    def show_requirements(self, requirements, result):
        self.tbw_result_table.setRowCount(len(requirements) + len(result))
        row_index = 0
        for req in requirements:
            self.show_materials(row_index, req.get_materials())
            self.show_facilities(row_index, req.get_facilities())
            self.show_byproducts(row_index, req.get_byproducts())
            self.show_power(row_index, req.power)
            row_index += 1
        for req in result:
            self.show_materials(row_index, req.get_materials())
            self.show_facilities(row_index, req.get_all_facilities())
            self.show_byproducts(row_index, req.get_all_byproducts())
            self.show_power(row_index, req.sum_power)
            row_index += 1
        self.tbw_result_table.horizontalHeader().resizeSections()

    def show_select_group_event(self, event):
        if self.wgt_settings.isVisible():
            self.wgt_settings.setVisible(False)
        else:
            self.wgt_settings.setVisible(True)
        self.setFixedHeight(self.vbl_widget.sizeHint().height())

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.setParent(None)
        self.destroy()
        self.all_windows[self.w_id] = None


class FormulaThingWidget(MTipsButton):
    size = QSize(40, 50)
    image_size = QSize(40, 40)
    value_style = '''
        QLabel {
            color: #99FFFF; 
            font-size: 12px; 
            qproperty-alignment: "AlignBottom | AlignRight";
        }
    '''

    def __init__(self, name=None, picture=None, value=None, parent=None):
        super(FormulaThingWidget, self).__init__(parent)
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        self.name = name
        self.set_icon(picture)
        self.lbl_value = QLabel(str(value), self)
        self.lbl_value.setStyleSheet(self.value_style)
        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.addWidget(self.lbl_value)
        self.vbl_widget.setContentsMargins(0, 0, 0, 0)


class FormulaTimeWidget(MPushButton):
    size = QSize(50, 50)
    image_size = QSize(36, 36)
    time_style = '''
        QLabel {
            color: #FFE594; 
            font-size: 12px; 
            qproperty-alignment: "AlignCenter";
        }
    '''

    def __init__(self, formula, parent=None):
        super(FormulaTimeWidget, self).__init__(parent)
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        self.set_icon('箭头.png')
        time_text = ''
        if isinstance(formula.time, str):
            time_text = formula.time
        elif isinstance(formula.time, (int, float)) and formula.time >= 0:
            time_text = str(formula.time)+'s'
        self.lbl_time = QLabel(time_text, self)
        self.lbl_time.setStyleSheet(self.time_style)
        self.btn_facility = MTipsButton(self)
        self.btn_facility.setFixedSize(QSize(20, 20))
        self.btn_facility.setIconSize(QSize(20, 20))
        facility_picture = ThingsMgr.create_inst().get_icon(formula.facility)
        self.btn_facility.set_icon(facility_picture)
        self.btn_facility.set_name(formula.facility)

        self.hbl_widget = QHBoxLayout()
        self.hbl_widget.setSpacing(0)
        self.hbl_widget.setContentsMargins(0, 0, 0, 0)
        self.hbl_widget.addStretch(1)
        self.hbl_widget.addWidget(self.btn_facility)
        self.hbl_widget.addStretch(1)

        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.setSpacing(5)
        self.vbl_widget.setContentsMargins(0, 0, 0, 0)
        self.vbl_widget.addWidget(self.lbl_time)
        self.vbl_widget.addLayout(self.hbl_widget)

        self.btn_facility.clicked.connect(self.clicked.emit)


class FormulaWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, formula, has_tip=False, parent=None):
        super(FormulaWidget, self).__init__(parent)
        self.left_pressed = False
        self.things_mgr = ThingsMgr.create_inst()
        self.hbl_widget = QHBoxLayout(self)
        self.hbl_widget.setSpacing(0)
        self.hbl_widget.addStretch(1)
        for name, value in formula.product.items():
            picture = self.things_mgr.get_icon(name)
            item = (FormulaThingWidget(name, picture, value)
                    if has_tip else FormulaThingWidget2(name, picture, value))
            item.clicked.connect(self.clicked.emit)
            self.hbl_widget.addWidget(item)
        item_time = FormulaTimeWidget(formula) if has_tip else FormulaTimeWidget2(formula)
        item_time.clicked.connect(self.clicked.emit)
        self.hbl_widget.addWidget(item_time)
        for name, value in formula.material.items():
            picture = self.things_mgr.get_icon(name)
            item = (FormulaThingWidget(name, picture, value)
                    if has_tip else FormulaThingWidget2(name, picture, value))
            item.clicked.connect(self.clicked.emit)
            self.hbl_widget.addWidget(item)
        self.hbl_widget.addStretch(1)
        self.hbl_widget.setContentsMargins(0, 0, 0, 0)
        self.hbl_widget.setSpacing(0)
        self.resize(self.hbl_widget.sizeHint())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_pressed = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.left_pressed:
            self.clicked.emit()
        self.left_pressed = False


class FormulaThingWidget2(MPushButton):
    size = QSize(40, 50)
    image_size = QSize(40, 40)
    value_style = '''
        QLabel {
            color: #99FFFF; 
            font-size: 12px; 
            qproperty-alignment: "AlignBottom | AlignRight";
        }
    '''

    def __init__(self, name=None, picture=None, value=None, parent=None):
        super(FormulaThingWidget2, self).__init__(parent)
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        self.set_icon(picture)
        self.lbl_value = QLabel(str(value), self)
        self.lbl_value.setStyleSheet(self.value_style)
        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.addWidget(self.lbl_value)
        self.vbl_widget.setContentsMargins(0, 0, 0, 0)


class FormulaTimeWidget2(MPushButton):
    size = QSize(50, 50)
    image_size = QSize(36, 36)
    time_style = '''
        QLabel {
            color: #FFE594; 
            font-size: 12px; 
            qproperty-alignment: "AlignCenter";
        }
    '''

    def __init__(self, formula, parent=None):
        super(FormulaTimeWidget2, self).__init__(parent)
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        self.set_icon('箭头.png')
        time_text = ''
        if isinstance(formula.time, str):
            time_text = formula.time
        elif isinstance(formula.time, (int, float)) and formula.time >= 0:
            time_text = str(formula.time)+'s'
        self.lbl_time = QLabel(time_text, self)
        self.lbl_time.setStyleSheet(self.time_style)
        self.btn_facility = MPushButton(self)
        self.btn_facility.setFixedSize(QSize(20, 20))
        self.btn_facility.setIconSize(QSize(20, 20))
        facility_picture = ThingsMgr.create_inst().get_icon(formula.facility)
        self.btn_facility.set_icon(facility_picture)

        self.hbl_widget = QHBoxLayout()
        self.hbl_widget.setSpacing(0)
        self.hbl_widget.setContentsMargins(0, 0, 0, 0)
        self.hbl_widget.addStretch(1)
        self.hbl_widget.addWidget(self.btn_facility)
        self.hbl_widget.addStretch(1)

        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.setSpacing(5)
        self.vbl_widget.setContentsMargins(0, 0, 0, 0)
        self.vbl_widget.addWidget(self.lbl_time)
        self.vbl_widget.addLayout(self.hbl_widget)

        self.btn_facility.clicked.connect(self.clicked.emit)


class FacilityPowerWidget(QWidget):
    style_sheet = '''
        #PowerName {
            font-size: 9pt;
            color: #989898;
            qproperty-alignment: "AlignLeft";
        }
        #PowerValue {
            font-size: 9pt;
            color: #FFFFFF;
            qproperty-alignment: "AlignRight";
        }
    '''

    def __init__(self, parent=None):
        super(FacilityPowerWidget, self).__init__(parent)
        self.things_mgr = ThingsMgr.create_inst()
        self.setStyleSheet(self.style_sheet)
        self.lbl_work_consumption = QLabel('工作功率', self)
        self.lbl_idle_consumption = QLabel('待机功率', self)
        self.lbl_power = QLabel('发电功率', self)
        self.lbl_input_power = QLabel('输入功率', self)
        self.lbl_output_power = QLabel('输出功率', self)
        self.lbl_basic_generation = QLabel('基础发电功率', self)
        self.lbl_max_charging_power = QLabel('最大充能功率', self)

        self.lbl_work_consumption_value = QLabel(self)
        self.lbl_idle_consumption_value = QLabel(self)
        self.lbl_power_value = QLabel(self)
        self.lbl_input_power_value = QLabel(self)
        self.lbl_output_power_value = QLabel(self)
        self.lbl_basic_generation_value = QLabel(self)
        self.lbl_max_charging_power_value = QLabel(self)

        self.gdl_widget = QGridLayout(self)
        self.gdl_widget.setSpacing(0)
        self.gdl_widget.setContentsMargins(0, 0, 0, 0)
        self.gdl_widget.setColumnStretch(0, 1)

        self._labels = [
            ['work_consumption', self.lbl_work_consumption, self.lbl_work_consumption_value],
            ['idle_consumption', self.lbl_idle_consumption, self.lbl_idle_consumption_value],
            ['power', self.lbl_power, self.lbl_power_value],
            ['input_power', self.lbl_input_power, self.lbl_input_power_value],
            ['output_power', self.lbl_output_power, self.lbl_output_power_value],
            ['basic_generation', self.lbl_basic_generation, self.lbl_basic_generation_value],
            ['max_charging_power', self.lbl_max_charging_power, self.lbl_max_charging_power_value]
        ]

        row = 0
        for attr, label_name, label_value in self._labels:
            label_name.setObjectName('PowerName')
            label_value.setObjectName('PowerValue')
            self.gdl_widget.addWidget(label_name, row, 0)
            self.gdl_widget.addWidget(label_value, row, 1)
            row += 1

        self.resize(self.gdl_widget.sizeHint())
        self.on_hide()

    def on_show(self, name):
        flag = False
        for attr, label_name, label_value in self._labels:
            value = self.things_mgr.get_item_attr(name, attr)
            if value and value > 0:
                label_name.setVisible(True)
                label_value.setVisible(True)
                label_value.setText(trans_power(value))
                flag = True
            else:
                label_name.setVisible(False)
                label_value.setVisible(False)

        if flag:
            self.setVisible(True)

    def on_hide(self):
        self.setVisible(False)


class ThingTooltipWindow(QFrame):
    inst = None
    name_style = '''
        QLabel {
            color: #FFE594; 
            font-size: 10pt; 
            qproperty-alignment: "AlignLeft | AlignBottom";
        }
    '''
    count_style = '''
        QLabel {
            color: #99FFFF; 
            font-size: 9pt; 
            qproperty-alignment: "AlignLeft | AlignBottom";
        }
    '''

    def __init__(self, parent=None):
        super(ThingTooltipWindow, self).__init__(parent)
        self.setWindowFlag(Qt.ToolTip)
        # self.setWindowOpacity(0.9)
        self.formulas_mgr = FormulasMgr.create_inst()
        self.timer_show = QTimer(self)
        self.name = None
        self.count = None
        self.pos = None
        self.lbl_name = QLabel(self)
        self.lbl_name.setStyleSheet(self.name_style)
        self.lbl_count = QLabel(self)
        self.lbl_count.setStyleSheet(self.count_style)
        self.wgt_power = FacilityPowerWidget(self)
        self.line = MHLine1(self)
        self.lbl_text = QLabel(self)
        self.lbl_text.setStyleSheet(self.count_style)

        self.hbl_name = QHBoxLayout()
        self.hbl_name.addWidget(self.lbl_name)
        self.hbl_name.addWidget(self.lbl_count, 1)
        self.vbl_formulas = QVBoxLayout()
        self.vbl_formulas.setSpacing(0)
        self.hbl_formulas = QHBoxLayout()
        self.hbl_formulas.setSpacing(0)
        self.hbl_formulas.addStretch(1)
        self.hbl_formulas.addLayout(self.vbl_formulas)
        self.hbl_formulas.addStretch(1)
        self.vbl_window = QVBoxLayout(self)
        self.vbl_window.setContentsMargins(0, 0, 0, 0)
        self.vbl_window.addLayout(self.hbl_name)
        self.vbl_window.addWidget(self.wgt_power)
        self.vbl_window.addWidget(self.line)
        self.vbl_window.addWidget(self.lbl_text)
        self.vbl_window.addLayout(self.hbl_formulas)
        self.timer_show.timeout.connect(self.on_show)

    def delay_show(self, name, pos, count=None):
        self.name = name
        self.pos = pos
        self.count = count
        self.timer_show.start(300)

    def show_relevant_formula(self, name, pos):
        self.name = name
        self.pos = pos
        self.count = None
        self.on_show(True)

    def on_show(self, relevant=False):
        self.timer_show.stop()
        if not self.name:
            return
        if self.isVisible():
            self.on_hide()
        self.lbl_name.setText(self.name)
        if self.count:
            self.lbl_count.setText(' x '+str(self.count))
            self.lbl_count.setVisible(True)
        self.wgt_power.on_show(self.name)
        if relevant:
            formulas = self.formulas_mgr.get_formulas_by_material(self.name)
            text = '相关公式：'
        else:
            formulas = self.formulas_mgr.get_formulas_by_product(self.name)
            text = '合成公式：'
        if len(formulas) > 0:
            self.lbl_text.setText(text)
            self.lbl_text.setVisible(True)
            self.line.setVisible(True)
        for formula in formulas:
            item = FormulaWidget(formula, False)
            self.vbl_formulas.addWidget(item)
        self.move(self.pos)
        self.show()
        self.resize(self.vbl_window.sizeHint())

    def on_hide(self):
        self.timer_show.stop()
        self.lbl_count.setVisible(False)
        self.wgt_power.on_hide()
        self.line.setVisible(False)
        self.lbl_text.setVisible(False)
        for row in range(self.vbl_formulas.count()):
            widget = self.vbl_formulas.itemAt(0).widget()
            if widget:
                self.vbl_formulas.removeWidget(widget)
                widget.deleteLater()
        self.hide()

    @classmethod
    def create_inst(cls, parent=None):
        if cls.inst is None:
            cls.inst = cls(parent)
        return cls.inst


class ThingTooltipWindow1(QListWidget):
    inst = None

    def __init__(self, parent=None):
        super(ThingTooltipWindow1, self).__init__(parent)
        self.setWindowFlag(Qt.ToolTip)
        self.formulas_mgr = FormulasMgr.create_inst()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑
        self.setSelectionMode(QAbstractItemView.NoSelection)  # 不可选中
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.hide()

    def on_show(self, name, pos):
        formulas = self.formulas_mgr.get_formulas_by_product(name)
        if not self.isVisible() and formulas:
            for formula in formulas:
                list_item = QListWidgetItem(self)
                item = FormulaWidget(formula, False)
                list_item.setSizeHint(item.sizeHint())
                self.setItemWidget(list_item, item)
            self.resize(self.sizeHintForColumn(0)+22, self.sizeHintForRow(0)*self.count()+22)
            self.move(pos)
            self.show()

    def on_hide(self):
        self.clear()
        self.hide()

    @classmethod
    def create_inst(cls, parent=None):
        if cls.inst is None:
            cls.inst = cls(parent)
        return cls.inst


class ThingTooltipWindow2(MTableWidget):
    inst = None

    def __init__(self, parent=None):
        super(ThingTooltipWindow2, self).__init__(parent)
        self.setWindowFlag(Qt.ToolTip)
        self.formulas_mgr = FormulasMgr.create_inst()
        self.setColumnCount(1)
        self.hide()

    def on_show(self, name, pos):
        formulas = self.formulas_mgr.get_formulas_by_product(name)
        if not self.isVisible() and formulas:
            self.setRowCount(len(formulas))
            index = 0
            for formula in formulas:
                item = FormulaWidget(formula, False)
                self.setCellWidget(index, 0, item)
                index += 1
            self.horizontalHeader().resizeSections()
            self.resize(self.sizeHint())
            self.move(pos)
            self.show()

    def on_hide(self):
        for row in range(self.rowCount()):
            self.cellWidget(row, 0).deleteLater()
        self.setRowCount(0)
        self.hide()

    @classmethod
    def create_inst(cls, parent=None):
        if cls.inst is None:
            cls.inst = cls(parent)
        return cls.inst


def trans_power(value):
    if value >= 1000000000:
        return '%.2f TW' % (value / 1000000000)
    elif value >= 1000000:
        return '%.2f GW' % (value / 1000000)
    elif value >= 1000:
        return '%.2f MW' % (value / 1000)
    else:
        return '%d kW' % value


class ThingsMgr(object):
    inst = None

    def __init__(self):
        self._all_things = {}
        self._components = {}
        self._buildings = {}
        self._others = {}
        self._exclude_things = {}
        self.utilization_level = 0
        self.assembler_level = '制造台MK.II'
        with open('Components.json', 'r', encoding='utf-8') as file:
            self._components = json.load(file)
        with open('Buildings.json', 'r', encoding='utf-8') as file:
            self._buildings = json.load(file)
        with open('Others.json', 'r', encoding='utf-8') as file:
            self._others = json.load(file)
        with open('Exclude.json', 'r', encoding='utf-8') as file:
            self._exclude_things = json.load(file)
        self._all_things.update(self._components)
        self._all_things.update(self._buildings)
        self._all_things.update(self._others)

    def components(self):
        return self._components

    def buildings(self):
        return self._buildings

    def others(self):
        return self._others

    def get_item(self, name):
        return self._all_things.get(name, {})

    def get_item_attr(self, name, attr):
        return self._all_things.get(name, {}).get(attr)

    def get_icon(self, name):
        return self._all_things.get(name, {}).get('icon', '')

    def get_work_consumption(self, name):
        return self._all_things.get(name, {}).get('work_consumption', 0)

    def is_exclude_product(self, name):
        return name in self._exclude_things['product']

    def is_exclude_facility(self, name):
        return name in self._exclude_things['facility']

    @classmethod
    def create_inst(cls):
        if cls.inst is None:
            cls.inst = cls()
        return cls.inst


class Formula(object):
    def __init__(self, product, material, time_, facility):
        self.things_mgr = ThingsMgr.create_inst()
        self.product = product
        self.material = material
        self.time = time_
        self.facility = facility

    def has_product(self, name):
        return name in self.product

    def get_requirement(self, product_name, speed):
        if (not isinstance(self.time, (int, float)) or self.time < 0 or
                self.things_mgr.is_exclude_product(product_name) or
                self.things_mgr.is_exclude_facility(self.facility)):
            return None
        product_num = self.product[product_name]
        # 原料生产速度
        material_speed = dict([(name, speed * num / product_num) for name, num in self.material.items()])
        # 设备数量
        facility_num = [{self.facility: speed * self.time / product_num / 60}]
        # 副产物
        byproduct_num = dict([(name, speed * num / product_num)
                              for name, num in self.product.items() if name != product_name])
        if self.facility == '采矿机':
            speed = speed / (1 + self.things_mgr.utilization_level * 0.1)
            material_speed = dict([(name, speed * num / product_num) for name, num in self.material.items()])
            miner_count = 0
            for value in material_speed.values():
                miner_count += int(value / 6 + 0.5) or 1
            facility_num = [{self.facility: miner_count}]
        elif self.facility == '抽水站':
            speed = speed / (1 + self.things_mgr.utilization_level * 0.1)
            facility_num = [{self.facility: speed * self.time / product_num / 60}]
        elif self.facility == '制造台MK.II':
            if self.things_mgr.assembler_level == '制造台MK.I':
                speed = speed / 0.75
            elif self.things_mgr.assembler_level == '制造台MK.III':
                speed = speed / 1.5
            facility_num = [{self.things_mgr.assembler_level: speed * self.time / product_num / 60}]
        return Requirement(material_speed, facility_num, byproduct_num)


class FormulasMgr(object):
    inst = None

    def __init__(self):
        self.all_formulas = []
        self.product_formulas = {}
        self.material_formulas = {}
        self.multi_formulas = {}
        self.selected_formulas = {}
        with open('Formulas.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        for data in json_data:
            formula = Formula(*data)
            self.all_formulas.append(formula)
            for name in formula.product:
                res = self.product_formulas.get(name, [])
                res.append(formula)
                self.product_formulas[name] = res
            for name in formula.material:
                res = self.material_formulas.get(name, [])
                res.append(formula)
                self.material_formulas[name] = res
        for name, formulas in self.product_formulas.items():  # 获取有多条合成公式的组件
            if len(formulas) > 1:
                self.multi_formulas[name] = formulas
                self.selected_formulas[name] = 0

    def get_formulas_by_product(self, name):
        return self.product_formulas.get(name, [])

    def get_formulas_by_material(self, name):
        return self.material_formulas.get(name, [])

    def get_requirements(self, product_name, production_speed):
        result = []
        formulas = self.product_formulas.get(product_name, [])
        if len(formulas) > 0:
            formula = formulas[self.selected_formulas.get(product_name, 0)]
            req = formula.get_requirement(product_name, production_speed)
            if req:
                result.append(req)
        return result

    # 获取所有多产物的合成公式
    def get_multi_products(self):
        result = []
        for formula in self.all_formulas:
            if len(formula.product) > 1:
                result.append(formula)
        return result

    def get_multi_formulas(self, name):
        return self.multi_formulas.get(name, [])

    def all_multi_formulas(self):
        return list(self.multi_formulas.items())

    def set_selected_formula(self, name, value):
        if name in self.selected_formulas:
            self.selected_formulas[name] = value

    def get_selected_formula(self, name):
        return self.selected_formulas.get(name, 0)

    @classmethod
    def create_inst(cls):
        if cls.inst is None:
            cls.inst = cls()
        return cls.inst


class Requirement(object):
    def __init__(self, materials=None, facilities=None, byproducts=None,
                 all_facilities=None, all_byproducts=None, power=0, sum_power=0):
        self.materials = materials.copy() if isinstance(materials, dict) else {}
        self.facilities = facilities.copy() if isinstance(facilities, list) else []
        self.byproducts = byproducts.copy() if isinstance(byproducts, dict) else {}
        self.all_facilities = all_facilities.copy() if isinstance(all_facilities, dict) else {}
        self.all_byproducts = all_byproducts.copy() if isinstance(all_byproducts, dict) else {}
        self.power = power
        self.sum_power = sum_power
        self.things_mgr = ThingsMgr.create_inst()

    def add_requirement(self, requirement):
        new_req = Requirement(self.materials, self.facilities, self.byproducts,
                              self.all_facilities, self.all_byproducts, self.power, self.sum_power)
        for name, value in requirement.materials.items():
            new_req.materials[name] = self.materials.get(name, 0) + value
        for name, value in requirement.byproducts.items():
            new_req.byproducts[name] = self.byproducts.get(name, 0) + value
            new_req.all_byproducts[name] = self.all_byproducts.get(name, 0) + value
        new_req.facilities.extend(requirement.facilities)
        for fac in requirement.facilities:
            for name, count in fac.items():
                new_req.all_facilities[name] = self.all_facilities.get(name, 0) + math.ceil(count)
                power = self.things_mgr.get_work_consumption(name) * count
                new_req.power += power
                new_req.sum_power += power
        return new_req

    def add_material(self, name, value):
        self.materials[name] = self.materials.get(name, 0) + value

    def get_materials(self):
        return list(self.materials.items())

    def get_facilities(self):
        data = []
        for fac in self.facilities:
            data.extend(list(fac.items()))
        return data

    def get_byproducts(self):
        return list(self.byproducts.items())

    def get_all_byproducts(self):
        return list(self.all_byproducts.items())

    def get_all_facilities(self):
        return list(self.all_facilities.items())


class ProductMgr(object):
    inst = None

    def __init__(self):
        self.formulas_mgr = FormulasMgr.create_inst()
        self.things_mgr = ThingsMgr.create_inst()
        self.requirements = []

    def calculate(self, name, speed):
        self.requirements = []
        require = Requirement()
        require.add_material(name, speed)
        result = self.cal_requirements([require])
        return self.requirements, result

    def cal_requirements(self, list_products):
        finish = True
        res_reqs = []
        for products in list_products:
            temp_reqs = [Requirement(all_facilities=products.all_facilities,
                                     all_byproducts=products.all_byproducts,
                                     sum_power=products.sum_power)]
            for name, speed in products.materials.items():
                requirements = self.formulas_mgr.get_requirements(name, speed)
                if self.things_mgr.is_exclude_product(name) or (not requirements):
                    for req1 in temp_reqs:
                        req1.add_material(name, speed)
                else:
                    new_reqs = []
                    for req1 in temp_reqs:
                        for req2 in requirements:
                            new_reqs.append(req1.add_requirement(req2))
                    temp_reqs = new_reqs
                    finish = False
            res_reqs.extend(temp_reqs)

        if finish:
            return res_reqs
        else:
            self.requirements.extend(res_reqs)
            return self.cal_requirements(res_reqs)

    @classmethod
    def create_inst(cls):
        if cls.inst is None:
            cls.inst = cls()
        return cls.inst


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    ThingTooltipWindow.create_inst()
    win = MainWindow.create_inst()
    win.show()  # 显示主窗体
    sys.exit(app.exec_())
