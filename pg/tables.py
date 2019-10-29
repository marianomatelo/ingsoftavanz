import django_tables2 as tables
from pg.models import Dataset_Meta, Daemon


class datasetTable(tables.Table):
    class Meta:
        model = Dataset_Meta


class runsTable(tables.Table):
    class Meta:
        model = Daemon