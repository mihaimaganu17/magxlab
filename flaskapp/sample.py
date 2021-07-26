# Basic Blueprint for handling files
# Create at 24/07/2021
# Written by Maganu Mihai(m3m0ry)


import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskapp.db import get_db

# Create a new blueprint for samples that are analysed
bp = Blueprint("sample", __name__, url_prefix='/sample')

@bp.route('/add', methods=["GET", "POST"])
def add_sample():
    if request.method == 'POST':
        # TODO: this should be removed, we should compute the sha256 on our own
        sha256 = request.form["sha256"]
        disk_path = request.form["disk_path"]
        print(sha256, disk_path)

        # Fetch the database
        db = get_db()

        # Current there is no error for the client to be displayed
        client_error = None

        if not sha256:
            client_error = "A sha256 hash is required for the file."
        elif not disk_path:
            client_error = "A local path of the file is required."
        else:
            # See if we already have the file in our database
            is_in_db = db.execute("SELECT id FROM samples WHERE sha256 = ?",
                (sha256,)).fetchone()
            if is_in_db:
                client_error = f"File {sha256} is already registered."


        if client_error is None:
            db.execute(
                "INSERT INTO samples (sha256, file_type, disk_path) VALUES \
                (?, ?, ?)", (sha256, "pe", disk_path)
            )
            db.commit()
            return redirect(url_for("sample.psych"))

        flash(client_error)

    return render_template("sample/add.html")


@bp.route('/psych', methods=["GET"])
def psych():
    return "<h2>Mice</h2>"
