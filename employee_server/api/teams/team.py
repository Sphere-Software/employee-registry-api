from flask_restx import Resource, Namespace, fields

from flask import current_app

import sqlite3

api = Namespace("teams", description="Teams")


def get_api():
    """
    Returns teams API.
    """
    return api


team = api.model(
    "Team",
    {
        "id": fields.Integer(required=True, description="Team id"),
        "name": fields.String(required=True, description="Team name"),
    },
)


@api.route("/")
class Teams(Resource):
    @api.doc("get_teams")
    @api.marshal_list_with(team)
    def get(self):
        """
        Returns list of teams.
        """
        db = current_app.__getattr__("get_db")()
        teams = db.execute("SELECT id, name FROM teams").fetchall()
        return teams

    @api.doc("create_team")
    @api.expect(team)
    @api.marshal_with(team, code=201)
    @api.response(
        400, description="The team with the same name already exists."
    )
    def post(self):
        """
        Adds new team.
        """
        db = current_app.__getattr__("get_db")()
        try:
            current_app.logger.debug(f"{api.payload}")
            name = api.payload["name"]
            result = db.execute("INSERT INTO teams (name) values (?)", (name,))
            db.commit()
            return {"id": result.lastrowid, "name": name}, 201
        except sqlite3.IntegrityError:
            current_app.logger.error(
                f"The team with name '{name}' already exists."
            )
            db.rollback()
            api.abort(400, f"The team with name '{name}' already exists")


@api.route("/<int:team_id>")
class Team(Resource):
    @api.doc("get_team")
    @api.marshal_with(team)
    @api.response(404, description="The team with given id does not exist")
    def get(self, team_id):
        """
        Returns team with gith given id.
        :param int team_id: An id if the team.
        """
        db = current_app.__getattr__("get_db")()
        team = db.execute(
            "SELECT id, name FROM teams WHERE id = ?", (team_id,)
        ).fetchone()
        if team is not None:
            return team
        api.abort(404, "The team does not exist.")
