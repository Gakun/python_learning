import psycopg2
import matplotlib.pyplot as plt
from pandas import DataFrame


# Connect
_database = 'ffs'
_host = 'bicluster-ffs.cpaytjecvzyu.us-west-2.redshift.amazonaws.com'
_port = '5439'
_user = 'zhisheng'
_password = 'Fkrku8Wws8LszYUw'
print 'Connecting...'
conn = psycopg2.connect(database=_database, host=_host, port=_port, user=_user, password=_password)
cur = conn.cursor()
print 'Connected!'

cur.execute("""
    select json_extract_path_text(properties, 'quest_ID') as id,
    json_extract_path_text(properties, 'level')::int as level
    from events_raw
    where ts >= '2017-06-06' and ts <= '2017-08-06' and event = 'QuestComplete'
    and json_extract_path_text(properties, 'quest_ID') in
    ('9000','9001','9002','9003','9004','9005', '9006','9007','9008','9009',
    '9018','9011','9012','9013','9014','9015','9016','9017', '9031');
    """)


rows = cur.fetchall()
df = DataFrame(rows, columns=['id', 'level'])

id_list = ['9000','9001','9002','9003','9004','9005', '9006','9007','9008','9009',
'9018','9011','9012','9013','9014','9015','9016','9017', '9031']

print 'Ploting'
# Create subplots
fig, axes = plt.subplots(1, len(id_list), sharey=True)

# Draw boxplots in the order of id_list
for j in range(len(id_list)):
    sub_df = df[df['id'] == id_list[j]]

    try:
        sub_df.boxplot(ax=axes[j], showfliers=False, widths=0.3)
        median = int(round(sub_df.level.median()))
        # Calculate .25 and .75 quantiles value, data must be float
        quantile25 = int(round(sub_df.level.quantile(0.25)))
        quantile75 = int(round(sub_df.level.quantile(0.75)))
        # Plot quantiles and median
        # Both coordinate and label are relative to axes itself
        axes[j].text(0.6, quantile25 - 0.5, str(quantile25), fontsize=10)
        axes[j].text(1.2, median - 0.5, str(median), fontsize=10)
        axes[j].text(0.6, quantile75 - 0.5, str(quantile75), fontsize=10)
        axes[j].set_xticklabels((id_list[j],), fontsize=10)  # Pass 1 element tuple, must be (a,) xticklabel: x axis scale
        ## Different with xticklabels
        #axes[j].set_xlabel(id_list[j])  #xlabel: the label of x axis
    except:
        print "Empty data"

plt.show()
