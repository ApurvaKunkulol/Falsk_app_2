import logging
import os
import string
import random

from flask import Flask, request
from flask_restplus import Resource
from flask_pymongo import PyMongo
from bson import json_util
from constants import local_connection_string
from app import app, api


app.config["MONGO_URI_2"] = local_connection_string.format("products")
product_mongo_conn = PyMongo(app)
ns_prod = api.namespace("product", description="Product Information.")


# @ns_prod.route("/api/v0.1/product_description/<int:product_id>")
class ProductDescAPI(Resource):
    def get(self, product_id):
        """
        Description: A function to get description of the product whose ID has been passed through query parameters.
        Argument(s):
            product_id: ID of the product whose description to be fetched.
        Returns:
            JSON containing product description.
        """
        try:
            if product_id:
                db_cursor = product_mongo_conn.db.catalogue.find({"prod_id": product_id})
                product_desc = db_cursor[0]
                return json_util.dumps({"status": "success", "message": "", "product_description": product_desc})
            else:
                return {"status": "error", "message": "Please supply product ID."}
        except IndexError as idx_err:
            logging.error("No product found for the given ID: {}".format(product_id))
            return {"status": "error", "message": "No product found for the given ID: {}".format(product_id)}
        except Exception as ex:
            logging.error("Error while fetching product details.", exc_info=True)
            return {"status": "success", "message": "Error while fetching product details"}


# @ns_prod.route("/api/v0.1/create_product")
class ProductCreationAPI(Resource):
    def post(self):
        """
        Description: A function to create a new product.
        Argument(s):
            product_id: ID of the product whose description to be fetched.
        Returns:
            JSON containing product description.
        """
        try:
            import pdb
            pdb.set_trace()
            product_data = request.get_json()
            if product_data:
                part_id = string.ascii_lowercase
                part_id = "".join(random.choice(part_id) for i in range(5))
                prod_id = "{name}_{part_id}".format(name=product_data.get("name"), part_id=part_id)
                product_data["product_id"] = prod_id
                inserted_id = product_mongo_conn.db.insert(product_data)
                return {"status": "success", "message": "Successfully inserted new product. ID: {}".format(inserted_id)}
            else:
                return {"status": "error", "message": "Please provide product details."}

        except Exception as ex:
            logging.error("Error while creating product.", exc_info=True)
            return {"status": "success", "message": "Error while creating product."}


ns_prod.add_resource(ProductCreationAPI, "/api/v0.1/create_product")
ns_prod.add_resource(ProductDescAPI, "/api/v0.1/product_description/<int:product_id>")
