# pythom import
import json, traceback

# modules import
from bson import json_util
from bson.objectid import ObjectId
from django.http import JsonResponse
from pymongo.message import delete
from rest_framework.views import APIView

# project import
from ecommerce.settings import db

class Category(APIView):
    '''APIs for category.'''
    def post(self, request):
        '''
        API to create category
        :param: categoryName str
        :param: parentCategoryId str
        '''
        try:
            data = request.data
            name = data.get("categoryName", False)
            parentCategoryId = data.get("parentCategoryId", "")
            if not name:
                response = {
                    "message": "Category Name is required field.",
                    "data": [],
                }
                return JsonResponse(response, status=422)
            id = db.category.insert({
                "categoryName": name,
                "parentCategoryId": parentCategoryId
            })
            response = {
                "data": str(id),
                "message": "Category created successfully."
            }
            return JsonResponse(response, status=200)
        except Exception as e:
            print(f"error: {str(e)}")
            traceback.print_exc()
            return JsonResponse({"message": f"Internal server error: {str(e)}", "data": []}, status=500)

    def get(self, request):
        '''
        API to get category.
        :param: from int
        :param: to int
        '''
        try:
            from_ = request.GET.get("from", 0)
            to = request.GET.get("to", 20)
            category = db.category.find().sort("_id", -1).skip(int(from_)).limit(int(to))
            data = json.loads(json_util.dumps(category))
            return JsonResponse(data, safe=False, status=200)
        except Exception as e:
            print(f"error: {str(e)}")
            traceback.print_exc()
            return JsonResponse({"message": f"Internal server error: {str(e)}", "data": []}, status=500)

    def patch(self, request):
        '''
        API to update category.
        :param: _id str: category id to update
        :param: categoryName str: Name to update
        :param: parentCategoryId str: parentCategoryId to update
        '''
        try:
            data = request.data
            _id = data.get("_id", False)
            if not _id:
                response = {
                    "message": "_id is required field to update data.",
                    "data": [],
                }
                return JsonResponse(response, status=422)
            name = data.get("categoryName", False)
            parentCategoryId = data.get("parentCategoryId", False)
            if not name and not parentCategoryId:
                response = {
                    "message": "No data to update received.",
                    "data": [],
                }
                return JsonResponse(response, status=422)
            data = {"$set": {}}
            if name:
                data['$set']['categoryName'] = name
            if parentCategoryId:
                data['$set']['parentCategoryId'] = parentCategoryId
            db.category.update({"_id": ObjectId(_id)}, data)
            response = {
                "data": _id,
                "message": "Category updated successfully."
            }
            return JsonResponse(response, status=200)
        except Exception as e:
            print(f"error: {str(e)}")
            traceback.print_exc()
            return JsonResponse({"message": f"Internal server error: {str(e)}", "data": []}, status=500)

    def delete(self, request):
        '''
        API to delete category.
        :param: _id str: category id to delete
        '''
        try:
            data = request.data
            _id = data.get("_id", False)
            if not _id:
                response = {
                    "message": "_id is required field to delete data.",
                    "data": [],
                }
                return JsonResponse(response, status=422)
            # delete category and child category
            db.category.remove({"_id": ObjectId(_id)})
            db.category.remove({"parentCategoryId": str(_id)})
            response = {
                "data": _id,
                "message": "Categories deleted successfully."
            }
            return JsonResponse(response, status=200)
        except Exception as e:
            print(f"error: {str(e)}")
            traceback.print_exc()
            return JsonResponse({"message": f"Internal server error: {str(e)}", "data": []}, status=500)

class Product(APIView):
    '''APIs for product'''
    def post(self, request):
        '''
        API to create product
        :param: name str
        :param: categoryId str
        :param: price float
        '''
        try:
            data = request.data
            name = data.get("name", False)
            categoryId = data.get("categoryId", "")
            price = data.get("price", False)
            if not name or not price:
                if not name:
                    string = "name is required field."
                if not price:
                    string = "price is required field."
                if not name and not price:
                    string = "name, price are required field."
                response = {
                    "message": string,
                    "data": [],
                }
                return JsonResponse(response, status=422)
            id = db.product.insert({
                "name": name,
                "categoryId": categoryId,
                "price": float(price)
            })
            response = {
                "data": str(id),
                "message": "Product created successfully."
            }
            return JsonResponse(response, status=200)
        except Exception as e:
            print(f"error: {str(e)}")
            traceback.print_exc()
            return JsonResponse({"message": f"Internal server error: {str(e)}", "data": []}, status=500)

    def get(self, request):
        '''
        API to get products.
        :param: from int
        :param: to int
        '''
        try:
            from_ = request.GET.get("from", 0)
            to = request.GET.get("to", 20)
            products = db.product.find().sort("_id", -1).skip(int(from_)).limit(int(to))
            data = json.loads(json_util.dumps(products))
            return JsonResponse(data, safe=False, status=200)
        except Exception as e:
            print(f"error: {str(e)}")
            traceback.print_exc()
            return JsonResponse({"message": f"Internal server error: {str(e)}", "data": []}, status=500)


    def patch(self, request):
        '''
        API to update product.
        :param: _id str: product id to update
        :param: categoryId str: categoryId to update
        :param: price str: price to update
        '''
        try:
            data = request.data
            _id = data.get("_id", False)
            if not _id:
                response = {
                    "message": "_id is required field to update data.",
                    "data": [],
                }
                return JsonResponse(response, status=422)
            name = data.get("name", False)
            categoryId = data.get("categoryId", False)
            price = data.get("price", False)
            if not name and not categoryId and not price:
                response = {
                    "message": "No data to update received.",
                    "data": [],
                }
                return JsonResponse(response, status=422)
            data = {"$set": {}}
            if name:
                data['$set']['name'] = name
            if categoryId:
                data['$set']['categoryId'] = categoryId
            if price:
                data['$set']['price'] = float(price)
            db.product.update({"_id": ObjectId(_id)}, data)
            response = {
                "data": _id,
                "message": "Product updated successfully."
            }
            return JsonResponse(response, status=200)
        except Exception as e:
            print(f"error: {str(e)}")
            traceback.print_exc()
            return JsonResponse({"message": f"Internal server error: {str(e)}", "data": []}, status=500)

    def delete(self, request):
        '''
        API to delete category.
        :param: _id str: category id to delete
        '''
        try:
            data = request.data
            _id = data.get("_id", False)
            if not _id:
                response = {
                    "message": "_id is required field to delete data.",
                    "data": [],
                }
                return JsonResponse(response, status=422)
            # delete category and child category
            db.product.remove({"_id": ObjectId(_id)})
            db.product.remove({"categoryId": str(_id)})
            response = {
                "data": _id,
                "message": "Product deleted successfully."
            }
            return JsonResponse(response, status=200)
        except Exception as e:
            print(f"error: {str(e)}")
            traceback.print_exc()
            return JsonResponse({"message": f"Internal server error: {str(e)}", "data": []}, status=500)
