from django.contrib import admin

from .models import Student, ScholarshipType, Division, Phone, Education, University

class EducationInline(admin.TabularInline):
    extra = 1
    model = Education


class PhoneInline(admin.TabularInline):
    extra = 1
    model = Phone

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'status', 'awarded_year', 'scholarship_type', 'country', 'major', 'special_emphasis', 'division', 'email')
    #list_filter = ['type']

    inlines = [
        PhoneInline,
        EducationInline,
    ]

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'status', 'awarded_year', 'scholarship_type', 'country', 'major', 'special_emphasis', 'division', 'email')
        }),
        ('Degree Sought', {
            'fields': ('degree_sought_bs', 'degree_sought_ms', 'degree_sought_dr'),
        }),
    )


admin.site.register(ScholarshipType)
admin.site.register(Division)
admin.site.register(University)
