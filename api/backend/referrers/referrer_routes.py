from flask import Blueprint, jsonify, make_response, request, current_app
from backend.db_connection import db

referrers = Blueprint('Referrers', __name__)


@referrers.route("/", methods=["GET"])
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

@referrers.route("/<referrerId>" , methods=["GET"])
def get_referrer(referrerId):
    query = '''
        SELECT r.referrerId, 
               r.name, 
               r.email,
               r.numReferrals,
               c.name as company_name
        FROM Referrers r
        JOIN Companies c ON r.companyId = c.companyId
        WHERE r.referrerId = %s
    '''

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (referrerId,))
        data = cursor.fetchall()
        res = make_response(jsonify(data))
        res.status_code = 200
    except Exception as e:
        res = make_response(jsonify({"error": str(e)}))
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

@referrers.route("/best", methods=["GET"])
def get_best_referrers():
    # Get the top_n parameter from the query string, default to 10 if not provided
    top_n = request.args.get("top_n", default=10, type=int)

    # Ensure that top_n is a positive integer
    if top_n <= 0:
        return make_response(jsonify({"error": "top_n must be a positive integer"}), 400)

    query = """
        SELECT ref.referrerId, 
       ref.name, 
       ref.email, 
       ref.phoneNumber,
       c.name AS companyName
    FROM Referrers ref 
    JOIN Companies c ON ref.companyId = c.companyId
    JOIN (
    SELECT r.companyId
    FROM Requests r
    WHERE r.pendingStatus = 'accepted'
    GROUP BY r.companyId
    ORDER BY COUNT(*) DESC
    LIMIT %s  
    ) AS TopCompanies ON ref.companyId = TopCompanies.companyId;


    """

    current_app.logger.info(f'Get /best query: {query} with top_n: {top_n}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (top_n,))  # Pass top_n as parameter
        data = cursor.fetchall()

    
        res = make_response(jsonify(data))
        res.status_code = 200

    except Exception as e:
        current_app.logger.error(f"Error in /best: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res



@referrers.route("/left", methods=["GET"])
def get_best_referrers_left():
    # Default to 5 if 'top_n' is not provided
    top_n = request.args.get("top_n", default=5, type=int)

    # Ensure 'top_n' is a positive integer
    if top_n <= 0:
        return make_response(jsonify({"error": "top_n must be a positive integer"}), 400)

    query = f"""
    SELECT referrerId, name, email, phoneNumber, numReferrals
    FROM Referrers
    ORDER BY numReferrals DESC
    LIMIT %s;
    """

    current_app.logger.info(f'Get /left query: {query} with top_n: {top_n}')

    try:
        cursor = db.get_db().cursor()
        cursor.execute(query, (top_n,))  # Execute with top_n parameter
        data = cursor.fetchall()


        res = make_response(jsonify(data))
        res.status_code = 200
    
    except Exception as e:
        current_app.logger.error(f"Error in /left: {str(e)}")
        res = make_response(jsonify({"error": str(e)}))
        res.status_code = 500

    return res
