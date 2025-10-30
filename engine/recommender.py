import json
import os

def load_products():
    " Loading products from JSON file "
    try:
        with open('data/products.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Products file not found!")
        return[]
    
def calculate_product_score(product, user_prefs):
    """
         Calculate how well a product matches user preferences

    """
    score=0

    # Priority-based scoring

    for i, tag in enumerate(user_prefs.get('priority_order', [])):
        if tag in product.get('sustainability_tags' , []):
            # Higher priority tags get more points
            priority_score = (len(user_prefs['priority_order']) - i) * 10
            score += priority_score

    # Buget consideration

    user_budget = user_prefs.get('budget_range' , [0,100])
    product_price = product.get('price', 0)

    if user_budget[0] <= product_price <= user_budget[1]:
        score += 20 # within budget bonus
    elif product_price< user_budget[0]:
        score += 10  # Below budget bonus

    # Deal breaker penalty

    for bad_tag in user_prefs.get('avoid_tags', []):
        if bad_tag in product.get('sustainability_tags', []):
            score = 0  # Complete deal breaker
            break
    
    return score

def recommend_products(user_prefs, products=None, top_n=5):
    """
    Main recommendation function
    """
    if products is None:
        products = load_products()
    
    scored_products = []
    
    for product in products:
        score = calculate_product_score(product, user_prefs)
        if score > 0:  # Only include products that match
            scored_products.append({
                'product': product,
                'score': score
            })
    
    # Sort by score (highest first) and return top N
    scored_products.sort(key=lambda x: x['score'], reverse=True)
    return scored_products[:top_n]

# Example usage for testing
if __name__ == "__main__":
    test_prefs = {
        'priority_order': ['vegan', 'organic', 'fair-trade'],
        'budget_range': [10, 50],
        'avoid_tags': ['animal-testing']
    }
    
    recommendations = recommend_products(test_prefs)
    for rec in recommendations:
        print(f"{rec['product']['name']} - Score: {rec['score']}")


  