from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import requests
from django.conf import settings
# Create your views here.
def search(request):
    return render(request, 'search.html')

def sm(request):
    return render(request, 'sm.html')

def ingridient_search_sugguestions(request):
    query=request.GET.get('q','').lower()
    
    file_path = os.path.join(settings.BASE_DIR, "recipe_data", "unique_ingridients.json")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Search logic
        results = [item for item in data if query in item["name"].lower()][:10]

        return JsonResponse({"suggestions": results})
        # return JsonResponse([results])
    except FileNotFoundError:
        return JsonResponse({"error": "File not found"}, status=500)


def fetch_recipes(request):
    api_url = "https://api.spoonacular.com/recipes/findByIngredients"
    api_key = "e1567f12699e4d64b65deff4634c8b1b"
    
    # GET request se ingredients lo
    ingredients = request.GET.get("ingredients", "")

    if not ingredients:
        return JsonResponse({"error": "No ingredients provided"}, status=400)

    # API call karo
    params = {
        "ingredients": ingredients,  # Comma-separated ingredients
        "number": 10,                # Max 10 recipes
        "apiKey": api_key            # API key
    }

    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        # **Filtered Data**
        filtered_data = []
        for recipe in data:
            all_ingredients = [
                ing["name"] for ing in recipe.get("usedIngredients", [])
            ] + [
                ing["name"] for ing in recipe.get("missedIngredients", [])
            ]

            filtered_data.append({
                "id": recipe["id"],
                "title": recipe["title"],
                "image": recipe["image"],
                "ingredients": all_ingredients
        })
        # return JsonResponse({"recipes": filtered_data})
        return render(request, "recipeList.html", {"recipes": filtered_data})
    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def recipe_details(request, id):
    api_url = f"https://api.spoonacular.com/recipes/{id}/information"
    api_key = "e1567f12699e4d64b65deff4634c8b1b"

    params = {
        "apiKey": api_key 
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  

        data = response.json()

        # Extract required fields
        recipe_info = {
            "image": data.get("image"),
            "title": data.get("title"),
            "readyInMinutes": data.get("readyInMinutes"),
            "vegetarian": data.get("vegetarian"),
            "servings": data.get("servings"),
            "dishTypes": data.get("dishTypes"),
            "diets": data.get("diets"),
            "summary": data.get("summary"),
            "instructions": [
                {"number": step["number"], "step": step["step"]}
                for instruction in data.get("analyzedInstructions", [])
                for step in instruction.get("steps", [])
            ],
        }

        # return JsonResponse(recipe_info)
        return render(request, "recipe.html", {"recipe": recipe_info})

    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
