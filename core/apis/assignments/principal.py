from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema,TeacherSchema, AssignmentGradeSchema
from core import db

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    principal_assignments=Assignment.get_submitted_and_graded_assignments()
    teachers_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)
   
@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""
    teachers=Teacher.get_all_teachers()
    teachers_dump=TeacherSchema().dump(teachers,many=True)
    return APIResponse.respond(data=teachers_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def update_assignment_grade(p,incoming_payload):
    """Grade or re-grade an assignment"""
    grade_update_payload=AssignmentGradeSchema().load(incoming_payload)
    updated_assignment=Assignment.update_grade(_id=grade_update_payload.id,grade=grade_update_payload.grade)
    db.session.commit()
    updated_assignment_dump=AssignmentSchema().dump(updated_assignment)
    return APIResponse.respond(data=updated_assignment_dump)



