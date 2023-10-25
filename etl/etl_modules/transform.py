from etl import models


class TransformToElastic:

    def transform_genres(self, genres) -> list[models.ElasticGenreRecord]:
        return [models.ElasticGenreRecord(
            uuid=rec['id'],
            name=rec['name'],
        ) for rec in list(genres)]

    def transform_persons(self, genres) -> list[models.ElasticPersonRecord]:
        return [models.ElasticPersonRecord(
            uuid=rec['id'],
            full_name=rec['full_name'],
            actors=self.get_films_nested(
                record=rec['films'], role_type=models.RoleType.ACTOR
            ),
            writers=self.get_films_nested(
                record=rec['films'], role_type=models.RoleType.WRITER
            ),
            directors=self.get_films_nested(
                record=rec['films'], role_type=models.RoleType.DIRECTOR,
            )
        ) for rec in list(genres)]

    def transform_films(self, films) -> list[models.ElasticFilmRecord]:
        return [models.ElasticFilmRecord(
            uuid=rec['id'],
            title=rec['title'],
            description=rec['description'],
            imdb_rating=rec['rating'],
            genre=self.get_genres(rec['genres']),
            director=self.get_director(rec['persons']),
            actors_names=self.get_persons_names(
                record=rec['persons'], role_type=models.RoleType.ACTOR
            ),
            writers_names=self.get_persons_names(
                record=rec['persons'], role_type=models.RoleType.WRITER
            ),
            actors=self.get_persons_nested(
                record=rec['persons'], role_type=models.RoleType.ACTOR
            ),
            writers=self.get_persons_nested(
                record=rec['persons'], role_type=models.RoleType.WRITER
            ),
            directors=self.get_persons_nested(
                record=rec['persons'], role_type=models.RoleType.DIRECTOR,
            )
        ) for rec in list(films)]

    def get_director(self, record: list) -> str | list:
        dir_filtered = self._filtered_roles(record, role=models.RoleType.DIRECTOR)
        if dir_filtered:
            return dir_filtered[0]['person_name']
        return []

    def get_persons_names(self, record, role_type: models.RoleType):
        filtered = self._filtered_roles(record, role=role_type)
        return [p['person_name'] for p in filtered]

    def get_genres(self, record):
        return [{'uuid': act['genre_id'], 'name': act['genre_name']} for act in record]

    def get_persons_nested(self, record, role_type: models.RoleType):
        filtered = self._filtered_roles(record, role=role_type)
        return [{'uuid': act['person_id'], 'full_name': act['person_name']} for act in filtered]

    def _filtered_roles(self, record, role: models.RoleType) -> list:
        return list(filter(lambda person: person['person_role'] == role.value, record))

    def get_films_nested(self, record, role_type: models.RoleType):
        filtered = self._filtered_roles(record, role=role_type)
        return [{'uuid': act['film_id'], 'title': act['title']} for act in filtered]
