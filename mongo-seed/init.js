let res = [
  db.loc.createIndex({ longitude: 1 }),
  db.loc.createIndex({ latitude: 1 }),
  db.loc.insert({ longitude: '35', latitude: '75'}),
  db.loc.insert({ longitude: '35.1', latitude: '75.1'}),
]

printjson(res)
