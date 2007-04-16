from sqlobject import *

from turbogears.database import PackageHub
from datetime import datetime
from conf import pkg

hub = PackageHub(pkg)
__connection__ = hub

# class YourDataClass(SQLObject):
#     pass


class BusyBe(SQLObject):
	deleted = BoolCol(notNone=True, default=False)
	#date_entered = DateTimeCol(notNone=True, default=sqlbuilder.func.NOW())
	date_entered = DateTimeCol(notNone=True, default=datetime.now())


class User(BusyBe):
	user = UnicodeCol(length=128, alternateID=True)
	password = UnicodeCol(length=128, notNone=True)
	user_group = ForeignKey('Community', notNone=True)
	access_level = ForeignKey('AccessLevel', notNone=True)


class AccessLevel(BusyBe):
	access_level = UnicodeCol(length=128, alternateID=True)
	permission = MultipleJoin('Permission')


class Permission(BusyBe):
	#user_group = ForeignKey('Community', notNone=True)
	access_level = ForeignKey('AccessLevel', notNone=True)
	class_name = UnicodeCol(length=128, notNone=True)
	function = UnicodeCol(length=128, notNone=True)


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


class Inbound(BusyBe):
	agent = IntCol(notNone=True)
	number = IntCol(notNone=True)
	start = DateTimeCol(notNone=True, default=datetime.now())
	end = DateTimeCol(notNone=True)
	comment = UnicodeCol()


class Outbound(BusyBe):
	agent = IntCol(notNone=True)
	number = IntCol(notNone=True)
	start = DateTimeCol(notNone=True, default=datetime.now())
	end = DateTimeCol(notNone=True)
	comment = UnicodeCol()


class Calltypecat(SQLObject):
	class sqlmeta:
		idName = 'calltypecatid'
	categoryname = UnicodeCol(length=20)
	calltype = UnicodeCol(length=1)


