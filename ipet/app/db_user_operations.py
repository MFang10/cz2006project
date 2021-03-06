from .models import PetOwner, Clinic, Vet, PhoneNumber
from django.core.exceptions import ObjectDoesNotExist
import datetime


'''
This is a function to check whether the entered phone number has been used yet.
A true indicates the phone number is unoccupied and vice versa.
'''


def check_phone_number(phone_number):
	try:
		PhoneNumber.objects.get(phone_number = phone_number)
	except PhoneNumber.DoesNotExist:
		return True
	return False

'''
The insert_user function takes in the name of the registrant, the phone number, the password,
the type of user and additional information.

The name for pet owners and vets need not be unique since people are having the same names, 
whereas for clinics, the names have to differ from each other.

The phone number should be unique for all the users (even in different domains),
the uniqueness of which would be checked inside the function.

The length of the password should between 6 and 16.

A 0 in the user type indicates a pet owner;
an 1 indicates a clinic;
a 2 indicates a vet.
For anything else input as a user_type, a TypeError is thrown.

The additional information should be passed in as a reference to a python list, 
the dimension of which depends on the user_type but would be checked inside the function.
However, the type of info must be checked before passing into the function.
For pet owners, info[0] and info[1] should be the breed and birthday of the pet respectively.
info[0] should be a string whereas info[1] should be an integer.
For clinics, info[0] and info[1] should be the address and the license respectively.
Both of them should be legitimate strings.
For vets, info only has one dimension, which is the name of the registrants' clinic.
The clinic should be a registered one (or documented one?), otherwise a value error would be thrown.
'''


def insert_user(name, phone_number, password, user_type, info):
	if len(name) > 32:
		raise ValueError('This name is too long')
	if len(phone_number) > 16 or len(phone_number) < 3:
		raise ValueError('Please enter a valid phone number')
	if len(password) > 16:
		raise ValueError('Passwords should not be longer that 16 characters')
	if len(password) < 6:
		raise ValueError('Passwords should consist of at least 6 characters')
	if user_type != 0 and user_type != 1 and user_type != 2:
		raise TypeError('Invalid user type')

	if check_phone_number(phone_number):
		if user_type != 2:
			number = PhoneNumber.objects.create(phone_number = phone_number)
	else:
		raise FileExistsError('The phone number has already been used for registration')

	if user_type == 0:  # PetOwner
		if len(info) < 2:
			raise NameError('Insufficient information about your pet')
		if len(info) > 2:
			raise SystemError('Oops! Something is wrong.')
		PetOwner.objects.create(name = name, phone_number = number, password = password,
								registration_date = datetime.datetime.today(), breed = info[0], birthday = info[1])
	elif user_type == 1:  # Clinic
		if len(info) < 2:
			raise NameError('Insufficient information')
		if len(info) > 2:
			raise SystemError('Oops! Something is wrong.')
		if len(info[0]) > 128:
			raise ValueError('The address is too long')
		try:
			Clinic.objects.get(name = name)
			raise ValueError('The clinic has already registered')
		except Clinic.DoesNotExist:
			Clinic.objects.create(name = name, phone_number = number, password = password,
								  registration_date = datetime.datetime.today(), address = info[0], license = info[1],
								  isVerified = False)
	else:  # Vet
		if len(info) < 1:
			raise NameError('Please enter the clinic you work for')
		if len(info) > 1:
			raise SystemError('Oops! Something is wrong.')
		try:
			entry = Clinic.objects.get(name = info[0])
		except Clinic.DoesNotExist:
			raise ValueError('Please enter a registered clinic')
		number = PhoneNumber.objects.create(phone_number = phone_number)
		Vet.objects.create(name = name, phone_number = number, password = password,
						   registration_date = datetime.datetime.today(), clinic = entry, isVerified = False)


'''
It is the simplest query based purely on phone number.
The exceptions would be raised if the queried phone number is not in database yet,
or there are multiple entries have the same phone number (unlikely but serious problem). 
The whole entry of the record would be returned if a result could be got.
'''


def query_user(phone_number):
	try:
		phone_number = PhoneNumber.objects.get(phone_number = phone_number)
	except PhoneNumber.DoesNotExist:
		raise ObjectDoesNotExist

	try:
		entry = PetOwner.objects.get(phone_number = phone_number)
		return entry
	except PetOwner.MultipleObjectsReturned:
		raise SystemError('Oops! Something is wrong with database')
	except PetOwner.DoesNotExist:
		pass

	try:
		entry = Clinic.objects.get(phone_number = phone_number)
		return entry
	except Clinic.MultipleObjectsReturned:
		raise SystemError('Oops! Something is wrong with database')
	except Clinic.DoesNotExist:
		pass

	try:
		entry = Vet.objects.get(phone_number = phone_number)
		return entry
	except Vet.MultipleObjectsReturned:
		raise SystemError('Oops! Something is wrong with database')
	except Vet.DoesNotExist:
		raise ObjectDoesNotExist


'''
The verify function is used for the email verification for both clinics and vet,
the phone number of being-verified should be passed in.
The isVerified field would be set to true if the phone number is found in db,
otherwise an ObjectDoesNotExist exception would be raised.
If the corresponding user of the given phone number has already been verified,
a PermissionError would be raised.
'''


def verify(phone_number):
	phone_number = PhoneNumber.objects.get(phone_number = phone_number)

	try:
		entry = Clinic.objects.get(phone_number = phone_number)
		if not entry.isVerified:
			entry.isVerified = True
			entry.save()
		else:
			raise PermissionError('It is already verified')
		return
	except Clinic.DoesNotExist:
		pass

	try:
		entry = Vet.objects.get(phone_number = phone_number)
		if not entry.isVerified:
			entry.isVerified = True
			entry.save()
		else:
			raise PermissionError('It is already verified')
		return
	except Vet.DoesNotExist:
		raise ObjectDoesNotExist
