import random
import requests
import json
import re

CARBOHYDRATE = ["carbohydrate" , "carb", "carbs", "carby", "sugar", "carbohidrade", "carbohydrade"]
PROTEIN = ["protein", "proteins", "proteen", "protean", "protien", "protin", "proting"]
CALORIES = ["calories", "calorie","kalories", "kalorie", "kalory", "calory", "kalory"]
FAT = ["fat", "fats", "fatty"]
MASTER_LIST = ["carbohydrate" , "carb", "carbs", "carby", "sugar", "carbohidrade", "carbohydrade", "protein", "proteins", "proteen", "protean", "protien", "protin", "proting", "calories", "calorie","kalories", "kalorie", "kalory", "calory", "kalory", "fat", "fats", "fatty"]
FIELD_LIST = [CARBOHYDRATE, PROTEIN, CALORIES, FAT]
RECIPE_CLUSTER ="https://search-sensor-cloud-3kouvsbrr2mcoorths4t4enioa.us-west-2.es.amazonaws.com/recipe_data/recipe/_search"
RECIPE_POST_CLUSTER ="https://search-sensor-cloud-3kouvsbrr2mcoorths4t4enioa.us-west-2.es.amazonaws.com/recipe_data/recipe/"

def search_recipies(search_string):
    ret = []
    nutrition_criteria = search_string_nutrition(search_string)
    if nutrition_criteria:
        search_field = "nutrition." + nutrition_criteria[0]
        operand = nutrition_criteria[1]
        value = nutrition_criteria[2]
        query1_nutrition = requests.post(RECIPE_CLUSTER, data=json.dumps({
            "query": {
                "filtered": {
                    "query": {
                        "multi_match": {
                           "query": "{}".format(search_string),
                           "fields": ["title", "steps", "description"]
                            }
                        },
                "filter": {
                    "range": { "{}".format(search_field) : { "{}".format(operand) : value }}
                    }
                }
            }
        }))
        
        query2_nutrition = requests.post(RECIPE_CLUSTER, data=json.dumps({
            "query": {
                "filtered": {
                    "query": {
                        "nested": {
                            "path": "ingredients",
                            "query": {
                                "bool": {
                                    "must": [
                                        { "match": { "ingredients.name": "{}".format(search_string) }} 
                                    ]
                                }
                            }
                        }
                      }
                    ,
                "filter": {
                    "range": { "{}".format(search_field) : { "{}".format(operand) : value }}
                    }
                }
            }
        }))
        for recipe in process_data(query1_nutrition.json()):
            ret.append(recipe)
        for recipe in process_data(query2_nutrition.json()):
            ret.append(recipe)
        return ret
            
    query1 = requests.post(RECIPE_CLUSTER, data=json.dumps({
    "query": {
        "multi_match": {
           "query": "{}".format(search_string),
           "fields": ["title", "steps", "description"]
            }
        }
    }))
    query2 = requests.post(RECIPE_CLUSTER, data=json.dumps({
    "query": {
        "nested": {
            "path": "ingredients",
            "query": {
                "bool": {
                    "must": [
                        { "match": { "ingredients.name": "{}".format(search_string) }} 
                    ]
                }
            }
        }
      }
    }))
    for recipe in process_data(query1.json()):
        ret.append(recipe)
    for recipe in process_data(query2.json()):
        ret.append(recipe)
    return ret

def search_string_nutrition(search_string):
    search_string_token_list = search_string.split()
    nutrition_field =  field_to_be_searched(search_string_token_list)
    if nutrition_field:
        return nutrition_operand_and_value(search_string_token_list, nutrition_field, search_string)
    return None

def field_to_be_searched(token_list):
    searched_field = ""
    searched_field_indx = None
    for indx in range(len(token_list)):
        if token_list[indx] in MASTER_LIST:
            for field in FIELD_LIST:
                if token_list[indx] in field:
                    return (field[0],indx)
    return None
                
def nutrition_operand_and_value(token_list, nutrition_field, search_string):
    searched_field = nutrition_field[0]
    searched_field_indx = nutrition_field[1]
    operand = "gte"
    value = 0
    if token_list[searched_field_indx + 1] == "less":
        operand = "lte"
    value = int(re.search(r'\d+', search_string).group())
    return (searched_field, operand, value)
    
def process_data(data):
    data =  data.get('hits', {'hits': {}}).get('hits', {})
    return [entry.get('_source') for entry in data]

def post_recipe(recipe):
    query1 = requests.post(RECIPE_POST_CLUSTER, data=json.dumps(recipe))
    return query1.text