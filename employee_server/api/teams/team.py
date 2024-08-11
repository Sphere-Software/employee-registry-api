from flask_restx import Resource, Namespace, fields

from flask import current_app

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
class TeamList(Resource):
    @api.doc("get")
    @api.marshal_list_with(team)
    def get(self):
        """
        Returns list of teams.
        """
        db = current_app.__getattr__("get_db")()
        teams = db.execute("SELECT id, name FROM teams").fetchall()
        return teams


@api.route("/<int:team_id>")
class Team(Resource):
    @api.doc("get")
    @api.marshal_with(team)
    def get(self, team_id):
        """
        Returns team with gith given id.
        """
        db = current_app.__getattr__("get_db")()
        team = db.execute(
            "SELECT id, name FROM teams WHERE id = ?", (team_id,)
        ).fetchone()
        return team
