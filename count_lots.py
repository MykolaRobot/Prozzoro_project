import pandas as pd


class DataPreproccessing:
    def __init__(self, data_source, churn_interval, start_period=None, end_period=None):
        # для статистики постачальника вибираємо проміжок [start_period,end_period]
        self.divide_data = pd.to_datetime('2018-12-20') - pd.DateOffset(days=churn_interval)
        self.data_source = data_source[pd.to_datetime(data_source['date_from_id']) <= self.divide_data]
        # для labeling вибираємо період [end_period, end_period+churn_interval]
        self.label_data = data_source[pd.to_datetime(data_source['date_from_id']) > self.divide_data]
        # вибираємо унікальних постачальників
        self.unique_id = list(self.data_source['participants'].value_counts().index)
        # створюємо dataframe з колонкою унікальних постачальників і туди будемо додавати features
        self.feature_data = pd.DataFrame(self.unique_id, columns=['unique_id'])

    def create_features(self):
        self.count_lots()

    def count_lots(self):
        freq = self.data_source['participants'].value_counts()

        def count_lots(raw, frequency):
            raw['count_lots'] = frequency[raw['unique_id']]
            return raw

        self.feature_data = self.feature_data.apply(count_lots, args=(freq,), axis=1)

    def count_win_lose(self):
        def win_lose(raw, data_source):
            d = data_source[data_source['participants'] == raw['unique_id']]
            # feature_engineering
            # 1. how many win
            raw['win'] = d[d['winner'] == 1].shape[0]
            raw['lose'] = raw['count_lots'] - raw['win']
            # 2. win in open and not open tenders
            d_open = d[d['tenders.procurementMethod'] == 'open']
            raw['count_open_lots'] = d_open.shape[0]
            raw['count_not_open_lots'] = raw['count_lots'] - raw['count_open_lots']
            #
            raw['win_open'] = d[d['winner'] == 1].shape[0]
            raw['win_not_open'] = raw['win'] - raw['win_open']
            # 3.
            raw['lose_open'] = d[d['winner'] == 0].shape[0]
            raw['lose_not_open'] = raw['lose'] - raw['lose_open']
            # інші ф-ції для features
            return raw

        self.feature_data = self.feature_data.apply(win_lose, args=(
            self.data_source[['participants', 'winner', 'tenders.procurementMethod']],), axis=1)

    def last_activity(self):
        def last_active(raw, data_source):
            # треба визначити останню активність учасника. Якщо лот конкурентний - біди, якщо неконкурентний - аварди.
            # self.divide_data - остання активність в днях
            raw['last_activity'] =  # self.divide_data - остання активність в днях

        self.feature_data = self.feature_data.apply(last_active, args=(
            self.data_source[['participants', 'tenders.procurementMethod',...]],), axis=1)



# df = pd.read_csv('part_50.csv', dtype={'unique_id': 'Int64'})
# prepr = DataPreproccessing(df, 100)
# prepr.create_features()
# d = prepr.feature_data
# print(d.head())
# a = 5
