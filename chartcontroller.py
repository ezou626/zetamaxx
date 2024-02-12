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
        
    @property
    def default_time(self):
        return self.default_time
    
    @default_time.setter
    def default_time(self, new_value):
        if (new_value and type(new_value) != bool):
            raise ValueError('Must be of type Optional[bool]')
        self.default_time = new_value
        
    @property
    def default_settings(self):
        return self.default_settings
    
    @default_settings.setter
    def default_settings(self, new_value):
        if (new_value and type(new_value) != bool):
            raise ValueError('Must be of type Optional[bool]')
        self.default_settings = new_value
        
    @property
    def ratio(self):
        return self.ratio
    
    @ratio.setter
    def ratio(self, new_value):
        if (new_value and type(new_value) != bool):
            raise ValueError('Must be of type Optional[bool]')
        self.ratio = new_value
        
    def _update_chart(self):
        """Utility method to update chart with query
        """
        x, y, limits = self.data_container.get_data(self.default_time,
                                                    self.default_settings,
                                                    self.ratio)
        self.chart.update_chart(x, y, limits)
        
    def add_point(self, time, score, seconds, default):
        self.data_container.add_point(time, score, seconds, default)
        self._update_chart()
        
    def remove_point(self):
        row = None
        if not self.data_container.has_last():
            return
        row = self.data_container.remove_last()
        self._update_chart()
        # in the future, put row onto the output message box
        return row
        