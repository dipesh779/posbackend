from employee.models import Employee


def token_helper(request=None, **kwargs):

    user_id = request._auth.payload['user_id']
    employee = Employee.objects.get(id=user_id)
    company = employee.company
    if employee.branchh is not None:
        branch = employee.branchh
    else:
        branch = None
    return company, branch


def token_helper_employee(request=None, **kwargs):
    user_id = request._auth.payload['user_id']
    employee = Employee.objects.get(id=user_id)
    return employee

