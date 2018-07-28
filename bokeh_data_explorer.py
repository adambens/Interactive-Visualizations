# Exploratory Data Tool with Bokeh

'''
PURPOSE:
Creating an interactive Bokeh app to explore 
Country data from the Gapminder dataset
'''


#########################
## Import statements ####
#########################
import os
import pandas as pd 
import numpy as np 

## Bokeh Imports
from bokeh.io import curdoc, output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CategoricalColorMapper, HoverTool, Slider, Select
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, column



##########################
##### Loading Data #######
##########################

## Reading in 'GapMinder' csv file to DataFrame
gapminder = pd.read_csv("Data/gapminder_tidy.csv", index_col='Year')

## Inspecting Data
# print(gapminder.head())

# dropping this country because it causes an issue while compiling
gapminder = gapminder[gapminder.Country != 'Congo, Dem. Rep.']

# renaming gdp to gdp per capita to be more accurate, same with life expectancy
gapminder.rename(columns={'gdp': 'gdp_per_capita', 'life': 'life_expectancy'}, inplace=True)

## Make the ColumnDataSource: source
source = ColumnDataSource(data={
						 		'x': gapminder.loc[1970]['gdp_per_capita'],
						 		'y': gapminder.loc[1970]['life_expectancy'],
						 		'country': gapminder.loc[1970]['Country'],
						 		'pop': gapminder.loc[1970]['population'],
						 		'region': gapminder.loc[1970]['region']
								})



############################
# Create plots and widgets #
############################

plot = figure(title='Gapminder Data', plot_height=800, plot_width=1400,
           	 )


# Add circle glyphs to the plot
plot.circle(x='x', y='y', fill_alpha=0.8, source=source)


# Make a list of the unique values from the region column: regions_list
regions_list = gapminder.region.unique().tolist()

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

# Add the color mapper to the circle glyph
plot.circle(x='x', y='y', fill_alpha=0.8, size=10, source=source,
            color=dict(field='region', transform=color_mapper), legend='region')

# Set the legend.location attribute of the plot to 'top_right'
plot.legend.location = ('top_left')




#########################
#### Add Callbacks  #####
#########################



def update_plot(attr, old, new):
    # # Read the current value off the slider and 2 dropdowns: yr, x, y
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # Set new data
    new_data = {
        'x'       : gapminder.loc[yr][x],
        'y'       : gapminder.loc[yr][y],
        'country' : gapminder.loc[yr].Country,
        'pop'     : (gapminder.loc[yr].population),
        'region'  : gapminder.loc[yr].region,
    }
    source.data = new_data

    # Set the range of all axes
    plot.x_range.start = min(gapminder[x])
    plot.x_range.end = max(gapminder[x])
    plot.y_range.start = min(gapminder[y])
    plot.y_range.end = max(gapminder[y])

    # Add title to figure: plot.title.text
    plot.title.text = 'Gapminder data for %d' % yr

# Make a slider object: slider
slider = Slider(start=1970, end=2013, step=1, value=1970, title='Year')

# Attach the callback to the 'value' property of slider
slider.on_change('value', update_plot)

# Create a dropdown Select widget for the x data: x_select
x_select = Select(
				    options=['fertility', 'life_expectancy', 'child_mortality', 'gdp_per_capita'],
				    value='fertility',
				    title='x-axis data'
				  )
# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['fertility', 'life_expectancy', 'child_mortality', 'gdp_per_capita'],
    value='life_expectancy',
    title='y-axis data'
)

# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)

# Create a HoverTool: hover
hover = HoverTool(tooltips=[('Country', '@country'), ('Population', '@pop'), ('Region', '@region')])

# Add the HoverTool to the plot
plot.add_tools(hover)


########################################
# Arrange plots and widgets in layouts #
########################################

# Make a row layout of widgetbox(slider) and plot and add it to the current document
layout = row(plot, widgetbox(slider, x_select, y_select))


# Add the plot to the current document and add a title
curdoc().add_root(layout)
curdoc().title = 'Gapminder'









'''
# Save the minimum and maximum values of the fertility column: xmin, xmax
xmin, xmax = min(gapminder.gdp), max(gapminder.gdp)
# Save the minimum and maximum values of the life expectancy column: ymin, ymax
ymin, ymax = min(gapminder.life), max(gapminder.life)
 x_range=(xmin, xmax), y_range=(ymin, ymax), x_axis_type="log"
'''