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

    def __init__(self, thing=None, parent=None):
        super(ThingsTableItem, self).__init__(parent)
        self.setFixedSize(self.size)
        self.setIconSize(self.image_size)
        self.set_thing(thing)
        self.clicked.connect(self.open_calculation)

    def open_calculation(self):
        if self._thing:
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

    def activate_settings(self, event):
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

    def __init__(self, name=None, picture=None, value=None, parent=None):
        super(RequirementThingWidget, self).__init__(parent)
        self.setFixedSize(self.size)
        self.name = name
        self.value = value
        self._thing = None
        self.btn_image = MTipsButton(self)
        self.lbl_value = QLabel(self)
        count_text = '%.2f' % value if value >= 0 else '不定'
        self.lbl_value.setStyleSheet(self.value_style)
        self.lbl_value.setText(count_text)
        self.btn_image.setFixedSize(self.image_size)
        self.btn_image.setIconSize(self.image_size)
        self.btn_image.set_thing(name)
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
        if self._thing:
            wnd_cal = CalculateWindow.new_window(self._thing, round(self.value, 2))
        #    wnd_cal.start_calculate()


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
            picture = ThingsMgr.inst().get_icon(name)
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


# 计算窗体
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

    def __init__(self, parent=None):
        super(CalculateWindow, self).__init__(parent)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)  # 无帮助按钮
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint, True)  # 窗体大小固定
        self.setStyleSheet(self.style_sheet)
        self.btn_product = MTipsButton(self)
        self.lbl_unit = QLabel('/min', self)
        self.ldt_production_speed = QLineEdit(self)
        self.btn_calculate = QPushButton('计算', self)
        self.btn_calculate.setObjectName('TextButton')
        self.btn_settings = QPushButton('隐藏设置', self)
        self.btn_settings.setObjectName('TextButton')
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

        self._thing = None
        self.w_id = self.win_id
        self.btn_calculate.clicked.connect(self.start_calculate)
        self.btn_settings.clicked.connect(self.show_settings_widget)

    @classmethod
    def new_window(cls, thing, value=60, parent=None):
        if not isinstance(value, (int, float)) or value < 0:
            value = 60
        try:
            new_win = cls(parent)
            cls.all_windows[cls.win_id] = new_win
            cls.win_id += 1
            new_win.on_show(thing, value)
            return new_win
        except ex:
            print(str(ex))

    def on_show(self, thing, value=60):
        self._thing = thing
        self.setWindowTitle(thing.name)
        self.setWindowIcon(QIcon(os.path.join(PICTURES_FOLDER, thing.icon)))
        self.btn_product.set_thing(thing)
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
            requirements, result = ProductMgr.inst().calculate(self._thing, speed)
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

    def show_settings_widget(self, event):
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

    def __init__(self, formula, can_tips=True,parent=None):
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
        for thing, count in formula.product:
            item = FormulaThingWidget(thing, count, has_tip)
            item.clicked.connect(self.clicked.emit)
            self.hbl_widget.addWidget(item)

        item_time = FormulaTimeWidget(formula, has_tip)
        item_time.clicked.connect(self.clicked.emit)
        self.hbl_widget.addWidget(item_time)

        for thing, count in formula.material:
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
        self.formulas_mgr = FormulasMgr.inst()
        self.timer_show = QTimer(self)
        self._thing = None
        self.count = None
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
        self.count = count
        self.timer_show.start(300)

    def show_relevant_formula(self, thing, pos):
        self._thing = thing
        self.pos = pos
        self.count = None
        self.on_show(True)

    def on_show(self, relevant=False):
        self.timer_show.stop()
        if not isinstance(self._thing, Thing):
            return
        if self.isVisible():
            self.on_hide()
        self.lbl_name.setText(self._thing.name)
        if self.count:
            self.lbl_count.setText(' x '+str(self.count))
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
    def __init__(self, name, icon='', row=-1, col=-1, facility_type=None, work_consumption=None, idle_consumption=None,
                 power=None, input_power=None, output_power=None, basic_generation=None, max_charging_power=None,
                 transport_speed=None, collecting_speed=None, collecting_speed_2=None, cycle_speed=None,
                 production_speed=None, exclude=None, origin=None):
        self.name = name
        self.icon = icon
        self.row = row
        self.col = col
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
        self.exclude = exclude
        self.origin = origin

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


class Formula(object):
    mineral_level = 0
    facility_selected = {'smelting': '电弧熔炉', 'assembler': '制造台MK.I', 'chemical': '化工厂', 'research': '矩阵研究站'}

    def __init__(self, product, material, time=0, facility=None, recipe=None):
        self.product = []
        self.material = []
        self.time = time
        self.facility = None
        self.recipe = None

        for name, count in product.items():
            thing = ThingsMgr.inst().get_thing(name)
            thing.append_product_formula(self)
            self.product.append((thing, count))

        for name, count in material.items():
            thing = ThingsMgr.inst().get_thing(name)
            thing.append_material_formula(self)
            self.material.append((thing, count))

        if facility:
            self.facility = ThingsMgr.inst().get_thing(facility)

        if recipe:
            self.recipe = ThingsMgr.inst().get_thing(recipe)
            self.recipe.append_product_formula(self)


