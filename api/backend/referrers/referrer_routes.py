from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

referrers = Blueprint('Referrers', __name__)


@referrers.route("/referrers", methods=["GET"])
def get_referrers():
    query = '''
        SELECT r.referrerId, 
               r.name, 
               r.email,
               r.numReferrals,
               c.name as company_name
        FROM Referrers r
        JOIN Companies c ON r.companyId = c.companyId
    '''

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res

@referrers.route("/", methods=["POST"])
def create_referrer():

    req = request.json
    current_app.logger.info(req)

    name = req["name"]
    email = req["email"]
    #phone can be null
    phoneNumber = req.get("phoneNumber", "")
    adminId = req["adminId"]
    companyId = req["companyId"]
    #numreferrals can be null
    numreferrals = req.get("numReferrals")

    #not sure if query inserting None is ok 
    query = f'''
        INSERT INTO Referrers (name, 
                               email, 
                               phoneNumber, 
                               adminId, 
                               companyId, 
                               numReferrals)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''

    current_app.logger.info(query)
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (name, email, phoneNumber, adminId, companyId, numreferrals))  # Pass the values here
        db.get_db().commit()
        res = make_response(jsonify({"message": "Referrer created"}))
        res.status_code = 201
    except Exception as e:
        res = make_response(jsonify({"error when creating referrer": str(e)}))
        res.status_code = 500

    return res


@referrers.route("/<referrerId>", methods=["PUT"])
def create_request(referrerId):

    req = request.json
    current_app.logger.info(req)

    companyId = req.get("companyId")
    email = req.get("email","")
    phoneNumber = req.get("phoneNumber","")
    referrerId = req.get("referrerId")

    query = """
        UPDATE Referrers
        SET companyId = %s, email = %s, phoneNumber = %s
        WHERE referrerId = %s
    """

    current_app.logger.info(f'PUT /<referrerId> query: {query}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (companyId, email, phoneNumber, referrerId))
        db.get_db().commit()

        res = make_response(jsonify({"message": f"Updated successful"}))
        res.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error updating referrer details: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res