# Basic Blueprint for handling files
# Create at 24/07/2021
# Written by Maganu Mihai(m3m0ry)


import os
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    current_app, send_from_directory
)

from flaskapp.db import get_db
from werkzeug.utils import secure_filename

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


@bp.route('/upload', methods=["GET", "POST"])
def upload_sample():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file_obj = request.files['file']

        # If the user does noe select a file, the browser submits an empty file
        # without a filename.
        if file_obj.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file_obj:
            filename = secure_filename(file_obj.filename)
            file_obj.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                filename))
            return redirect(url_for('sample.download_file', name=filename))

    return render_template("sample/upload.html")


@bp.route("/uploads/<name>", methods=["GET"])
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)


@bp.route("/analyze", methods=["GET"])
def analyze_sample():
    return render_template("sample/analyze.html")


@bp.route('/list', methods=["GET"])
def list_samples():
    return render_template("sample/list.html")
