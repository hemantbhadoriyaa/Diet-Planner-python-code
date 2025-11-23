import math
import random
from collections import Counter

ACTIVITY_MULTIPLIERS = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "very_active": 1.725, "athlete": 1.9}
MACRO_SPLITS = {
    "shred": (0.40, 0.20, 0.40), "bulk": (0.30, 0.25, 0.45), "maintain": (0.25, 0.30, 0.45),
    "keto": (0.25, 0.70, 0.05), "low_carb": (0.30, 0.35, 0.35)
}
CALORIES_PER_GRAM = {"protein": 4, "carbs": 4, "fat": 9}
MEAL_NAMES = ["Breakfast", "Lunch", "Snack", "Dinner"]
EXCHANGE_RATES = {"USD": 1.00, "EUR": 1.087, "GBP": 1.266, "INR": 0.012, "CAD": 0.73, "AUD": 0.66}
COUNTRY_REGIONS = {
    "us": ["united states", "canada", "mexico", "brazil"], "in": ["india", "china", "japan", "south korea"],
    "eu": ["united kingdom", "germany", "france", "italy", "spain"], "aud": ["australia", "new zealand"]
}
ALL_COUNTRIES = sorted(list({c for v in COUNTRY_REGIONS.values() for c in v} | {"usa", "uk", "bharat"}))

MEAL_STRUCTURE = {
    "Breakfast": ["primary_protein", "stable_carb", "fruit"], "Lunch": ["primary_protein", "lentil_protein", "stable_carb"],
    "Snack": ["fat_source", "fruit"], "Dinner": ["primary_protein", "stable_carb", "fat_source"],
}

FOOD_DATABASE = {
    "Chicken Breast": {"diet": "non-veg", "size": 100, "p": 31, "f": 4, "c": 0, "cost": 1.50, "regions": ["us", "in", "eu", "ca", "aud"], "food_group": "primary_protein"},
    "Salmon Fillet": {"diet": "non-veg", "size": 100, "p": 20, "f": 13, "c": 0, "cost": 3.00, "regions": ["us", "eu", "ca", "aud"], "food_group": "primary_protein"},
    "Eggs (2 large)": {"diet": "non-veg", "size": 100, "p": 13, "f": 10, "c": 1, "cost": 0.50, "regions": ["us", "in", "eu", "ca", "aud"], "food_group": "primary_protein"},
    "Tofu (firm)": {"diet": "veg", "size": 100, "p": 8, "f": 5, "c": 2, "cost": 0.80, "regions": ["us", "in", "eu", "ca", "aud"], "food_group": "primary_protein"},
    "Paneer": {"diet": "veg", "size": 100, "p": 18, "f": 21, "c": 1, "cost": 1.20, "regions": ["in"], "food_group": "primary_protein"},
    "Greek Yogurt": {"diet": "veg", "size": 150, "p": 15, "f": 4, "c": 10, "cost": 0.70, "regions": ["us", "in", "eu", "ca", "aud"], "food_group": "primary_protein"},
    "Lentils (Cooked Dal)": {"diet": "veg", "size": 100, "p": 9, "f": 0, "c": 20, "cost": 0.15, "regions": ["in", "us", "eu", "ca", "aud"], "food_group": "lentil_protein"},
    "Brown Rice (cooked)": {"diet": "veg", "size": 150, "p": 4, "f": 2, "c": 38, "cost": 0.10, "regions": ["us", "in", "eu", "ca", "aud"], "food_group": "stable_carb"},
    "Roti/Chapati": {"diet": "veg", "size": 40, "p": 4, "f": 1, "c": 19, "cost": 0.05, "regions": ["in"], "food_group": "stable_carb"},
    "Oats (dry)": {"diet": "veg", "size": 40, "p": 5, "f": 3, "c": 27, "cost": 0.20, "regions": ["us", "in", "eu", "ca", "aud"], "food_group": "stable_carb"},
    "Sweet Potato": {"diet": "veg", "size": 150, "p": 2, "f": 0, "c": 30, "cost": 0.30, "regions": ["us", "eu", "ca", "aud"], "food_group": "stable_carb"},
    "Avocado (half)": {"diet": "veg", "size": 100, "p": 2, "f": 15, "c": 9, "cost": 1.00, "regions": ["us", "ca", "aud"], "food_group": "fat_source"},
    "Peanut Butter (1 tbsp)": {"diet": "veg", "size": 16, "p": 4, "f": 8, "c": 3, "cost": 0.25, "regions": ["us", "in", "eu", "ca", "aud"], "food_group": "fat_source"},
    "Apple": {"diet": "veg", "size": 150, "p": 1, "f": 0, "c": 25, "cost": 0.40, "regions": ["us", "in", "eu", "ca", "aud"], "food_group": "fruit"},
    "Banana": {"diet": "veg", "size": 120, "p": 1, "f": 0, "c": 27, "cost": 0.20, "regions": ["us", "in", "eu", "ca", "aud"], "food_group": "fruit"},
}

