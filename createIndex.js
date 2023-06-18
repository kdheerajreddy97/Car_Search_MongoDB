const connection = new Mongo(`localhost:27017`),
  db = connection.getDB(`Craiglist`),
  geoCollection = db.getCollection(`Cars`);

let result = 0;

geoCollection.updateMany(
  {},
  [
    {
      $set: {
        location: {
          // Using aggregation pipeline $cond operator
          // to populate `location` with null
          // if lat or long is empty.
          $cond: {
            if: {
              $or: [
                {
                  $eq: ["$long", ""]
                },
                {
                  $eq: ["$lat", ""]
                }
              ]
            },
            then: null,
            else: {
              type: `Point`,
              coordinates: ["$long", "$lat"]
            }
          }
        }
      }
    },
    {
      $unset: ["long", "lat"]
    }
  ]
);

geoCollection.createIndex( { location: `2dsphere` } );