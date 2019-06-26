import csv
import gzip
import logging
from math import ceil

from geo.models import GeographicFeature


class GNISLoader:

    allowed_feature_classes = {"AIRPORT", "CIVIL", "ISLAND", "POPULATED PLACE"}
    batch_size = 10000
    logger = logging.getLogger("moistmaster.geo")

    def __init__(self, path):
        self.path = path

    def load(self):
        with gzip.open(self.path, "rt", encoding="utf-8-sig") as fh:
            line_count = 0
            for i, _ in enumerate(fh):
                line_count += 1
            batch_count = ceil(line_count/self.batch_size)
            fh.seek(0)
            reader = csv.DictReader(fh, delimiter='|')
            kept, skipped, batch_number = (0, 0, 1)
            GeographicFeature.objects.all().delete()
            batch = []
            for row in reader:
                if row["FEATURE_CLASS"].upper() in self.allowed_feature_classes and row["FEATURE_ID"].isdigit():
                    if row["ELEV_IN_M"].isdigit():
                        elevation = int(row["ELEV_IN_M"])
                    else:
                        elevation = None
                    data = {
                        "usgs_id": int(row["FEATURE_ID"]),
                        "name": row["FEATURE_NAME"],
                        "kind": row["FEATURE_CLASS"],
                        "state": row["STATE_ALPHA"],
                        "county": row["COUNTY_NAME"],
                        "latitude": float(row["PRIM_LAT_DEC"]),
                        "longitude": float(row["PRIM_LONG_DEC"]),
                        "elevation": elevation
                    }
                    kept += 1
                    batch.append(data)
                    if len(batch) >= self.batch_size:
                        self.store_batch(batch, batch_number, batch_count)
                        batch_number += 1
                        batch = []
                else:
                    skipped += 1
            self.store_batch(batch, batch_number, batch_count)
            self.logger.info("Saved {} places, discarded {}.".format(kept, skipped))

    def store_batch(self, batch, batch_number, batch_count):
        self.logger.info("Storing batch of {} places: #{} of {}...".format(len(batch), batch_number, batch_count))
        GeographicFeature.objects.bulk_create([GeographicFeature(**data) for data in batch])
