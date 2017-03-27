from .base import BaseChart


class BaseGChart(BaseChart):
    def get_html_template(self):
        return "graphosjat/gchart/html.html"

class JatGChart(BaseChart):
    def get_html_template(self):
        return "graphosjat/gchart/html_percent.html"

class LineChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/line_chart.html"


class GaugeChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/gauge_chart.html"


class ColumnChart(JatGChart):
    def get_js_template(self):
        return "graphosjat/gchart/column_chart.html"


class StackedBarChart(JatGChart):
    def get_js_template(self):
        return "graphosjat/gchart/stacked_bar_chart.html"

    def get_options(self):
        options = super(StackedBarChart, self).get_options()
        if not 'vAxis' in options:
            vaxis = self.data_source.get_header()[0]
            options['vAxis'] = {'title': vaxis}
        return options

class BarChart(JatGChart):
    def get_js_template(self):
        return "graphosjat/gchart/bar_chart.html"

    def get_options(self):
        options = super(BarChart, self).get_options()
        if not 'vAxis' in options:
            vaxis = self.data_source.get_header()[0]
            options['vAxis'] = {'title': vaxis}
        return options

class CandlestickChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/candlestick_chart.html"


class PieChart(JatGChart):
    def get_js_template(self):
        return "graphosjat/gchart/pie_chart.html"


class TreeMapChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/treemap_chart.html"


class AreaChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/area_chart.html"
