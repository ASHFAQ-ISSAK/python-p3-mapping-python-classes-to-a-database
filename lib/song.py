from config import CONN, CURSOR


class Song:
    def __init__(self, name, album):
        self.id = None
        self.name = name
        self.album = album

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """
        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.album))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM songs").fetchone()[0]

    @classmethod
    def create(cls, name, album):
        song = Song(name, album)
        song.save()
        return song


class TestClass:
    def test_creates_songs_table(self):
        Song.create_table()
        CURSOR.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='songs'"
        )
        result = CURSOR.fetchone()
        assert result is not None

    def test_initializes_with_name_and_album(self):
        song = Song("Hold On", "Born to Sing")
        assert song.name == "Hold On" and song.album == "Born to Sing"

    def test_saves_song_to_table(self):
        CURSOR.execute("DROP TABLE IF EXISTS songs")
        Song.create_table()

        song = Song("Hold On", "Born to Sing")
        song.save()
        db_song = CURSOR.execute(
            "SELECT * FROM songs WHERE name=? AND album=?", ("Hold On", "Born to Sing")
        ).fetchone()
        assert db_song[1] == song.name and db_song[2] == song.album

    def test_creates_and_returns_song(self):
        CURSOR.execute("DROP TABLE IF EXISTS songs")
        Song.create_table()

        song = Song.create("Hold On", "Born to Sing")
        db_song = CURSOR.execute(
            "SELECT * FROM songs WHERE name=? AND album=?", ("Hold On", "Born to Sing")
        ).fetchone()

        assert (
            db_song[0] == song.id
            and db_song[1] == song.name
            and db_song[2] == song.album
        )


# Create an instance of TestClass
test_instance = TestClass()

# Run the tests
test_instance.test_creates_songs_table()
test_instance.test_initializes_with_name_and_album()
test_instance.test_saves_song_to_table()
test_instance.test_creates_and_returns_song()
