from bokeh.io import output_file, show
from bokeh.layouts import widgetbox, row
from bokeh.models import CustomJS, ColumnDataSource, Span
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider, RangeSlider
from bokeh.plotting import figure
from bokeh.layouts import layout
import numpy as np
from neo.io import AxonIO

# Set output
output_file("dashboard.html")

# Read data
reader = AxonIO('/home/matt/Downloads/2017_02_23_0110.abf')
block = reader.read()
ch1_data = []
ch2_data = []
for idx, seg in enumerate(block[0].segments):
    ch1_data.append(seg.analogsignals[0])
    ch2_data.append(seg.analogsignals[1])

ch1_data = np.array(ch1_data).reshape(10,100000)
ch2_data = np.array(ch2_data).reshape(10,100000)

# Plot data
source = ColumnDataSource(data=dict(
                                x=np.arange(0, len(ch2_data[0])),
                                y=ch2_data[0],
                                main=ch2_data[0]
                                )
                        )


p = figure(plot_width=1500, plot_height=500)
geom_1 = p.line('x', 'y', source=source)

# create some widgets
callback = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var scale = scale.value;
        x = data['x']
        data['y'] = data['main'].slice()
        y = data['y']
        for (i = 0; i < x.length; i++) {
            y[i] = y[i] * scale;
        }
        source.change.emit();
    """)

slider1 = Slider(
            start=0,
            end=10,
            value=1,
            step=.1,
            title="Scale Slider",
            callback=callback)
callback.args["scale"] = slider1


slider2 = Slider(
            start=0,
            end=len(ch2_data[0]),
            value=1,
            step=1,
            title="Peak Slider")


peak_start = Span(
            location=slider2.value,
            dimension='height',
            line_color='red',
            line_dash='dashed',
            line_width=1)
p.add_layout(peak_start)

slider2.callback = CustomJS(args=dict(span=peak_start, slider=slider2), code="""
        span.location = slider.value;
    """)

cb_up = CustomJS(args=dict(span=peak_start, slider=slider2), code="""
        span.location = span.location + 1;
        slider.value = span.location;
    """)
cb_down = CustomJS(args=dict(span=peak_start, slider=slider2), code="""
        span.location = span.location - 1;
        slider.value = span.location;
    """)

button_up = Button(label=">", callback=cb_up)
button_down = Button(label="<", callback=cb_down)

button_group = RadioButtonGroup(
                    labels=["Option 1", "Option 2", "Option 3"],
                    active=0
                    )

select = Select(
            title="Option:",
            value="foo",
            options=["foo", "bar", "baz", "quux"]
            )

button_1 = Button(label="Button 1")
button_2 = Button(label="Button 2")

top_slider = widgetbox(slider2, width=1400)
up = widgetbox(button_up, width=50)
down = widgetbox(button_down, width=50)

wbox_top = row(top_slider, down, up)
wbox = widgetbox(
            button_1,
            slider1,
            button_group,
            select,
            button_2,
            width=300
            )


l=layout([[p], [wbox_top], [wbox]])
# put the results in a row
show(l)
