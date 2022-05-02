import pandas as pd
import pymysql
import seaborn as sns
import matplotlib.pyplot as plt

conn = pymysql.connect(user='root', password='root', database='GL_OffLine', host='10.170.2.108', port=3306)
# cursor = conn.cursor()
# cursor.execute('select * from otn_performance')

OTN_Performance = pd.read_sql("select recvData from otn_performance where equipment_id=391", con=conn)

plt.figure(figsize=(12, 14))
plt.title('OTN performance')
sns.barplot(x='Date', y='Receive Data', data=OTN_Performance)
sns.set_style('whitegrid', {'font.sans-serif': ['simhei', 'Arial']})
