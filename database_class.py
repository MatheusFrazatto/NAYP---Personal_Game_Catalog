import sqlite3


class Database:
    def __init__(self, db_name='gamelog.db'):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS games (
                id_rawg INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                released TEXT,
                description TEXT,
                developers TEXT,
                publishers TEXT,
                genres TEXT
            );
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            if conn:
                conn.close()

    def add_game(self, game_data):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            insert_query = "INSERT OR IGNORE INTO games (id_rawg, name, released, description, developers, publishers, genres) VALUES (?, ?, ?, ?, ?, ?, ?);"

            developers_str = ", ".join(game_data.get('developers', []))
            publishers_str = ", ".join(game_data.get('publishers', []))
            genres_str = ", ".join(game_data.get('genres', []))

            game_tuple = (
                game_data.get('id'),
                game_data.get('name'),
                game_data.get('released'),
                game_data.get('description'),
                developers_str,
                publishers_str,
                genres_str
            )
            cursor.execute(insert_query, game_tuple)
            conn.commit()
        except sqlite3.Error as e:
            print(
                f"Error while trying to add game '{game_data.get('name')}': {e}")
        finally:
            if conn:
                conn.close()

    def list_all_games(self):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            select_query = "SELECT * FROM games;"
            cursor.execute(select_query)
            games = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error while trying to list all games: {e}")
        finally:
            if conn:
                conn.close()
        return games

    def delete_game(self, game_id):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            delete_query = "DELETE FROM games WHERE id_rawg = ?;"
            cursor.execute(delete_query, (game_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error while trying to delete game with ID {game_id}: {e}")
        finally:
            if conn:
                conn.close()
