.. _integrator_fulltext_search:

Full-text search
================

If *full-text search* is enabled in the application, a table dedicated to
full-text search is needed in the database.

Create the full-text search table
---------------------------------

This full-text search table must be named ``tsearch`` (for *text search*) and
must be in the application-specific schema.

To create the table, the following SQL can be used::

    $ sudo -u postgres psql -c "CREATE TABLE <schema_name>.tsearch (
        id SERIAL PRIMARY KEY,
        layer_name TEXT,
        label TEXT,
        ts TSVECTOR);" <db_name>
    $ sudo -u postgres psql -c "SELECT AddGeometryColumn('<schema_name>', 'tsearch', 'the_geom', <srid>, 'GEOMETRY', 2);" <db_name>
    $ sudo -u postgres psql -c "CREATE INDEX tsearch_ts_idx ON <schema_name>.tsearch USING gin(ts);" <db_name>
    $ sudo -u postgres psql -c "GRANT SELECT ON TABLE <schema_name>.tsearch TO "<db_user>";" <db_name>

with ``<schema_name>``, ``<srid>``, and ``<db_user>`` substituted as
appropriate.

Populate the full-text search table
-----------------------------------

Here's an example of an insertion in the ``tsearch`` table::

    INSERT INTO app_schema.tsearch
      (the_geom, layer_name, label, ts)
    VALUES
      (ST_GeomFromText('POINT(2660000 1140000)', 21781, 'Layer group',
       'text to display', to_tsvector('french', 'text to search'));

Where ``Layer group`` is the name of the layer group that should be activated,
``text to display`` is the text that is displayed in the results,
``test to search`` is the text that we search for,
``french`` is the used language.

Here's another example where rows from a ``SELECT`` are inserted::

    INSERT INTO app_schema.tsearch
      (the_geom, layer_name, label, ts)
    SELECT
      geom, 21781, 'layer group name', text, to_tsvector('german', text)
    FROM table;

