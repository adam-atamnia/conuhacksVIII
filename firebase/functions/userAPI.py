from flask import Blueprint, request, jsonify
from firebase_admin import firestore
import uuid

db = firestore.client()
user_Ref = db.collection('user')

userAPI = Blueprint('userAPI', __name__)

@userAPI.route('/add', methods=['POST'])
def create():
  try:
    id = uuid.uuid4()
    user_Ref.document(str(id)).set(request.json)
    return jsonify({"success": True}), 200
  except Exception as e:
    return f'An ErrorOccured: {e}'