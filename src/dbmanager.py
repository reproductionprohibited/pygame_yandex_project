import string
import sqlite3
import typing as tp


class DBManager:
    valid_chars = string.ascii_letters + string.digits + '.-()[]:;'

    def __init__(self, db_filepath: str) -> None:
        self.connection = sqlite3.connect(database=db_filepath)
        self.cursor = self.connection.cursor()
        self.__init_high_scores_table()
    
    def __init_high_scores_table(self) -> None:
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS scores
                (id INTEGER PRIMARY KEY AUTOINCREMENT, points INTEGER, fruit INTEGER, coins INTEGER)
        '''
        )

    def save_new_run_record(
        self,
        points: int,
        fruit: int,
        coins: int,
    ):
        self.cursor.execute(
            f'''
            INSERT INTO scores(points, fruit, coins)
                VALUES ({points}, {fruit}, {coins})
        '''
        )
        self.connection.commit()

    def get_top_runs_points(self) -> tp.List[tp.Tuple[str, int]]:
        top_3_runs_by_pts = self.cursor.execute(
            '''
            SELECT points FROM scores
            ORDER BY points DESC
            LIMIT 3
        '''
        ).fetchall()
        return top_3_runs_by_pts
    
    def get_top_runs_fruit(self) -> tp.List[tp.Tuple[str, int]]:
        top_3_runs_by_fruit = self.cursor.execute(
            '''
            SELECT fruit FROM scores
            ORDER BY fruit DESC
            LIMIT 3
        '''
        ).fetchall()
        return top_3_runs_by_fruit
    
    def get_top_runs_coins(self) -> tp.List[tp.Tuple[str, int]]:
        top_3_runs_by_coins = self.cursor.execute(
            '''
            SELECT coins FROM scores
            ORDER BY coins DESC
            LIMIT 3
        '''
        ).fetchall()
        return top_3_runs_by_coins
    
    def get_top_runs_sum(self) -> tp.List[tp.Tuple[str, int]]:
        top_3_runs_by_sum = self.cursor.execute(
            '''
            SELECT (points + fruit + coins) FROM scores
            ORDER BY (points + fruit + coins) DESC
            LIMIT 3
        '''
        ).fetchall()
        return top_3_runs_by_sum

    def __shut_connection(self) -> None:
        self.cursor.close()
        self.connection.close()
    
    def __del__(self) -> None:
        self.__shut_connection()
