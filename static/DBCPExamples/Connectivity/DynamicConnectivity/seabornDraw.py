import seaborn as sns
import scipy.io as scio
import os

for local_file in os.listdir('./'):
    print(local_file)
    MatrixData = scio.loadmat(local_file)
    sns.set_theme()
    ax = sns.heatmap(MatrixData['connectivity'], cmap='rainbow', xticklabels=False, yticklabels=False,
                     cbar=False)
    s1 = ax.get_figure()
    filename = './' + local_file.split('.')[0] + '.jpg'
    s1.savefig(filename, dpi=50, bbox_inches='tight')
