import requests

def get_nutritional_data(food_item, api_key):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_item}&api_key={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        return "Error fetching data"

    data = response.json()

    foods = data.get('foods', [])
    if not foods:
        return "No data found for the specified item"

    # Get the first food item from the list
    food_data = foods[0]

    # Print the name of the item
    print("Item Description:", food_data.get('description'))

    nutrients = {
        'Protein': 0,
        'Cholesterol': 0,
        'Energy': 0,
        'Carbohydrate, by difference': 0
    }

    for nutrient in food_data.get('foodNutrients', []):
        nutrient_name = nutrient.get('nutrientName')
        if nutrient_name in nutrients:
            nutrients[nutrient_name] = nutrient.get('value', 0)

    return nutrients


# Usage
api_key = "V7DRp5nywS4bKNSbRdxkWE4niwwYSXJhYDTGY2oZ"


# Print selected nutritional data
