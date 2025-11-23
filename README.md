Diet Planner – Python Project

This project is a command-line based Diet Planner written in Python. It creates a personalized daily, weekly, or monthly meal plan based on user details such as age, gender, activity level, fitness goal, dietary preference, and even allergies or health issues.
The program also calculates daily calories, macronutrient requirements, and water intake.

 Features

Calculates BMR and TDEE using Mifflin–St Jeor equation

Supports goals: Shred, Bulk, and Maintain

Macronutrient distribution based on selected goal

Generates daily/weekly/monthly meal plans

Avoids food repetition by tracking frequency

Meal distribution across: Breakfast, Lunch, Snack, Dinner

Handles vegetarian and non-vegetarian preferences

Considers health issues and allergies (informational output)

Clean input validation for all user entries

 How the Meal Plan Works

The script uses a built-in food database containing protein, fat, carb, and calorie breakdown for each food item.
Foods are grouped into categories like protein, carb, fat, and fruit.

Each meal (Breakfast, Lunch, Snack, Dinner) expects certain food groups. Example:

Breakfast: protein + carb + fruit

Lunch: protein + carb

Snack: fat + fruit

Dinner: protein + carb + fat

The program:

Identifies all foods allowed based on user’s dietary preference

Weighs food choices based on how often they were used recently

Randomly selects balanced meals with slight day-to-day variation

Ensures variety across the plan

 Calculations Performed
1. Basal Metabolic Rate (BMR)

Uses Mifflin-St Jeor formula:

BMR = 10*weight + 6.25*height – 5*age + S
S = +5 for male, -161 for female

2. Total Daily Energy Expenditure (TDEE)
TDEE = BMR × Activity Factor


Activity factors include sedentary, light, moderate, very_active, athlete.

3. Goal-Adjusted Calories

Shred: TDEE – 500

Bulk: TDEE + 300

Maintain: TDEE

4. Macro Breakdown

Ratios depend on the selected fitness goal:

Protein

Fat

Carbs
Each converted into grams per day.

5. Water Intake
35 ml × body weight (kg)

 Project Structure
diet_planner/
│
├── diet_planner.py      # main script
└── README.md            # documentation

 Requirements

Only built-in Python libraries are used:

math

random

collections.Counter

No external installation is required.

Running the Program

Run the script normally in a terminal:

python diet_planner.py

User Inputs Collected

The program will ask for:

Gender

Age

Height (cm)

Weight (kg)

Activity level

Fitness goal

Diet preference (veg / non-veg)

Plan duration (day / week / month)

Health issues (optional)

Allergies (optional)

 Example Output (Shortened)
--------------------------------------------------
           PLAN FOR 7 DAYS
--------------------------------------------------

--- DAY 1 ---
BREAKFAST: (Cals: 320 | P: 20g)
 - Oats (40g)
 - Paneer (100g)
 - Apple (150g)

LUNCH: (Cals: 410 | P: 35g)
 - Chicken Breast (100g)
 - Brown Rice (150g)

...

Min Water Intake: 2.45 Liters
HEALTH NOTE: diabetes
ALLERGIES: peanuts
--------------------------------------------------

 Possible Improvements

Future upgrades could include:

Adding more foods to the database

Exporting plans as PDF/CSV

GUI using Tkinter

Tracking user progress

Nutrition API integration

 Author

Hemant Singh Bhadoriya
