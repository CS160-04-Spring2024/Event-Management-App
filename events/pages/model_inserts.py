from django.utils import timezone
from models import *

depts_list = [Department(name="CS"),
              Department(name="ENGR"),
              Department(name="MUSC"),
              Department(name="ART"),
              Department(name="BUS1")]

tags_list = [Tag(name='Fun'),
             Tag(name='Technical'),
             Tag(name='Sports'),
             Tag(name='Extracurricular'),
             Tag(name='Food'),
             Tag(name='Math'),
             ]


Department.objects.bulk_create(depts_list)
Tag.objects.bulk_create(tags_list)

Location.objects.create(building_name="Boccardo Business",
                        address="1 Washington Sq, San Jose, CA 95112",
                        image="https://www.sjsu.edu/mgmt/pics/BBC%20Building.jpg")


Major.objects.create(major_name="Mechanical Engineering",
                     department=Department.objects.get(pk='ENGR'))
Major.objects.create(major_name="Electrical Engineering",
                     department=Department.objects.get(pk='ENGR'))
Major.objects.create(major_name="Industrial Engineering",
                     department=Department.objects.get(pk='ENGR'))
Major.objects.create(major_name="Digital Media",
                     department=Department.objects.get(pk='ART'))
Major.objects.create(major_name="Data Science",
                     department=Department.objects.get(pk='CS'))

Organization.objects.create(
    name='Innovators Club',
    description='Fostering innovation and creativity among members.',
    location_id=1,
    banner='https://as2.ftcdn.net/v2/jpg/02/09/19/15/1000_F_209191528_GYzxi0vEm0fV8oyqIWbmkgEM2BH4X47e.jpg',
    club_logo='https://media.licdn.com/dms/image/C560BAQGRZzF33Ji0dg/company-logo_200_200/0/1630667094779/sjsumlclub_logo?e=1720051200&v=beta&t=G5IvvlTtCNLZGnpV1Nis_b4BKm6OW6d-1MOswkE4by0',
    members=50,
    department_id=Department.objects.get(pk='ENGR'),
    email='innovators@example.com',
    website_link='https://innovatorsclub.com'
)

# Insert statement for Organization 2
Organization.objects.create(
    name='Code Masters Guild',
    description='Exploring the world of programming and software development.',
    location_id=1,
    banner='https://as2.ftcdn.net/v2/jpg/02/09/19/15/1000_F_209191528_GYzxi0vEm0fV8oyqIWbmkgEM2BH4X47e.jpg',
    club_logo='https://media.licdn.com/dms/image/C560BAQGRZzF33Ji0dg/company-logo_200_200/0/1630667094779/sjsumlclub_logo?e=1720051200&v=beta&t=G5IvvlTtCNLZGnpV1Nis_b4BKm6OW6d-1MOswkE4by0',
    members=40,
    department_id=Department.objects.get(pk='CS'),
    email='codemasters@example.com',
    website_link='https://codemastersguild.com'
)

# Insert statement for Organization 3
Organization.objects.create(
    name='Tech Explorers Society',
    description='Exploring the latest trends in technology and science.',
    location_id=1,
    banner='https://as2.ftcdn.net/v2/jpg/02/09/19/15/1000_F_209191528_GYzxi0vEm0fV8oyqIWbmkgEM2BH4X47e.jpg',
    club_logo='https://media.licdn.com/dms/image/C560BAQGRZzF33Ji0dg/company-logo_200_200/0/1630667094779/sjsumlclub_logo?e=1720051200&v=beta&t=G5IvvlTtCNLZGnpV1Nis_b4BKm6OW6d-1MOswkE4by0',
    members=35,
    department_id=Department.objects.get(pk='CS'),
    email='techexplorers@example.com',
    website_link='https://techexplorerssociety.com'
)

# Insert statement for Organization 4
Organization.objects.create(
    name='Design Visionaries',
    description='Unleashing creativity through design and artistry.',
    location_id=1,
    banner='https://as2.ftcdn.net/v2/jpg/02/09/19/15/1000_F_209191528_GYzxi0vEm0fV8oyqIWbmkgEM2BH4X47e.jpg',
    club_logo='https://media.licdn.com/dms/image/C560BAQGRZzF33Ji0dg/company-logo_200_200/0/1630667094779/sjsumlclub_logo?e=1720051200&v=beta&t=G5IvvlTtCNLZGnpV1Nis_b4BKm6OW6d-1MOswkE4by0',
    members=45,
    department_id=Department.objects.get(pk='ART'),
    email='designvisionaries@example.com',
    website_link='https://designvisionaries.org'
)


# Retrieve organization IDs for use in events
organization1 = Organization.objects.get(name='Innovators Club')
organization2 = Organization.objects.get(name='Code Masters Guild')
organization3 = Organization.objects.get(name='Tech Explorers Society')
organization4 = Organization.objects.get(name='Design Visionaries')

# Insert statement for Event 1
Event.objects.create(
    event_name='Tech Summit 2024',
    description='A conference on the latest technology trends and innovations.',
    mode_of_operation='In-Person',
    location_id=1,
    start_time=timezone.now(),
    end_time=timezone.now(),
    fees=50.00,
    organization=organization1,
    event_image='https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
)

# Insert statement for Event 2
Event.objects.create(
    event_name='AI Workshop Series',
    description='A series of workshops on artificial intelligence and machine learning.',
    mode_of_operation='In-Person',
    location_id=1,
    start_time=timezone.now(),
    end_time=timezone.now(),
    fees=25.00,
    organization=organization2,
    event_image='https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
)

# Insert statement for Event 3
Event.objects.create(
    event_name='Hackathon 2024',
    description='A coding marathon to build innovative solutions.',
    mode_of_operation='In-Person',
    location_id=1,
    start_time=timezone.now(),
    end_time=timezone.now(),
    fees=40.00,
    organization=organization3,
    event_image='https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
)

# Insert statement for Event 4
Event.objects.create(
    event_name='Data Science Symposium',
    description='A symposium on data science applications and best practices.',
    mode_of_operation='In-Person',
    location_id=1,
    start_time=timezone.now(),
    end_time=timezone.now(),
    fees=30.00,
    organization=organization4,
    event_image='https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
)
