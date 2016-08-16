from django.db import models


class PersonalDetails(models.Model):
    first_name = models.CharField(max_length=250)
    salutation = models.CharField(max_length=10)
    middle_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=6)
    date_of_birth = models.DateField('Date of Birth')
    age_group = models.CharField(max_length=20)
    place_of_birth = models.CharField(max_length=150)
    date_of_ftv = models.DateField('Date of first time visit')
    referrer = models.OneToOneField('self', blank='true', null='true')


class Addresses(models.Model):
    stand_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    suburb = models.CharField(max_length=250)
    city_town = models.CharField(max_length=250)
    country = models.CharField(max_length=250)


class PersonsAddresses(models.Model):
    addresses = models.ForeignKey(Addresses, null=True)
    personal_details = models.ForeignKey(PersonalDetails, null=True)
    date_of_entry = models.DateField('Date of Entrance')
    date_of_leaving = models.DateField('Date of Leaving')
    used_for = models.CharField(max_length=20)


class ContactInfo(models.Model):
    contact_info_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    personal_details = models.ForeignKey(PersonalDetails)
    contact_info_type = models.ForeignKey('ContactInfoType')


class ContactInfoType(models.Model):
    contact_info_type_name = models.CharField(max_length=100)
    # This includes contact details like Mobile, Fax Number, Landline, Twitter, E-mail, Facebook, Skype, LinkedIn
    contact_info_type_code = models.CharField(max_length=10)
    # This is the code as will be used on forms or reports. E.g Twitter-Handle, FB, etc
    contact_info_type_description = models.TextField()


class MaritalStatus(models.Model):
    marital_status_name = models.CharField(max_length=20)
    code = models.CharField(max_length=5)
    description = models.TextField()


class PersonsMaritalStatus(models.Model):
    personal_details = models.ForeignKey(PersonalDetails)
    marital_status_name = models.ForeignKey(MaritalStatus)
    date_from = models.DateField()
    date_to = models.DateField()


class HomegroupVenues(models.Model):
    homegroup_name = models.CharField(max_length=250)
    area_zone = models.ForeignKey('AreaZone')
    meeting_day = models.CharField(max_length=10)
    start_time = models.TimeField()
    finish_time = models.TimeField()
    address = models.ForeignKey(Addresses)



class AreaZone(models.Model):
    zone_name = models.CharField(max_length=100)
    areas_covered = models.TextField()


class AreaZoneRoles(models.Model):
    zone_name = models.ForeignKey('AreaZone')
    personal_details = models.ForeignKey(PersonalDetails)
    role_name = models.ForeignKey('Roles')
    # This is to pick its role name from the Role table which pertains to the departments since the structure cascades
    # down to the grassroots structures
    date_assumed = models.DateField('Date of assumption of role')
    date_left = models.DateField('Date of leaving role')


class Roles(models.Model):
    role_name = models.CharField(max_length=50)
    ministry_outline = models.TextField()
    # This is the job description for this role
    parent_role = models.OneToOneField('self', blank='true', null='true')
    # This field will define the role that the role in question reports, thus helping define the structure


class HomegroupRoles(models.Model):
    homegroup_name = models.ForeignKey(HomegroupVenues)
    personal_details = models.ForeignKey(PersonalDetails)
    role_name = models.ForeignKey(Roles)
    # This is to pick its role name from the Role table which pertains to the departments since the structure cascades
    # down to the grassroots structures
    date_assumed = models.DateField('Date of assumption of role')
    date_left = models.DateField('Date of leaving role')


class Spirituals(models.Model):
    personal_details = models.ForeignKey(PersonalDetails)
    # The person in question
    spirituals_type = models.ForeignKey('SpiritualsType')
    # The type of the spirituals from the Spirituals type table
    spirituals_name = models.CharField(max_length=200)
    # The name of the spiritual
    spirituals_status = models.CharField(max_length=20)
    date_spirituals_received = models.DateField()
    where_spirituals_received = models.CharField(max_length=250)


class SpiritualsType(models.Model):
    name = models.CharField(max_length=100)
    # Examples of these include SALVATION and baptism in the HOLY SPIRIT
    description = models.TextField()
    # Just a brief description or definition of what this type of spirituals is
    scripture_reference = models.TextField()
    # These will be scripture references from the Bible defining, descibing or substantiating this type
    howto = models.TextField()
    # Some guidelines on how this type can be ministered


