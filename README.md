# uniquode
Web site - Uniquode.IO

## NOTES
(mainly reminders for myself)

- top level: `./initdb.sh -r` drops the roles and database, ready for all migrations.
- app level: `./manage.py migrations` to apply migrations
- app level: `./manage.py sitetree_resync_app` to re-generate the sitetree database from `<app_name>/sitetrees.py`
