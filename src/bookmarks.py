from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,HTTP_409_CONFLICT
from src.database import Bookmark,db
from flask_jwt_extended import get_jwt_identity, jwt_required
bookmarks = Blueprint('bookmarks',__name__,url_prefix="/api/v1/bookmarks")

@bookmarks.route('/', methods=["POST","GET"])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()
    if request.method == "POST":
        categories_current_id = request.get_json().get('category_id','')
        body= request.get_json().get('body','null')
        url = request.get_json().get('url','null')
        piriority = request.get_json().get('piriority','Average')
        title = request.get_json().get('title','')

        if not validators.url(url):
            return jsonify({
                "error": "Enter valid url"
            }), HTTP_400_BAD_REQUEST
        if len(url) > 5 and Bookmark.query.filter_by(url=url).first():
            return jsonify({
                "error": "Url already exists"
            }),HTTP_409_CONFLICT
        if len(title) < 2:
            return jsonify({
                "error": "Enter required fields"
            }),HTTP_400_BAD_REQUEST
        if piriority.lower() != 'average' and piriority.lower() != 'vip' and piriority.lower() != 'basic':
            return jsonify({
                "error": "Not correct arguments"
            }), HTTP_400_BAD_REQUEST
        
        bookmark = Bookmark(url=url, body=body, user_id=current_user,categories_id=categories_current_id,piriority=piriority,title=title)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            "message":"Bookmark added successfully"
        }), HTTP_201_CREATED
    else:
        categories_current_id = request.args.get('category_id')
        bookmark = Bookmark.query.filter_by(user_id=current_user, categories_id = categories_current_id)
        bookmark_data=[]
        for item in bookmark:
            bookmark_data.append({
                "id":item.id,
                "title":item.title,
                "url":item.url,
                "short_url":item.short_url,
                "visit":item.visits,
                "body": item.body,
                "piriority": item.piriority,
                "created_at": item.created_at,
                "updated_at": item.updated_at
            })
            
        return jsonify({
            "data":bookmark_data
        }),HTTP_200_OK