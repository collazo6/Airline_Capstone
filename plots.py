import pull_data
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.graph_objs import Layout
import plotly.plotly as py
import plotly

def barplot_ratings(dfs):
    '''
    INPUT:
    dfs: dataframes of airlines to use for mean representation of particular attribute of flight rating

    OUTPUT:
    figure with barplot subplots of mean star rating for each attribute among airlines
    '''
    southwest_df,american_df,delta_df,united_df,ana_df,japan_df,qatar_df = dfs
    fig, ax = plt.subplots(figsize=(20,10), ncols=5, nrows=2)
    i,j = 0,0
    for col in southwest_df._get_numeric_data().columns[1:]:
        ax[i][j].set_title(col)
        ax[i][j].set_ylim([0,5])
        if j == 4:
            ax[i][j].set_ylim([0,10])
        elif col == 'positive':
            ax[i][j].set_ylim([0,1])
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

def boxplot_ratings(dfs,col):
    '''
    INPUT:
    dfs: dataframes of airlines to take data of a particular attribute of flight review
    col: specified attribute to create boxplot on

    OUTPUT:
    boxplots, displayed in webpage, for each airline based on col attribute
    '''

    southwest_df,american_df,delta_df,united_df,ana_df,japan_df,qatar_df = dfs

    y0 = southwest_df[col]
    y1 = american_df[col]
    y2 = delta_df[col]
    y3 = united_df[col]
    y4 = ana_df[col]
    y5 = japan_df[col]
    y6 = qatar_df[col]

    trace0 = go.Box(
        y=y0,
        name = 'Southwest'
    )
    trace1 = go.Box(
        y=y1,
        name = 'American'
    )
    trace2 = go.Box(
        y=y2,
        name = 'Delta'
    )
    trace3 = go.Box(
        y=y3,
        name = 'United'
    )
    trace4 = go.Box(
        y=y4,
        name = 'ANA'
    )
    trace5 = go.Box(
        y=y5,
        name = 'Japan'
    )
    trace6 = go.Box(
        y=y6,
        name = 'Qatar'
    )

    data = [trace0,trace1,trace2,trace3,trace4,trace5,trace6]

    plotly.offline.plot({
    "data": data,
    "layout": Layout(title="Ratings ({})".format(col))
    })


def rating_dist(df,airline):
    '''
    INPUT:
    df: which airline we would like to analyze
    airline: name of the airline as a string
    
    OUTPUT:
    subplots of countplot for each attribute to see distribution of possible rating options
    '''
    fig, ax = plt.subplots(figsize=(20,10), ncols=5, nrows=2)
    i,j = 0,0
    for col in df._get_numeric_data().columns[1:]:
        ax[i][j].set_title('{}:{}'.format(airline,col))
        sns.countplot(df[col], ax = ax[i,j],palette = 'magma')
        j += 1
        if j >=5:
            j = 0
            i = 1
    for i, ax in enumerate(fig.axes):
        ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)
    plt.tight_layout()
    plt.show()

def violin_ratings(dfs,col,country = 'United States'):
    '''
    INPUT:
    dfs: dataframes of all airlines
    col: attribute of airline reviews to analyze

    OUTPUT:
    violin plots of 'col' data for each airline split on country of origin (USA or other)
    '''
    fig, ax = plt.subplots(figsize=(20,10), ncols=4, nrows=2)
    i,j = 0,0
    airlines = ['Southwest','American','Delta','United','ANA','Japan','Qatar']
    for ind,df in enumerate(dfs):
        df['Country of Origin'] = df['country'] == country
        df['Country of Origin'] = df['Country of Origin'].apply(lambda x: country if x == True else 'Other')
        df[''] = airlines[ind]
        df.sort_values(by = ['Country of Origin'],ascending = 0, inplace = True)
        ax[i][j].set_title('{} : {}'.format(airlines[ind],col))
        sns.violinplot(x='', y=col, hue='Country of Origin', data=df, palette='coolwarm', ax=ax[i,j],split=True)
        j += 1
        if j >=4:
            j = 0
            i = 1
    plt.tight_layout()
    plt.show()
    

if __name__ == '__main__':
    southwest_df,american_df,delta_df,united_df,ana_df,japan_df,qatar_df,dfs = pull_data.get_data()
    barplot_ratings(dfs)
    boxplot_ratings(dfs,'value_for_money') #will pull up graph in webpage
    rating_dist(ana_df,'ANA')
    violin_ratings(dfs,'rating','United States')