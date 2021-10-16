# -*- encoding = utf-8 -*-
import  pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
df1=pd.read_csv("东京奥运会奖牌数据.csv")
df2=pd.read_csv("东京奥运会奖牌分日数据.csv")
import warnings
warnings.filterwarnings("ignore")
# print(df1.head())
# print(df2.head())

df1.rename(columns={"Unnamed: 2":"金牌数",
                    "Unnamed: 3":"银牌数",
                    "Unnamed: 4":"铜牌数"

                    },inplace=True)
# print(df1.head())

# print(df2.info())
# print(df2["获奖时间"].head())
df2["获奖时间"]=pd.to_datetime(df2["获奖时间"])
# print(df2["获奖时间"].head())
df2=df2.sort_values(by=["获奖时间","奖牌类型"],ascending=True)
# print(df2.head())
temp=pd.merge(df1,df2,on="国家id")
# print(temp)
temp["获奖时间"]=pd.to_datetime(temp["获奖时间"])
# print(temp)
temp=temp.sort_values(by=["获奖时间","奖牌类型"],ascending=True)
df2["国家"]=temp["国家奥委会"]
# print(df2)
# print(temp)

df=df2.groupby("国家")["奖牌类型"].count().sort_values(ascending=False)
# print(df.head())

# print(df2["运动员"].value_counts().sort_values(ascending=False).head())

# print(df2[df2["运动类别"]=="乒乓球"])+

result=pd.pivot_table(df2,values=["奖牌类型"],index=["国家","运动类别"],aggfunc="count")
# print(result)

# print(result.query("国家==['中国']"))
import matplotlib.pyplot as plt
(result.query("国家 == ['中国']")
.style
.bar(subset=['奖牌类型'],color='skyblue'))
plt.show()

def time_format(x):
    return x.strftime('%m{m}%d{d} ').format(m='月',d='日')

df2['获奖时间'] = df2['获奖时间'].map(time_format)
# print(df2)

# print(df2.groupby("获奖时间")["国家"].count().sort_values())
# print(pd.pivot_table(df2,values = ['奖牌类型'],index = ['运动类别','国家'],aggfunc = 'count'))
# print(pd.pivot_table(df2,values=["奖牌类型"],index=["获奖时间","国家"],aggfunc="count").query("国家==['中国']").cumsum())

data = pd.pivot_table(df2,values = ['奖牌类型'],index = ['获奖时间','国家'],aggfunc = 'count').query("国家 == ['美国', '中国', '日本', '英国', 'ROC', '澳大利亚', '荷兰', '法国', '德国', '意大利']")
data=data.unstack()
data.columns=data.columns.get_level_values(1)
data.columns.name=None
data=data.cumsum()
data=data.fillna(axis=0,method="ffill").fillna(0)
# print(df1)
import matplotlib as mpl
import numpy as np
# print(df1["金牌数"][:20] )
#
#
# plt.rcdefaults()
# fig, ax = plt.subplots()
# # Example data
#
# y_pos = np.arange(len(df1["国家奥委会"][:20]))
#
#
#
# ax.barh(y_pos, df1["金牌数"][:20] , align='center')
# ax.set_yticks(y_pos)
# ax.set_yticklabels(df1["国家奥委会"][:20])
# ax.invert_yaxis()  # labels read top-to-bottom
# plt.title("东京奥运会金牌排行榜")
#
# plt.show()





from pyecharts import options as opts
from pyecharts.charts import Bar,Pie
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
gold = list(df1['金牌数'].head(10))
silver = list(df1['银牌数'].head(10))
bronze = list(df1['铜牌数'].head(10))
countrys = list(df1['国家奥委会'].head(10))
c = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(countrys)
    .add_yaxis("金牌", gold, stack="stack1", category_gap="50%")
    .add_yaxis("银牌", silver, stack="stack1", category_gap="50%")
    .add_yaxis("铜牌", bronze, stack="stack1", category_gap="50%")
    .set_series_opts(
        label_opts=opts.LabelOpts(
            position="right",

        )
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="东京奥运会榜10奖牌分布"))
    .render()

)


data = pd.pivot_table(df2,values = ['奖牌类型'],index = ['国家','运动类别'],aggfunc = 'count').query("国家 == ['中国']")
jiangpai = list(data['奖牌类型'])
xiangmu = [data.index[i][1] for i in range(len(data))]
print(data)
print(jiangpai)
print(xiangmu)
(
    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add(
        "",
        [list(z) for z in zip(xiangmu, jiangpai)],
        radius=["40%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="中国队奖牌分布"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("1.html")
)





(
    Pie(init_opts=opts.InitOpts(width="560px", height="500px"))
    .add(
        series_name="",
        data_pair=[list(z) for z in zip(xiangmu, jiangpai)],
        radius=["50%", "70%"],
        label_opts=opts.LabelOpts(is_show=False, position="center"),
    )
     .set_global_opts(
        title_opts=opts.TitleOpts(title="中国队奖牌分布"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
    )
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        # label_opts=opts.LabelOpts(formatter="{b}: {c}")
    )
    .render("doughnut_chart.html")
)

import bar_chart_race as bcr
data = pd.pivot_table(df2,values = ['奖牌类型'],index = ['获奖时间','国家'],aggfunc = 'count').query("国家 == ['美国', '中国', '日本', '英国', 'ROC', '澳大利亚', '荷兰', '法国', '德国', '意大利']")
data = data.unstack()
data.columns = data.columns.get_level_values(1)
data.columns.name = None
data = data.cumsum()
data = data.fillna(axis=0,method='ffill').fillna(0)
data.columns = ['Russia', 'China','Italian', 'Japan', 'the Netherlands',' German ',' France ', 'Australia', 'US',' British ']

def time_format(x):
    x = x.replace('月','-')
    x = x.replace('日','')
    x = '2021-' + x
    return x
data = data.reset_index()
data['获奖时间'] = data['获奖时间'].map(time_format)
data['获奖时间'] = pd.to_datetime(data['获奖时间'])
data = data.set_index('获奖时间')
print(data)
