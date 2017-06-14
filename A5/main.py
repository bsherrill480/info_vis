import pandas as p
from bokeh.plotting import figure, output_file, show

# Consts
OUTPUT_FILE_NAME = 'output'

# Data Consts
YEAR = 'Year'
RECREATION_VISITORS = 'Recreation Visitors'

data = p.read_csv('./NationalParkVisits.csv')
del data['RV Campers']
del data['Backcountry Campers']
del data['Tent Campers']
del data['Unnamed: 6']
data = data.fillna(0)
rank = data.groupby([YEAR])[RECREATION_VISITORS].rank(ascending=False)
data['rank'] = rank

# prepare some data
# x = [1, 2, 3, 4, 5]
# y = [6, 7, 2, 4, 5]
parks = data['Park'].unique()
NHP = data.loc[data['Park'] == parks[0]]



exit()

# output to static HTML file
output_file(OUTPUT_FILE_NAME)

# create a new plot with a title and axis labels
p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')


# add a line renderer with legend and line thickness
p.line(x, y, legend="Temp.", line_width=2)

# show the results
show(p)

