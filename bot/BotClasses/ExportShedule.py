import datetime

from .StudentShedule import StudentShedule
from ics import Calendar, Event

tt_dict = {
    "08:00": "05:00",
    "09:40": "06:40",
    "11:20": "08:20",
    "13:30": "10:30",
    "15:10": "12:10",
    "16:50": "13:50",
    "18:25": "15:25",
    "20:00": "17:00",
    "08:00:00": "05:00:00",
    "09:40:00": "06:40:00",
    "11:20:00": "08:20:00",
    "13:30:00": "10:30:00",
    "15:10:00": "12:10:00",
    "16:50:00": "13:50:00",
    "18:25:00": "15:25:00",
    "20:00:00": "17:00:00",
}


class ExportShedule(StudentShedule):
    async def makeFile(self, week):

        c = Calendar()
        today = datetime.date.today()
        current_date = today - datetime.timedelta(days=today.isoweekday()) + datetime.timedelta(days=1)
        isNormal, response = await super()._get_response()
        days_in_week = list(response.keys())
        days_in_week.sort()

        current_week = 0
        while (current_week <= week):
            if str(current_date.isoweekday()) not in days_in_week:
                current_date += datetime.timedelta(days=1)
                continue
            for key in days_in_week:
                if (current_date.month == 12 and current_date.day == 30) or (
                        current_date.month == 7 and current_date.day == 1):
                    break
                chetnost = False if (datetime.date(current_date.year, current_date.month,
                                                   current_date.day).isocalendar()[
                                         1] + self.chetn) % 2 else True  # Если True чет, False - неч

                for row in response[key]:
                    dayDate = row["dayDate"].rstrip().lower()
                    prefix = ""

                    if (dayDate == 'чет' and not chetnost) or (dayDate == 'неч' and chetnost):
                        continue
                    elif dayDate == 'чет/неч':
                        if chetnost:
                            prefix = " (1) гр."
                        else:
                            prefix = " (2) гр."
                    elif dayDate == 'неч/чет':
                        if chetnost:
                            prefix = " (2) гр."
                        else:
                            prefix = " (1) гр."

                    e = Event()
                    tt = row["dayTime"].rstrip() if len(row["dayTime"].rstrip()) < 6 else row["dayTime"].rstrip()[:5]
                    tt = tt_dict[tt]
                    begin_time = str(current_date) + " {}:00".format(tt)
                    # end_time = str(current_date) + " {}:00".format(time_dict[row["dayTime"].rstrip()])
                    e.name = prefix + row["disciplType"].rstrip().upper() + " " + row["disciplName"].rstrip()
                    e.begin = begin_time
                    e.duration = datetime.timedelta(
                        minutes=190 if row["disciplType"].rstrip().upper() == 'Л.Р.' else 90)
                    e.location = "В {} ауд. {} зд".format(row["audNum"].rstrip(), row["buildNum"].rstrip())
                    e.description = "В {} ауд. {} зд".format(row["audNum"].rstrip(), row["buildNum"].rstrip())
                    c.events.add(e)
                current_date = current_date + datetime.timedelta(days=1)
                if str(current_date.isoweekday()) not in days_in_week:
                    current_date = current_date + datetime.timedelta(days=1)
                    continue
            current_week += 1
        return str(c).encode('UTF-8')
        # with open('{}.ics'.format(self.group_id), 'w', encoding="utf-8") as f:
        #     f.write(str(c))
