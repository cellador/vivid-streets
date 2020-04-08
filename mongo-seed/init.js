let res = [
  db.loc_public.createIndex({ longitude: 1 }),
  db.loc_public.createIndex({ latitude: 1 }),
  db.loc_public.insert({ longitude: 8.689848, latitude: 49.408508}),
  db.loc_public.insert({ longitude: 8.72, latitude: 49.40}),
  db.loc_public.insert({ longitude: 8.8, latitude: 49.408508}),
]

printjson(res)
