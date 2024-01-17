def test_get_assignments_student_1(client, h_student_1):
    """
    success case : List all assignments of student_1
    """
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    """
    success case : List all assignments of student_2
    """
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    """
    success case : Assignment create
    """
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_edit_assignment_student_1(client, h_student_1):
    """
    success case: Assignment edit
    """
    content = 'NEW CONTENT'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id':5,
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_edit_submitted_assignment(client, h_student_1):
    """
    failure case: only assignment in draft state can be edited
    """
    content = 'Test content'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id':1,
            'content': content
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only assignment in draft state can be edited'


def test_submit_assignment_student_2(client, h_student_2):
    """
    success case : Assignment submission
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'id': 6,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 2
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    """
    failure case : Assignment cannot be resubmitted
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 6,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'


def test_bad_assignment_submit_error(client, h_student_1):
    """
    failure case: If an assignment does not exist, it should throw 404
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 10000,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 404
    assert error_response['error'] == 'FyleError'


def test_submit_assignment_cross(client,h_student_1):
    """
    failure case : assignment belongs to student_2 and not student_1
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 8,
            'teacher_id': 1
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response['message'] == "This assignment belongs to some other student"