class ThingsMgr(object):
    _inst = None

    def __init__(self):
        self._all_things = {}
        self._components = {}
        self._others = {}
        self._buildings = {}
        self._items = {}
        self._all_formulas = []

        self.assembler_level = '制造台MK.II' #??

    def load_things(self):
        with open(os.path.join(FILES_FOLDER, 'Components.json'), 'r', encoding='utf-8') as file:
            for name, data in json.load(file).items():
                self._components[name] = Thing(name, **data)
        with open(os.path.join(FILES_FOLDER, 'Buildings.json'), 'r', encoding='utf-8') as file:
            for name, data in json.load(file).items():
                self._buildings[name] = Thing(name, **data)
        with open(os.path.join(FILES_FOLDER, 'Others.json'), 'r', encoding='utf-8') as file:
            for name, data in json.load(file).items():
                self._others[name] = Thing(name, **data)

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

    def get_icon(self, name):  #??
        return self._all_things.get(name).icon

    def get_work_consumption(self, name):  #??
        return self._all_things.get(name).work_consumption

    def is_exclude_product(self, name):  #??
        return not not self._items.get(name).exclude

    def is_origin_facility(self, name):  #??
        return not not self._buildings.get(name).origin

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = cls()
        return cls._inst


class Formula2(object):
    def __init__(self, data):
        self.things_mgr = ThingsMgr.inst()
        self.product = {}
        self.material = {}
        self.time = 0
        self.facility = None
        self.recipe = None
        self.__dict__.update(data)

    def has_product(self, name):
        return name in self.product

    def get_requirement(self, product_name, speed):
        if (not isinstance(self.time, (int, float)) or self.time < 0 or
                self.things_mgr.is_exclude_product(product_name) or
                self.things_mgr.is_origin_facility(self.facility)):
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
            speed = speed / (1 + Formula.mineral_level * 0.1)
            material_speed = dict([(name, speed * num / product_num) for name, num in self.material.items()])
            miner_count = 0
            for value in material_speed.values():
                miner_count += int(value / 6 + 0.5) or 1
            facility_num = [{self.facility: miner_count}]
        elif self.facility == '抽水站':
            speed = speed / (1 + Formula.mineral_level * 0.1)
            facility_num = [{self.facility: speed * self.time / product_num / 60}]
        elif self.facility == '制造台MK.II':
            if self.things_mgr.assembler_level == '制造台MK.I':
                speed = speed / 0.75
            elif self.things_mgr.assembler_level == '制造台MK.III':
                speed = speed / 1.5
            facility_num = [{self.things_mgr.assembler_level: speed * self.time / product_num / 60}]
        return Requirement(material_speed, facility_num, byproduct_num)


class FormulasMgr(object):
    _inst = None

    def __init__(self):
        self._all_formulas = []
        self._product_formulas = {}
        self._material_formulas = {}
        self._recipe_formulas = {}
        self._multi_formulas = {}
        self._selected_formulas = {}
        with open(os.path.join(FILES_FOLDER, 'Formulas.json'), 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        for data in json_data:
            formula = Formula2(data)
            self._all_formulas.append(formula)
            for name in formula.product:
                res = self._product_formulas.get(name, [])
                res.append(formula)
                self._product_formulas[name] = res
            for name in formula.material:
                res = self._material_formulas.get(name, [])
                res.append(formula)
                self._material_formulas[name] = res
            if formula.recipe:
                res = self._recipe_formulas.get(formula.recipe, [])
                res.append(formula)
                self._recipe_formulas[formula.recipe] = res

        for name, formulas in self._product_formulas.items():  # 获取有多条合成公式的组件
            if len(formulas) > 1:
                self._multi_formulas[name] = formulas
                self._selected_formulas[name] = 0

    def get_formulas_by_product(self, name):
        return self._product_formulas.get(name, [])

    def get_formulas_by_material(self, name):
        return self._material_formulas.get(name, [])

    def get_formulas_by_recipe(self, recipe):
        return self._recipe_formulas.get(recipe, [])

    def get_requirements(self, product_name, production_speed):
        result = []
        formulas = self._product_formulas.get(product_name, [])
        if len(formulas) > 0:
            formula = formulas[self._selected_formulas.get(product_name, 0)]
            req = formula.get_requirement(product_name, production_speed)
            if req:
                result.append(req)
        return result

    # 获取所有多产物的合成公式
    def get_multi_products(self):
        result = []
        for formula in self._all_formulas:
            if len(formula.product) > 1:
                result.append(formula)
        return result

    def get_multi_formulas(self, name):
        return self._multi_formulas.get(name, [])

    def all_multi_formulas(self):
        return list(self._multi_formulas.items())

    def set_selected_formula(self, name, value):
        if name in self._selected_formulas:
            self._selected_formulas[name] = value

    def get_selected_formula(self, name):
        return self._selected_formulas.get(name, 0)

    @classmethod
    def inst(cls):
        if cls._inst is None:
            cls._inst = cls()
        return cls._inst


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
        self.things_mgr = ThingsMgr.inst()

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
    _inst = None

    def __init__(self):
        self.formulas_mgr = FormulasMgr.inst()
        self.things_mgr = ThingsMgr.inst()
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
