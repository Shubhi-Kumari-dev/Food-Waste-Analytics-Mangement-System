"""
Recommendations and Insights Engine for Food Waste Reduction.
Extracts empirical findings from the active dataset and generates actionable,
transparent operational recommendations. Also provides Scikit-learn regression
analysis between food preparation and food waste.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

def run_regression_analysis(df):
    """
    Fits a Scikit-Learn Simple Linear Regression model:
    Food_Wasted_Kg = slope * Food_Prepared_Kg + intercept
    Returns: dict of regression metrics and explanation
    """
    if df.empty or 'Food_Prepared_Kg' not in df.columns or 'Food_Wasted_Kg' not in df.columns:
        return None

    clean = df[['Food_Prepared_Kg', 'Food_Wasted_Kg']].dropna()
    if len(clean) < 10:
        return None

    X = clean[['Food_Prepared_Kg']].values
    y = clean['Food_Wasted_Kg'].values

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    slope = float(model.coef_[0])
    intercept = float(model.intercept_)

    # Plain language explanation
    explanation = (
        f"For every additional 10 kg of food prepared, an estimated {slope * 10:.2f} kg is wasted. "
        f"The coefficient of determination (R² = {r2:.3f}) indicates that approximately "
        f"{r2 * 100:.1f}% of the variation in food waste is linearly explained by the quantity of food prepared."
    )

    return {
        'slope': round(slope, 4),
        'intercept': round(intercept, 4),
        'r2_score': round(r2, 4),
        'rmse': round(rmse, 2),
        'explanation': explanation,
        'equation': f"Food_Wasted_Kg = ({slope:.3f} × Food_Prepared_Kg) + ({intercept:.3f})"
    }

def generate_waste_reduction_insights(df):
    """
    Calculates empirical findings and generates data-backed, prioritized kitchen action protocols
    matching the decision-support governance framework.
    Returns: list of structured protocol dicts with priority, operational focus, finding, action, and follow-up.
    """
    insights = []

    if df.empty or 'Food_Wasted_Kg' not in df.columns:
        return insights

    total_wasted = df['Food_Wasted_Kg'].sum()
    total_prep = df['Food_Prepared_Kg'].sum() if 'Food_Prepared_Kg' in df.columns else 0

    # Protocol 1: Priority Food Category Preparation (HIGH)
    if 'Food_Category' in df.columns:
        cat_agg = df.groupby('Food_Category')['Food_Wasted_Kg'].sum().sort_values(ascending=False)
        top_cat = cat_agg.index[0]
        top_cat_waste = cat_agg.iloc[0]
        top_cat_share = (top_cat_waste / total_wasted) * 100 if total_wasted > 0 else 0

        insights.append({
            'title': f"Rationalize Preparation for '{top_cat}'",
            'priority': 'HIGH',
            'icon': '🍲',
            'focus': 'Portion & Batch Sizing',
            'finding': f"'{top_cat}' accounts for the highest physical loss at {top_cat_waste:,.1f} kg ({top_cat_share:.1f}% of total waste in active horizon).",
            'action': f"Adjust morning/midday batch cooking volumes for {top_cat} downward by 10-15% and switch to progressive tiered batch preparation.",
            'followup': f"Track daily leftover log for {top_cat} for the next 14 days."
        })

    # Protocol 2: High Waste Ratio Facility (HIGH)
    if 'Location' in df.columns and 'Food_Prepared_Kg' in df.columns:
        loc_agg = df.groupby('Location').agg({
            'Food_Prepared_Kg': 'sum',
            'Food_Wasted_Kg': 'sum'
        }).reset_index()
        loc_agg['Waste_Pct'] = np.where(
            loc_agg['Food_Prepared_Kg'] > 0,
            (loc_agg['Food_Wasted_Kg'] / loc_agg['Food_Prepared_Kg']) * 100,
            0.0
        )
        loc_agg = loc_agg.sort_values(by='Waste_Pct', ascending=False)
        worst_loc = loc_agg.iloc[0]['Location']
        worst_loc_pct = loc_agg.iloc[0]['Waste_Pct']

        insights.append({
            'title': f"Standardize Serving Portions at '{worst_loc}'",
            'priority': 'HIGH',
            'icon': '🏢',
            'focus': 'Serving & Counter Governance',
            'finding': f"{worst_loc} exhibits the highest waste-to-preparation ratio across all facilities at {worst_loc_pct:.1f}%.",
            'action': f"Introduce standardized portioning ladles and implement plate-scraping audits during high-traffic lunch and dinner sessions.",
            'followup': f"Perform 7-day before-and-after audit comparing waste percentage at {worst_loc}."
        })

    # Protocol 3: Primary Root Cause Mitigation (HIGH / MEDIUM)
    if 'Waste_Cause' in df.columns:
        cause_agg = df.groupby('Waste_Cause')['Food_Wasted_Kg'].sum().sort_values(ascending=False)
        top_cause = cause_agg.index[0]
        top_cause_kg = cause_agg.iloc[0]
        top_cause_share = (top_cause_kg / total_wasted) * 100 if total_wasted > 0 else 0

        action_map = {
            'Plate Waste': "Plate waste is dominant. Review diner tray habits, reduce default grain scoop sizes by 15%, and offer free second helpings instead of large initial plates.",
            'Over-preparation': "Over-preparation is dominant. Align headcounts strictly with historical attendance trends and freeze buffer cooking at 5% instead of 15%.",
            'Spoilage': "Spoilage is dominant. Improve cold storage temperature logging (+2°C to +4°C) and enforce strict First-In, First-Out (FIFO) inventory controls.",
            'Kitchen Trimmings': "Kitchen trimmings are elevated. Train culinary staff on high-yield vegetable carving and repurpose edible trimmings into soup stocks.",
            'Expired Ingredients': "Expired ingredients detected. Lower bulk purchase delivery quantities and implement high-visibility color-coded date tags.",
            'Poor Storage': "Storage degradation detected. Inspect dry-pantry sealing, humidity controls, and cold-room evaporator air circulation."
        }

        insights.append({
            'title': f"Mitigate Root Cause: '{top_cause}'",
            'priority': 'HIGH' if top_cause_share > 30 else 'MEDIUM',
            'icon': '⚠️',
            'focus': 'Operational Workflow Mitigation',
            'finding': f"'{top_cause}' is responsible for {top_cause_kg:,.1f} kg ({top_cause_share:.1f}% of total waste generated).",
            'action': action_map.get(top_cause, "Implement targeted operational waste reduction protocols."),
            'followup': f"Review weekly incident tags and confirm downward reduction in '{top_cause}' logs."
        })

    # Protocol 4: Inventory FIFO & Pantry Rotation (MEDIUM)
    insights.append({
        'title': "Enforce FIFO Inventory & Pantry Shelf Life Controls",
        'priority': 'MEDIUM',
        'icon': '📦',
        'focus': 'Pantry & Storage Management',
        'finding': "Pre-preparation spoilage and batch shelf aging contribute directly to avoidable raw ingredient disposal.",
        'action': "Implement digital FIFO color tags on bulk dry and cold stock bins; mandate daily end-of-shift walk-throughs by head cook.",
        'followup': "Conduct weekly inventory turnover audit and check expiry risk log."
    })

    # Protocol 5: Surplus Repurposing & Cold-Holding (MEDIUM)
    insights.append({
        'title': "Establish Safe Surplus Preservation & Recovery Channel",
        'priority': 'MEDIUM',
        'icon': '🍱',
        'focus': 'Surplus Recovery & Community Logistics',
        'finding': "Consistently safe, unserved buffet surplus can be preserved before plate contamination.",
        'action': "Establish a rapid chilling protocol (+4°C) for unserved kitchen surplus and partner with campus community shelters for timely distribution.",
        'followup': "Track daily kilograms of safe food rescued versus sent to disposal in the kitchen entry log."
    })

    # Protocol 6: Outlier Anomaly Detection & Holiday Adjustment (LOW)
    if 'Date' in df.columns:
        daily_waste = df.groupby('Date')['Food_Wasted_Kg'].sum()
        if len(daily_waste) > 7:
            mean_waste = daily_waste.mean()
            std_waste = daily_waste.std()
            spike_threshold = mean_waste + (1.96 * std_waste)
            spike_days = daily_waste[daily_waste > spike_threshold]
            num_spikes = len(spike_days)
            spike_text = f"Observed {num_spikes} statistical anomaly day(s) exceeding normal operational variation (+2σ)."
        else:
            spike_text = "Weekend and academic schedule transitions historically introduce high volatility in dining counts."

        insights.append({
            'title': "Calibrate Weekend & Holiday Headcount Forecasts",
            'priority': 'LOW',
            'icon': '📅',
            'focus': 'Headcount Forecasting & Event Calibration',
            'finding': spike_text,
            'action': "Integrate hostel leave registers and academic exam calendars into daily kitchen prep requisitions 48 hours in advance.",
            'followup': "Compare weekend actual diner turnout against forecasted kitchen prep requisitions."
        })

    return insights

def simulate_waste_reduction(df, prep_reduction_pct=10, plate_reduction_pct=15, cost_per_kg=65.0):
    """
    What-If Simulation Model for Kitchen Management:
    Computes projected kilograms, financial savings, meals rescued, and CO2 emissions
    prevented when targeted operational waste reductions are applied.
    """
    if df.empty or 'Food_Wasted_Kg' not in df.columns:
        return None

    total_wasted = df['Food_Wasted_Kg'].sum()
    total_prep = df['Food_Prepared_Kg'].sum() if 'Food_Prepared_Kg' in df.columns else 0.0

    # Over-preparation subset
    if 'Waste_Cause' in df.columns:
        overprep_waste = df[df['Waste_Cause'] == 'Over-preparation']['Food_Wasted_Kg'].sum()
        plate_waste = df[df['Waste_Cause'] == 'Plate Waste']['Food_Wasted_Kg'].sum()
    else:
        overprep_waste = total_wasted * 0.35
        plate_waste = total_wasted * 0.40

    prep_saved = overprep_waste * (prep_reduction_pct / 100.0)
    plate_saved = plate_waste * (plate_reduction_pct / 100.0)
    total_saved_kg = prep_saved + plate_saved

    cost_saved = total_saved_kg * cost_per_kg
    co2_prevented = total_saved_kg * 2.5
    meals_rescued = int(total_saved_kg / 0.4) if total_saved_kg > 0 else 0

    new_waste_kg = max(0.0, total_wasted - total_saved_kg)
    new_waste_pct = (new_waste_kg / total_prep * 100.0) if total_prep > 0 else 0.0
    current_waste_pct = (total_wasted / total_prep * 100.0) if total_prep > 0 else 0.0

    return {
        'total_saved_kg': round(total_saved_kg, 1),
        'cost_saved': round(cost_saved, 0),
        'co2_prevented_kg': round(co2_prevented, 1),
        'meals_rescued': meals_rescued,
        'new_waste_kg': round(new_waste_kg, 1),
        'new_waste_pct': round(new_waste_pct, 1),
        'current_waste_pct': round(current_waste_pct, 1),
        'pct_improvement': round(current_waste_pct - new_waste_pct, 1)
    }
