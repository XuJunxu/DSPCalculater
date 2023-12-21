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
FILES_FOLDER = "Files"


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
    FormulaWidget, AttributeWidget {
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
        color: #99FFFF;
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
        color: #99FFFF;
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
        color: #99FFFF;
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
    #TextButton {
        border: 1px solid #415E68;
        border-radius: 4px;
        background-color: transparent;
        color: #99FFFF;
        padding: 5px 12px 5px 12px;
    }
    #TextButton:hover {
        border: 1px solid #557b88;
        background-color: #33435b;
    }  
'''


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)  # 窗体大小固定
        self.setWindowIcon(QIcon('Logo.png'))

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
        self.wnd_components.show_items(ThingsMgr.inst().components())
        self.wnd_buildings.show_items(ThingsMgr.inst().buildings())
        self.wnd_others.show_items(ThingsMgr.inst().others())

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


class MPushButton(QPushButton):
    def __init__(self, parent=None):
        super(MPushButton, self).__init__(parent)

    def set_icon(self, picture):
        self.setIcon(QIcon(os.path.join(PICTURES_FOLDER, picture or '')))


class MTipsButton(QPushButton):
    def __init__(self, parent=None):
        super(MTipsButton, self).__init__(parent)
        self._count = None
        self._thing = None
        self._can_tips = True
        self.right_pressed = False
        self.clicked.connect(self.leaveEvent)

    def set_thing(self, thing):
        if isinstance(thing, Thing):
            self._thing = thing
            self.set_icon(self._thing.icon)

    def set_count(self, count):
        self._count = count

    def set_icon(self, picture):
        self.setIcon(QIcon(os.path.join(PICTURES_FOLDER, picture or '')))

    def disableTooltips(self, can):
        self._can_tips = can

    def enterEvent(self, event):
        if not self._can_tips:
            return
        x = event.globalPos().x() - event.localPos().x() + self.width() / 2
        y = event.globalPos().y() - event.localPos().y() + self.height() + 5
        ThingTooltipWindow.inst().delay_show(self._thing, QPoint(int(x), int(y)), self._count)

    def leaveEvent(self, event):
        if not self._can_tips:
            return
        ThingTooltipWindow.inst().on_hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.right_pressed = True
        super(MTipsButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._can_tips and event.button() == Qt.RightButton and self.right_pressed:
            x = event.globalPos().x() - event.localPos().x() + self.width() / 2
            y = event.globalPos().y() - event.localPos().y() + self.height() + 5
            ThingTooltipWindow.inst().show_relevant_formula(self._thing, QPoint(int(x), int(y)))
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


# 悬浮提示框中的分割线
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


# 计算窗体中的分割线
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


# 主窗体中顶部切换表格的按键
class TopButton(MPushButton):
    size = QSize(70, 70)
    image_size = QSize(60, 60)

    def __init__(self, parent=None, picture=None):
        super(TopButton, self).__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        self.set_icon(picture)


# 主窗体中的物品表格单元
class ThingsTableItem(MTipsButton):
    size = QSize(60, 60)
    image_size = QSize(50, 50)

    def __init__(self, parent=None):
        super(ThingsTableItem, self).__init__(parent)
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        self.clicked.connect(self.open_calculation)

    def open_calculation(self):
        if self._thing and self._thing.product_formulas():
            CalculateWindow.new_window(self._thing)


# 主窗体中的物品表格
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

    def show_items(self, data):
        for name, thing in data.items():
            if thing.row >= 0 and thing.col >= 0:
                item = self.cellWidget(thing.row, thing.col)
                item.set_thing(thing)
                item.setCursor(Qt.PointingHandCursor)


# 计算窗体中选择使用公式的选择框的下拉列表
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


# 计算窗体中选择使用公式的选择框
class FormulaSelectWidget(QComboBox):
    def __init__(self, thing, parent=None):
        super(FormulaSelectWidget, self).__init__(parent)
        self._thing = thing
        self._current_formula = None
        self.list_widget = FormulaListWidget(self)
        self.setModel(self.list_widget.model())
        self.setView(self.list_widget)
        self.vbl_widget = QVBoxLayout()
        self.vbl_widget.setSpacing(0)
        self.hbl_widget = QHBoxLayout(self)
        self.hbl_widget.addLayout(self.vbl_widget)
        self.hbl_widget.setSpacing(0)
        self.hbl_widget.setContentsMargins(0, 0, 18, 0)
        self.list_widget.itemClicked.connect(self.on_select)

        self.list_widget.add_formulas(self._thing.product_formulas())
        for formula in self._thing.product_formulas():
            item = FormulaWidget(formula, True)
            item.clicked.connect(self.showPopup)
            self.vbl_widget.addWidget(item)
        self.show_item(self._thing.selected_formula())
    #    self.setMinimumWidth(self.list_widget.sizeHintForColumn(0))

    def save_current_selected(self):
        self._thing.set_selected_formula(self._current_formula)

    def show_item(self, formula):
        if formula is None or self._current_formula == formula:
            return

        self._current_formula = formula
        for i in range(self.vbl_widget.count()):
            item = self.vbl_widget.itemAt(i).widget()
            if item.formula() == formula:
                item.setVisible(True)
                self.setCurrentIndex(i)
            else:
                item.setVisible(False)

    def on_select(self, list_item):
        self.hidePopup()
        item = self.list_widget.itemWidget(list_item)
        self.show_item(item.formula())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.showPopup()

    def wheelEvent(self, event):
        pass


# 计算窗体中的设置部分
class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)
        self._select_facility_widget = []
        self._select_formula_widget = []
        self.lbl_mineral_utilization = QLabel('矿物利用等级：', self)
        self.ldt_mineral_level = QLineEdit(self)
        self.ldt_mineral_level.setFixedWidth(60)
        self.ldt_mineral_level.setValidator(QRegExpValidator(QRegExp(r"[0-9]+")))
        self.ldt_mineral_level.setText(str(Formula.mineral_level))
        self.btn_save_settings = QPushButton('保存', self)
        self.btn_save_settings.setObjectName('TextButton')
        self.btn_save_settings.setCursor(Qt.PointingHandCursor)
        self.btn_save_settings.clicked.connect(self.activate_settings)

        self.gpb_select_facility_group = QGroupBox(self)
        self.gpb_select_facility_group.setTitle('选择生产设备')
        self.gdl_select_facility = QGridLayout(self.gpb_select_facility_group)
        self.gdl_select_facility.setSpacing(0)
        self.add_select_facility_widget()

        self.gpb_select_formula_group = QGroupBox(self)
        self.gpb_select_formula_group.setTitle('选择合成公式')
        self.gdl_select_formula = QGridLayout(self.gpb_select_formula_group)
        self.add_select_formula_widget()

        self.hbl_settings = QHBoxLayout()
        self.hbl_settings.setSpacing(0)
        self.hbl_settings.addSpacing(13)
        self.hbl_settings.addWidget(self.lbl_mineral_utilization)
        self.hbl_settings.addWidget(self.ldt_mineral_level)
        self.hbl_settings.addStretch(1)
        self.hbl_settings.addWidget(self.btn_save_settings)
        self.hbl_settings.addSpacing(13)

        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.setContentsMargins(0, 0, 0, 0)
        self.vbl_widget.addWidget(MHLine2(self))
        self.vbl_widget.addLayout(self.hbl_settings)
        self.vbl_widget.addWidget(self.gpb_select_facility_group)
        self.vbl_widget.addWidget(self.gpb_select_formula_group)

        self.resize(self.vbl_widget.sizeHint())

    def add_select_facility_widget(self):
        row = 0
        col = 0
        for facility_type, current_fac in Formula.facility_selected.items():
            facilities = ThingsMgr.inst().get_by_facility_type(facility_type)
            select_box = QComboBox(self)
            select_box.setFixedWidth(140)
            select_box.addItems([fac.name for fac in facilities])
            select_box.setView(QListView())
            select_box.setCurrentText(current_fac)
            select_box.facility_type = facility_type
            self.gdl_select_facility.addWidget(select_box, row, col)
            self._select_facility_widget.append(select_box)
            col += 1
            if col >= 4:
                row += 1
                col = 0

    def add_select_formula_widget(self):
        row = 0
        col = 0
        for thing in ThingsMgr.inst().get_multi_formula_things():
            if thing.exclude:
                continue
            select_widget = FormulaSelectWidget(thing, self)
            self.gdl_select_formula.addWidget(select_widget, row, col)
            self._select_formula_widget.append(select_widget)
            col += 1
            if col >= 3:
                row += 1
                col = 0
        self.gpb_select_formula_group.resize(self.gdl_select_formula.totalSizeHint())

    def activate_settings(self, event=None):
        Formula.mineral_level = int(self.ldt_mineral_level.text() or 0)

        for select_box in self._select_facility_widget:
            Formula.facility_selected[select_box.facility_type] = select_box.currentText()

        for select_wdg in self._select_formula_widget:
            select_wdg.save_current_selected()


# 显示计算结果的表格单元中的单个物品
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

    def __init__(self, thing, count, parent=None):
        super(RequirementThingWidget, self).__init__(parent)
        self.setFixedSize(self.size)
        self._thing = thing
        self._count = count
        self.btn_image = MTipsButton(self)
        self.lbl_value = QLabel(self)
        count_text = '%.2f' % count if count >= 0 else '不定'
        self.lbl_value.setStyleSheet(self.value_style)
        self.lbl_value.setText(count_text)
        self.btn_image.setFixedSize(self.image_size)
        self.btn_image.setIconSize(self.image_size)
        self.btn_image.set_thing(thing)
        self.btn_image.set_count(count_text)

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
        if self._thing and self._thing.product_formulas():
            CalculateWindow.new_window(self._thing, round(self._count, 2))


# 显示计算结果的表格单元，显示物品列表
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
            thing = ThingsMgr.inst().get_thing(name)
            item = RequirementThingWidget(thing, value)
            self.setCellWidget(row, col, item)
            col += 1
            if col >= col_count:
                row += 1
                col = 0
        self.horizontalHeader().resizeSections()
        self.resize(self.sizeHint())

    def currentChanged(self, *event):
        self.setCurrentIndex(QModelIndex())


# 显示计算结果的表格单元，显示功率
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


# 显示计算结果的表格
class RequirementTableWidget(MTableWidget):
    def __init__(self, parent=None):
        super(RequirementTableWidget, self).__init__(parent)
        self.setShowGrid(True)
        self.horizontalHeader().setVisible(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.set_min_section(RequirementThingWidget.size)

    def show_things(self, things, row, col, col_count):
        if things:
            table_widget = RequirementTableItem(col_count, things)
            self.setCellWidget(row, col, table_widget)

    def show_power(self, power, row, col):
        if power:
            widget = RequirementPowerWidget(power)
            self.setCellWidget(row, col, widget)


class RequirementTableFour(RequirementTableWidget):
    material_count = 6
    facility_count = 5
    byproduct_count = 1

    def __init__(self, parent=None):
        super(RequirementTableFour, self).__init__(parent)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(('所需原料', '所需设备', '副产物', '工作功率'))
        self.setRowCount(10)
        self.setCellWidget(0, 0, RequirementTableItem(self.material_count, []))
        self.setCellWidget(0, 1, RequirementTableItem(self.facility_count, []))
        self.setCellWidget(0, 2, RequirementTableItem(self.byproduct_count, []))
        self.setCellWidget(0, 3, RequirementPowerWidget(99999))
        self.horizontalHeader().resizeSections()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setStretchLastSection(True)
        self.setFixedSize(self.sizeHint())
        self.setRowCount(0)

    def show_requirements(self, requirements):
        self.setRowCount(len(requirements))
        row_index = 0
        for req in requirements:
            self.show_things(req.materials_list(), row_index, 0, self.material_count)
            self.show_things(req.facilities(), row_index, 1, self.facility_count)
            self.show_things(req.byproducts_list(), row_index, 2, self.byproduct_count)
            self.show_power(req.work_consumption(), row_index, 3)
            row_index += 1
        self.horizontalHeader().resizeSections()


class RequirementTableFive(RequirementTableWidget):
    product_count = 1
    material_count = 5
    facility_count = 5
    byproduct_count = 1

    def __init__(self, parent=None):
        super(RequirementTableFive, self).__init__(parent)
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(('产物', '所需原料', '所需设备', '副产物', '工作功率'))
        self.setRowCount(10)
        self.setCellWidget(0, 0, RequirementTableItem(self.product_count, []))
        self.setCellWidget(0, 1, RequirementTableItem(self.material_count, []))
        self.setCellWidget(0, 2, RequirementTableItem(self.facility_count, []))
        self.setCellWidget(0, 3, RequirementTableItem(self.byproduct_count, []))
        self.setCellWidget(0, 4, RequirementPowerWidget(99999))
        self.horizontalHeader().resizeSections()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setStretchLastSection(True)
        self.setFixedSize(self.sizeHint())
        self.setRowCount(0)

    def show_requirements(self, requirements):
        self.setRowCount(len(requirements))
        row_index = 0
        for req in requirements:
            self.show_things(req.product_list(), row_index, 0, self.product_count)
            self.show_things(req.materials_list(), row_index, 1, self.material_count)
            self.show_things(req.facilities(), row_index, 2, self.facility_count)
            self.show_things(req.byproducts_list(), row_index, 3, self.byproduct_count)
            self.show_power(req.work_consumption(), row_index, 4)
            row_index += 1
        self.horizontalHeader().resizeSections()


# 计算窗体
class CalculateWindow(QDialog):
    win_id = 0
    all_windows = {}
    style_sheet = '''
         QLabel {
            color: #989898;
            font-size: 9pt;
            qproperty-alignment: "AlignCenter";
        }
    '''

    def __init__(self, thing, value, parent=None):
        super(CalculateWindow, self).__init__(parent)
        self._thing = thing
        self.w_id = self.win_id

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # 无帮助按钮
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)  # 窗体大小固定
        self.setStyleSheet(self.style_sheet)
        self.setWindowTitle(thing.name)
        self.setWindowIcon(QIcon(os.path.join(PICTURES_FOLDER, thing.icon)))

        self.btn_product = MTipsButton(self)
        self.btn_product.set_thing(thing)
        self.lbl_unit = QLabel('/min', self)
        self.ldt_production_speed = QLineEdit(self)
        self.ldt_production_speed.setText(str(value))
        self.btn_calculate = QPushButton('计算', self)
        self.btn_calculate.setObjectName('TextButton')
        self.btn_settings = QPushButton('隐藏设置', self)
        self.btn_settings.setObjectName('TextButton')
        self.btn_switch_table = QPushButton('切换表格', self)
        self.btn_switch_table.setObjectName('TextButton')

        self.wgt_settings = SettingsWidget(self)
        self.wgt_requirements = QWidget(self)
        self.tbw_current_requirement_table = RequirementTableFour(self)
        self.tbw_different_requirement_table = RequirementTableFive(self)

        self.btn_product.setFixedSize(QSize(50, 50))
        self.btn_product.setIconSize(QSize(50, 50))
        self.ldt_production_speed.setFixedWidth(60)
        self.ldt_production_speed.setValidator(QRegExpValidator(QRegExp(r"[0-9]+.[0-9]+")))
        self.btn_calculate.setDefault(True)
        self.btn_calculate.setCursor(Qt.PointingHandCursor)
        self.btn_settings.setCursor(Qt.PointingHandCursor)
        self.btn_switch_table.setCursor(Qt.PointingHandCursor)

        self.hbl_topbar = QHBoxLayout()
        self.hbl_topbar.addWidget(self.btn_product)
        self.hbl_topbar.addWidget(self.ldt_production_speed)
        self.hbl_topbar.addWidget(self.lbl_unit)
        self.hbl_topbar.addSpacing(10)
        self.hbl_topbar.addWidget(self.btn_calculate)
        self.hbl_topbar.addStretch(1)
        self.hbl_topbar.addWidget(self.btn_settings)
        self.hbl_topbar.addSpacing(10)
        self.hbl_topbar.addWidget(self.btn_switch_table)

        self.vbl_requirements = QVBoxLayout(self.wgt_requirements)
        self.vbl_requirements.setContentsMargins(0, 0, 0, 0)
        self.vbl_requirements.addWidget(MHLine2(self))
        self.vbl_requirements.addWidget(self.tbw_current_requirement_table)
        self.vbl_requirements.addWidget(self.tbw_different_requirement_table)
        self.wgt_requirements.resize(self.vbl_requirements.sizeHint())

        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.addLayout(self.hbl_topbar)
        self.vbl_widget.addWidget(self.wgt_settings)
        self.vbl_widget.addWidget(self.wgt_requirements)
        self.resize(self.vbl_widget.sizeHint())

        self.btn_calculate.clicked.connect(self.start_calculate)
        self.btn_settings.clicked.connect(self.switch_settings_visible)
        self.btn_switch_table.clicked.connect(self.switch_table)

        self.tbw_current_requirement_table.setVisible(True)
        self.tbw_different_requirement_table.setVisible(False)
        self.wgt_requirements.setVisible(False)
        self.wgt_settings.setVisible(True)
        self.setFixedHeight(self.vbl_widget.sizeHint().height())
        self.show()

    @classmethod
    def new_window(cls, thing, value=60, parent=None):
        if not isinstance(value, (int, float)) or value < 0:
            value = 60

        new_win = cls(thing, value, parent)
        cls.all_windows[cls.win_id] = new_win
        cls.win_id += 1
        return new_win

    def start_calculate(self):
        self.btn_calculate.setEnabled(False)
        self.wgt_settings.activate_settings()

        speed = float(self.ldt_production_speed.text() or 0)
        results, results2 = ThingsMgr.inst().calcu_requirements(self._thing, speed)

        self.tbw_current_requirement_table.show_requirements(results)
        self.tbw_different_requirement_table.show_requirements(results2)

        self.wgt_requirements.setVisible(True)
        self.wgt_settings.setVisible(False)
        self.btn_settings.setText('显示设置')
        self.setFixedHeight(self.vbl_widget.sizeHint().height())
        self.btn_calculate.setEnabled(True)

    def switch_table(self):
        if self.tbw_current_requirement_table.isVisible():
            self.tbw_current_requirement_table.setVisible(False)
            self.tbw_different_requirement_table.setVisible(True)
        else:
            self.tbw_current_requirement_table.setVisible(True)
            self.tbw_different_requirement_table.setVisible(False)

    def switch_settings_visible(self, event=None):
        if self.wgt_settings.isVisible():
            self.wgt_settings.setVisible(False)
            self.btn_settings.setText('显示设置')
        else:
            self.wgt_settings.setVisible(True)
            self.btn_settings.setText('隐藏设置')

        self.setFixedHeight(self.vbl_widget.sizeHint().height())

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.setParent(None)
        self.destroy()
        self.all_windows[self.w_id] = None


# 公式两边的物品
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

    def __init__(self, thing, count, can_tips=True, parent=None):
        super(FormulaThingWidget, self).__init__(parent)
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        self._can_tips = can_tips
        self.set_thing(thing)
        self.lbl_count = QLabel(str(count), self)
        self.lbl_count.setStyleSheet(self.value_style)
        self.vbl_widget = QVBoxLayout(self)
        self.vbl_widget.addWidget(self.lbl_count)
        self.vbl_widget.setContentsMargins(0, 0, 0, 0)


# 公式中间的箭头部分
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

    def __init__(self, formula, can_tips=True, parent=None):
        super(FormulaTimeWidget, self).__init__(parent)
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        self.set_icon('箭头.png')
        time_text = ''
        if isinstance(formula.time, (int, float)) and formula.time > 0:
            time_text = str(formula.time)+'s'
        elif formula.time_str:
            time_text = formula.time_str
        self.lbl_time = QLabel(time_text, self)
        self.lbl_time.setStyleSheet(self.time_style)
        self.btn_facility = MTipsButton(self)
        self.btn_facility.setFixedSize(QSize(20, 20))
        self.btn_facility.setIconSize(QSize(20, 20))
        self.btn_facility.set_thing(formula.facility)
        self.btn_facility.disableTooltips(can_tips)

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


# 显示一条完整的公式
class FormulaWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, formula, has_tip=False, parent=None):
        super(FormulaWidget, self).__init__(parent)
        self._formula = formula
        self.left_pressed = False
        self.hbl_widget = QHBoxLayout(self)
        self.hbl_widget.setSpacing(0)
        self.hbl_widget.addStretch(1)
        for thing, count in formula.products:
            item = FormulaThingWidget(thing, count, has_tip)
            item.clicked.connect(self.clicked.emit)
            self.hbl_widget.addWidget(item)

        item_time = FormulaTimeWidget(formula, has_tip)
        item_time.clicked.connect(self.clicked.emit)
        self.hbl_widget.addWidget(item_time)

        for thing, count in formula.materials:
            item = FormulaThingWidget(thing, count, has_tip)
            item.clicked.connect(self.clicked.emit)
            self.hbl_widget.addWidget(item)

        self.hbl_widget.addStretch(1)
        self.hbl_widget.setContentsMargins(0, 0, 0, 0)
        self.hbl_widget.setSpacing(0)
        self.resize(self.hbl_widget.sizeHint())

    def formula(self):
        return self._formula

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_pressed = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.left_pressed:
            self.clicked.emit()
        self.left_pressed = False


# 鼠标悬浮提示框中显示属性的组件
class AttributeWidget(QWidget):
    style_sheet = '''
        #AttributeName {
            font-size: 9pt;
            color: #aaaaaa;
            qproperty-alignment: "AlignLeft";
        }
        #AttributeValue {
            font-size: 9pt;
            color: #dddddd;
            qproperty-alignment: "AlignRight";
        }
    '''

    def __init__(self, parent=None):
        super(AttributeWidget, self).__init__(parent)
        self.setStyleSheet(self.style_sheet)
        self.lbl_work_speed = QLabel('', self)
        self.lbl_work_consumption = QLabel('工作功率', self)
        self.lbl_idle_consumption = QLabel('待机功率', self)
        self.lbl_power = QLabel('发电功率', self)
        self.lbl_input_power = QLabel('输入功率', self)
        self.lbl_output_power = QLabel('输出功率', self)
        self.lbl_basic_generation = QLabel('基础发电功率', self)
        self.lbl_max_charging_power = QLabel('最大充能功率', self)

        self.lbl_work_speed_value = QLabel('', self)
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
        self.gdl_widget.setHorizontalSpacing(20)

        self._labels = [
            ['', self.lbl_work_speed, self.lbl_work_speed_value],
            ['work_consumption', self.lbl_work_consumption, self.lbl_work_consumption_value],
            ['idle_consumption', self.lbl_idle_consumption, self.lbl_idle_consumption_value],
            ['power', self.lbl_power, self.lbl_power_value],
            ['input_power', self.lbl_input_power, self.lbl_input_power_value],
            ['output_power', self.lbl_output_power, self.lbl_output_power_value],
            ['basic_generation', self.lbl_basic_generation, self.lbl_basic_generation_value],
            ['max_charging_power', self.lbl_max_charging_power, self.lbl_max_charging_power_value]
        ]

        self._attrs = {
            'transport_speed': {'attr_name': '运载量', 'unit': '/s'},
            'collecting_speed': {'attr_name': '开采速度', 'unit': '/min 每矿脉'},
            'collecting_speed_2': {'attr_name': '采集速度', 'unit': '/min'},
            'cycle_speed': {'attr_name': '往返速度', 'unit': ' 往返/秒/格'},
            'production_speed': {'attr_name': '制造速度', 'unit': 'x'},
        }

        row = 0
        for attr, label_name, label_value in self._labels:
            label_name.setObjectName('AttributeName')
            label_value.setObjectName('AttributeValue')
            self.gdl_widget.addWidget(label_name, row, 0)
            self.gdl_widget.addWidget(label_value, row, 1)
            row += 1

        self.resize(self.gdl_widget.sizeHint())
        self.on_hide()

    def on_show(self, thing):
        flag = False
        for attr, label_name, label_value in self._labels:
            value = getattr(thing, attr, None)
            if value and value > 0:
                label_name.setVisible(True)
                label_value.setVisible(True)
                label_value.setText(trans_power(value))
                flag = True
            else:
                label_name.setVisible(False)
                label_value.setVisible(False)

        for attr, data in self._attrs.items():
            value = getattr(thing, attr, None)
            if value is not None:
                self.lbl_work_speed.setText(data['attr_name'])
                if isinstance(value, str):
                    self.lbl_work_speed_value.setText(value)
                else:
                    self.lbl_work_speed_value.setText('%s%s' % (str(value), data['unit']))
                self.lbl_work_speed.setVisible(True)
                self.lbl_work_speed_value.setVisible(True)
                flag = True

        if flag:
            self.setVisible(True)

    def on_hide(self):
        self.setVisible(False)


# 鼠标悬浮提示框
class ThingTooltipWindow(QFrame):
    _inst = None
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
        self.timer_show = QTimer(self)
        self._thing = None
        self._count = None
        self.pos = None
        self.lbl_name = QLabel(self)
        self.lbl_name.setStyleSheet(self.name_style)
        self.lbl_count = QLabel(self)
        self.lbl_count.setStyleSheet(self.count_style)
        self.wgt_attribute = AttributeWidget(self)
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
        self.vbl_window.addWidget(self.wgt_attribute)
        self.vbl_window.addWidget(self.line)
        self.vbl_window.addWidget(self.lbl_text)
        self.vbl_window.addLayout(self.hbl_formulas)
        self.timer_show.timeout.connect(self.on_show)

    def delay_show(self, thing, pos, count=None):
        self._thing = thing
        self.pos = pos
        self._count = count
        self.timer_show.start(300)

    def show_relevant_formula(self, thing, pos):
        self._thing = thing
        self.pos = pos
        self._count = None
        self.on_show(True)

    def on_show(self, relevant=False):
        self.timer_show.stop()
        if not isinstance(self._thing, Thing):
            return
        if self.isVisible():
            self.on_hide()
        self.lbl_name.setText(self._thing.name)
        if self._count:
            self.lbl_count.setText(' x '+str(self._count))
            self.lbl_count.setVisible(True)

        self.wgt_attribute.on_show(self._thing)
        if relevant:
            formulas = self._thing.material_formulas()
            text = '相关公式：'
        else:
            formulas = self._thing.product_formulas()
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
        self.wgt_attribute.on_hide()
        self.line.setVisible(False)
        self.lbl_text.setVisible(False)
        for row in range(self.vbl_formulas.count()):
            widget = self.vbl_formulas.itemAt(0).widget()
            if widget:
                self.vbl_formulas.removeWidget(widget)
                widget.deleteLater()
        self.hide()

    @classmethod
    def inst(cls, parent=None):
        if cls._inst is None:
            cls._inst = cls(parent)
        return cls._inst


def trans_power(value):
    if value >= 1000000000:
        return '%.2f TW' % (value / 1000000000)
    elif value >= 1000000:
        return '%.2f GW' % (value / 1000000)
    elif value >= 1000:
        return '%.2f MW' % (value / 1000)
    else:
        return '%d kW' % value


class Thing(object):
    def __init__(self, name, icon='', row=-1, col=-1):
        self.name = name
        self.icon = icon
        self.row = row
        self.col = col

        self._selected_formula = None
        self._product_formulas = []
        self._material_formulas = []

    def selected_formula(self):
        if self._selected_formula:
            return self._selected_formula
        elif len(self._product_formulas) > 0:
            return self._product_formulas[0]
        else:
            return None

    def set_selected_formula(self, formula):
        if formula is not None and formula in self._product_formulas:
            self._selected_formula = formula

    def product_formulas(self):
        return self._product_formulas

    def append_product_formula(self, formula):
        if formula not in self._product_formulas:
            self._product_formulas.append(formula)

    def material_formulas(self):
        return self._material_formulas

    def append_material_formula(self, formula):
        if formula not in self._material_formulas:
            self._material_formulas.append(formula)

    def calcu_requirement(self, speed, check=False):
        formula = self.selected_formula()
        if formula:
            return formula.calcu_requirement(self, speed, check)

        return None


class Component(Thing):
    def __init__(self, name, icon='', row=-1, col=-1, exclude=None):
        super(Component, self).__init__(name, icon, row, col)
        self.exclude = exclude


class Building(Thing):
    def __init__(self, name, icon='', row=-1, col=-1, facility_type=None, work_consumption=None, idle_consumption=None,
                 power=None, input_power=None, output_power=None, basic_generation=None, max_charging_power=None,
                 transport_speed=None, collecting_speed=None, collecting_speed_2=None, cycle_speed=None,
                 production_speed=None, origin=None, mineral=None):
        super(Building, self).__init__(name, icon, row, col)
        self.facility_type = facility_type
        self.work_consumption = work_consumption
        self.idle_consumption = idle_consumption
        self.power = power
        self.input_power = input_power
        self.output_power = output_power
        self.basic_generation = basic_generation
        self.max_charging_power = max_charging_power
        self.transport_speed = transport_speed
        self.collecting_speed = collecting_speed
        self.collecting_speed_2 = collecting_speed_2
        self.cycle_speed = cycle_speed
        self.production_speed = production_speed
        self.origin = origin
        self.mineral = mineral


class Formula(object):
    mineral_level = 0
    facility_selected = {'smelting': '电弧熔炉', 'assembler': '制造台MK.I', 'chemical': '化工厂', 'research': '矩阵研究站'}

    def __init__(self, products, materials, time=-1, facility=None, recipe=None, relation=None, time_str=None):
        self.products = []      # [(thing1, count1), (thing2, count2), ...]
        self.materials = []
        self.time = time
        self.facility = None
        self.recipe = None
        self.relation = None
        self.time_str = time_str

        for name, count in products.items():
            thing = ThingsMgr.inst().get_thing(name)
            thing.append_product_formula(self)
            self.products.append((thing, count))

        for name, count in materials.items():
            thing = ThingsMgr.inst().get_thing(name)
            thing.append_material_formula(self)
            self.materials.append((thing, count))

        if facility:
            self.facility = ThingsMgr.inst().get_thing(facility)

        if recipe:
            self.recipe = ThingsMgr.inst().get_thing(recipe)
            self.recipe.append_product_formula(self)

        if relation:
            self.relation = ThingsMgr.inst().get_thing(relation)

    # 计算每分钟的产物、原料和设备数量，speed为每分钟产物thing的生产数量
    def calcu_requirement(self, product, speed, check=False):
        if self.recipe == product:
            product = self.relation

        if check and (product.exclude or self.facility.origin):
            return None

        requirement = Requirement(product.name, speed)
        product_count = None
        for item, count in self.products:
            if item.name == product.name:
                product_count = count
                break

        facility_count = 0
        if isinstance(self.time, (int, float)) and self.time > 0:
            facility_count = (speed * self.time) / (product_count * 60.0)

        if self.facility.mineral:
            facility_count = facility_count / (1 + 0.1 * self.mineral_level)

        use_facility = self.facility
        if self.facility.facility_type in self.facility_selected:
            use_facility = ThingsMgr.inst().get_thing(self.facility_selected[self.facility.facility_type])
            facility_count = facility_count / use_facility.production_speed

        requirement.add_facility([use_facility.name, facility_count])

        materials_count = {}
        for item, count in self.materials:
            materials_count[item.name] = count * speed / product_count

        requirement.add_materials(materials_count)

        byproducts_count = {}
        for item, count in self.products:
            if item != product:
                byproducts_count[item.name] = count * speed / product_count

        return requirement


class Requirement(object):
    def __init__(self, product=None, count=0):
        self.product = product
        self.count = count
        self._materials = {}        # {name1: count1, name2: count2, ...}
        self._facilities = []       # [[name1, count1], [name2, count2], ...]
        self._byproducts = {}

    def product_list(self):
        if self.product:
            return [(self.product, self.count)]
        return []

    def materials(self):
        return self._materials

    def materials_list(self):
        return list(self._materials.items())

    def add_materials(self, data):
        for name, count in data.items():
            self._materials[name] = self._materials.get(name, 0) + count

    def byproducts(self):
        return self._byproducts

    def byproducts_list(self):
        return list(self._byproducts.items())

    def add_byproducts(self, data):
        for name, count in data.items():
            self._byproducts[name] = self._byproducts.get(name, 0) + count

    def facilities(self):
        return self._facilities

    def add_facilities(self, data):
        self._facilities.extend(data)

    def add_facility(self, data):
        self._facilities.append(data)

    def merge_facilities(self, data):
        if len(data) == 1 and len(self._facilities) == len(data):
            self._facilities[0][1] += data[0][1]
        else:
            self.add_facilities(data)

    def merge_requirement(self, requirement, merge=False):
        self.add_materials(requirement.materials())
        self.add_byproducts(requirement.byproducts())
        if merge and self.product and self.product == requirement.product:
            self.count += requirement.count
            self.merge_facilities(requirement.facilities())
        else:
            self.add_facilities(requirement.facilities())

    def work_consumption(self, max_=False):
        total = 0
        for name, count in self._facilities:
            thing = ThingsMgr.inst().get_thing(name)
            if thing.work_consumption:
                total += thing.work_consumption * (math.ceil(count) if max_ else count)
        return total


class ThingsMgr(object):
    _inst = None

    def __init__(self):
        self._all_things = {}
        self._components = {}
        self._others = {}
        self._buildings = {}
        self._items = {}
        self._all_formulas = []

    def load_things(self):
        with open(os.path.join(FILES_FOLDER, 'Components.json'), 'r', encoding='utf-8') as file:
            for name, data in json.load(file).items():
                self._components[name] = Component(name, **data)

        with open(os.path.join(FILES_FOLDER, 'OtherComponents.json'), 'r', encoding='utf-8') as file:
            for name, data in json.load(file).items():
                self._others[name] = Component(name, **data)

        with open(os.path.join(FILES_FOLDER, 'Buildings.json'), 'r', encoding='utf-8') as file:
            for name, data in json.load(file).items():
                self._buildings[name] = Building(name, **data)

        self._items.update(self._components)
        self._items.update(self._others)
        self._all_things.update(self._components)
        self._all_things.update(self._buildings)
        self._all_things.update(self._others)

    def load_formulas(self):
        with open(os.path.join(FILES_FOLDER, 'Formulas.json'), 'r', encoding='utf-8') as file:
            for data in json.load(file):
                self._all_formulas.append(Formula(**data))

    def components(self):
        return self._components

    def buildings(self):
        return self._buildings

    def others(self):
        return self._others

    def get_thing(self, name):
        thing = self._all_things.get(name)
        if thing is None:
            print('get_thing', name)
        return thing

    def get_multi_formula_things(self):
        temp = []
        for thing in self._all_things.values():
            if len(thing.product_formulas()) > 1:
                temp.append(thing)
        return temp

    def get_by_facility_type(self, facility_type):
        temp = []
        for thing in self._buildings.values():
            if facility_type == thing.facility_type:
                temp.append(thing)
        return temp

    def calcu_requirements(self, product, speed):
        if product.selected_formula() is None:
            return None

        result = self.calcu_all_requirements({product.name: speed})
        current_requirement_list = []
        different_requirements = {}
        if len(result) == 1:
            return [product.calcu_requirement(speed)], []

        final_requirement = Requirement()
        for current_result in result:
            requirement = Requirement()
            for data in current_result:
                req = data[2]
                if req:
                    requirement.merge_requirement(req)
                    if req.product in different_requirements:
                        different_requirements[req.product].merge_requirement(req, True)
                    else:
                        different_requirements[req.product] = req
                    final_requirement.add_byproducts(req.byproducts())
                else:
                    final_requirement.add_materials({data[0]: data[1]})

            current_requirement_list.append(requirement)

        different_final_requirement = Requirement(product.name, speed)
        different_requirements = list(different_requirements.values())
        for req in different_requirements:
            different_final_requirement.merge_requirement(req)
            final_requirement.add_facilities(req.facilities())

        current_requirement_list.append(final_requirement)
        different_requirements.append(Requirement())
        different_requirements.append(different_final_requirement)
        return current_requirement_list, different_requirements

    def calcu_all_requirements(self, products, all_requirements=None):
        if all_requirements is None:
            all_requirements = []

        requirements = []
        materials = {}
        for name, count in products.items():
            thing = self.get_thing(name)
            req = thing.calcu_requirement(count, True)
            if req:
                for name2, count2 in req.materials_list():
                    materials[name2] = materials.get(name2, 0) + count2

            requirements.append((name, count, req))

        all_requirements.append(requirements)
        if materials:
            return self.calcu_all_requirements(materials, all_requirements)
        else:
            return all_requirements

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = cls()
        return cls._inst


if __name__ == '__main__':
    # 必须先加载物品再加载公式
    ThingsMgr.inst().load_things()
    ThingsMgr.inst().load_formulas()

    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    ThingTooltipWindow.inst()
    win = MainWindow()
    win.show()  # 显示主窗体
    sys.exit(app.exec_())
