from flask import request, jsonify
from . import players_bp # Import the blueprint instance
from ..services.player_parsing_service import process_player_html
from werkzeug.utils import secure_filename
import pandas as pd

ALLOWED_EXTENSIONS = {'html'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@players_bp.route('/upload_players', methods=['POST'])
def handle_player_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if not file.filename or file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(file.filename)
    extension = filename.rsplit('.', 1)[1].lower()

    df = None
    try:
        if extension == 'html':
            df = process_player_html(file)

        if df is None:
            return jsonify({"error": "Could not parse file"}), 400

        # # Call specific player analysis logic
        # processed_df = calculate_player_percentiles(df)

        # --- Database saving logic will go here later ---

        # data_as_json = processed_df.to_json(orient="records")
        # return jsonify(data_as_json)
        return jsonify({"message": "File processed successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500