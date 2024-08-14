from flask import current_app
from flask_restx import Namespace, Resource, fields
from flask_restx._http import HTTPStatus
from sqlalchemy.exc import IntegrityError

from employee_server.db import get_db
from employee_server.models.team import Team as TeamModel

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
        teams = TeamModel.query.all()
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
        session = get_db().session
        name = api.payload["name"]
        try:
            team = TeamModel(name)
            session.add(team)
            session.commit()
            return {"id": team.id, "name": name}, 201
        except IntegrityError:
            current_app.logger.error(
                f"The team with name '{
                    name}' already exists."
            )
            session.rollback()
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
        team = get_db().session.get(TeamModel, team_id)
        if team is not None:
            return team

        api.abort(HTTPStatus.NOT_FOUND, "The team does not exist.")
