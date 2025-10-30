import pandas as pd
from pathlib import Path
from importlib import resources
from activities import data
import matplotlib.pyplot as plt

def prepare_paralympics_data(df_raw, df_npc):
    cols_to_drop = ['URL', 'disabilities_included', 'highlights']
    present_to_drop = []
    for c in cols_to_drop:       # 遍历每个要删除的列名
        if c in df_raw.columns:  # 如果这列真的存在
            present_to_drop.append(c)

    df_prepared = df_raw.drop(columns=present_to_drop)
    df_prepared = df_prepared.drop(index=[0, 17, 31])
    df_prepared = df_prepared.reset_index(drop=True)
    df_prepared.loc[df_prepared['type'] == 'Summer', 'type'] = 'summer'
    df_prepared['type'] = df_prepared['type'].str.strip()
    

    columns_to_change= ['countries', 'events', 'participants_m', 'participants_f', 'participants']
    df_prepared[columns_to_change] = df_prepared[columns_to_change].astype('Int64')
    
    df_prepared['start'] = pd.to_datetime(df_prepared['start'], format='%d/%m/%Y')
    df_prepared['end'] = pd.to_datetime(df_prepared['end'], format='%d/%m/%Y')
    duration_values = (df_prepared['end'] - df_prepared['start']).dt.days.astype('Int64')
    df_prepared.insert(df_prepared.columns.get_loc('end') + 1, 'duration', duration_values)
    
    replacement_names = {
    'UK': 'Great Britain',
    'USA': 'United States of America',
    'Korea': 'Republic of Korea',
    'Russia': 'Russian Federation',
    'China': "People's Republic of China"
    }
    df_prepared['country'] = df_prepared['country'].replace(replacement_names)
    df_prepared = df_prepared.merge(df_npc, how='left', left_on='country', right_on='Name')
    print(df_prepared[['country', 'Code', 'Name']])
    df_prepared = df_prepared.drop(columns=['Name'])

    data_dir = Path(resources.files(data)) 
    out_path = data_dir / "paralympics_prepared.csv"       # 输出文件路径
    df_prepared.to_csv(out_path, index=False)

    return df_prepared
    

if __name__ == '__main__':
    path_para_raw = resources.files(data).joinpath("paralympics_raw.csv")
    npc_codes_path = resources.files(data).joinpath("npc_codes.csv")
    df_data = pd.read_csv(path_para_raw)
    npc_codes = pd.read_csv(npc_codes_path, usecols=['Code', 'Name'])

    df_prepared = prepare_paralympics_data(df_data, npc_codes)
    pairs = (df_prepared[['host', 'country']]
         .drop_duplicates()
         .sort_values(by='country'))
    print(pairs)
    print(df_prepared[['year','start','end','type','host','country']].sort_values('start'))
    # 总量
    df_prepared.sort_values('year').plot(x='year', y='participants', kind='line', title='Participants (Total)')

    # 男女拆分
    df_prepared.sort_values('year').plot(x='year', y=['participants_m','participants_f'], kind='line',
                            title='Participants by gender')

    # 冬夏季分组
    by_type = df_prepared.sort_values('year').groupby('type')
    for t, sub in by_type:
        sub.plot(x='year', y='participants', kind='line', title=f'Participants — {t}')
    plt.show()

