import csv

from django.core.management.base import BaseCommand, CommandError
from django_countries.fields import Country

from scholartracker.models import *

class Command(BaseCommand):
    help = 'Import CSV'

    STATUS_DICT = {
        'กำลังศึกษา' : 'CO',
        'ไม่สำเร็จการศึกษาตามโครงการ' : 'FL',
        'สำเร็จการศึกษา' : 'GR' ,
        'อยู่ระหว่างการเตรียมตัว': 'PR',
    }

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str)

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        print(csv_path)

        with open(csv_path, newline='') as csvfile:    
            csv_reader = csv.reader(csvfile, delimiter=',')
            next(csv_reader, None)
            for row in csv_reader:
                student = Student()
                
                row[0] = row[0].replace(')', ') ')
                if row[0]:
                    name = row[0].split()
                    first = name[0]
                    last = ' '.join(name[1:])
                else:
                    first = 'N/A'
                    last = 'N/A'

                student.first_name = first
                student.last_name  = last

                student.status = Command.STATUS_DICT[row[1]]
                student.awarded_year = int(row[2]) - 543
                
                scholarship_type, _ = ScholarshipType.objects.get_or_create(type_name=row[3])
                student.scholarship_type = scholarship_type

                if row[4] == 'ญี่ปุ่น':
                    student.country = Country(code='JP')
                elif row[4] == 'ไทย':
                    student.country = Country(code='TH')
                elif row[4] == 'ฝรั่งเศส':
                    student.country = Country(code='FR')
                elif row[4] == 'สหรัฐอเมริกา':
                    student.country = Country(code='US')
                elif row[4] == 'อังกฤษ':
                    student.country = Country(code='GB')
                elif row[4] == 'แคนาดา':
                    student.country = Country(code='CA')
                elif row[4] == 'เบลเยี่ยม':
                    student.country = Country(code='BE')
                elif row[4] == 'เยอรมนี':
                    student.country = Country(code='DE')
                elif row[4] == 'ลักเซมเบอร์ก':
                    student.country = Country(code='LU')
                else:
                    student.country = Country(code='NA')

                student.major = row[5]
                student.special_emphasis = row[6]

                division, _ = Division.objects.get_or_create(name=row[7])
                student.division = division

                if row[8] == 'เอก':
                    cur_degree = 'PH'
                elif row[8] == 'โท':
                    cur_degree = 'MS'
                elif row[8] == 'ตรี':
                    cur_degree = 'BS'

                cur_university = row[9]

                student.email = row[10]

                student.degree_sought_dr = False
                student.degree_sought_ms = False
                student.degree_sought_bs = False

                sought_degree = row[11].replace(' หรือเอก','-').split('-')
                for degree in sought_degree:
                    if degree == 'เอก':
                        student.degree_sought_dr = True
                    elif degree == 'โท':
                        student.degree_sought_ms = True
                    elif degree == 'ตรี':
                        student.degree_sought_bs = True

                student.save()

                university, _ = University.objects.get_or_create(name=cur_university)
                education, _ = Education.objects.get_or_create(owner=student, university=university)
                education.degree = cur_degree
                education.save()

                phones = row[12].replace('-','').replace('/', ',').replace(' ','').split(',')
                for p in phones:
                    Phone.objects.get_or_create(owner=student, number=p)

                print('Add: ' + str(student))