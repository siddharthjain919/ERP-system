from .models import branch_detail,branch_subjects
from django.db.models.query import QuerySet

def get_subjects_by_branch(branch:branch_detail):
    return branch_subjects.branch_sub_obj.filter(branch=branch)

def get_labs(subjects:QuerySet[branch_subjects])->QuerySet[branch_subjects]:
    return subjects.filter(branch_subject__is_lab=True)

def get_subjects_by_teacher(teacher)->QuerySet[branch_subjects]:
    return branch_subjects.branch_sub_obj.filter(subject_teacher=teacher).order_by('branch')

def filter_branch_subjects(branchsubjects:QuerySet[branch_subjects]|None=None,branch:branch_detail|None=None,teacher=None,subject=None)->QuerySet[branch_subjects]:
    if not branchsubjects:
        branchsubjects=branch_subjects.branch_sub_obj.all()
    if teacher:
        branchsubjects=branchsubjects.filter(subject_teacher=teacher)
    if branch:
        branchsubjects=branchsubjects.filter(branch=branch)
    if subject:
        branchsubjects=branchsubjects.filter(branch_subject=subject)
    return branchsubjects