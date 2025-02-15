import pandas as pd
import matplotlib.pyplot as plt
# Read the CSV file
df = pd.read_csv('data/all_surveys_specs5.csv')
# Create figure with four subplots
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 25))
def make_subplot(ax, data, y_column, title):
    # Filter data
    df_filtered = data[data[y_column] > 1]
    
    # Split data into SPEC-S5 and others
    specs5_data = df_filtered[df_filtered['instrument'] == 'Spec-S5']
    other_data = df_filtered[df_filtered['instrument'] != 'Spec-S5']
    
    # Plot other points
    ax.scatter(other_data['start_year'], other_data[y_column], alpha=0.6, color='blue')
    
    # Plot SPEC-S5 as a red star
    if not specs5_data.empty:
        ax.scatter(specs5_data['start_year'], specs5_data[y_column], 
                  alpha=0.6, color='red', marker='*', s=400)
    
    # Add labels with different x offsets based on position
    for idx, row in df_filtered.iterrows():
        if row['instrument'] == 'Spec-S5':
            label = r'$\mathbf{Spec}$-$\mathbf{S5}$'
            color = 'red'
            x_offset = 10
            y_offset = 0.1
            fontsize=20
        else:
            label = row['instrument']
            color = 'black'
            # Alternate x offsets based on index to spread out labels
            x_offset = 10 if idx % 2 == 0 else -10
            y_offset = -0.1 if idx % 2 == 0 else 0.1
            fontsize=12
            
        ax.annotate(label, 
                   (row['start_year'], row[y_column]),
                   xytext=(x_offset, 0),
                   textcoords='offset points',
                   fontsize=fontsize,
                   color=color,
                   ha='right' if x_offset < 0 else 'left',
                   rotation=30,  # Added 30-degree rotation
                   rotation_mode='anchor')  # This ensures rotation around the connection point
    
    # Set y-axis to log scale
    ax.set_yscale('log')
    
    # Customize the subplot
    ax.set_title(title, fontsize=14, pad=20)
    ax.set_xlabel('Start Year', fontsize=20)
    ax.grid(True, which="both", ls="-", alpha=0.2)
    
    # Set tick label size
    ax.tick_params(axis='both', which='major', labelsize=20)
    
    # Set x-axis limits with some padding
    ax.set_xlim(1998, 2043)
# Create each subplot
make_subplot(ax1, df, 'galaxy_z_gt_2.1', 'Galaxy Redshifts (z > 2.1) by Survey Start Year')
make_subplot(ax2, df, 'galaxy_z_lt_2.1', 'Galaxy Redshifts (z < 2.1) by Survey Start Year')
make_subplot(ax3, df, 'star_rvs', 'Star RVs by Survey Start Year')
make_subplot(ax4, df, 'area', 'Survey Area [deg²] by Start Year')
# Set y-labels
ax1.set_ylabel('Number of Galaxies (log scale)', fontsize=20)
ax2.set_ylabel('Number of Galaxies (log scale)', fontsize=20)
ax3.set_ylabel('Number of Star RVs (log scale)', fontsize=20)
ax4.set_ylabel('Area [deg²] (log scale)', fontsize=20)
# Adjust layout
plt.subplots_adjust(hspace=0.3)
# Save the plot as PDF
plt.savefig('survey_stats_comparison.pdf', bbox_inches='tight', dpi=300)