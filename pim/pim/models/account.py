from decimal import Decimal

from django.db import models
from pim.models.base_entity import BaseEntity


class Account(BaseEntity):
    account_number = models.CharField(max_length=15)
    idtp_vid = models.CharField(max_length=100, null=True, blank=True)
    account_status = models.CharField(max_length=15, default="ACTIVE")
    idtp_status = models.CharField(max_length=15, default="CONFIRMED")
    currency_code = models.CharField(max_length=100, default="BDT")
    balance = models.DecimalField(decimal_places=2, max_digits=20, default=100000.0)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    nid = models.CharField(max_length=100, null=True, blank=True)
    tin = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    address_line1 = models.TextField(null=True, blank=True)
    address_line2 = models.TextField(null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)

    def get_dict(self):
        _items = { k:v for k, v in self.__dict__.items() }
        print(_items)
        return _items

    @classmethod
    def debit(cls, idtp_vid, amount):
        acc_instances = Account.objects.filter(idtp_vid__iexact=idtp_vid, account_status="ACTIVE")
        if acc_instances.exists():
            acc_instance = acc_instances.first()
            acc_instance.balance -= Decimal(amount)
            if acc_instance.balance < 0:
                raise Exception("The account does not have sufficient balance")
            acc_instance.save()
        else:
            raise Exception("The account number provided either invalid or inactive")

    @classmethod
    def credit(cls, idtp_vid, amount):
        acc_instances = Account.objects.filter(idtp_vid__iexact=idtp_vid, account_status="ACTIVE")
        if acc_instances.exists():
            acc_instance = acc_instances.first()
            acc_instance.balance += Decimal(amount)
            acc_instance.save()
        else:
            raise Exception("The account number provided either invalid or inactive")

    @classmethod
    def check_if_valid(cls, nid, **kwargs):
        _filters = {
            "nid__iexact": nid,
            "account_status": "ACTIVE"
        }
        _filters.update(**kwargs)
        return cls.objects.filter(**_filters).exists()

    @classmethod
    def create_or_update(cls, **kwargs):
        _instances = cls.objects.filter(account_number__iexact=kwargs.get("account_number"))
        if not _instances.exists():
            _instance = cls()
        else:
            _instance = _instances.first()

        for k, v in kwargs.items():
            setattr(_instance, k, v)

        _instance.save()

