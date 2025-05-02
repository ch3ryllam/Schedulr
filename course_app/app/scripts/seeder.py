from flask.cli import with_appcontext
import click
from ..db import db
from ..scripts.scraper import seed_courses, seed_core, seed_prereq, seed_schedules


@click.command("seed-all")
@with_appcontext
def seed_all():
    db.create_all()
    seed_courses()
    seed_core()
    seed_prereq()
    seed_schedules()
