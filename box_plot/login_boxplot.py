import psycopg2
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame

# Connect to Database
print 'Connecting to datebase...'
conn = psycopg2.connect(database='ffs', host='bicluster-ffs.cpaytjecvzyu.us-west-2.redshift.amazonaws.com', port='5439', user='zhisheng', password='Fkrku8Wws8LszYUw')  # connect local database
cur = conn.cursor()
print 'Connected!'

cur.execute('''select * from
    (select trunc(ts) as date, os, json_extract_path_text(properties, 'dt')::numeric / 1000 as dt
    from events_raw where ts >= '2017-06-10' and ts <= '2017-06-16' and event = 'loading_light' and os in ('ffs.global.android', 'ffs.global.iOS') and json_extract_path_text(properties, 'action') = 'load total time')
    where dt <= 200
    ''')

rows = cur.fetchall()

df = DataFrame(rows, columns=['date', 'os', 'dt'])
df.dt = df.dt.astype(float)

# create sub-dataframe by date
date_list = np.sort(df.date.unique())
df_list = list()

i = 0
for i in range(len(date_list)):
    exec('df%d = DataFrame()' % i)
    exec('df%d = df[df.date == date_list[i]]' % i)
    exec('df_list.append(df%d)' % i)

# create subplots
fig, axes = plt.subplots(2, len(date_list), sharex=True)

# plot basic sub-boxplot
j = 0
sys = ['ffs.global.android', 'ffs.global.iOS']
for j in range(len(date_list)):
    df_list[j].boxplot(ax=axes[0, j], by='os', showmeans=True, showfliers=False)
    # add real data points to the figuer
    for k in range(len(sys)):
        y = df_list[j].dt[df.os == sys[k]].dropna()
        # add some random distance to the x-axis
        x = np.random.normal(k + 1, 0.04, size=len(y))
        axes[1, j].plot(x, y, 'r.', alpha=0.2)
        # plot mean value text
        mean = round(df_list[j].dt[df_list[j].os == sys[k]].mean(), 2)
        median = round(df_list[j].dt[df_list[j].os == sys[k]].median(), 2)
        axes[0, j].text(k + 1.1, mean, 'mean: ' + str(mean), fontsize=9)   # WARNING: if some version's data is lacked at some date, will throw error
        axes[0, j].text(k + 1.1, median, 'median: ' + str(median), fontsize=9)

    axes[0, j].set_title(date_list[j], fontsize=10)
    axes[0, j].set_xlabel('')

axes[0, 0].set_ylabel('t(seconds)')
axes[1, 0].set_ylabel('t(seconds)')
fig.suptitle('Loading Time - Login - Total', fontsize="x-large")
plt.subplots_adjust(wspace=None, hspace=None)  # doesn't work??

plt.show()
