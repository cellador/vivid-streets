let res = [
  db.loc.createIndex({ longitude: 1 }),
  db.loc.createIndex({ latitude: 1 }),
  db.loc.insert({ longitude: 8.689848, latitude: 49.408508}),
  db.loc.insert({ longitude: 8.72, latitude: 49.40}),
  db.loc.insert({ longitude: 8.8, latitude: 49.408508}),
]

printjson(res)
