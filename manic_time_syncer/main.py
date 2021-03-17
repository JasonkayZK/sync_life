import datetime
import sqlite3

now = datetime.datetime.now()
before_time = now + datetime.timedelta(hours=-24)

sql_str = """select
    cg.Name ApplicationName,
    sum((julianday(datetime(a.EndLocalTime))-julianday(datetime(a.StartLocalTime))))*24*60 sum_time
from
    Ar_Activity a
join
    Ar_CommonGroup cg on a.CommonGroupId = cg.CommonId
join
    Ar_Timeline t on a.ReportId = t.ReportId
join
    Ar_User u on u.UserId = t.OwnerId
where
    t.SchemaName = 'ManicTime/Applications' and
    a.StartLocalTime > '{}' and
    a.EndLocalTime < '{}'
group by ApplicationName
ORDER BY sum_time desc 
LIMIT 15""".format(before_time.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m-%d %H:%M:%S"))

# print(sql_str)

conn = sqlite3.connect('D:\\ManicTime-Backup\\ManicTimeReports.db')
# conn = sqlite3.connect('/root/workspace/manictimeserver/Data/ManicTimeReports.db')
cursor = conn.cursor()

cursor.execute(sql_str)

values = cursor.fetchall()

print(values)
