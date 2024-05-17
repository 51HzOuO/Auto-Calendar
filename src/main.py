import auto_calendar
import utils

instance1 = auto_calendar.auto_calendar()

instance1.get_codeforces_contest()
instance1.get_atcoder_contest()
instance1.get_nowcoder_contest()
instance1.get_luogu_contest()
# instance1.get_lanqiao_contest()

utils.show_notification()
