class Game:
    def __init__(self, api_data):
        self.id = api_data.get('id')
        self.name = api_data.get('name')
        self.released = api_data.get('released')
        self.description = api_data.get('description_raw')

        developers_list = api_data.get('developers', [])
        self.developers = [dev.get('name') for dev in developers_list]

        publishers_list = api_data.get('publishers', [])
        self.publishers = [pub.get('name') for pub in publishers_list]

        genres_list = api_data.get('genres', [])
        self.genres = [genre.get('name') for genre in genres_list]

    def __repr__(self):
        return f"Game(id={self.id}, name='{self.name}', released='{self.released}', developers={self.developers}, publishers={self.publishers}, genres={self.genres})"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'released': self.released,
            'description': self.description,
            'developers': self.developers,
            'publishers': self.publishers,
            'genres': self.genres
        }
