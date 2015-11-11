from django.contrib import admin

from grades.models import Student, Subject, Unit, StudiedSubject, Chapter, \
    StudentGrade


#Inlines
class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1

class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1

class StudiedSubjectInline(admin.TabularInline):
    model = StudiedSubject
    extra = 1

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

#Admins
class SubjectAdmin(admin.ModelAdmin):
    inlines = [UnitInline]

class StudentAdmin(admin.ModelAdmin):
    inlines = [StudiedSubjectInline]

class UnitAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(StudentGrade, admin.ModelAdmin)