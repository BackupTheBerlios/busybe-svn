from sqlobject import *

from turbogears.database import PackageHub
from datetime import datetime

hub = PackageHub("busybe")
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass


class BusyBe(SQLObject):
	deleted = BoolCol(notNone=True, default=False)
	#date_entered = DateTimeCol(notNone=True, default=sqlbuilder.func.NOW())
	date_entered = DateTimeCol(notNone=True, default=datetime.now())


class Community(BusyBe):
	name = UnicodeCol(length=64, notNone=True, unique=True)
	leader = ForeignKey('Person', notNone=True)


class Event(BusyBe):
	owner = ForeignKey('Person', notNone=True)
	name = UnicodeCol(length=128, notNone=True)
	venue = UnicodeCol(length=128)
	description = UnicodeCol()
	start = DateTimeCol(notNone=True)
	end = DateTimeCol(notNone=True)


class Participant(BusyBe):
	event = ForeignKey('Event', notNone=True)
	person = ForeignKey('Person', notNone=True)


class Person(BusyBe):
	name = UnicodeCol(length=64, notNone=True, unique=True)
	full_name = UnicodeCol(length=128)
	address = UnicodeCol()
	home_phone = UnicodeCol(length=32)
	mobile_phone = UnicodeCol(length=32)
	office_phone = UnicodeCol(length=32)
	birth_date = DateCol()
	money = DecimalCol(size=10.2, precision=2)
	no_of_peanuts = IntCol()
	weight = FloatCol()
	active = BoolCol(notNone=True, default=True)


class PersonCommunity(BusyBe):
	community = ForeignKey('Community', notNone=True)
	person = ForeignKey('Person', notNone=True)
	active = BoolCol(notNone=True, default=True)



