from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# from tinymce import models as tinymce_models
# from django_quill.fields import QuillField
from ckeditor.fields import RichTextField


class Department(models.Model):
    name = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'department'


class User(models.Model):
    user_email = models.TextField(primary_key=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # 'student' or 'professor'
    role = models.BooleanField(default=0)
    major = models.ForeignKey('Major', null=True, on_delete=models.DO_NOTHING)
    department = models.ForeignKey('Department', on_delete=models.DO_NOTHING)
    funds = models.FloatField(default=0.00, validators=[
                              MinValueValidator(0), MaxValueValidator(1000)])
    is_admin = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag', related_name='users')

    class Meta:
        db_table = 'user'


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(
        'Location', on_delete=models.DO_NOTHING, blank=True, null=True)
    banner = models.URLField(
        default='https://www.sjsu.edu/communications/pics/SpartanSpirit_variation.png', blank=True, null=True)
    club_logo = models.URLField(
        default='https://www.sjsu.edu/_images/news/news_prez-seal-communications_010621.jpg', blank=True, null=True)
    members = models.IntegerField(default=1, validators=[
        MinValueValidator(1), MaxValueValidator(300)])
    department = models.ForeignKey('Department', on_delete=models.DO_NOTHING)

    # socials - email and linkedin
    email = models.EmailField(blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organization'


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    mode_of_operation = models.TextField()
    location = models.ForeignKey('Location', on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    fees = models.DecimalField(max_digits=6, decimal_places=2)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    event_image = models.URLField(
        default='https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', blank=True, null=True)
    tags = models.ManyToManyField('Tag', related_name='events')

    class Meta:
        db_table = 'event'


class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.name

    # class Meta:
    #     db_table = 'tag'


# class UserInterest(models.Model):
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     tag = models.ManyToManyField('Tag')

#     class Meta:
#         db_table = 'user_interest'
        # unique_together = (('user', 'tag'),)


class Admin(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

    class Meta:
        db_table = 'admin'
        unique_together = (('user', 'organization'))


class Registration(models.Model):
    user_email = models.ForeignKey('User', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    class Meta:
        db_table = 'registration'
        unique_together = (('user_email', 'event'))


# class EventTag(models.Model):
#     event = models.ForeignKey('Event', on_delete=models.CASCADE)
#     tag = models.ManyToManyField('Tag')

#     class Meta:
#         db_table = 'event_tag'
#         # unique_together = (('event', 'tag'))


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    sjsu_roadmap_image = models.URLField(
        default='https://www.cs.sjsu.edu/su/practicalities_files/image002.jpg', blank=True, null=True)
    building_name = models.CharField(max_length=255)
    room_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.URLField(
        default='https://www.sjsu.edu/sustainability/pics/cv2building.jpg', blank=True, null=True)

    class Meta:
        db_table = 'location'


class Major(models.Model):
    major_name = models.TextField(primary_key=True)
    department = models.ForeignKey('Department', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.major_name

    class Meta:
        db_table = 'major'
# class Event(models.Model):
#     content = RichTextField()
# Create your models here.

# <<<<<<< Jae2
# class eventPanel:
#     title: str
#     eventName: str
#     meetingOption: str
#     meetingTime: str
#     meetingAttributes: list

# class searchData:
#     title: str
#     event: str
#     club: str
#     department: str
# =======

# # class ClubDepartment(models.Model):
# #     club_id = models.ForeignKey('Organization', on_delete=models.CASCADE)
# #     department = models.ForeignKey('Department', on_delete=models.CASCADE)

# #     class Meta:
# #         db_table = 'club_department'
# #         unique_together = (('club_id', 'department'))
# >>>>>> main
