from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT
from src.database import Categories,db
from flask_jwt_extended import get_jwt_identity, jwt_required
categories = Blueprint('categories',__name__,url_prefix="/api/v1/categories")

@categories.route('/', methods=["POST", "GET"])
@jwt_required()
def handle_categories():
    current_user = get_jwt_identity()
    if request.method == "POST":
        title = request.get_json().get('title','')
        description = request.get_json().get('description','')
        is_public = request.get_json().get('is_public',False)


        categorie = Categories(title=title, description=description, user_id=current_user,is_public=is_public)
        db.session.add(categorie)
        db.session.commit()

        return jsonify({
            "message":"Category is created successfully",
            "id":categorie.id,
            "title":categorie.title,
            "description":categorie.description
        }), HTTP_201_CREATED
    
    else:
        categorie = Categories.query.filter_by(user_id=current_user)
        categories_data = []
        for item in categorie:
            categories_data.append({
                "id":item.id,
                "title":item.title,
                "is_public": item.is_public,
                "description":item.description
            })
        return jsonify({
            "data":categories_data
        }), HTTP_200_OK