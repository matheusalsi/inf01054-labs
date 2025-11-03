#!/usr/bin/env python3
"""
DSE Results Analysis and Plotting Script
Generates visualization plots for Design Space Exploration results
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Read the CSV file
csv_path = 'dse_results/results.csv'
df = pd.read_csv(csv_path, skipinitialspace=True)

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# Calculate maximum frequency (GHz) from minimum period (ns)
df['Max_Frequency(GHz)'] = 1 / df['Min_Period(ns)']

# Create output directory if it doesn't exist
output_dir = 'dse_results'
os.makedirs(output_dir, exist_ok=True)

# Set style for better-looking plots
try:
    plt.style.use('seaborn-darkgrid')
except:
    plt.style.use('ggplot')
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# Get unique values for grouping
n_values = sorted(df['N'].unique())
n_inputs_values = sorted(df['N_INPUTS'].unique())

print("Generating DSE analysis plots...")

# ============================================================================
# Plot 1: Area vs N (grouped by N_INPUTS)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
for i, n_inputs in enumerate(n_inputs_values):
    data = df[df['N_INPUTS'] == n_inputs]
    ax.plot(data['N'], data['Area(um^2)'], marker='o', linewidth=2, 
            markersize=8, label=f'N_INPUTS={n_inputs}', color=colors[i])

ax.set_xlabel('N (Bit Width)', fontsize=12, fontweight='bold')
ax.set_ylabel('Area (μm²)', fontsize=12, fontweight='bold')
ax.set_title('Area vs Bit Width', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xscale('log', base=2)
ax.set_yscale('log')
plt.tight_layout()
plt.savefig(f'{output_dir}/area_vs_n.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: {output_dir}/area_vs_n.png")
plt.close()

# ============================================================================
# Plot 2: Power vs N (grouped by N_INPUTS)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
for i, n_inputs in enumerate(n_inputs_values):
    data = df[df['N_INPUTS'] == n_inputs]
    ax.plot(data['N'], data['Power(mW)'], marker='s', linewidth=2, 
            markersize=8, label=f'N_INPUTS={n_inputs}', color=colors[i])

ax.set_xlabel('N (Bit Width)', fontsize=12, fontweight='bold')
ax.set_ylabel('Power (mW)', fontsize=12, fontweight='bold')
ax.set_title('Power Consumption vs Bit Width', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xscale('log', base=2)
ax.set_yscale('log')
plt.tight_layout()
plt.savefig(f'{output_dir}/power_vs_n.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: {output_dir}/power_vs_n.png")
plt.close()

# ============================================================================
# Plot 3: Throughput vs N (grouped by N_INPUTS)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
for i, n_inputs in enumerate(n_inputs_values):
    data = df[df['N_INPUTS'] == n_inputs]
    ax.plot(data['N'], data['Throughput(Gops/s)'], marker='^', linewidth=2, 
            markersize=8, label=f'N_INPUTS={n_inputs}', color=colors[i])

ax.set_xlabel('N (Bit Width)', fontsize=12, fontweight='bold')
ax.set_ylabel('Throughput (GOPS/s)', fontsize=12, fontweight='bold')
ax.set_title('Throughput vs Bit Width', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xscale('log', base=2)
plt.tight_layout()
plt.savefig(f'{output_dir}/throughput_vs_n.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: {output_dir}/throughput_vs_n.png")
plt.close()

# ============================================================================
# Plot 4: Max Frequency vs N (grouped by N_INPUTS)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
for i, n_inputs in enumerate(n_inputs_values):
    data = df[df['N_INPUTS'] == n_inputs]
    ax.plot(data['N'], data['Max_Frequency(GHz)'], marker='D', linewidth=2, 
            markersize=8, label=f'N_INPUTS={n_inputs}', color=colors[i])

ax.set_xlabel('N (Bit Width)', fontsize=12, fontweight='bold')
ax.set_ylabel('Max Frequency (GHz)', fontsize=12, fontweight='bold')
ax.set_title('Maximum Frequency vs Bit Width', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xscale('log', base=2)
plt.tight_layout()
plt.savefig(f'{output_dir}/frequency_vs_n.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: {output_dir}/frequency_vs_n.png")
plt.close()

# ============================================================================
# Plot 5: Area vs N_INPUTS (grouped by N)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
for i, n in enumerate(n_values):
    data = df[df['N'] == n]
    ax.plot(data['N_INPUTS'], data['Area(um^2)'], marker='o', linewidth=2, 
            markersize=8, label=f'N={n}', color=colors[i])

ax.set_xlabel('N_INPUTS (Number of Inputs)', fontsize=12, fontweight='bold')
ax.set_ylabel('Area (μm²)', fontsize=12, fontweight='bold')
ax.set_title('Area vs Number of Inputs', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xscale('log', base=2)
ax.set_yscale('log')
plt.tight_layout()
plt.savefig(f'{output_dir}/area_vs_ninputs.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: {output_dir}/area_vs_ninputs.png")
plt.close()

# ============================================================================
# Plot 6: Throughput vs N_INPUTS (grouped by N)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
for i, n in enumerate(n_values):
    data = df[df['N'] == n]
    ax.plot(data['N_INPUTS'], data['Throughput(Gops/s)'], marker='^', linewidth=2, 
            markersize=8, label=f'N={n}', color=colors[i])

ax.set_xlabel('N_INPUTS (Number of Inputs)', fontsize=12, fontweight='bold')
ax.set_ylabel('Throughput (GOPS/s)', fontsize=12, fontweight='bold')
ax.set_title('Throughput vs Number of Inputs', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xscale('log', base=2)
plt.tight_layout()
plt.savefig(f'{output_dir}/throughput_vs_ninputs.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: {output_dir}/throughput_vs_ninputs.png")
plt.close()

# ============================================================================
# Plot 7: Area-Power Trade-off (Pareto-like view)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
for i, n_inputs in enumerate(n_inputs_values):
    data = df[df['N_INPUTS'] == n_inputs]
    ax.scatter(data['Area(um^2)'], data['Power(mW)'], s=150, 
               alpha=0.7, label=f'N_INPUTS={n_inputs}', color=colors[i])
    # Annotate with N values
    for _, row in data.iterrows():
        ax.annotate(f"N={int(row['N'])}", 
                   (row['Area(um^2)'], row['Power(mW)']),
                   fontsize=8, ha='right')

ax.set_xlabel('Area (μm²)', fontsize=12, fontweight='bold')
ax.set_ylabel('Power (mW)', fontsize=12, fontweight='bold')
ax.set_title('Area-Power Trade-off', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xscale('log')
ax.set_yscale('log')
plt.tight_layout()
plt.savefig(f'{output_dir}/area_power_tradeoff.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: {output_dir}/area_power_tradeoff.png")
plt.close()

# ============================================================================
# Plot 8: Throughput vs Power (Efficiency view)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
for i, n_inputs in enumerate(n_inputs_values):
    data = df[df['N_INPUTS'] == n_inputs]
    ax.scatter(data['Power(mW)'], data['Throughput(Gops/s)'], s=150, 
               alpha=0.7, label=f'N_INPUTS={n_inputs}', color=colors[i])
    # Annotate with N values
    for _, row in data.iterrows():
        ax.annotate(f"N={int(row['N'])}", 
                   (row['Power(mW)'], row['Throughput(Gops/s)']),
                   fontsize=8, ha='right')

ax.set_xlabel('Power (mW)', fontsize=12, fontweight='bold')
ax.set_ylabel('Throughput (GOPS/s)', fontsize=12, fontweight='bold')
ax.set_title('Power-Throughput Trade-off', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xscale('log')
plt.tight_layout()
plt.savefig(f'{output_dir}/power_throughput_tradeoff.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: {output_dir}/power_throughput_tradeoff.png")
plt.close()

# ============================================================================
# Plot 9: Energy Efficiency (GOPS/W)
# ============================================================================
df['Energy_Efficiency(GOPS/W)'] = df['Throughput(Gops/s)'] / (df['Power(mW)'] / 1000)

fig, ax = plt.subplots(figsize=(10, 6))
for i, n_inputs in enumerate(n_inputs_values):
    data = df[df['N_INPUTS'] == n_inputs]
    ax.plot(data['N'], data['Energy_Efficiency(GOPS/W)'], marker='*', linewidth=2, 
            markersize=12, label=f'N_INPUTS={n_inputs}', color=colors[i])

ax.set_xlabel('N (Bit Width)', fontsize=12, fontweight='bold')
ax.set_ylabel('Energy Efficiency (GOPS/W)', fontsize=12, fontweight='bold')
ax.set_title('Energy Efficiency vs Bit Width', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xscale('log', base=2)
plt.tight_layout()
plt.savefig(f'{output_dir}/energy_efficiency.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: {output_dir}/energy_efficiency.png")
plt.close()

# ============================================================================
# Plot 10: 3D Plot - Area vs Power vs Throughput (Fixed Scaling)
# ============================================================================
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import numpy as np

fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Color and marker maps
color_map_3d = {8: 'blue', 16: 'orange', 64: 'green'}
marker_map_3d = {4: 'o', 8: 's', 16: '^'}

# Apply log scale to reduce clustering
area_log = np.log10(df['Area(um^2)'])
power_log = np.log10(df['Power(mW)'])
throughput_log = np.log10(df['Throughput(Gops/s)'])

for idx, row in df.iterrows():
    n = int(row['N'])
    n_inputs = int(row['N_INPUTS'])
    ax.scatter(
        np.log10(row['Area(um^2)']),
        np.log10(row['Power(mW)']),
        np.log10(row['Throughput(Gops/s)']),
        c=color_map_3d[n],
        marker=marker_map_3d[n_inputs],
        s=200,
        alpha=0.8,
        edgecolors='black',
        linewidth=1.2
    )

# Axis labels with log indication
ax.set_xlabel('log₁₀(Area [μm²])', fontsize=11, fontweight='bold', labelpad=10)
ax.set_ylabel('log₁₀(Power [mW])', fontsize=11, fontweight='bold', labelpad=10)
ax.set_zlabel('log₁₀(Throughput [GOPS/s])', fontsize=11, fontweight='bold', labelpad=10)

ax.set_title('3D Design Space Exploration\nArea vs Power vs Throughput (log scale)',
             fontsize=13, fontweight='bold', pad=15)

ax.grid(True, alpha=0.3)

# Custom legends
legend_elements_n = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', 
           markersize=10, label='N=8', markeredgecolor='black', markeredgewidth=1.5),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', 
           markersize=10, label='N=16', markeredgecolor='black', markeredgewidth=1.5),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', 
           markersize=10, label='N=64', markeredgecolor='black', markeredgewidth=1.5),
]
legend_elements_inputs = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
           markersize=10, label='N_INPUTS=4', markeredgecolor='black', markeredgewidth=1.5),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray', 
           markersize=10, label='N_INPUTS=8', markeredgecolor='black', markeredgewidth=1.5),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='gray', 
           markersize=10, label='N_INPUTS=16', markeredgecolor='black', markeredgewidth=1.5),
]

legend1 = ax.legend(handles=legend_elements_n, loc='upper left',
                    title='Bit Width (N)', fontsize=9, title_fontsize=10, framealpha=0.9)
ax.add_artist(legend1)
ax.legend(handles=legend_elements_inputs, loc='upper right',
          title='Number of Inputs', fontsize=9, title_fontsize=10, framealpha=0.9)

# Adjust view for better separation
ax.view_init(elev=25, azim=45)

plt.tight_layout()
plt.savefig(f'{output_dir}/3d_area_power_throughput_fixed.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: {output_dir}/3d_area_power_throughput_fixed.png")
plt.close()

# ============================================================================
# Create summary statistics table
# ============================================================================
print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)
print(f"\nDataset contains {len(df)} design points")
print(f"N values: {n_values}")
print(f"N_INPUTS values: {n_inputs_values}")
print(f"\nArea range: {df['Area(um^2)'].min():.2f} - {df['Area(um^2)'].max():.2f} μm²")
print(f"Power range: {df['Power(mW)'].min():.3f} - {df['Power(mW)'].max():.3f} mW")
print(f"Throughput range: {df['Throughput(Gops/s)'].min():.2f} - {df['Throughput(Gops/s)'].max():.2f} GOPS/s")
print(f"Max Frequency range: {df['Max_Frequency(GHz)'].min():.3f} - {df['Max_Frequency(GHz)'].max():.3f} GHz")
print(f"Energy Efficiency range: {df['Energy_Efficiency(GOPS/W)'].min():.2f} - {df['Energy_Efficiency(GOPS/W)'].max():.2f} GOPS/W")

print("\n" + "="*70)
print("3D PLOT LEGEND")
print("="*70)
print("Colors represent bit width (N):")
print("  • Blue = N=8")
print("  • Orange = N=16")
print("  • Green = N=64")
print("\nMarkers represent number of inputs (N_INPUTS):")
print("  • Circle (o) = N_INPUTS=4")
print("  • Square (s) = N_INPUTS=8")
print("  • Triangle (^) = N_INPUTS=16")

print("\n" + "="*70)
print("All plots have been generated successfully!")
print("="*70)
