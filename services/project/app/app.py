from flask import Flask, request
from db_util import Database

db=Database()
app=Flask(__name__)

@app.route("/project", methods=["GET"])
def get_project():
    ''' Returns a all projects in the database '''
    data=request.json
    if not data:
        return {"error": "Missing request body"}, 400
    
    trace_id=data.get('trace_id')
    user_id=data.get('user_id')

    if not trace_id or not user_id:
        return {"error": "Missing trace_id or user_id"}, 400

    query = '''SELECT
                u.id AS user_id,
                u.username,
                r.id AS role_id,
                r.name AS role_name,
                p.id AS permission_id,
                p.name AS permission_name,
                p.resource,
                p.action,
                p.description
                FROM users u
                INNER JOIN user_roles ur
                    ON u.id = ur.user_id
                INNER JOIN roles r
                    ON ur.role_id = r.id
                INNER JOIN role_permissions rp
                    ON r.id = rp.role_id
                INNER JOIN permissions p
                    ON rp.permission_id = p.id
                WHERE u.id = ?;'''

    result = db.execute_query(query, (user_id,))
    return {"projects": result}



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)