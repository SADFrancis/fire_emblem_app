# Fire Emblem Heroes Resplendent API

A REST API for new characters who receive "resplendent" skins (new art) for the mobile title Fire Emblem Heroes. The data is stored in a Django database.

## Endpoints

The API is hosted at: `https://feh-resplendent.herokuapp.com/`

Here are the available endpoints:

Endpoint | Method | Body | Description
--- | --- | --- | ---
`/realms/` | GET | null | Returns each Realm name
`/realms/id` | GET | null | Returns all resplendent units sharing a design theme of a specific realm
`/characters/` | GET/POST | null | Returns an array of characters and allows to create one
`/characters/<str:Name>` | GET | null | Returns all resplendent characters with (case insensitve) Name (`/characters/Ishtar`)
`/characters/latest` | GET | null | Returns the most recently revealed unit published on the site
`/titles/` | GET | null | Returns a dictionary of game titles
`/titles/<str:key>` | GET | null | Returns all archived characters from the game title of a corresponding key (`/titles/FE1`). Current and future units are omitted due to lack of data.
`/year/` | GET | null | Returns all characters, for year filtering
`/year/<str:year>` | GET | null | Returns all characters of a specified year
`/year/<str:year>/<str:month>` | GET | null | Returns all characters of a specified year and month (`/year/2020/2`)

