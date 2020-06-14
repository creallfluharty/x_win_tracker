# X Window Activity Tracker

Little sandbox project for me to manage a database and develop a app usage tracker. Very unfinished.

## Black Triangle

```bash
$ alembic upgrade head
$ python main.py
```

At which point the program should start spewing out some information about which windows have been opened / changed

## TODO

Basically everything. There's a database with the right schemas, but the activity tracker isn't hooked up to it yet.

More Specifically:

- Output the activities to the database (as well as hopefully make it possible to attach other outputs)
- Don't just track the name of windows (adjust the table as well as the tracking)
- Create some mechanism for permanently identifying each window (since X window IDs are reused)
- Maybe someday add some (web) front-end to the database
- Clean up the `orm/` folder (simultaneously over-engineered and not as flexible as it seems)


## Schema

Not that this is of much use while the database is unused, but in any case, here's a sketch-up of the current tables (also see `orm/tables`):

![][doc/activity_tracker_db.png]