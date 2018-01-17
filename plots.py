import pull_data
import seaborn as sns
import matplotlib.pyplot as plt
import sys

def graph_ratings(dfs):
    southwest_df,american_df,delta_df,united_df,ana_df,japan_df,qatar_df = dfs
    fig, ax = plt.subplots(figsize=(20,10), ncols=5, nrows=2)
    i,j = 0,0
    for col in southwest_df._get_numeric_data().columns[1:]:
        ax[i][j].set_title(col)
        ax[i][j].set_ylim([0,5])
        if j == 4:
            ax[i][j].set_ylim([0,10])
        sns.barplot(x = ['Southwest','American','Delta','United','ANA','Japan','Qatar'], 
                    y = [southwest_df[col].mean(),american_df[col].mean(),delta_df[col].mean(),
                         united_df[col].mean(),ana_df[col].mean(),japan_df[col].mean(),
                         qatar_df[col].mean()],palette = 'magma',ax=ax[i,j])
        j += 1
        if j >=5:
            j = 0
            i = 1
    for i, ax in enumerate(fig.axes):
        ax.set_xticklabels(ax.get_xticklabels(), rotation = 42)
    plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    southwest_df,american_df,delta_df,united_df,ana_df,japan_df,qatar_df,dfs = pull_data.get_data()
    graph_ratings(dfs)