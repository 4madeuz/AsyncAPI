sql_queries = {
    'films': """SELECT
   fw.id,
   fw.title,
   fw.description,
   fw.rating,
   fw.created,
   fw.modified,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
   ) as persons,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'genre_name', g.name,
               'genre_id', g.id
           )
       ) FILTER (WHERE g.id is not null),
       '[]'
   ) as genres
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.modified > %s OR p.modified > %s OR g.modified > %s
GROUP BY fw.id
ORDER BY fw.modified;
""",
    'genres': """SELECT
    g.id,
    g.name
    FROM content.genre g
    WHERE g.modified > %s
    ORDER BY g.modified;
    """,
    'persons': """SELECT
    p.id,
    p.full_name,
    COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'film_id', fw.id,
               'title', fw.title
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
   ) as films
    FROM content.person p
    LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
    LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
    WHERE p.modified > %s
    GROUP BY p.id
    ORDER BY p.modified;
    """,
}
