import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('data/all_surveys_specs5.csv')

# Create a figure with three subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 25))

def make_subplot(ax, data, x_column, y_column, title, xlim=None, ylim=None):
    # Calculate total galaxy redshifts if needed
    if x_column == 'total_redshifts':
        data['total_redshifts'] = data['galaxy_z_lt_2.1'] + data['galaxy_z_gt_2.1']
    
    # Plot points
    for idx, row in data.iterrows():
        if row['instrument'] == 'Spec-S5':
            color = 'red'
            marker = '*'
            size = 400
            label = r'$\mathbf{Spec}$-$\mathbf{S5}$'
            fontsize = 20
        else:
            color = 'blue'
            marker = 'o'
            size = 100
            label = row['instrument']
            fontsize = 12
            
        ax.scatter(row[x_column], row[y_column], 
                  alpha=0.6, color=color, marker=marker, s=size)
        ax.annotate(label,
                   (row[x_column], row[y_column]),
                   xytext=(10 if idx % 2 == 0 else -10, 0),
                   textcoords='offset points',
                   fontsize=fontsize,
                   color=color,
                   ha='left' if idx % 2 == 0 else 'right',
                   rotation=0,
                   rotation_mode='anchor')
    
    # Set log scales
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    # Customize the subplot
    ax.set_title(title, fontsize=14, pad=20)
    ax.grid(True, which="both", ls="-", alpha=0.2)
    ax.tick_params(axis='both', which='major', labelsize=20)

# Calculate total redshifts
df['total_redshifts'] = df['galaxy_z_lt_2.1'] + df['galaxy_z_gt_2.1']

# Create each subplot
make_subplot(ax1, df, 'total_redshifts', 'area', 
            'Survey Area vs. Total Galaxy Redshifts', xlim=[1E5,1E9])
ax1.set_xlabel('Total Galaxy Redshifts (log scale)', fontsize=20)
ax1.set_ylabel('Area [deg2] (log scale)', fontsize=20)

make_subplot(ax2, df, 'galaxy_z_lt_2.1', 'galaxy_z_gt_2.1', 
            'Galaxy Redshifts (z > 2.1) vs. Galaxy Redshifts (z < 2.1)', xlim=[1E5,1E9], ylim=[1E4,1E9])
ax2.set_xlabel('Galaxy Redshifts z < 2.1 (log scale)', fontsize=20)
ax2.set_ylabel('Galaxy Redshifts z > 2.1 (log scale)', fontsize=20)

make_subplot(ax3, df, 'total_redshifts', 'star_rvs', 
            'Stellar RVs vs. Total Galaxy Redshifts', xlim=[1E5,1E9], ylim=[1E5,1E9])
ax3.set_xlabel('Total Galaxy Redshifts (log scale)', fontsize=20)
ax3.set_ylabel('Number of Star RVs (log scale)', fontsize=20)

# Adjust layout
plt.subplots_adjust(hspace=0.3)

# Save the plot as PDF
plt.savefig('survey_correlations.pdf', bbox_inches='tight', dpi=300)