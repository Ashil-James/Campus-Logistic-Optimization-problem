# Campus City Logistics -- Supply Distribution Optimization

---

## 📌 Problem Statement

As an optimization analyst at **Campus City Logistics**, the objective
is to design an optimal supply distribution network for essential
resources across campus facilities. The current ad-hoc distribution
system is inefficient and costly.

### 🎯 Goal

Determine the optimal warehouse locations and distribution plan that: -
Minimizes total annual cost - Meets all facility demands - Respects
warehouse capacity constraints - Operates within the allocated annual
budget

---

## 📊 Dataset Overview

### 🏫 Facilities Data

Six critical campus facilities were selected:

Facility ID Facility Name Type Daily Demand (Units)

---

MED_CENTER Campus Medical Center Hospital \~80
ENG_BUILDING Engineering Building Academic \~30
SCIENCE_HALL Science Hall Academic \~28--35
DORM_A North Dormitory Residential \~49--55
DORM_B South Dormitory Residential \~45--51
LIBRARY Main Library Academic \~25--30

**Total Daily Demand ≈ 269--270 Units/Day**

---

### 🏭 Warehouse Data

---

Warehouse ID Warehouse Name Daily Capacity Construction Operational
(Units) Cost Cost / Day

---

WH_NORTH North Campus 400 \$300,000 \$800
Warehouse

WH_SOUTH South Campus 350 \$280,000 \$700
Warehouse

WH_EAST East Gate 450 \$320,000 \$900
Warehouse

---

**Total Capacity = 1200 Units/Day**

---

### 🚚 Transportation Costs

- Cost Range ≈ **\$3.4 -- \$4.7 per unit**
- Based on geographic distance calculations

---

## 💰 Financial Constraints

Parameter Value

---

Annual Budget \$1,500,000
Planning Period 365 Days
Construction Amortization 10 Years

---

## ⚙️ Business Constraints

- Select **exactly 2 warehouses**
- Meet **100% facility demand**
- Shipment from warehouse ≤ Annual capacity
- Total annual cost ≤ Budget
- Shipment quantities ≥ 0

---

## 🧠 Solution Approach

### Optimization Technique

**Mixed Integer Linear Programming (MILP)** using PuLP

### Decision Variables

Variable Type Meaning

---

Warehouse Selection Binary Open or Close Warehouse
Shipment Quantity Continuous Units shipped Warehouse → Facility

### Objective Function

Minimize:

    Total Cost = Fixed Cost + Transportation Cost

---

## 🧮 Model Implementation Features

- CSV-based dynamic data loading
- Annual demand and capacity calculation
- Fixed cost amortization
- Real transportation cost integration
- Budget constraint enforcement
- Supply network visualization

---

## 📈 Optimization Results

### 💵 Financial Summary

Metric Value

---

Total Annual Cost \$959,466.05
Fixed Costs \$605,500
Transport Costs \$353,966.05
Remaining Budget \$540,533.95

---

### 🏭 Selected Warehouses

Warehouse Selected

---

WH_NORTH ✅
WH_SOUTH ✅
WH_EAST ❌

---

### 📦 Distribution Plan (Annual Units)

Warehouse Facility Units Shipped

---

WH_NORTH MED_CENTER 29,565
WH_NORTH ENG_BUILDING 10,950
WH_NORTH DORM_A 17,885
WH_NORTH LIBRARY 10,950
WH_SOUTH SCIENCE_HALL 10,220
WH_SOUTH DORM_B 18,615

---

## 📊 Key Insights

- All facility demand fully satisfied
- Warehouses operate below full capacity (cost-efficient)
- WH_EAST excluded due to higher fixed cost vs transport savings
- Solution operates well within budget

---

## 🛠 Technologies Used

Technology Purpose

---

Python Core Programming
PuLP Optimization Modeling
Pandas Data Processing
Matplotlib Visualization

---

## 📌 Conclusion

The MILP optimization model successfully determines the most
cost-effective warehouse selection and supply distribution strategy. The
system is fully data-driven and scalable for real-world logistics
optimization.

---

## 👤 Project

Campus City Logistics Optimization Project
