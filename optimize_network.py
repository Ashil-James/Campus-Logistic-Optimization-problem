import pandas as pd
import pulp
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. SETUP & DATA LOADING
# ==========================================
print("Loading data...")

# Define the folder name
DATA_FOLDER = 'data'

# Helper function to get the correct path
def get_path(filename):
    return os.path.join(DATA_FOLDER, filename)

try:
    demands_df = pd.read_csv(get_path('demands.csv'))
    warehouses_df = pd.read_csv(get_path('warehouses.csv'))
    transport_df = pd.read_csv(get_path('transportation_costs.csv'))
    facilities_df = pd.read_csv(get_path('facilities.csv'))
except FileNotFoundError as e:
    print(f"\nERROR: Could not find the files in the '{DATA_FOLDER}' folder.")
    print(f"Details: {e}")
    print(f"Current working directory is: {os.getcwd()}")
    print("Please ensure you have a folder named 'data' containing all 4 CSV files.")
    exit()

# Parameters from Problem Statement
TARGET_FACILITIES = ['MED_CENTER', 'ENG_BUILDING', 'SCIENCE_HALL', 
                     'DORM_A', 'DORM_B', 'LIBRARY']
TARGET_WAREHOUSES = ['WH_NORTH', 'WH_SOUTH', 'WH_EAST']

DAYS_PER_YEAR = 365
AMORTIZATION_YEARS = 10
BUDGET_LIMIT = 1500000

# ==========================================
# 2. DATA PRE-PROCESSING
# ==========================================
# Filter and Annualize Demand
demands_subset = demands_df[demands_df['facility_id'].isin(TARGET_FACILITIES)].set_index('facility_id')
annual_demand = (demands_subset['daily_demand'] * DAYS_PER_YEAR).to_dict()

# Filter and Annualize Warehouse Data
warehouses_subset = warehouses_df[warehouses_df['warehouse_id'].isin(TARGET_WAREHOUSES)].set_index('warehouse_id')
annual_capacity = (warehouses_subset['capacity'] * DAYS_PER_YEAR).to_dict()

# Calculate Annualized Fixed Cost: (Construction / 10) + (Daily Op * 365)
annual_fixed_cost = {}
for wh_id, row in warehouses_subset.iterrows():
    cost = (row['construction_cost'] / AMORTIZATION_YEARS) + (row['operational_cost'] * DAYS_PER_YEAR)
    annual_fixed_cost[wh_id] = cost

# Filter Transportation Costs
transport_costs = {}
for _, row in transport_df.iterrows():
    if row['from_warehouse'] in TARGET_WAREHOUSES and row['to_facility'] in TARGET_FACILITIES:
        transport_costs[(row['from_warehouse'], row['to_facility'])] = row['cost_per_unit']

# ==========================================
# 3. OPTIMIZATION MODEL (PuLP)
# ==========================================
print("Solving optimization model...")
prob = pulp.LpProblem("Campus_City_Emergency_Distribution", pulp.LpMinimize)

# Decision Variables
# y[j]: Binary (1 if warehouse is Open, 0 if Closed)
y = pulp.LpVariable.dicts("Open", TARGET_WAREHOUSES, cat='Binary')

# x[j][i]: Continuous (Amount shipped from Warehouse j to Facility i)
x = pulp.LpVariable.dicts("Ship", (TARGET_WAREHOUSES, TARGET_FACILITIES), lowBound=0, cat='Continuous')

# Objective Function: Minimize Total Annual Cost
prob += (
    pulp.lpSum([annual_fixed_cost[j] * y[j] for j in TARGET_WAREHOUSES]) +
    pulp.lpSum([transport_costs[(j, i)] * x[j][i] for j in TARGET_WAREHOUSES for i in TARGET_FACILITIES])
), "Total_Annual_Cost"

# Constraints
# 1. Demand Satisfaction
for i in TARGET_FACILITIES:
    prob += pulp.lpSum([x[j][i] for j in TARGET_WAREHOUSES]) == annual_demand[i], f"Demand_{i}"

# 2. Capacity Constraints
for j in TARGET_WAREHOUSES:
    prob += pulp.lpSum([x[j][i] for i in TARGET_FACILITIES]) <= annual_capacity[j] * y[j], f"Capacity_{j}"

# 3. Select Exactly 2 Warehouses
prob += pulp.lpSum([y[j] for j in TARGET_WAREHOUSES]) == 2, "Select_2_Warehouses"

# 4. Budget Constraint
prob += (
    pulp.lpSum([annual_fixed_cost[j] * y[j] for j in TARGET_WAREHOUSES]) +
    pulp.lpSum([transport_costs[(j, i)] * x[j][i] for j in TARGET_WAREHOUSES for i in TARGET_FACILITIES])
) <= BUDGET_LIMIT, "Budget_Limit"

