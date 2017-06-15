import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import FuncTickFormatter, FixedTicker, Title
from bokeh.palettes import Category10
# from bokeh.io import curdoc

# Consts
CATEGORY_NUM = 10
OUTPUT_FILE_NAME = 'output.html'
GREAT_SMOKEY_MOUNTAINS = 'Great Smoky Mountains NP'
COLORED_PARK_NAMES = {
    GREAT_SMOKEY_MOUNTAINS,
    'Grand Canyon NP',
    'Yosemite NP',
    'Yellowstone NP',
    'Zion NP',
    'Acadia NP',
    'Hot Springs NP',
    'Denali NP & PRES',
    'Carlsbad Caverns NP',
    'Great Basin NP'
}
COLORED_PARK_NAMES_TO_DISPLAY_NAME = {
    GREAT_SMOKEY_MOUNTAINS: 'Great Smokey Mountains',
    'Grand Canyon NP': 'Grand Canyon',
    'Yosemite NP': 'Yosemite',
    'Yellowstone NP': 'Yellowstone',
    'Zion NP': 'Zion',
    'Acadia NP': 'Acadia',
    'Hot Springs NP': 'Hot Springs',
    'Denali NP & PRES': 'Denali',
    'Carlsbad Caverns NP': 'Carlsbad Caverns',
    'Great Basin NP': 'Great Basin'
}
DEFAULT_LINE_COLOR = '#DCDCDC'
PLOT_DIM = 900

# Data Consts
YEAR = 'Year'
RECREATION_VISITORS = 'Recreation Visitors'
PARK = 'Park'
RANK = 'rank'
RV_CAMPERS = 'RV Campers'
BACKCOUNTRY_CAMPERS = 'Backcountry Campers'
TENT_CAMPERS = 'Tent Campers'
TOTAL_VISITORS = 'Total Visitors'

data = pd.read_csv('./NationalParkVisits.csv', thousands=',')

# fill parks with NaN as just empty string
data[PARK] = data[PARK].fillna('')

# filter to just national parks
data = data[data[PARK].str.contains(' NP')]
data = data[~data[PARK].str.contains('NPRES')]

# # convert to same datatype
# data[[RV_CAMPERS, BACKCOUNTRY_CAMPERS, TENT_CAMPERS, RECREATION_VISITORS]] = \
#     data[[RV_CAMPERS, BACKCOUNTRY_CAMPERS, TENT_CAMPERS, RECREATION_VISITORS]].apply(
#         pd.to_numeric
#     )

# fill empty data
data[RV_CAMPERS] = data[RV_CAMPERS].fillna(0.0)
data[BACKCOUNTRY_CAMPERS] = data[BACKCOUNTRY_CAMPERS].fillna(0.0)
data[TENT_CAMPERS] = data[TENT_CAMPERS].fillna(0.0)
# data[RECREATION_VISITORS] = pd.to_numeric(data[RECREATION_VISITORS], errors='coerce')
data[RECREATION_VISITORS] = data[RECREATION_VISITORS].fillna(0.0)
# data['Unnamed: 6'] = data['Unnamed: 6']

# get total
data[TOTAL_VISITORS] = data[RV_CAMPERS] + \
                       data[BACKCOUNTRY_CAMPERS] + \
                       data[TENT_CAMPERS] + \
                       data[RECREATION_VISITORS]

# add rank
# rank = data.groupby([YEAR])[TOTAL_VISITORS].rank(ascending=False)
rank = data.groupby([YEAR])[RECREATION_VISITORS].rank(ascending=False)
data[RANK] = rank

output_file(OUTPUT_FILE_NAME)

# create a new plot with a title and axis labels
# y_range = [str(i) for i in range(70, 0, -1)]
# p = figure(title="simple line example", y_range=y_range)
p = figure(y_range=(-60, 2), plot_width=PLOT_DIM, plot_height=PLOT_DIM, x_range=(1900, 2045))
p.background_fill_color = '#F0F0F0'
p.yaxis.ticker = FixedTicker(ticks=[-1, -25, -50])
p.xaxis.ticker = FixedTicker(ticks=[1925, 1950, 1975, 2000])
p.grid.grid_line_color = None

p.yaxis.formatter = FuncTickFormatter(code="""
    return Math.abs(tick) + (tick == -1 ? 'st' : 'th')
""")


park_names = data[PARK].unique()
print(len(park_names))
for park_name in park_names:
    if park_name not in COLORED_PARK_NAMES:
        park_rows = data.loc[data[PARK] == park_name]
        x_values = park_rows[YEAR]
        x_values_list = [int(i) for i in x_values]
        y_values = park_rows[RANK]
        y_values_list = [-i for i in y_values]
        p.line(x_values_list, y_values_list, line_width=1, line_color=DEFAULT_LINE_COLOR)

for i, park_name in enumerate(COLORED_PARK_NAMES):
    park_rows = data.loc[data[PARK] == park_name]
    x_values = park_rows[YEAR]
    x_values_list = [int(i) for i in x_values]
    y_values = park_rows[RANK]
    y_values_list = [-i for i in y_values]
    line_color = Category10[CATEGORY_NUM][i]
    p.line(x_values_list, y_values_list, line_color=line_color, line_width=2)
    park_name_display = COLORED_PARK_NAMES_TO_DISPLAY_NAME[park_name].upper()

    if park_name is not GREAT_SMOKEY_MOUNTAINS:
        # slight adjustments to positioning to make it look better
        p.text(x_values_list[-1] + 2, y_values_list[-1] - .5, text=[park_name_display],
               text_color=line_color)
    else:
        # manually finding positioning for Great
        p.text(x_values_list[-1] - 40, -.5, text=[park_name_display], text_color=line_color)

# p.add_layout(Title(text='Foobar1', align='left', offset=100), 'above')
# p.add_layout(Title(text='Foobar2', align='left'), 'above')
show(p)
# curdoc().add_root(p)
# curdoc().title = 'Export CSV'

