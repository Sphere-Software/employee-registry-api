import sqlite3

from employee_server.db import get_db
from flask import current_app
from flask_restx import Namespace, Resource, fields
from flask_restx._http import HTTPStatus

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
        db = get_db()
        teams = db.execute("SELECT id, name FROM teams").fetchall()
        return teams

    @api.doc("create_team")
    @api.expect(team)
    @api.marshal_with(team, code=HTTPStatus.CREATED)
    @api.response(
        HTTPStatus.CONFLICT,
        description="The team with the same name already exists.",
    )
    def post(self):
        """
        Adds new team.
        """
        db = get_db()
        name = api.payload["name"]
        try:
            current_app.logger.debug(f"{api.payload}")
            result = db.execute("INSERT INTO teams (name) values (?)", (name,))
            db.commit()
            return {"id": result.lastrowid, "name": name}, 201
        except sqlite3.IntegrityError:
            current_app.logger.error(
                f"The team with name '{name}' already exists."
            )
            db.rollback()
            api.abort(
                HTTPStatus.CONFLICT,
                f"The team with name '{name}' already exists",
            )


@api.route("/<int:team_id>")
class Team(Resource):
    @api.doc("get_team")
    @api.marshal_with(team)
    @api.response(
        HTTPStatus.NOT_FOUND,
        description="The team with given id does not exist",
    )
    def get(self, team_id):
        """
        Returns team with gith given id.
        :param int team_id: An id if the team.
        """
        db = get_db()
        team = db.execute(
            "SELECT id, name FROM teams WHERE id = ?", (team_id,)
        ).fetchone()
        if team is not None:
            return team
        api.abort(HTTPStatus.NOT_FOUND, "The team does not exist.")
