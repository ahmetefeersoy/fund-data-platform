from dagster import Definitions, load_assets_from_modules
from . import ingestion, analytics

defs = Definitions(
    assets=[
        *load_assets_from_modules([ingestion]),
        *load_assets_from_modules([analytics]),
    ],
)
