import json
from flask import request
from core.libs import assertions
from functools import wraps

from core.models.students import Student
from core.models.teachers import Teacher
from core.models.principals import Principal


class AuthPrincipal:
    def __init__(self, user_id, student_id=None, teacher_id=None, principal_id=None):
        self.user_id = user_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.principal_id = principal_id


def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper


def authenticate_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'principal not found')
        p_dict = json.loads(p_str)
        p = AuthPrincipal(
            user_id=p_dict['user_id'],
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id'),
            principal_id=p_dict.get('principal_id')
        )

        if request.path.startswith('/student'):
            assertions.assert_true( (p.student_id is not None) and (p.student_id in [row[0] for row in Student.query.with_entities(Student.id).all()]), 'requester should be a student')
            assertions.assert_true(p.user_id == Student.filter(Student.id == p.student_id ).first().user_id,'User id and Student id does not match')
        
        elif request.path.startswith('/teacher'):
            assertions.assert_true( (p.teacher_id is not None) and (p.teacher_id in [row[0] for row in Teacher.query.with_entities(Teacher.id).all()]), 'requester should be a teacher')
            assertions.assert_true(p.user_id == Teacher.filter(Teacher.id == p.teacher_id).first().user_id,'User id and Teacher id does not match')
        
        elif request.path.startswith('/principal'):
            assertions.assert_true( (p.principal_id is not None) and (p.principal_id in [row[0] for row in Principal.query.with_entities(Principal.id).all()]), 'requester should be a principal')
            assertions.assert_true(p.user_id == Principal.filter(Principal.id == p.principal_id).first().user_id, 'User id and Principal id does not match')
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper
