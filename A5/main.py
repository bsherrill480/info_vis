import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import FuncTickFormatter, FixedTicker, Title, TickFormatter
from bokeh.palettes import Category10
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.core.templates import FILE
from os.path import join, dirname

### https://github.com/bokeh/bokeh/blob/master/bokeh/core/templates.py
### START TEMPLATE SETUP
import json
from jinja2 import Environment, FileSystemLoader, Markup

templates_path = join(dirname(__file__), 'templates')
_env = Environment(loader=FileSystemLoader(templates_path))
_env.filters['json'] = lambda obj: Markup(json.dumps(obj))

template = _env.get_template('index.html')

### END

# Consts
CATEGORY_NUM = 10
OUTPUT_FILE_NAME = 'index.html'
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

# fill empty data
data[RV_CAMPERS] = data[RV_CAMPERS].fillna(0.0)
data[BACKCOUNTRY_CAMPERS] = data[BACKCOUNTRY_CAMPERS].fillna(0.0)
data[TENT_CAMPERS] = data[TENT_CAMPERS].fillna(0.0)
data[RECREATION_VISITORS] = data[RECREATION_VISITORS].fillna(0.0)

# get total
data[TOTAL_VISITORS] = data[RV_CAMPERS] + \
                       data[BACKCOUNTRY_CAMPERS] + \
                       data[TENT_CAMPERS] + \
                       data[RECREATION_VISITORS]

# add rank
rank = data.groupby([YEAR])[RECREATION_VISITORS].rank(ascending=False)
data[RANK] = rank

output_file(OUTPUT_FILE_NAME)

# create a new plot with a title and axis labels
p = figure(y_range=(-60, 2), plot_width=PLOT_DIM, plot_height=PLOT_DIM, x_range=(1900, 2050))
p.background_fill_color = '#F0F0F0'
p.yaxis.ticker = FixedTicker(ticks=[-1, -25, -50])
p.xaxis.ticker = FixedTicker(ticks=[1925, 1950, 1975, 2000])
p.grid.grid_line_width = 2
p.ygrid.ticker = FixedTicker(ticks=[-1, -25, -50])
p.xgrid.ticker = FixedTicker(ticks=[1925, 1950, 1975, 2000])
p.add_layout(Title(text='Rank', align="center"), 'left')

p.yaxis.formatter = FuncTickFormatter(code="""
    return Math.abs(tick) + (tick == -1 ? 'st' : 'th')
""")


park_names = data[PARK].unique()
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

# show(p)
html = file_html(p, CDN, 'myplot', template=template)

with open(OUTPUT_FILE_NAME, 'w+') as f:
    f.writelines(html)

