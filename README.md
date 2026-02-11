# Campus City Logistics -- Supply Distribution Optimization

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

### Facilities Data

Six critical campus facilities were selected:

Facility ID Facility Name Type Daily Demand

---

MED_CENTER Campus Medical Center Hospital \~80 units
ENG_BUILDING Engineering Building Academic \~30 units
SCIENCE_HALL Science Hall Academic \~28--35 units
DORM_A North Dormitory Residential \~49--55 units
DORM_B South Dormitory Residential \~45--51 units
LIBRARY Main Library Academic \~25--30 units

Total Daily Demand ≈ **269--270 units/day**

---

### Warehouse Data

---

Warehouse ID Name Daily Capacity Construction Operational
Cost Cost / Day

---

WH_NORTH North Campus 400 \$300,000 \$800
Warehouse

WH_SOUTH South Campus 350 \$280,000 \$700
Warehouse

WH_EAST East Gate 450 \$320,000 \$900
Warehouse

---

Total Capacity = **1200 units/day**

---

### Transportation Costs

- Range ≈ **\$3.4 -- \$4.7 per unit**
- Based on real geographic distance calculations

---

## 💰 Financial Constraints

- Annual Budget = **\$1,500,000**
- Planning Period = **365 days**
- Construction Cost amortized over **10 years**
- All costs annualized

---

## ⚙️ Business Constraints

- Select **exactly 2 warehouses**
- Meet **100% facility demand**
- Warehouse shipment ≤ Annual Capacity
- Total Annual Cost ≤ Budget
- Shipment quantities ≥ 0

---

## 🧠 Solution Approach

### Optimization Technique

Mixed Integer Linear Programming (MILP) using **PuLP**

### Decision Variables

- Binary → Warehouse open/close decision
- Continuous → Shipment quantities

### Objective Function

Minimize:

    Total Cost = Fixed Cost + Transportation Cost

---

## 🧮 Model Implementation Features

✅ CSV-driven data loading\
✅ Annual demand & capacity calculation\
✅ Fixed cost amortization\
✅ Real transportation cost integration\
✅ Budget constraint enforcement\
✅ Visualization of supply network

---

## 📈 Optimization Results

### 💵 Financial Summary

- Total Annual Cost: **\$959,466.05**
- Fixed Costs: **\$605,500**
- Transport Costs: **\$353,966.05**
- Remaining Budget: **\$540,533.95**

---

### 🏭 Warehouse Selection

Selected Warehouses: - ✅ WH_NORTH - ✅ WH_SOUTH - ❌ WH_EAST

---

### 📦 Distribution Plan (Annual Units)

Warehouse Facility Units

---

WH_NORTH MED_CENTER 29,565
WH_NORTH ENG_BUILDING 10,950
WH_NORTH DORM_A 17,885
WH_NORTH LIBRARY 10,950
WH_SOUTH SCIENCE_HALL 10,220
WH_SOUTH DORM_B 18,615

---

## 📊 Key Insights

- Demand fully satisfied for all facilities
- Warehouses operate below full capacity (cost-efficient operation)
- WH_EAST excluded due to higher fixed cost vs transport savings
- Solution well within budget limit

---

## 🛠 Technologies Used

- Python
- PuLP (Optimization)
- Pandas (Data Processing)
- Matplotlib (Visualization)

---

## 📌 Conclusion

The developed MILP optimization model successfully identifies the most
cost-effective warehouse selection and supply distribution strategy. The
model is fully data-driven and scalable for real-world logistics
planning scenarios.

---

## 👤 Author: Ashil George James

Campus City Logistics Optimization Project
