import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from model.user import User
from model.stress_module import StressModule
from data_storage.data_store import IndicatorsDataStorage


class MenstruationDelayModule:
    def __init__(self, user: User, sm: StressModule, ds: IndicatorsDataStorage):
        self.user = user
        self.stress_module = sm
        self.ds = ds
        self.current_cycle = [[{}]]

        data = self.__form_training_data(self.__get_menstrual_info())[:10]
        self.normal_cycle_length = min([el['cycle_length'] for el in data])
        X = self.__create_np_array(data)
        y = np.array([d['cycle_length'] for d in data])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')
        print("\033[91mMenstruationDelayModule created! \033[0m")

    def __create_np_array(self, data: list[dict]) -> np.array:
        X = np.array([[d['abdominal_pain'], d['digestive_disorders'], d['breast_pain'], d['skin_rash'], d['bad_mood'],
                       d['neutral_mood'], d['good_mood'], d['stress']] for d in data])
        return X

    def __get_menstrual_info(self):
        return self.ds.get_menstual_info(self.user.name)

    def __convert_tuples_to_list_of_dicts(self, data: list[tuple]) -> list[dict]:
        data_headers = ['user_id', 'abdominal_pain', 'digestive_disorders', 'breast_pain', 'skin_rash', 'mood',
                        'menstruation_status', 'date']
        result_data = []
        for temp_tuple in data:
            result_data.append(dict(zip(data_headers, temp_tuple)))
        return result_data

    def __split_list_into_cycles(self, data):
        data = ['0' if el == '' else el for el in "".join([str(el) for el in data]).split("0")]
        prev = data[0]
        list_of_strs = []
        for i in range(1, len(data)):
            if data[i] == '0':
                prev += data[i]
            else:
                list_of_strs.append(prev)
                prev = data[i]
        list_of_strs.append(prev)

        cycles = []
        for el in list_of_strs:
            cycle = list(el)
            cycle = [int(day) for day in cycle]
            cycle.append(0)
            cycles.append(cycle)
        return cycles

    def __count_entries(self, indicator_str: str, indicator_int: int, data: list[dict]) -> int:
        return sum(1 for entry in data if entry[indicator_str] == indicator_int)

    def __get_start_date_of_cycle(self, data: list[dict]) -> str:
        return data[0]["date"]

    def __get_end_date_of_cycle(self, data: list[dict]) -> str:
        return data[-1]["date"]

    def __split_data_into_cycles(self, data: list[dict]) -> list[list[dict]]:
        new_list = []
        for string in data:
            new_list.append(string['menstruation_status'])
        cycles = self.__split_list_into_cycles(new_list)

        start = 0
        result_cycles = []
        for cycle in cycles:
            result_cycles.append(data[start:start + len(cycle)])
            start += len(cycle)
        return result_cycles

    def __form_temp_test_data(self, result_cycles: list[list[dict]]) -> list[dict]:
        cycles = []
        for cycle in result_cycles:
            abdominal_pain_counter = self.__count_entries('abdominal_pain', 1, cycle)
            digestive_disorders_counter = self.__count_entries("digestive_disorders", 1, cycle)
            breast_pain_counter = self.__count_entries('breast_pain', 1, cycle)
            skin_rash_counter = self.__count_entries('skin_rash', 1, cycle)
            bad_mood_counter = self.__count_entries('mood', 1, cycle)
            neutral_mood_counter = self.__count_entries('mood', 2, cycle)
            good_mood_counter = self.__count_entries('mood', 3, cycle)
            start_date = self.__get_start_date_of_cycle(cycle)
            end_date = self.__get_end_date_of_cycle(cycle)
            cycles.append({'abdominal_pain': abdominal_pain_counter,
                           "digestive_disorders": digestive_disorders_counter,
                           'breast_pain': breast_pain_counter,
                           'skin_rash': skin_rash_counter,
                           'bad_mood': bad_mood_counter,
                           'neutral_mood': neutral_mood_counter,
                           'good_mood': good_mood_counter,
                           'stress': self.stress_module.get_average_stress_by_period(start_date, end_date),
                           'cycle_length': len(cycle)})
        return cycles

    def __form_training_data(self, data: list[tuple]) -> list[dict]:
        data = self.__split_data_into_cycles(self.__convert_tuples_to_list_of_dicts(data))
        self.current_cycle = [data[-1]]
        res = self.__form_temp_test_data(data)
        return res

    # MAIN predict date
    def predict_menstruation(self) -> str:
        data = self.__form_temp_test_data(self.current_cycle)
        start_date = self.__get_start_date_of_cycle(self.current_cycle[0])
        data = self.__create_np_array(data)
        res_length = round(self.model.predict(data)[0])
        if res_length < self.normal_cycle_length:
            res_length = self.normal_cycle_length
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        res = start_date + timedelta(days=res_length)
        return res.strftime("%Y-%m-%d")

    def set_menstruation_data(self, data: dict):
        self.ds.insert_menstruation_data(data)

