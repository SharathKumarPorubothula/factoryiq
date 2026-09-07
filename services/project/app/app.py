from flask import Flask, request
from db_util import Database

app = Flask(__name__)


# ============================================================
# Database Connections
# ============================================================

# Project Service database
project_db = Database("project_db")

# Identity database - users/project members
identity_db = Database("identity_db")

# Master data database - customers/sites
master_db = Database("master_data_db")


# ============================================================
# Project API
# ============================================================


@app.route("/project", methods=["GET"])
def get_projects():
    """
    Returns project information for the Projects UI.
    """

    try:
        # ----------------------------------------------------
        # 1. Get projects
        # ----------------------------------------------------

        projects_query = """
            SELECT
                id,
                program_id,
                project_code,
                name,
                description,
                status,
                start_date,
                end_date,
                created_at,
                updated_at
            FROM projects
            ORDER BY created_at DESC;
        """

        projects = project_db.execute(projects_query)

        if not projects:
            return {"projects": [], "message": "No projects found"}, 200

        # ----------------------------------------------------
        # 2. Get all programs
        # ----------------------------------------------------

        programs_query = """
            SELECT
                id,
                name,
                description,
                status,
                start_date,
                end_date,
                created_at,
                updated_at
            FROM programs;
        """

        programs = project_db.execute(programs_query)

        program_map = {str(program["id"]): program for program in programs}

        # ----------------------------------------------------
        # 3. Get project members
        # ----------------------------------------------------

        members_query = """
            SELECT
                id,
                project_id,
                user_id,
                role,
                created_at
            FROM project_members;
        """

        members = project_db.execute(members_query)

        members_by_project = {}

        for member in members:
            project_id = str(member["project_id"])

            if project_id not in members_by_project:
                members_by_project[project_id] = []

            members_by_project[project_id].append(member)

        # ----------------------------------------------------
        # 4. Get users from identity_db
        # ----------------------------------------------------

        users_query = """
            SELECT
                id,
                username,
                email,
                first_name,
                last_name,
                is_active,
                last_login_at,
                created_at,
                updated_at
            FROM users;
        """

        users = identity_db.execute(users_query)

        user_map = {str(user["id"]): user for user in users}

        # ----------------------------------------------------
        # 5. Get milestones
        # ----------------------------------------------------

        milestones_query = """
            SELECT
                id,
                project_id,
                name,
                description,
                due_date,
                status,
                created_at
            FROM milestones;
        """

        milestones = project_db.execute(milestones_query)

        milestones_by_project = {}

        for milestone in milestones:
            project_id = str(milestone["project_id"])

            if project_id not in milestones_by_project:
                milestones_by_project[project_id] = []

            milestones_by_project[project_id].append(milestone)

        # ----------------------------------------------------
        # 6. Get risks
        # ----------------------------------------------------

        risks_query = """
            SELECT
                id,
                project_id,
                title,
                description,
                probability,
                impact,
                status,
                created_at
            FROM risks;
        """

        risks = project_db.execute(risks_query)

        risks_by_project = {}

        for risk in risks:
            project_id = str(risk["project_id"])

            if project_id not in risks_by_project:
                risks_by_project[project_id] = []

            risks_by_project[project_id].append(risk)

        # ----------------------------------------------------
        # 7. Get dependencies
        # ----------------------------------------------------

        dependencies_query = """
            SELECT
                id,
                project_id,
                predecessor_id,
                successor_id,
                dependency_type,
                created_at
            FROM dependencies;
        """

        dependencies = project_db.execute(dependencies_query)

        dependencies_by_project = {}

        for dependency in dependencies:
            project_id = str(dependency["project_id"])

            if project_id not in dependencies_by_project:
                dependencies_by_project[project_id] = []

            dependencies_by_project[project_id].append(dependency)

        # ----------------------------------------------------
        # 8. Get status history
        # ----------------------------------------------------

        history_query = """
            SELECT
                id,
                project_id,
                old_status,
                new_status,
                changed_by,
                changed_at
            FROM status_history
            ORDER BY changed_at DESC;
        """

        status_history = project_db.execute(history_query)

        history_by_project = {}

        for history in status_history:
            project_id = str(history["project_id"])

            if project_id not in history_by_project:
                history_by_project[project_id] = []

            history_by_project[project_id].append(history)

        # ----------------------------------------------------
        # 9. Build final response
        # ----------------------------------------------------

        response = []

        for project in projects:
            project_id = str(project["id"])
            program_id = str(project["program_id"]) if project["program_id"] else None

            # Program
            program = program_map.get(program_id)

            # Members + users
            project_members = []

            for member in members_by_project.get(project_id, []):
                user_id = str(member["user_id"])

                user = user_map.get(user_id)

                project_members.append(
                    {
                        "id": member["id"],
                        "user_id": member["user_id"],
                        "role": member["role"],
                        "created_at": member["created_at"],
                        "user": user,
                    }
                )

            # ------------------------------------------------
            # Project response
            # ------------------------------------------------

            project_data = {
                # Project fields
                "id": project["id"],
                "project_code": project["project_code"],
                "name": project["name"],
                "description": project["description"],
                "status": project["status"],
                "start_date": project["start_date"],
                "end_date": project["end_date"],
                "created_at": project["created_at"],
                "updated_at": project["updated_at"],
                # Program
                "program": program,
                # Members / Owners
                "members": project_members,
                # Project related data
                "milestones": milestones_by_project.get(project_id, []),
                "risks": risks_by_project.get(project_id, []),
                "dependencies": dependencies_by_project.get(project_id, []),
                "status_history": history_by_project.get(project_id, []),
            }

            response.append(project_data)

        # ----------------------------------------------------
        # Final API response
        # ----------------------------------------------------

        return {"projects": response, "count": len(response)}, 200

    except Exception as e:
        return {"error": "Failed to fetch projects", "details": str(e)}, 500


# ============================================================
# Application
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
