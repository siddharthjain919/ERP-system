from .models import branch_detail,branch_subjects

def get_subjects_by_branch(branch:branch_detail):
    return branch_subjects.branch_sub_obj.filter(branch=branch)