def calculate_bmr(p):
    W, H, A = p["weight_kg"], p["height_cm"], p["age"]
    S = 5 if p["gender"].lower() == "male" else -161
    return round((10 * W) + (6.25 * H) - (5 * A) + S, 0)

def calculate_tdee(bmr, level):
    return round(bmr * ACTIVITY_MULTIPLIERS.get(level.lower()), 0)

def determine_target_calories(tdee, goal):
    if goal.lower() == "shred":
        return max(tdee - 500, 1200)
    elif goal.lower() == "bulk":
        return tdee + 300
    return tdee

def calculate_macros(cals, goal):
    p_pct, f_pct, c_pct = MACRO_SPLITS.get(goal.lower())
    return {
        "protein": round((cals * p_pct) / CALORIES_PER_GRAM["protein"], 0),
        "fat": round((cals * f_pct) / CALORIES_PER_GRAM["fat"], 0),
        "carbs": round((cals * c_pct) / CALORIES_PER_GRAM["carbs"], 0)
    }

def calculate_water_intake(weight_kg):
    return round((weight_kg * 35) / 1000, 2)

def get_input_string_choice(prompt, allowed_values):
    while True:
        try:
            print("\n-> " + prompt + " (" + ", ".join(allowed_values) + "):")
            choice = raw_input("   Enter value: ").strip().lower()
            if choice in [v.lower() for v in allowed_values]:
                return choice
            else:
                print("   [Error] Invalid input. Please enter one of the options listed.")
        except Exception:
            pass

def get_input_value(prompt, type_func):
    while True:
        try:
            value = raw_input("-> " + prompt + ": ").strip()
            if not value: raise ValueError
            return type_func(value)
        except ValueError: print("   [Error] Invalid input. Enter a valid number.")

