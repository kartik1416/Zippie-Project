from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Task
from .schemas import TaskSchema

tasks_bp = Blueprint('tasks', __name__)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@tasks_bp.route('/tasks', methods=['GET'])
def list_tasks():
    # pagination
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    completed = request.args.get('completed', type=str)

    query = Task.query
    if completed is not None:
        if completed.lower() in ['true', '1', 'yes']:
            query = query.filter_by(completed=True)
        elif completed.lower() in ['false', '0', 'no']:
            query = query.filter_by(completed=False)

    pag = query.order_by(Task.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': tasks_schema.dump(pag.items),
        'total': pag.total,
        'page': pag.page,
        'pages': pag.pages
    })


@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return task_schema.jsonify(task)


@tasks_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json() or {}
    # simple validation: title is required
    if not data.get('title'):
        return jsonify({'message': 'Title is required'}), 400
    # identity is stored as string id; additional claims carry role/username
    identity = get_jwt_identity()
    jwt_claims = get_jwt()
    user_id = int(identity)
    task = Task(title=data.get('title'), description=data.get('description'), completed=data.get('completed', False), user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify(task_schema.dump(task)), 201


@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    identity = get_jwt_identity()
    jwt_claims = get_jwt()
    current_user = {'id': int(identity), 'role': jwt_claims.get('role')}
    data = request.get_json() or {}
    # role check: admin or owner
    if current_user['role'] != 'admin' and task.user_id != current_user['id']:
        return jsonify({'message': 'Forbidden'}), 403
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify(task_schema.dump(task))


@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    identity = get_jwt_identity()
    jwt_claims = get_jwt()
    current_user = {'id': int(identity), 'role': jwt_claims.get('role')}
    if current_user['role'] != 'admin' and task.user_id != current_user['id']:
        return jsonify({'message': 'Forbidden'}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({}), 204
