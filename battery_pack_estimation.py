# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 13:56:14 2024

@author: vsharma
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFormLayout
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt

class CostEstimator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Battery Cost Estimator')
        self.setGeometry(100, 100, 600, 500)

        # Create tab widget
        tabs = QTabWidget()
        cell_tab = QWidget()
        pack_tab = QWidget()

        tabs.addTab(cell_tab, "Cell Cost")
        tabs.addTab(pack_tab, "Pack Cost")

        # Cell Cost Tab
        cell_layout = QVBoxLayout()
        cell_form = QFormLayout()

        # Input fields for cell cost
        self.cell_inputs = {}
        cell_params = [
            ('N', 'Number of cells', '1000000'),
            ('C', 'Cell capacity (Ah)', '10'),
            ('V', 'Nominal voltage (V)', '3.2'),
            ('M_li', 'Lithium carbonate cost ($/kg)', '17.5'),
            ('M_fe', 'Iron phosphate cost ($/kg)', '12.5'),
            ('M_gr', 'Graphite cost ($/kg)', '12.5'),
            ('M_el', 'Electrolyte cost ($/kg)', '12.5'),
            ('M_se', 'Separator cost ($/m²)', '1.5'),
            ('M_cu', 'Copper foil cost ($/kg)', '17.5'),
            ('M_al', 'Aluminum foil cost ($/kg)', '4'),
            ('F', 'Manufacturing cost ($/kWh)', '12.5'),
            ('O', 'Overhead and R&D cost ($/kWh)', '7.5'),
            ('E_D', 'Engineering & Development cost per cell ($)', '1'),
            ('scrap_rate', 'Scrap rate (%)', '10'),
            ('warranty_rate', 'Warranty failure rate (%)', '0.5'),
        ]

        for param, label, default in cell_params:
            self.cell_inputs[param] = QLineEdit()
            self.cell_inputs[param].setAlignment(Qt.AlignRight)
            self.cell_inputs[param].setFixedWidth(100)
            self.cell_inputs[param].setText(default)
            self.cell_inputs[param].setValidator(QDoubleValidator())
            cell_form.addRow(label, self.cell_inputs[param])

        cell_layout.addLayout(cell_form)

        # Calculate button for cell cost
        calc_cell_btn = QPushButton('Calculate Cell Cost')
        calc_cell_btn.clicked.connect(self.calculate_cell_cost)
        cell_layout.addWidget(calc_cell_btn)

        # Result display for cell cost
        self.cell_result = QTextEdit()
        self.cell_result.setReadOnly(True)
        cell_layout.addWidget(self.cell_result)

        cell_tab.setLayout(cell_layout)

        # Pack Cost Tab
        pack_layout = QVBoxLayout()
        pack_form = QFormLayout()

        # Input fields for pack cost
        self.pack_inputs = {}
        pack_params = [
            ('pack_capacity', 'Pack Capacity (kWh)', '60'),
            ('cell_cost', 'Cell Cost ($/kWh)', '100'),
            ('bms_cost', 'BMS Cost ($)', '1000'),
            ('thermal_cost', 'Thermal Management Cost ($)', '500'),
            ('housing_cost', 'Housing Cost ($/kWh)', '10'),
            ('assembly_cost', 'Assembly Cost ($/kWh)', '5'),
            ('overhead_percent', 'Overhead and Profit (%)', '15')
        ]

        for param, label, default in pack_params:
            self.pack_inputs[param] = QLineEdit()
            self.pack_inputs[param].setAlignment(Qt.AlignRight)
            self.pack_inputs[param].setFixedWidth(100)
            self.pack_inputs[param].setText(default)
            self.pack_inputs[param].setValidator(QDoubleValidator())
            pack_form.addRow(label, self.pack_inputs[param])

        pack_layout.addLayout(pack_form)

        # Calculate button for pack cost
        calc_pack_btn = QPushButton('Calculate Pack Cost')
        calc_pack_btn.clicked.connect(self.calculate_pack_cost)
        pack_layout.addWidget(calc_pack_btn)

        # Result display for pack cost
        self.pack_result = QTextEdit()
        self.pack_result.setReadOnly(True)
        pack_layout.addWidget(self.pack_result)

        pack_tab.setLayout(pack_layout)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def calculate_cell_cost(self):
        try:
            # Extract values from inputs
            N = float(self.cell_inputs['N'].text())
            C = float(self.cell_inputs['C'].text())
            V = float(self.cell_inputs['V'].text())
            M_li = float(self.cell_inputs['M_li'].text())
            M_fe = float(self.cell_inputs['M_fe'].text())
            M_gr = float(self.cell_inputs['M_gr'].text())
            M_el = float(self.cell_inputs['M_el'].text())
            M_se = float(self.cell_inputs['M_se'].text())
            M_cu = float(self.cell_inputs['M_cu'].text())
            M_al = float(self.cell_inputs['M_al'].text())
            F = float(self.cell_inputs['F'].text())
            O = float(self.cell_inputs['O'].text())
            E_D = float(self.cell_inputs['E_D'].text())
            scrap_rate = float(self.cell_inputs['scrap_rate'].text()) / 100
            warranty_rate = float(self.cell_inputs['warranty_rate'].text()) / 100

            # Calculate material cost (simplified, assuming usage factors of 1)
            M = M_li + M_fe + M_gr + M_el + M_se + M_cu + M_al

            # Scrap factor
            S = 1 / (1 - scrap_rate)

            # Energy per cell in kWh
            E = C * V / 1000

            # Initial cost calculation without warranty
            initial_cost = ((M + F) * S + O) * E + E_D

            # Iterative calculation for warranty cost
            for _ in range(5):  # 5 iterations should be enough for convergence
                W = warranty_rate * 1.5 * initial_cost
                initial_cost = ((M + F) * S + O) * E + E_D + W

            cost_per_cell = initial_cost
            total_cost = cost_per_cell * N

            result = f"Cost per cell: ${cost_per_cell:.2f}\n"
            result += f"Total cost for {N:,.0f} cells: ${total_cost:,.2f}\n"
            result += f"Cost per kWh: ${(cost_per_cell / E):.2f}/kWh"

            self.cell_result.setText(result)

        except ValueError:
            self.cell_result.setText("Error: Please ensure all inputs are valid numbers.")

    def calculate_pack_cost(self):
        try:
            # Extract values from inputs
            pack_capacity = float(self.pack_inputs['pack_capacity'].text())
            cell_cost = float(self.pack_inputs['cell_cost'].text())
            bms_cost = float(self.pack_inputs['bms_cost'].text())
            thermal_cost = float(self.pack_inputs['thermal_cost'].text())
            housing_cost = float(self.pack_inputs['housing_cost'].text())
            assembly_cost = float(self.pack_inputs['assembly_cost'].text())
            overhead_percent = float(self.pack_inputs['overhead_percent'].text()) / 100

            # Calculate costs
            cell_total = cell_cost * pack_capacity
            housing_total = housing_cost * pack_capacity
            assembly_total = assembly_cost * pack_capacity

            subtotal = cell_total + bms_cost + thermal_cost + housing_total + assembly_total
            overhead = subtotal * overhead_percent
            total_cost = subtotal + overhead

            cost_per_kwh = total_cost / pack_capacity

            result = f"Cell cost: ${cell_total:,.2f}\n"
            result += f"BMS cost: ${bms_cost:,.2f}\n"
            result += f"Thermal management cost: ${thermal_cost:,.2f}\n"
            result += f"Housing cost: ${housing_total:,.2f}\n"
            result += f"Assembly cost: ${assembly_total:,.2f}\n"
            result += f"Subtotal: ${subtotal:,.2f}\n"
            result += f"Overhead: ${overhead:,.2f}\n"
            result += f"Total pack cost: ${total_cost:,.2f}\n"
            result += f"Cost per kWh: ${cost_per_kwh:.2f}/kWh"

            self.pack_result.setText(result)

        except ValueError:
            self.pack_result.setText("Error: Please ensure all inputs are valid numbers.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CostEstimator()
    ex.show()
    sys.exit(app.exec_())