from typing import Optional
from chart import Chart
from containers import DataContainer

class ChartController():
    """Controls the updates of the chart and other display widgets, stores state
    """
    def __init__(self, chart: Chart, data_container: DataContainer):
        """Sets up initial settings

        Args:
            chart (Chart): the chart being managed
            data_container (DataContainer): the data container being used
        """
        self.chart = chart
        self.data_container = data_container

        self.default_time = True
        self.default_settings = True
        self.ratio = False
        
    def update_chart(self):
        """Utility method to update chart with query
        """
        x, y, limits = self.data_container.get_data(self.default_time,
                                                    self.default_settings,
                                                    self.ratio)
        self.chart.update_chart(x, y, limits)
        
    def set_display_options(self, 
                            time: Optional[bool], 
                            settings: Optional[bool], 
                            ratio: bool) -> None:
        self.default_time = time
        self.default_settings = settings
        self.ratio = ratio
        self.update_chart()
        
    def add_point(self, time, score, seconds, default) -> None:
        self.data_container.add_point(time, score, seconds, default)
        self.update_chart()
        
    def remove_point(self) -> None:
        row = None
        if not self.data_container.has_last():
            return
        row = self.data_container.remove_last()
        self.update_chart()
        # in the future, put row onto the output message box
        