# Solve
prob.solve()

# ==========================================
# 4. REPORTING RESULTS
# ==========================================
print("\n" + "="*40)
print(f"OPTIMIZATION STATUS: {pulp.LpStatus[prob.status]}")
print("="*40)

if pulp.LpStatus[prob.status] != 'Optimal':
    print("Solution not found. Check constraints.")
    exit()

total_cost = pulp.value(prob.objective)
total_fixed = sum([annual_fixed_cost[j] * pulp.value(y[j]) for j in TARGET_WAREHOUSES])
total_transport = sum([transport_costs[(j, i)] * pulp.value(x[j][i]) for j in TARGET_WAREHOUSES for i in TARGET_FACILITIES])

print(f"\nFINANCIAL SUMMARY:")
print(f"Total Annual Cost:      ${total_cost:,.2f}")
print(f"  - Fixed Costs:        ${total_fixed:,.2f}")
print(f"  - Transport Costs:    ${total_transport:,.2f}")
print(f"Remaining Budget:       ${BUDGET_LIMIT - total_cost:,.2f}")

print("\nWAREHOUSE SELECTION:")
for j in TARGET_WAREHOUSES:
    if pulp.value(y[j]) > 0.5:
        used_capacity = sum([pulp.value(x[j][i]) for i in TARGET_FACILITIES])
        utilization = (used_capacity / annual_capacity[j]) * 100
        print(f"  [X] {j} (Utilization: {utilization:.1f}%)")
    else:
        print(f"  [ ] {j}")

print("\nDETAILED SHIPPING PLAN (Units/Year):")
print(f"{'Warehouse':<15} {'Facility':<20} {'Units':<10} {'Cost':<10}")
print("-" * 55)
for j in TARGET_WAREHOUSES:
    for i in TARGET_FACILITIES:
        val = pulp.value(x[j][i])
        if val > 0:
            cost = val * transport_costs[(j, i)]
            print(f"{j:<15} {i:<20} {val:<10.0f} ${cost:,.2f}")

# ==========================================
# 5. VISUALIZATION
# ==========================================
print("\nGenerating Network Map...")

# Filter coordinates
fac_coords = facilities_df[facilities_df['facility_id'].isin(TARGET_FACILITIES)].set_index('facility_id')
wh_coords = warehouses_df[warehouses_df['warehouse_id'].isin(TARGET_WAREHOUSES)].set_index('warehouse_id')

plt.figure(figsize=(12, 8))

# Plot Facilities
plt.scatter(fac_coords['longitude'], fac_coords['latitude'], c='blue', s=100, label='Facilities', zorder=3)
for idx, row in fac_coords.iterrows():
    plt.text(row['longitude'], row['latitude'] + 0.0005, idx, fontsize=8, ha='center')

# Plot Warehouses (Color by Selection)
for wh in TARGET_WAREHOUSES:
    lat, lon = wh_coords.loc[wh, 'latitude'], wh_coords.loc[wh, 'longitude']
    if pulp.value(y[wh]) > 0.5:
        plt.scatter(lon, lat, c='red', s=250, marker='s', edgecolors='black', zorder=4, label='Open Warehouse' if wh == TARGET_WAREHOUSES[0] else "")
        plt.text(lon, lat - 0.0005, wh, fontsize=10, fontweight='bold', ha='center')
    else:
        plt.scatter(lon, lat, c='gray', s=100, marker='x', zorder=2, label='Closed Warehouse' if wh == TARGET_WAREHOUSES[2] else "")

# Plot Flow Lines
max_flow = max([pulp.value(x[j][i]) for j in TARGET_WAREHOUSES for i in TARGET_FACILITIES])
for j in TARGET_WAREHOUSES:
    for i in TARGET_FACILITIES:
        val = pulp.value(x[j][i])
        if val > 0:
            # Line width proportional to shipment size
            w_lon, w_lat = wh_coords.loc[j, 'longitude'], wh_coords.loc[j, 'latitude']
            f_lon, f_lat = fac_coords.loc[i, 'longitude'], fac_coords.loc[i, 'latitude']
            width = 1 + (val / max_flow) * 5
            plt.plot([w_lon, f_lon], [w_lat, f_lat], 'k--', linewidth=width, alpha=0.5, zorder=1)

plt.title(f'Optimal Supply Distribution Network (Total Cost: ${total_cost:,.0f})', fontsize=14)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True, linestyle=':', alpha=0.6)

# Handle duplicate labels in legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

# Save and Show
plt.savefig('campus_distribution_map.png', dpi=300)
print("Map saved as 'campus_distribution_map.png'.")
plt.show()