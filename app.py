from pyecharts import options as opts
from pyecharts.charts import Map
from flask import Flask, render_template, request
from datetime import datetime

import pandas as pd
import sqlite3
import json
import re


app = Flask(__name__, static_folder='static', template_folder='templates')


def fetchdb(index_en='all', index_zh=None):
    conn = sqlite3.connect('db')
    cursor = conn.cursor()
    if index_en == 'all':
        data = cursor.execute("select * from nCoV where level = 3;").fetchall()
    else:
        data = cursor.execute(f"select * from nCoV where level = 4 and parent_name like '{index_zh}%';").fetchall()
    colnames = [x[0] for x in cursor.description]
    conn.close()
    data = pd.DataFrame(data, columns=colnames)
    data.sort_values('ann_date', ascending=False, inplace=True)
    df = data.groupby('area_name').head(1).copy()
    if index_en == 'all':
        with open('json/provinces.json', 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
    else:
        with open(f'json/{index_en}.json', 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
    df['area_name'] = df['area_name'].replace(dictionary)
    return df.dropna(axis=0, subset=['area_name']), str(datetime.strptime(max(df['ann_date']), '%Y%m%d').date())


def map_visualmap(df, up_to_date, map_name, title_suffix='') -> Map:
    now_num = (df['confirmed_num'] - df['cured_num'] - df['dead_num']).tolist()
    c = (
        Map(init_opts=opts.InitOpts())
        .add('现有确诊人数', [list(z) for z in zip(df['area_name'].tolist(), now_num)], map_name)
        .add('累计确诊人数', [list(z) for z in zip(df['area_name'].tolist(), df['confirmed_num'].tolist())], map_name)
        .add('累计治愈人数', [list(z) for z in zip(df['area_name'].tolist(), df['cured_num'].tolist())], map_name)
        .add('累计死亡人数', [list(z) for z in zip(df['area_name'].tolist(), df['dead_num'].tolist())], map_name)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"新型冠状肺炎最新情况（中国内地）{title_suffix}", subtitle=f'数据更新至{up_to_date}', subtitle_link='https://tushare.pro/', pos_left='center', title_textstyle_opts={'fontWeight': 'bolder', 'fontSize': 40, 'color': '#BC3B20'}, subtitle_textstyle_opts={'fontSize': 20, 'fontStyle': 'normal', 'color': 'lightgrey', 'fontFamily': 'SimSun'}),
            legend_opts=opts.LegendOpts(pos_top='middle', pos_right='10%', orient='vertical', textstyle_opts={'fontSize': 20}, selected_mode='single'),
            visualmap_opts=opts.VisualMapOpts(max_=sorted(now_num)[-2] if len(now_num) > 1 else sorted(now_num)[-1], pos_top='middle', pos_left='5%', textstyle_opts={'color': 'white'}, range_text=['High', 'Low']),
            tooltip_opts=opts.TooltipOpts(trigger='item', formatter='{b}</br>{a}:{c}')
        )
    )
    return c


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/')
def china():
    return render_template('map-china.html')


@app.route('/yunnan')
def yunnan():
    return render_template('map-provinces-yunnan.html')


@app.route('/neimenggu')
def neimenggu():
    return render_template('map-provinces-neimenggu.html')


@app.route('/beijing')
def beijing():
    return render_template('map-provinces-beijing.html')


@app.route('/jilin')
def jilin():
    return render_template('map-provinces-jilin.html')


@app.route('/sichuan')
def sichuan():
    return render_template('map-provinces-sichuan.html')


@app.route('/ningxia')
def ningxia():
    return render_template('map-provinces-ningxia.html')


@app.route('/anhui')
def anhui():
    return render_template('map-provinces-anhui.html')


@app.route('/shandong')
def shandong():
    return render_template('map-provinces-shandong.html')


@app.route('/shanxi')
def shanxi():
    return render_template('map-provinces-shanxi.html')


@app.route('/guangdong')
def guangdong():
    return render_template('map-provinces-guangdong.html')


@app.route('/guangxi')
def guangxi():
    return render_template('map-provinces-guangxi.html')


@app.route('/jiangsu')
def jiangsu():
    return render_template('map-provinces-jiangsu.html')


@app.route('/jiangxi')
def jiangxi():
    return render_template('map-provinces-jiangxi.html')


@app.route('/hebei')
def hebei():
    return render_template('map-provinces-hebei.html')


@app.route('/henan')
def henan():
    return render_template('map-provinces-henan.html')


@app.route('/zhejiang')
def zhejiang():
    return render_template('map-provinces-zhejiang.html')


@app.route('/hainan')
def hainan():
    return render_template('map-provinces-hainan.html')


@app.route('/hubei')
def hubei():
    return render_template('map-provinces-hubei.html')


@app.route('/hunan')
def hunan():
    return render_template('map-provinces-hunan.html')


@app.route('/gansu')
def gansu():
    return render_template('map-provinces-gansu.html')


@app.route('/fujian')
def fujian():
    return render_template('map-provinces-fujian.html')


@app.route('/guizhou')
def guizhou():
    return render_template('map-provinces-guizhou.html')


@app.route('/liaoning')
def liaoning():
    return render_template('map-provinces-liaoning.html')


@app.route('/chongqing')
def chongqing():
    return render_template('map-provinces-chongqing.html')


@app.route('/shaanxi')
def shaanxi():
    return render_template('map-provinces-shaanxi.html')


@app.route('/heilongjiang')
def heilongjiang():
    return render_template('map-provinces-heilongjiang.html')


@app.route('/xinjiang')
def xinjiang():
    return render_template('map-provinces-xinjiang.html')


@app.route('/qinghai')
def qinghai():
    return render_template('map-provinces-qinghai.html')


@app.route('/tianjin')
def tianjin():
    return render_template('map-provinces-tianjin.html')


@app.route('/shanghai')
def shanghai():
    return render_template('map-provinces-shanghai.html')


@app.route('/xizang')
def xizang():
    return render_template('map-provinces-xizang.html')


@app.route('/data', methods=['POST'])
def ajax():
    if request.form['type'] == 'map-china':
        df, up_to_date = fetchdb()
        return map_visualmap(df, up_to_date, 'china').dump_options_with_quotes()
    else:
        province_en = re.search(r'\w+$', request.form['type']).group(0)
        with open(f'json/en_zh_provinces.json', 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
        province_zh = dictionary[province_en]
        df, up_to_date = fetchdb(province_en, province_zh)
        return map_visualmap(df, up_to_date, province_zh, f'- {province_zh}').dump_options_with_quotes()


if __name__ == '__main__':
    app.run(threaded=True)
