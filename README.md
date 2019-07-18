# Starship Trader

## Importing ship models

Importing ship models from the SWAPI is done via a management command so this command can be run regularly on a cron job.

The command is as follows: `./manage.py update_database`

## Creating new ship models

`POST: /shiptrader/starships/`

Example JSON payload:

```
    {
        "model": "Sentinel-class landing craft",
        "starship_class": "landing craft",
        "manufacturer": "Sienar Fleet Systems, Cyngus Spaceworks",
        "length": 38.0,
        "hyperdrive_rating": 1.0,
        "cargo_capacity": 180000,
        "crew": 5,
        "passengers": 75
    }
```

## Getting ship models

Get all ships:

`GET: /shiptrader/starships/`

Get specific ship class

`GET: /shiptrader/starships/?class=landing%20craft`

Get specific ship

`GET: /shiptrader/starships/<ship_id>/`

## Deleting ship models

`DELETE: /shiptrader/starships/<ship_id>/`

## Creating new listing

`POST: /shiptrader/listings/`

Example JSON payload:

```
    {
        "name": "test",
        "price": 399,
        "active": false,
        "ship_type": 1
    }
```

"ship_type" refers to the ID of a the star ship model in the database.

## Getting listings

Get all listings:

`GET: /shiptrader/listings/`

Get specific listing 

`GET: /shiptrader/listing/<listing_id>/`

## Activating/Deactivating listings

Activating and deactivating listings can be done with the following action endpoint

Activate: `PATCH: /shiptrader/listing/<listing_id>/action/activate/`

Deactivate `PATCH: /shiptrader/listing/<listing_id>/action/deactivate/`

## Sorting results

Results lists can be sorted either ascending or descending on any value using the `sort_asc` or `sort_desc` query parameter.

Examples:

Sorting ships by length: `GET: /shiptrader/starships/?sort_asc=length`

Sorting listings by price: `GET: /shiptrader/listings/?sort_desc=price`


