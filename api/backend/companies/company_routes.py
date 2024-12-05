
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