def get_country_selection():
    def get_region_code(country):
        country_l = country.lower()
        for code, countries in COUNTRY_REGIONS.items():
            if country_l in countries: return code
        return "us"

    def similarity(s1, s2):
        s1_l, s2_l = s1.lower(), s2.lower()
        if s1_l == s2_l: return 1.0
        return len(set(s1_l) & set(s2_l)) / max(len(s1_l), len(s2_l)) * 0.7

    while True:
        c_in = raw_input("-> Enter your Country (e.g., India, USA): ").strip()
        if c_in.lower() in [c for c in ALL_COUNTRIES]: return c_in.title(), get_region_code(c_in)

        scores = sorted([(similarity(c_in, c), c) for c in ALL_COUNTRIES if similarity(c_in, c) > 0.3], reverse=True)[:4]
        if not scores:
            print("   [Error] Could not find a match for '" + c_in + "'.")
            continue

        print("\n   Did you mean one of these?")
        for i, (_, name) in enumerate(scores, 1): print("   [" + str(i) + "] " + name)

        choice = raw_input("   Select number or press Enter to re-type: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(scores):
                c_name = scores[index][1]
                return c_name, get_region_code(c_name)
        elif choice: print("   [Error] Invalid choice.")

def get_user_profile():
    global raw_input
    try: raw_input
    except NameError: raw_input = input
        
    print("\n" + "="*30 + "\n   DIET PLANNER SETUP\n" + "="*30)
    
    p = {}
    p["gender"] = get_input_string_choice("Gender", ["Male", "Female"])
    p["age"] = get_input_value("Age (years)", int)
    p["height_cm"] = get_input_value("Height (cm)", float)
    p["weight_kg"] = get_input_value("Weight (kg)", float)
    p["activity_level"] = get_input_string_choice("Activity Level", list(ACTIVITY_MULTIPLIERS.keys()))
    p["goal"] = get_input_string_choice("Fitness Goal", list(MACRO_SPLITS.keys()))
    p["dietary_restriction"] = get_input_string_choice("Dietary Preference", ["veg", "non-veg"])
    p["plan_duration"] = get_input_string_choice("Plan Duration", ["day", "week", "month", "year"])
    p["budget_currency"] = get_input_string_choice("Budget Currency", list(EXCHANGE_RATES.keys()))
    p["budget_amount"] = get_input_value("Daily Budget Amount", float)
    p["country"], p["region_code"] = get_country_selection()
    p["health_issues"] = raw_input("-> Chronic Issues (e.g., Diabetes, or 'none'): ").strip()
    p["allergies"] = [a.strip() for a in raw_input("-> Food Allergies (e.g., Peanuts, Dairy, or 'none'): ").strip().split(',') if a.strip().lower() != 'none']
    return p

def filter_foods(p):
    d_filter = p["dietary_restriction"].lower()
    allowed = {}
    
    for name, data in FOOD_DATABASE.items():
        if data.get("diet", "veg").lower() == d_filter or d_filter == "non-veg":
            is_allergic = any(a.lower() in name.lower() for a in p["allergies"])
            if not is_allergic and p["region_code"].lower() in data.get("regions", []):
                allowed[name] = data
    return allowed

def enforce_budget(meal_plan, daily_budget_usd, all_allowed_foods):
    cost = sum(m['cost'] for m in meal_plan)
    
    for _ in range(5):
        if cost <= daily_budget_usd: break
            
        most_exp, target_meal = None, None
        for meal in meal_plan:
            for item in meal['items']:
                if most_exp is None or item['cost'] > most_exp['cost']: most_exp, target_meal = item, meal
        if most_exp is None: break 

        old_name = most_exp['food']
        old_group = all_allowed_foods.get(old_name, {}).get('food_group')
        if not old_group: continue

        subs = sorted([(n, d) for n, d in all_allowed_foods.items() if d.get('food_group') == old_group and d['cost'] < most_exp['cost']], key=lambda x: x[1]['cost'])
        
        if subs:
            n_name, n_data = subs[0]
            for i, item in enumerate(target_meal['items']):
                if item['food'] == old_name:
                    cost += n_data['cost'] - most_exp['cost']
                    target_meal['cost'] += n_data['cost'] - most_exp['cost']
                    target_meal['items'][i] = {"food": n_name, "serving_g": n_data["size"], "protein": n_data["p"], "fat": n_data["f"], "carbs": n_data["c"], "cost": n_data["cost"]}
                    break
        else:
            target_meal['items'] = [i for i in target_meal['items'] if i['food'] != old_name]
            cost -= most_exp['cost']
            target_meal['cost'] -= most_exp['cost']
            
    return cost, meal_plan

def generate_meal_plan(targets, p, budget_usd, freq, mod=1.0):
    all_allowed = filter_foods(p)
    if not all_allowed: return "ERROR: Food options exhausted.", 0.0, set() 

    meal_plan = []; cost = 0.0; used_foods = set()
    
    for label in MEAL_NAMES:
        meal_items = []; m_cost = 0.0
        for group in MEAL_STRUCTURE[label]:
            avail = [(n, d) for n, d in all_allowed.items() if d.get("food_group") == group and n not in used_foods]
            
            if avail:
                avail.sort(key=lambda x: x[1]['cost'])
                weighted = []
                for name, data in avail[:5]:
                    weight = max(1, 5 - freq.get(name, 0))
                    weighted.extend([(name, data)] * weight)

                name, data = random.choice(weighted)
                
                meal_items.append({"food": name, "serving_g": data["size"], "protein": data["p"], "fat": data["f"], "carbs": data["c"], "cost": data["cost"]})
                m_cost += data["cost"]
                used_foods.add(name)

        p_total, f_total, c_total = sum(i['protein'] for i in meal_items), sum(i['fat'] for i in meal_items), sum(i['carbs'] for i in meal_items)
        cals = (p_total * 4) + (c_total * 4) + (f_total * 9)
        
        meal_plan.append({"name": label, "items": meal_items, "cost": m_cost,
                         "totals": {"protein": round(p_total, 1), "fat": round(f_total, 1), "carbs": round(c_total, 1), "calories": round(cals, 0)}})
        cost += m_cost
        
    if cost > budget_usd * 1.10: cost, meal_plan = enforce_budget(meal_plan, budget_usd, all_allowed)
    return meal_plan, cost, used_foods

def generate_full_plan(targets, p):
    days = {"day": 1, "week": 7, "month": 30, "year": 365}.get(p['plan_duration'])
    rate = EXCHANGE_RATES.get(p["budget_currency"], 1.0)
    budget_usd = p["budget_amount"] * rate
    freq = Counter()
    full_plan = []
    
    for day in range(1, days + 1):
        mod = random.uniform(0.95, 1.05)
        plan, cost, foods = generate_meal_plan(targets, p, budget_usd, freq, mod)
        
        err = None
        if isinstance(plan, str): err = plan; plan = []
            
        full_plan.append({"day": day, "plan": plan, "cost": cost, "modifier": mod, "error": err})
        for f in foods: freq[f] += 1
    return full_plan

def display_plan(p, targets, water, full_plan):
    print("\n" + "="*50 + "\n           NUTRITION PLAN REPORT\n" + "="*50)
    
    print("\n--- 1. Metabolic Targets ---")
    print("Goal: %s | Activity: %s" % (p['goal'].upper(), p['activity_level'].title().replace('_', ' ')))
    print("Cals/day: %.0f kcal (BMR: %.0f)" % (targets['cals'], targets['bmr']))
    print("\nDaily Macro Goals:")
    for macro, grams in targets['macros'].items():
        print("  - %s: %.0fg" % (macro.capitalize(), grams))

    print("\n--- 2. Health & Hydration ---")
    print("Min Water: %.2f Liters" % water)
    if p["health_issues"].lower() != 'none' or p["allergies"]:
        print("!! ATTENTION: Check Health Notes Below !!")
        if p["health_issues"].lower() != 'none': print("  - Chronic Issue: " + p['health_issues'].capitalize() + ".")
        if p["allergies"]: print("  - Allergies: " + ', '.join(p['allergies']).capitalize() + ".")
    
    print("\n--- 3. Detailed %s Plan ---" % p['plan_duration'].capitalize())
    
    rate = EXCHANGE_RATES.get(p["budget_currency"])
    currency = p['budget_currency']
    total_cost_usd = 0
    
    for d in full_plan:
        cost = d['cost'] / rate
        total_cost_usd += d['cost']
        
        print("\n--- DAY %d --- (Cost: %.2f %s)" % (d['day'], cost, currency))

        if d.get('error'): print("  Plan Failure: " + d['error']); continue

        if cost > p['budget_amount'] * 1.10: print("  [ALERT] Daily cost exceeds target budget of %.2f %s. Foods substituted." % (p['budget_amount'], currency))
        
        for meal in d['plan']:
            print("\n  " + meal['name'].upper() + ": (Cals: %.0f | P: %.0fg)" % (meal['totals']['calories'], meal['totals']['protein']))
            if meal['items']:
                for item in meal['items']: print("    - %s (%.0fg)" % (item['food'], item['serving_g']))
            else: print("    - No items generated.")
    
    final_cost = total_cost_usd / rate
    print("\n" + "="*50 + "\n           PLAN SUMMARY\n" + "="*50)
    print("Total Plan Cost (%d Days): %.2f %s" % (len(full_plan), final_cost, currency))
    print("Average Daily Cost: %.2f %s" % (final_cost / len(full_plan), currency))
    print("\nNOTE: Consult a professional before major dietary changes.")


def main():
    try:
        profile = get_user_profile()
        
        bmr = calculate_bmr(profile)
        tdee = calculate_tdee(bmr, profile["activity_level"])
        target_cals = determine_target_calories(tdee, profile["goal"])
        target_macros = calculate_macros(target_cals, profile["goal"])

        targets = {"bmr": bmr, "tdee": tdee, "cals": target_cals, "macros": target_macros}
        water_intake = calculate_water_intake(profile["weight_kg"])
        
        full_plan = generate_full_plan(target_macros, profile)
        
        display_plan(profile, targets, water_intake, full_plan)

    except Exception as e:
        print("\n[PROGRAM ERROR] An issue occurred: " + str(e))

if __name__ == "__main__":
    main()
