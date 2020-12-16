import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager

font_location = "C:\\Windows\\Fonts\\malgun.ttf"
font_name = font_manager.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)
matplotlib.rcParams['axes.unicode_minus'] = False
dfs = []

for i in range(0, 4):
    dfs.append(pd.read_excel('C:\\Temp\\GameRank11.xlsx',
                             sheet_name='S'+str(i+1), index_col='게임명'))


sumdf = dfs[0].add(dfs[1], fill_value=51).add(
    dfs[2], fill_value=51).add(dfs[3], fill_value=51)

sortdf = sumdf.sort_values(by='순위', ascending=True)
sortdf = sortdf.rank(method='first')
sortdf.plot(kind='barh')

plt.show()