class Department(models.Model):
    name = models.CharField(max_length=200)
    mission = models.TextField()
    description = models.TextField()

class DepartmentCategory(models.Model):
    name = models.TextField()
    description = models.TextField()
    # Examples of this would be Sector department

class DepartmentalMembership(models.Model):
    name = models.ForeignKey(Department)
    role_name = models.ForeignKey(Roles)
    personal_details = models.ForeignKey(PersonalDetails)
    date_joined = models.DateField()
    date_left = models.DateField()


class FollowUpType(models.Model):
    follow_up_type_name = models.CharField(max_length=100)
    follow_up_type_description = models.TextField()
    follow_up_type_code = models.CharField(max_length=5)


class FollowUpMode(models.Model):
    follow_up_mode_name = models.CharField(max_length=100)
    follow_up_mode_code = models.CharField(max_length=5)
    follow_up_mode_description = models.TextField()


class FollowUp(models.Model):
    person_being_followed_up = models.ForeignKey(PersonalDetails, related_name="disciple")
    date_scheduled = models.DateField()
    follow_up_type_name = models.ForeignKey(FollowUpType)
    follow_up_mode = models.ForeignKey(FollowUpMode)
    person_following_up_scheduled = models.ForeignKey(PersonalDetails, related_name="discipler")
    follow_up_name = models.CharField(max_length=250)
    # The initial follow up scheduling is done automatically and is based upon AGEGROUP, GENDER, MARITAL_STATUS of the
    # FTV or new convert.
    # Every attempt is made to pair the FTV/New Convert with a minister who is of the same placing or extraction
    # using the above mentioned parameters


class FollowUpOutcomes(models.Model):
    follow_up_name = models.ForeignKey(FollowUp)
    follow_up_status = models.ForeignKey('FollowUpStatus')
    person_following_up_actual = models.ForeignKey(PersonalDetails)
    actual_date = models.DateField()
    requests_needs_of_person = models.TextField()
    ministry_given = models.TextField()
    home_group_invitation = models.TextField()
    # Tell the person of a home group near them and invite them if they are free and check if they are able to attend.
    # If they are, notify home group leader to take over if they have not followed up already
    # Then check with the person followed up the following day if they managed to attend.
    # If not, find out why they failed to attended
    # and either help them if you can or escalate
    thursday_invitation = models.TextField()
    # Tell the person of our Thursday prayer and invite them if they are free and be there on the day to receive
    # them if they are able to attend.
    # Then check with the person followed up if they managed to attend. If not, find out why they failed to attended
    # and either help them if you can or escalate
    sunday_invitation = models.TextField()
    # Find out if the person is able to attend Sunday service and invite them
    # and be there on the day to receive them if they are able to attend.
    next_action = models.TextField()
    date_of_next_action = models.DateTimeField()
    # From the follow up outcome, an entry is automatically created in the follow_up table based primarily on the
    # next action field, date of next action with the person following up being the same except where there is
    # escalation or delegation of ministry whatever the case might be


class FollowUpStatus(models.Model):
    follow_up_status_name = models.CharField(max_length=10)
    description = models.TextField()


class SkillsCategory(models.Model):
	skills_category_name = models.CharField(max_length=100)
	skills_category_description = models.TextField()


class skills(models.Model):
	skills_name = models.CharField(max_length=100)
	skills_category_name = models.ForeignKey(SkillsCategory)
	skills_description = models.TextField()

class Mentorship(models.Model):
    mentor = models.ForeignKey(PersonalDetails)
    mentoree = models.ForeignKey(PersonalDetails)
    start_date = models.DateField()
    end_date = models.DateField()
    mentorship_type = models.TextField()

class Sessions(models.Model):
    mentorship = models.ForeignKey(Mentorship)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.TextField()

class MentorshipSessionsOutcomes(models.Model):
    session = models.ForeignKey(Sessions)
    deliverable = models.ForeignKey(Deliverables)
    outcome =models.TextField()

class Deliverables(models.Model):
    name = models.TextField()
    description = models.TextField()
    howto = models.TextField()

class DeptDeliverables(models.Model):
    deliverable = models.ForeignKey(Deliverables)
    department = models.ForeignKey(Department)

