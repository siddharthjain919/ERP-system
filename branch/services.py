from .models import branch_detail,branch_subjects
from django.db.models.query import QuerySet

def get_subjects_by_branch(branch:branch_detail):
    return branch_subjects.branch_sub_obj.filter(branch=branch)

def get_labs(subjects:QuerySet[branch_subjects])->QuerySet[branch_subjects]:
    return subjects.filter(branch_subject__is_lab=True)