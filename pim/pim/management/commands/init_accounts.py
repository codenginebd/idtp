import csv
import os
from decimal import Decimal

from django.core.management.base import BaseCommand

from pim.models import Account


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Inside Init Accounts")
        project_directory = os.path.abspath(".")
        data_directory = os.path.join(project_directory, "pim", "data")
        with open(os.path.join(data_directory, "accounts.csv"), "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for i, row in enumerate(csv_reader):
                print("Processing %s" % i)
                if i == 0: continue
                _data = {
                    "account_number": row[1].strip(),
                    "balance": Decimal(row[2]),
                    "full_name": row[3].strip(),
                    "dob": row[4].strip(),
                    "tin": row[5].strip(),
                    "nid": row[6].strip(),
                    "address_line1": row[7].strip(),
                    "address_line2": row[8].strip(),
                    "mobile_number": row[9].strip(),
                    "email": row[10].strip()
                }
                if i == 7:
                    _data["account_status"] = "INACTIVE"

                Account.create_or_update(**_data)

                print("Item %s processed" % i)


