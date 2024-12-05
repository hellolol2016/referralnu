from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
companies = Blueprint('companies', __name__)


@companies.route("/", methods=["GET"])
def get_all_companies():
    """
    Fetch all companies from the database.
    """
    query = "SELECT * FROM Companies;"
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error fetching all companies: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500
    return res


@companies.route("/<int:company_id>", methods=["GET"])
def get_company_by_id(company_id):
    """
    Fetch a specific company by its ID.
    """
    query = "SELECT * FROM Companies WHERE companyId = %s;"
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (company_id,))
        data = cursor.fetchone()
        if data:
            res = make_response(jsonify(data))
            res.status_code = 200
        else:
            res = make_response(jsonify({"message": "Company not found"}))
            res.status_code = 404
    except Exception as e:
        current_app.logger.error(f"Error fetching company with ID {company_id}: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500
    return res


@companies.route('/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    try:
        # Connect to the database
        cursor = db.get_db().cursor()

        # Execute the DELETE query
        cursor.execute("DELETE FROM Companies WHERE companyId = %s", (company_id,))
        db.get_db().commit()

        # Return success response
        return jsonify({"message": "Company deleted successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error deleting company: {str(e)}")
        return jsonify({"error": str(e)}), 500
