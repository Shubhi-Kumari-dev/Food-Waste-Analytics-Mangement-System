"""
Script to generate a realistic sample dataset for the Food Waste Analytics and Management System.
Creates approximately 400 records across multiple locations, meal types, and categories.
Ensures internal consistency:
- Food_Prepared_Kg >= Food_Served_Kg >= Food_Wasted_Kg >= 0
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_food_waste_dataset(num_records=420, output_path="data/food_waste_sample.csv"):
    np.random.seed(42)  # For reproducibility

    # Define realistic categorical values
    categories = ['Rice', 'Vegetables', 'Bread', 'Dairy', 'Fruits', 'Meat', 'Other']
    category_weights = [0.22, 0.20, 0.16, 0.12, 0.12, 0.10, 0.08]

    locations = ['Hostel', 'Canteen', 'Restaurant', 'Catering']
    location_weights = [0.35, 0.30, 0.20, 0.15]

    meal_types = ['Breakfast', 'Lunch', 'Dinner']
    meal_weights = [0.25, 0.45, 0.30]

    waste_causes = [
        'Plate Waste',
        'Over-preparation',
        'Spoilage',
        'Kitchen Trimmings',
        'Expired Ingredients',
        'Poor Storage'
    ]
    waste_cause_weights = [0.35, 0.25, 0.15, 0.10, 0.08, 0.07]

    # Date range: 140 days starting from 2026-01-01
    start_date = datetime(2026, 1, 1)
    
    records = []
    
    for i in range(num_records):
        # Pick date (roughly 2-4 records per day across locations)
        day_offset = int(i * (140 / num_records))
        record_date = (start_date + timedelta(days=day_offset)).strftime('%Y-%m-%d')
        
        category = np.random.choice(categories, p=category_weights)
        location = np.random.choice(locations, p=location_weights)
        meal = np.random.choice(meal_types, p=meal_weights)
        cause = np.random.choice(waste_causes, p=waste_cause_weights)
        
        # Scale quantities based on location & meal
        if location == 'Hostel':
            base_prep = np.random.uniform(50, 140)
        elif location == 'Canteen':
            base_prep = np.random.uniform(40, 110)
        elif location == 'Restaurant':
            base_prep = np.random.uniform(25, 75)
        else:  # Catering
            base_prep = np.random.uniform(60, 160)
            
        if meal == 'Lunch':
            base_prep *= 1.25
        elif meal == 'Breakfast':
            base_prep *= 0.75
            
        # Food prepared rounded to 1 decimal place
        food_prepared = round(base_prep, 1)
        
        # Food served: 80% to 98% of prepared food
        served_ratio = np.random.uniform(0.80, 0.98)
        food_served = round(food_prepared * served_ratio, 1)
        
        # Food wasted: 6% to 28% of food served, with slight weekly/category variations
        waste_ratio = np.random.uniform(0.06, 0.28)
        
        # Certain categories produce more waste (e.g., Rice, Vegetables, Bread)
        if category in ['Rice', 'Bread']:
            waste_ratio *= 1.15
        elif category in ['Meat', 'Dairy']:
            waste_ratio *= 0.85
            
        # Ensure waste ratio doesn't exceed served food
        waste_ratio = min(waste_ratio, 0.40)
        food_wasted = round(food_served * waste_ratio, 1)
        
        # Absolute safety check: Prepared >= Served >= Wasted >= 0
        if food_served > food_prepared:
            food_served = food_prepared
        if food_wasted > food_served:
            food_wasted = food_served

        records.append({
            'Date': record_date,
            'Food_Category': category,
            'Location': location,
            'Meal_Type': meal,
            'Food_Prepared_Kg': food_prepared,
            'Food_Served_Kg': food_served,
            'Food_Wasted_Kg': food_wasted,
            'Waste_Cause': cause
        })

    df = pd.DataFrame(records)
    
    # Ensure destination directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} sample records saved to: {output_path}")
    return df

if __name__ == '__main__':
    generate_food_waste_dataset()
