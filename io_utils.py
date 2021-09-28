from sqlite3 import connect

from pandas import read_sql, DataFrame, to_datetime


class DataBaseReader:
    def __init__(self, sqlite_db_path: str):
        self.__connection = connect(sqlite_db_path)

    def read_trading_session(self) -> DataFrame:
        data = read_sql("select * from trading_session", self.__connection, index_col="id")
        return data

    def read_chart_data(self) -> DataFrame:
        data = read_sql("select * from chart_data", self.__connection, index_col="id")
        return data

    def get_union_data(self, remove_duplicates: bool = True) -> DataFrame:
        trading_session = self.read_trading_session()
        chart_data = self.read_chart_data()
        union = chart_data.join(trading_session, on="session_id", how="inner")
        union["timestamp"] = to_datetime(union[["date", "time"]].apply(lambda row: " ".join(row), axis=1))
        union.drop(["date", "time"], axis=1, inplace=True)
        if remove_duplicates:
            union.sort_values(by="timestamp", inplace=True, ignore_index=True)
            union.drop_duplicates(subset="deal_id", keep="first", inplace=True)
        return union

    def close(self):
        self.__connection.close()
