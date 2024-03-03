from typing import Optional
from visualization import Chart, Stats
from data_container import DataContainer
from datetime import datetime

class Controller():
    """Controls the updates of the chart and other display widgets, stores state"""
    
    def __init__(self, chart: Chart, stats: Stats, data_container: DataContainer):
        """Sets up initial settings

        Args:
            chart (Chart): the chart being managed
            data_container (DataContainer): the data container being used
        """
        
        self.chart = chart
        self.stats = stats
        self.data_container = data_container

        self.default_time = True
        self.default_settings = True
        self.ratio = False
        
    def update_displays(self):
        """Update chart with current display settings"""
        
        x, y, limits = self.data_container.get_data(self.default_time,
                                                    self.default_settings,
                                                    self.ratio)
        self.chart.update_chart(x, y, limits)
        if len(y) != 0:
            self.stats.update_stats(y.max(), round(y.mean(), 3))
        else:
            self.stats.update_stats('-', '-')
        
    def set_display_options(self, 
                            time: Optional[bool], 
                            settings: Optional[bool], 
                            ratio: bool) -> None:
        """Change current display settings

        Args:
            time (Optional[bool]): Standard time setting, None if all
            settings (Optional[bool]): Standard settings, None if all
            ratio (bool): Whether to display data as ratio
        """
        
        self.default_time = time
        self.default_settings = settings
        self.ratio = ratio
        self.update_displays()
        
    def add_point(self, time: datetime, score: int, seconds: int, default: bool) -> None:
        """Adds a datapoint to data container and update chart

        Args:
            timestamp (datetime.datetime): Time of result
            score (int): Score achieved
            seconds (int): Number of seconds in time limit
            default (bool): True if default settings, False otherwise
        """
        
        self.data_container.add_point(time, score, seconds, default)
        self.update_displays()
        
    def remove_point(self) -> None:
        """Removes last data entry if it exists added and updates chart"""
        
        row = None
        if not self.data_container.has_last():
            return
        row = self.data_container.remove_last()
        self.update_displays()
        # in the future, put row onto the output message box
        