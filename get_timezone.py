import tzlocal
import pytz

local_tz = tzlocal.get_localzone()
local_pytz = pytz.timezone(local_tz.key)