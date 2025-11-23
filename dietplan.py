def calculate_bmr(gender, weight, height, age):
    if gender == "male":
        s = 5
    else:
        s = -161
    return (10 * weight) + (6.25 * height) - (5 * age) + s


def calculate_tdee(bmr, activity):
    if activity == "low":
        return bmr * 1.2
    elif activity == "medium":
        return bmr * 1.55
    elif activity == "high":
        return bmr * 1.9
    else:
        return bmr


def adjust_calories(tdee, goal):
    if goal == "shred":
        return tdee - 300
    elif goal == "bulk":
        return tdee + 300
    else:
        return tdee


def get_meal_plan(diet):
    if diet == "veg":
        breakfast = "Oats with milk"
        lunch = "Dal, rice and vegetables"
        snack = "Fruits or nuts"
        dinner = "Paneer with roti"
    else:
        breakfast = "Eggs and toast"
        lunch = "Chicken, rice and vegetables"
        snack = "Fruits or yogurt"
        dinner = "Chicken curry with roti"

    return breakfast, lunch, snack, dinner


def main():
    print("---- DIET PLANNER ----")

    name = input("Enter your name: ")
    gender = input("Gender (male/female): ").lower()
    age = int(input("Age: "))
    height = float(input("Height in cm: "))
    weight = float(input("Weight in kg: "))
    activity = input("Activity level (low/medium/high): ").lower()
    goal = input("Goal (shred/bulk/maintain): ").lower()
    diet = input("Diet type (veg/non-veg): ").lower()

    bmr = calculate_bmr(gender, weight, height, age)
    tdee = calculate_tdee(bmr, activity)
    target_calories = adjust_calories(tdee, goal)

    breakfast, lunch, snack, dinner = get_meal_plan(diet)
    water = weight * 0.035

    print("\n----- RESULT -----")
    print("Name: " + name)
    print("BMR: " + str(round(bmr)))
    print("Daily Calorie Requirement: " + str(round(target_calories)))
    print("\nDaily Meal Plan:")
    print("Breakfast: " + breakfast)
    print("Lunch: " + lunch)
    print("Snack: " + snack)
    print("Dinner: " + dinner)
    print("\nRecommended Water Intake (liters): " + str(round(water, 2)))


main()
