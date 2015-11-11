
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, RedirectView
from grades.forms import AddSubjectForm, RegisterForm
from grades.models import Student, StudiedSubject, StudentGrade, GRADES_LIST


class HomeView(TemplateView):
    template_name = "grades/index.html"
    predicted_grades = dict()
    test_grades = dict()
    studied_subjects = None
    page_title= "Home"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["studied_subjects"] = self.studied_subjects
        context["test_grades"] = self.test_grades
        context["predicted_grades"] = self.predicted_grades
        context["grades"] = GRADES_LIST
        return context

    def get_grade(self, studied_subject, chapter):
        try:
            grade = StudentGrade.objects.get(student_id=studied_subject.student.id, chapter_id=chapter.id)
        except StudentGrade.DoesNotExist:
            grade = StudentGrade.objects.create(student_id=studied_subject.student.id, chapter_id=chapter.id, predicted_grade=1, test_grade=1)
        return grade

    def post(self, request):
        self.studied_subjects = request.user.student.studiedsubject_set.all()
        for studied_subject in self.studied_subjects:
            for unit in studied_subject.subject.unit_set.all():
                for chapter in unit.chapter_set.all():
                    grade = self.get_grade(studied_subject, chapter)
                    self.predicted_grades[str(chapter.id)] = grade.predicted_grade = int(request.POST['predicted-grade-' + str(studied_subject.id) + '-' + str(unit.id) + '-' + str(chapter.id)])
                    self.test_grades[str(chapter.id)] = grade.test_grade = int(request.POST['test-grade-' + str(studied_subject.id) + '-' + str(unit.id) + '-' + str(chapter.id)])
                    grade.save()

        return render(request, self.template_name, self.get_context_data())

    def get(self, request):
        self.studied_subjects = request.user.student.studiedsubject_set.all()
        for studied_subject in self.studied_subjects:
            for unit in studied_subject.subject.unit_set.all():
                for chapter in unit.chapter_set.all():
                    grade = self.get_grade(studied_subject, chapter)
                    self.test_grades[str(chapter.id)] = grade.test_grade
                    self.predicted_grades[str(chapter.id)] = grade.predicted_grade

        return render(request, self.template_name, self.get_context_data())

class SubjectDeleteView(RedirectView):
    url = "/grades/subjects/"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        StudiedSubject.objects.get(id=self.kwargs['subject_id']).delete()
        return super(SubjectDeleteView, self).dispatch(request, *args, **kwargs)

class SubjectListView(TemplateView):
    template_name = "grades/subjects.html"
    page_title = "Your Subjects"
    studied_subjects = None
    form = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SubjectListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubjectListView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["studied_subjects"] = self.studied_subjects
        context["form"] = self.form
        return context

    def post(self, request):
        self.form = AddSubjectForm(request.POST)
        if self.form.is_valid():
            subject = self.form.save(commit=False)
            subject.student = request.user.student
            subject.save()

        return self.get(request)

    def get(self, request):
        self.form = AddSubjectForm()
        self.studied_subjects = request.user.student.studiedsubject_set.all()
        return render(request, self.template_name, self.get_context_data())

class RegisterView(TemplateView):
    template_name = "grades/register.html"
    page_title = "Register"
    form = None

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context["page_title"] = self.page_title
        context["form"] = self.form
        return context

    def post(self, request):
        self.form = RegisterForm(request.POST)
        if self.form.is_valid():
            email = self.form.cleaned_data['email']
            username = self.form.cleaned_data['username']
            password = self.form.cleaned_data['password1']
            date_of_birth = self.form.cleaned_data['dob_year'] + '-' + self.form.cleaned_data['dob_month'] + '-' + self.form.cleaned_data['dob_day']
            user = User.objects.create_user(username, email, password)
            Student.objects.create(user=user, date_of_birth=date_of_birth)

            return render(request, "grades/register_thanks.html", self.get_context_data())
        else:
            return render(request, self.template_name, self.get_context_data())

    def get(self, request):
        self.form = RegisterForm()
        return render(request, self.template_name, self.get_context_data())
