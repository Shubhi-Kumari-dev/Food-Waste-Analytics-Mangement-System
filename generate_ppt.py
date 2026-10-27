import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path="Food_Waste_Analytics_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Culinary Bistro Colors
    CLR_DARK_BG = RGBColor(20, 16, 13)       # #14100D Espresso
    CLR_LIGHT_BG = RGBColor(253, 251, 247)   # #FDFBF7 Soft Warm Cream
    CLR_CARD_BG = RGBColor(255, 255, 255)    # #FFFFFF Pure Card White
    CLR_CARD_BORDER = RGBColor(235, 221, 207)# #EBDDCF Muted Border
    CLR_TEXT_MAIN = RGBColor(42, 27, 16)     # #2A1B10 Deep Charcoal Roast
    CLR_TEXT_MUTED = RGBColor(107, 87, 70)   # #6B5746 Warm Grayish Brown
    CLR_TEXT_LIGHT = RGBColor(253, 245, 237) # #FDF5ED Ivory for dark slides
    CLR_TEXT_LIGHT_MUTED = RGBColor(191, 175, 162) # #BFAFA2
    CLR_SAFFRON = RGBColor(234, 88, 12)      # #EA580C Saffron Accent
    CLR_AMBER = RGBColor(217, 119, 6)        # #D97706 Warm Amber
    CLR_TERRACOTTA = RGBColor(124, 45, 18)   # #7C2D12 Deep Terracotta
    CLR_TAG_BG = RGBColor(255, 247, 237)     # #FFF7ED
    CLR_TAG_BORDER = RGBColor(254, 215, 170) # #FED7AA
    CLR_HIGH = RGBColor(220, 38, 38)         # #DC2626 Crimson

    def add_light_header(slide, tag_text, title_text, sub_text):
        ribbon = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
        ribbon.fill.solid()
        ribbon.fill.fore_color.rgb = CLR_SAFFRON
        ribbon.line.fill.background()

        tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(3.8), Inches(0.32))
        tag_box.fill.solid()
        tag_box.fill.fore_color.rgb = CLR_TAG_BG
        tag_box.line.color.rgb = CLR_TAG_BORDER
        tag_box.line.width = Pt(1)
        tf = tag_box.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.03)
        tf.margin_bottom = Inches(0.03)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = tag_text.upper()
        r.font.size = Pt(9)
        r.font.bold = True
        r.font.color.rgb = CLR_SAFFRON

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title_text
        r.font.size = Pt(21)
        r.font.bold = True
        r.font.color.rgb = CLR_TEXT_MAIN

        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.4))
        tf = sub_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = sub_text
        r.font.size = Pt(10.5)
        r.font.color.rgb = CLR_TEXT_MUTED

    def add_light_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = CLR_LIGHT_BG
        bg.line.fill.background()

    def add_card(slide, x, y, w, h, top_color=None):
        c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        c.fill.solid()
        c.fill.fore_color.rgb = CLR_CARD_BG
        c.line.color.rgb = CLR_CARD_BORDER
        c.line.width = Pt(1)
        if top_color:
            rib = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Inches(0.08))
            rib.fill.solid()
            rib.fill.fore_color.rgb = top_color
            rib.line.fill.background()
        return c

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = CLR_DARK_BG
    bg1.line.fill.background()

    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = CLR_SAFFRON
    bar1.line.fill.background()

    c1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    c1.fill.solid()
    c1.fill.fore_color.rgb = RGBColor(27, 21, 17)
    c1.line.color.rgb = RGBColor(61, 45, 34)
    c1.line.width = Pt(1.5)

    pill1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(1.5), Inches(4.8), Inches(0.38))
    pill1.fill.solid()
    pill1.fill.fore_color.rgb = RGBColor(44, 32, 24)
    pill1.line.color.rgb = CLR_SAFFRON
    p = pill1.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "✦ DATA ANALYTICS & VISUALIZATION (DAV) LAB PROJECT"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = CLR_SAFFRON

    tb = s1.shapes.add_textbox(Inches(1.8), Inches(2.1), Inches(9.8), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "Food Waste Analytics &\nManagement System"
    r.font.size = Pt(36)
    r.font.bold = True
    r.font.color.rgb = CLR_TEXT_LIGHT

    tb = s1.shapes.add_textbox(Inches(1.8), Inches(3.6), Inches(9.8), Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "Operational Intelligence, Econometric Forecasting & Menu Optimization for Large-Scale Dining Facilities"
    r.font.size = Pt(13.5)
    r.font.color.rgb = CLR_TEXT_LIGHT_MUTED

    meta_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(4.5), Inches(9.7), Inches(1.5))
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = RGBColor(34, 26, 21)
    meta_box.line.color.rgb = RGBColor(61, 45, 34)
    tf = meta_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "Project Domain: Data Analytics & Computational Sustainability\n"
    r.font.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = CLR_SAFFRON
    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = "• Technology Stack: Python, Streamlit, Plotly, Pandas, NumPy, Scikit-Learn, Statsmodels (ARIMA), SQLite\n• Evaluation Criteria: EDA, Outlier Profiling, Time-Series Smoothing, Regression Modeling & Decision Support\n• Presenter: [Student Name / Group Members] | Department of Computer Science & Engineering"
    r2.font.size = Pt(10)
    r2.font.color.rgb = CLR_TEXT_LIGHT_MUTED

    # =========================================================================
    # SLIDE 2: 1. INTRODUCTION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_light_bg(s2)
    add_light_header(s2, "Section 1", "1. Introduction", "Context, background, and the critical need for food waste analytics in dining facilities.")

    s2_cards = [
        ("Global & Institutional Context", CLR_SAFFRON, [
            ("Magnitude of Food Loss", "According to the UN UNEP Food Waste Index, approximately 1.05 billion tonnes of food is wasted globally each year, with institutional food services contributing over 26%."),
            ("Campus & Canteen Footprint", "Institutional dining halls (hostel messes, university canteens, corporate cafeterias) handle hundreds of kilograms of perishable inventory daily with high variance."),
            ("Triple Bottom Line Impact", "Food waste represents a severe economic drain, high greenhouse gas emissions (methane and CO₂), and discarded edible meals.")
        ]),
        ("The Role of Data Analytics", CLR_AMBER, [
            ("Transition from Guesswork", "Traditional kitchen planning relies on subjective estimations, leading to chronic over-preparation to prevent stockouts."),
            ("Data as an Operational Asset", "By tracking meal-by-meal prepared vs served volumes, facilities can identify hidden inefficiencies, cyclical patterns, and food category vulnerabilities."),
            ("Modern Visual Intelligence", "Interactive analytics platforms empower kitchen supervisors with actionable diagnostic metrics rather than static retrospective logs.")
        ]),
        ("Project Motivation & Scope", CLR_TERRACOTTA, [
            ("Core Focus", "Developing an end-to-end analytics dashboard covering data ingestion, statistical profiling, time-series forecasting, and simulation."),
            ("Multi-Facility Tracking", "Benchmarking across Hostel Mess, Central Canteen, Faculty Restaurant, and Event Catering over a 6-month timeline."),
            ("Closing the Loop", "Moving beyond passive reporting into algorithmic, prioritized kitchen action recommendations.")
        ])
    ]
    l3 = [Inches(0.8), Inches(4.8), Inches(8.8)]
    for i, (title, col, bullets) in enumerate(s2_cards):
        add_card(s2, l3[i], Inches(1.95), Inches(3.7), Inches(5.1), col)
        tb = s2.shapes.add_textbox(l3[i] + Inches(0.2), Inches(2.15), Inches(3.3), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = CLR_TEXT_MAIN
        for h, b in bullets:
            p2 = tf.add_paragraph()
            p2.space_before = Pt(8)
            r2 = p2.add_run()
            r2.text = f"• {h}: "
            r2.font.bold = True
            r2.font.size = Pt(10)
            r2.font.color.rgb = col
            r3 = p2.add_run()
            r3.text = b
            r3.font.size = Pt(9.5)
            r3.font.color.rgb = CLR_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: 2. PROBLEM STATEMENT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_light_bg(s3)
    add_light_header(s3, "Section 2", "2. Problem Statement", "Core operational vulnerabilities, financial drains, and ecological challenges in dining facilities.")

    s3_cards = [
        ("Operational Blindspots & Volatility", CLR_HIGH, [
            ("Diner Headcount Fluctuations", "Student and diner attendance varies wildly due to exam schedules, weekend leave, festivals, and weather, causing massive forecast errors."),
            ("Fixed Batch-Cooking Mandates", "Chefs cook in large, uncalibrated batch sizes (e.g. 50–100 kg pots) without real-time attendance signals, guaranteeing leftover surplus."),
            ("Lack of Feedback Mechanism", "Waste data is rarely logged or analyzed systematically, leaving kitchen supervisors blind to recurring structural failure points.")
        ]),
        ("Severe Economic & Environmental Drain", CLR_SAFFRON, [
            ("Direct Financial Losses", "Commercial dining incurs ₹45–₹80 per kg in unrecoverable raw ingredient expenditure, leading to lakhs in preventable recurring losses."),
            ("Carbon & Ecological Footprint", "Every kg of discarded food produces approximately 2.5 kg CO₂e in greenhouse gas emissions during decomposition in landfills."),
            ("Social Inefficiency", "Nutritious, edible meals are discarded while campus sustainability targets and social food redistribution goals remain unmet.")
        ]),
        ("The Analytical Problem to Solve", CLR_TERRACOTTA, [
            ("Over-Preparation Sensitivity", "How does preparation volume mathematically correlate with waste volume, and where is the critical tipping point?"),
            ("Temporal Dependency", "Can multi-week trend smoothing and 7-day cyclical seasonal patterns accurately forecast demand 14 days in advance?"),
            ("Actionability Gap", "How can predictive insights be translated into simple, automated operational protocols for non-technical kitchen staff?")
        ])
    ]
    for i, (title, col, bullets) in enumerate(s3_cards):
        add_card(s3, l3[i], Inches(1.95), Inches(3.7), Inches(5.1), col)
        tb = s3.shapes.add_textbox(l3[i] + Inches(0.2), Inches(2.15), Inches(3.3), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = CLR_TEXT_MAIN
        for h, b in bullets:
            p2 = tf.add_paragraph()
            p2.space_before = Pt(8)
            r2 = p2.add_run()
            r2.text = f"• {h}: "
            r2.font.bold = True
            r2.font.size = Pt(10)
            r2.font.color.rgb = col
            r3 = p2.add_run()
            r3.text = b
            r3.font.size = Pt(9.5)
            r3.font.color.rgb = CLR_TEXT_MUTED

    # =========================================================================
    # SLIDE 4: 3. OBJECTIVES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_light_bg(s4)
    add_light_header(s4, "Section 3", "3. Project Objectives", "Strategic, analytical, and practical milestones of the Food Waste Management System.")

    s4_cards = [
        ("Primary Analytical Goals", CLR_SAFFRON, [
            ("1. Multi-Dimensional EDA", "Perform comprehensive exploratory data analysis across food categories, dining facilities, meal types, and root causes of loss."),
            ("2. Statistical Outlier Profiling", "Deploy Interquartile Range (IQR) boundary checks to detect and profile operational anomaly days exceeding +2σ variation."),
            ("3. Econometric Time-Series Analysis", "Implement 7-day Moving Averages, Exponential Smoothing (EWMA), Seasonal Decomposition, and ARIMA(1,1,1) for predictive demand forecasting.")
        ]),
        ("Computational & ML Objectives", CLR_AMBER, [
            ("4. Regression Sensitivity Modeling", "Formulate Scikit-Learn linear regression models to determine the mathematical relationship between food prepared and food wasted."),
            ("5. Interactive What-If Simulator", "Develop a real-time scenario simulation engine enabling managers to model 0–50% prep and plate reduction targets."),
            ("6. Quantified Impact Tracking", "Automatically compute projected food rescued (kg), cost savings (INR), meals preserved, and carbon abatement (kg CO₂e).")
        ]),
        ("Operational & UI Deliverables", CLR_TERRACOTTA, [
            ("7. Decision Support Protocol Engine", "Dynamically generate priority-ranked operational protocols (High, Medium, Low) with empirical findings, actions, and verification steps."),
            ("8. Executive Streamlit Command Hub", "Engineer an intuitive, aesthetic web interface supporting Light/Dark themes, structured card boxes, and zero-clutter navigation."),
            ("9. Live SQLite Data Logging", "Provide an operational terminal for staff to append new daily meal observations and export filtered audit records to CSV.")
        ])
    ]
    for i, (title, col, bullets) in enumerate(s4_cards):
        add_card(s4, l3[i], Inches(1.95), Inches(3.7), Inches(5.1), col)
        tb = s4.shapes.add_textbox(l3[i] + Inches(0.2), Inches(2.15), Inches(3.3), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = CLR_TEXT_MAIN
        for h, b in bullets:
            p2 = tf.add_paragraph()
            p2.space_before = Pt(8)
            r2 = p2.add_run()
            r2.text = f"{h}: "
            r2.font.bold = True
            r2.font.size = Pt(10)
            r2.font.color.rgb = col
            r3 = p2.add_run()
            r3.text = b
            r3.font.size = Pt(9.5)
            r3.font.color.rgb = CLR_TEXT_MUTED

    # =========================================================================
    # SLIDE 5: 4. EXISTING SYSTEM & ITS LIMITATIONS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_light_bg(s5)
    add_light_header(s5, "Section 4", "4. Existing System & Its Limitations", "Comparison between traditional kitchen recordkeeping and modern requirements.")

    # 2 Comparison Columns
    add_card(s5, Inches(0.8), Inches(1.95), Inches(5.6), Inches(5.1), CLR_HIGH)
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.15), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "📋 Characteristics of Existing System"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = CLR_HIGH

    ex_points = [
        ("Manual Paper Registers", "Daily kitchen logs are hand-written by supervisors, prone to missing entries, illegible data, and physical loss."),
        ("Static Retrospective Spreadsheets", "Where Excel is used, it functions merely as a passive historical archive without live dynamic dashboards or visual analysis."),
        ("Subjective Rule-of-Thumb Cooking", "Preparation volume is dictated entirely by chef intuition, causing persistent 15–25% buffer over-preparation."),
        ("No Demand Forecasting", "Zero capability to forecast upcoming week consumption or model cyclical weekend/holiday drop-offs."),
        ("Siloed Operations", "Hostels, canteens, and catering services operate independently with no standardized metrics or shared benchmarking.")
    ]
    for k, v in ex_points:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {k}: "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = CLR_HIGH
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(10)
        r2.font.color.rgb = CLR_TEXT_MUTED

    add_card(s5, Inches(6.9), Inches(1.95), Inches(5.6), Inches(5.1), CLR_TERRACOTTA)
    tb = s5.shapes.add_textbox(Inches(7.2), Inches(2.15), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "⚠️ Operational & Business Limitations"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = CLR_TERRACOTTA

    lim_points = [
        ("High Latency & Inaction", "Data is reviewed weeks later at billing time, making real-time intervention and immediate food rescue impossible."),
        ("Absence of Root Cause Attribution", "Fails to distinguish whether loss stems from kitchen over-prep, dining plate discards, or cold-chain spoilage."),
        ("Uncontrolled Financial Drain", "Facilities lose ₹4 Lakhs+ annually per kitchen without visibility into specific high-waste categories like Rice and Bread."),
        ("No Scenario Testing", "Supervisors cannot answer: 'What happens if we reduce batch sizes by 15%?' before taking operational risks."),
        ("Compliance & Audit Gaps", "Inability to generate instant verifiable waste reduction reports for campus governance or sustainability audits.")
    ]
    for k, v in lim_points:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {k}: "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = CLR_TERRACOTTA
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(10)
        r2.font.color.rgb = CLR_TEXT_MUTED

    # =========================================================================
    # SLIDE 6: 5. PROPOSED SYSTEM
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_light_bg(s6)
    add_light_header(s6, "Section 5", "5. Proposed System: Food Sense Analytics", "A modern, intelligent, end-to-end food waste analytics and governance platform.")

    s6_cards = [
        ("Real-Time Analytics & Validation", CLR_SAFFRON, [
            ("Mass Conservation Enforcement", "Automated physical validation (`Food_Prepared = Food_Served + Food_Wasted`) ensures 100% data integrity."),
            ("Interactive Multi-Facility Filters", "Dynamic sidebar controls allow filtering by Facility, Food Category, Meal Type, and Date Horizon."),
            ("Executive KPI Deck", "Live tracking of Total Waste (kg), Waste Rate (%), Financial Loss (INR), Rescued Meals, and Carbon Footprint (CO₂e).")
        ]),
        ("Econometric & Machine Learning Engine", CLR_AMBER, [
            ("Time-Series Trend Smoothing", "7-Day Moving Averages and Exponential Smoothing (EWMA, alpha=0.30) filter daily attendance noise."),
            ("7-Day Seasonal Decomposition", "Isolates systemic weekly cycles to predict weekend drop-offs and mid-week attendance peaks."),
            ("ARIMA(1,1,1) Forward Forecasts", "Projects 14-day waste trajectories with 95% statistical confidence intervals for inventory requisitioning."),
            ("Scikit-Learn Regression", "Quantifies empirical sensitivity: every 100 kg cooked yields ~15.2 kg waste (r = 0.689, R² = 0.474).")
        ]),
        ("Decision Support & Simulation", CLR_TERRACOTTA, [
            ("Interactive What-If Simulator", "Enables supervisors to slide prep-cut and plate-cut targets and simulate food rescued, cost saved, and new waste rates."),
            ("Data-Backed Kitchen Recommendations", "Translates anomalies into 6 prioritized operational protocols with clear actions and verification checkpoints."),
            ("Structured Culinary Bistro UI", "Modern card-boxed visualization widgets, dark/light themes, zero 'undefined' text artifacts, and live SQLite terminal.")
        ])
    ]
    for i, (title, col, bullets) in enumerate(s6_cards):
        add_card(s6, l3[i], Inches(1.95), Inches(3.7), Inches(5.1), col)
        tb = s6.shapes.add_textbox(l3[i] + Inches(0.2), Inches(2.15), Inches(3.3), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = CLR_TEXT_MAIN
        for h, b in bullets:
            p2 = tf.add_paragraph()
            p2.space_before = Pt(8)
            r2 = p2.add_run()
            r2.text = f"• {h}: "
            r2.font.bold = True
            r2.font.size = Pt(10)
            r2.font.color.rgb = col
            r3 = p2.add_run()
            r3.text = b
            r3.font.size = Pt(9.5)
            r3.font.color.rgb = CLR_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: 6. SYSTEM ARCHITECTURE / BLOCK DIAGRAM
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_light_bg(s7)
    add_light_header(s7, "Section 6", "6. System Architecture & Block Diagram", "Four-tier architectural pipeline from data persistence to executive decision support.")

    pipe_4 = [
        ("Layer 1: Data Storage & Ingestion", CLR_TERRACOTTA, [
            "SQLite Database Engine (`kitchen_waste.db`)",
            "CSV Log Parser & Dataset Generator",
            "420 Verified Baseline Meal Observations",
            "Real-Time Kitchen Entry Form"
        ]),
        ("Layer 2: Preprocessing & Validation", CLR_SAFFRON, [
            "Conservation of Mass Guardrails",
            "Automated Null & Type Handling",
            "IQR Anomaly Profiler (1.5*IQR threshold)",
            "Multi-Facility Dynamic Slicing & Resampling"
        ]),
        ("Layer 3: Analytical & ML Engine", CLR_AMBER, [
            "Seaborn/Plotly Pearson Heatmaps",
            "Moving Average & EWMA Smoothing",
            "Additive Seasonal Decomposition",
            "ARIMA(p,d,q) 14-Day Predictor",
            "Scikit-Learn OLS Linear Regression"
        ]),
        ("Layer 4: UI & Decision Support", CLR_HIGH, [
            "Streamlit Responsive Web Application",
            "Executive Hub with Boxed Chart Cards",
            "Interactive 'What-If' Scenario Simulator",
            "6 Prioritized Kitchen Action Protocols",
            "Light & Dark Bistro Culinary Themes"
        ])
    ]
    p4_lefts = [Inches(0.8), Inches(3.8), Inches(6.8), Inches(9.8)]
    for i, (title, col, items) in enumerate(pipe_4):
        add_card(s7, p4_lefts[i], Inches(1.95), Inches(2.75), Inches(5.1), col)
        sh = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p4_lefts[i] + Inches(0.12), Inches(2.1), Inches(2.5), Inches(0.48))
        sh.fill.solid()
        sh.fill.fore_color.rgb = col
        sh.line.fill.background()
        p = sh.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = title
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

        tb = s7.shapes.add_textbox(p4_lefts[i] + Inches(0.18), Inches(2.75), Inches(2.4), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        for idx, item in enumerate(items):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_before = Pt(12)
            r = p.add_run()
            r.text = f"✔ {item}"
            r.font.size = Pt(10)
            r.font.color.rgb = CLR_TEXT_MAIN

    # =========================================================================
    # SLIDE 8: 7. TECHNOLOGIES USED (HARDWARE & SOFTWARE)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_light_bg(s8)
    add_light_header(s8, "Section 7", "7. Technologies Used (Hardware & Software)", "Specifications of the development and production deployment environment.")

    # 2 Big Cards: Software Stack and Hardware/Libraries
    add_card(s8, Inches(0.8), Inches(1.95), Inches(5.6), Inches(5.1), CLR_SAFFRON)
    tb = s8.shapes.add_textbox(Inches(1.1), Inches(2.15), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "💻 Software Environment & Frameworks"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = CLR_SAFFRON

    sw_items = [
        ("Python 3.11+", "Core runtime programming language for data manipulation and backend modeling."),
        ("Streamlit 1.56+", "Modern reactive web application framework with custom CSS theme tokens and segmented navigation controls."),
        ("Plotly Express & Graph Objects", "Interactive, publication-grade visualization engine with custom zoom, tooltips, and bottom-positioned legends."),
        ("Pandas & NumPy", "Vectorized dataset aggregation, dynamic filtering, datetime resampling, and matrix computations."),
        ("Scikit-Learn", "Machine learning library providing LinearRegression, cross-validation metrics, RMSE, and R² evaluation."),
        ("Statsmodels", "Econometric package running seasonal_decompose and ARIMA(p,d,q) forecasting."),
        ("SQLite 3", "Lightweight ACID-compliant embedded relational database for persistence and live meal logging.")
    ]
    for k, v in sw_items:
        p = tf.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"• {k}: "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = CLR_SAFFRON
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = CLR_TEXT_MUTED

    add_card(s8, Inches(6.9), Inches(1.95), Inches(5.6), Inches(5.1), CLR_AMBER)
    tb = s8.shapes.add_textbox(Inches(7.2), Inches(2.15), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "🖥️ Hardware & Deployment Requirements"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = CLR_AMBER

    hw_items = [
        ("Processor / CPU", "Intel Core i5 / AMD Ryzen 5 or higher (minimum quad-core 2.4 GHz) for smooth time-series fitting."),
        ("System Memory (RAM)", "8 GB RAM minimum (16 GB recommended for concurrent multi-facility forecasting)."),
        ("Storage Footprint", "500 MB free disk space for SQLite database, Python virtual environment, and cached charts."),
        ("Display Resolution", "Optimized for 1080p FHD (1920x1080) and 768p responsive laptop screens with 5-card KPI single-row layout."),
        ("Operating System", "Cross-platform compatibility: Windows 10/11, macOS Monterey+, and Ubuntu Linux 20.04+ LTS."),
        ("Browser Compatibility", "Google Chrome, Mozilla Firefox, Microsoft Edge, Safari with WebGL hardware acceleration enabled.")
    ]
    for k, v in hw_items:
        p = tf.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"• {k}: "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = CLR_AMBER
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = CLR_TEXT_MUTED

    # =========================================================================
    # SLIDE 9: 8. METHODOLOGY / WORKING PROCESS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_light_bg(s9)
    add_light_header(s9, "Section 8", "8. Methodology / Working Process", "Structured 4-phase analytical workflow implemented in the system.")

    method_phases = [
        ("Phase 1: Ingestion & Verification", CLR_TERRACOTTA, [
            ("Data Ingestion", "System loads baseline 420 records from SQLite or uploads new operational meal records via CSV/Form."),
            ("Sanity Checks", "Verifies column data types: Date (datetime64), Category/Facility/Cause (object), Prep/Served/Wasted (float64)."),
            ("Conservation Assertions", "Enforces mass balance: Prepared = Served + Wasted; rejects illegal negative volumes.")
        ]),
        ("Phase 2: EDA & Anomaly Profiling", CLR_SAFFRON, [
            ("Categorical Pareto Modeling", "Computes waste distribution across 7 food categories to detect dominant drivers (Rice/Bread)."),
            ("IQR Outlier Identification", "Calculates Q1, Q3, and IQR = Q3 - Q1; marks observations exceeding Q3 + 1.5*IQR as anomalies."),
            ("Bivariate Correlation", "Generates Pearson correlation matrix (r) between preparation volume and waste.")
        ]),
        ("Phase 3: Time-Series Modeling", CLR_AMBER, [
            ("Resampling & Interpolation", "Resamples data by Daily ('D') or Weekly ('W') frequency, handling gaps via forward fill."),
            ("Smoothing Filter", "Applies 7-day Moving Average and Exponential Smoothing (alpha=0.30) to track trend lines."),
            ("Seasonal Decomposition", "Decomposes series into Trend, Seasonal (7-day cycle), and Residual components."),
            ("ARIMA Forecasting", "Fits ARIMA(1,1,1) model and projects expected waste 14 days ahead with confidence intervals.")
        ]),
        ("Phase 4: Simulation & Protocols", CLR_HIGH, [
            ("What-If Simulation", "Takes user inputs for over-prep reduction (%) and plate-waste reduction (%) and projects kg/INR rescued."),
            ("Linear Regression", "Fits Ordinary Least Squares (OLS) model: Food_Wasted = beta1 * Food_Prepared + beta0."),
            ("Action Generation", "Evaluates statistical thresholds to trigger 6 prioritized operational intervention protocols.")
        ])
    ]
    for i, (title, col, steps) in enumerate(method_phases):
        add_card(s9, p4_lefts[i], Inches(1.95), Inches(2.75), Inches(5.1), col)
        sh = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p4_lefts[i] + Inches(0.12), Inches(2.1), Inches(2.5), Inches(0.48))
        sh.fill.solid()
        sh.fill.fore_color.rgb = col
        sh.line.fill.background()
        p = sh.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = title
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

        tb = s9.shapes.add_textbox(p4_lefts[i] + Inches(0.18), Inches(2.75), Inches(2.4), Inches(4.1))
        tf = tb.text_frame
        tf.word_wrap = True
        for idx, (h, b) in enumerate(steps):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_before = Pt(8)
            r1 = p.add_run()
            r1.text = f"• {h}: "
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = col
            r2 = p.add_run()
            r2.text = b
            r2.font.size = Pt(9)
            r2.font.color.rgb = CLR_TEXT_MUTED

    # =========================================================================
    # SLIDE 10: 9. IMPLEMENTATION / MODULE BREAKDOWN
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_light_bg(s10)
    add_light_header(s10, "Section 9", "9. Implementation & Module Breakdown", "Core application modules implemented in the Streamlit web dashboard.")

    modules = [
        ("Tab 1: Kitchen Executive Hub", CLR_SAFFRON, [
            ("5-Card KPI Plate Deck", "Total Food Wasted, Total Meals Logged, Prep vs Served, Financial Loss (INR), and Rescued Meals."),
            ("Structured Graph Cards", "Weekly Waste Trajectory, Category Donut Chart, Facility Volumes, and Root Cause Loss in bordered boxes."),
            ("Operations Matrix", "Aggregated prepared, served, wasted kg and waste percentage table across all dining facilities.")
        ]),
        ("Tab 2 & 3: Analytics & Forecasting", CLR_AMBER, [
            ("Distribution Curves", "Histograms with customizable bin granularity and stratification by Meal Type, Category, or Location."),
            ("Outlier Profiler", "Boxplots displaying IQR distributions to isolate operational anomalies."),
            ("Time-Series Engine", "Interactive moving averages, exponential smoothing, 7-day seasonal decomposition, and ARIMA forecasts.")
        ]),
        ("Tab 4, 5 & 6: Simulator, Actions & Logs", CLR_TERRACOTTA, [
            ("Menu Portion Simulator", "What-If scenario sliders with live calculation of food saved, cost saved, and new projected waste rates."),
            ("Action Recommendations", "Dedicated hub containing 6 prioritized operational protocols with empirical findings and verification steps."),
            ("Kitchen Observation Terminal", "Searchable observation database with keyword filtering, CSV export, and new entry creation form.")
        ])
    ]
    for i, (title, col, items) in enumerate(modules):
        add_card(s10, l3[i], Inches(1.95), Inches(3.7), Inches(5.1), col)
        tb = s10.shapes.add_textbox(l3[i] + Inches(0.2), Inches(2.15), Inches(3.3), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = CLR_TEXT_MAIN
        for h, b in items:
            p2 = tf.add_paragraph()
            p2.space_before = Pt(8)
            r2 = p2.add_run()
            r2.text = f"• {h}: "
            r2.font.bold = True
            r2.font.size = Pt(10)
            r2.font.color.rgb = col
            r3 = p2.add_run()
            r3.text = b
            r3.font.size = Pt(9.5)
            r3.font.color.rgb = CLR_TEXT_MUTED

    # =========================================================================
    # SLIDE 11: 10. RESULTS AND DISCUSSION
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_light_bg(s11)
    add_light_header(s11, "Section 10", "10. Results and Discussion", "Empirical findings, statistical performance metrics, and operational evaluation.")

    s11_cards = [
        ("Key Statistical Metrics", CLR_HIGH, [
            ("Total Baseline Waste", "7,800+ kg wasted out of 51,000+ kg prepared (15.24% cumulative waste rate across 420 observations)."),
            ("Pearson Correlation (r)", "r = 0.689 indicating strong positive correlation between preparation volume and waste."),
            ("Regression Fit (R²)", "R² = 0.474; preparation volume alone explains ~47.4% of total waste variance across facilities."),
            ("Model Equation", "Food_Wasted = 0.1524 * Food_Prepared + 1.28 kg (RMSE = 12.3 kg per session).")
        ]),
        ("Empirical Discoveries", CLR_SAFFRON, [
            ("Staple Category Vulnerability", "Rice (24.4%) and Bread (17.3%) comprise 41.7% of all food discarded due to fixed batch cooking sizes."),
            ("Over-Preparation Dominance", "Over-preparation accounts for 48% of total loss, proving pre-service cooking is the primary failure point."),
            ("Hostel Weekend Anomalies", "Hostels produce the highest loss (2,355 kg) with 6 statistical anomaly days exceeding +2σ variation on weekends.")
        ]),
        ("Intervention Simulation Results", CLR_AMBER, [
            ("Policy Target Scenario", "Simulating a 15% reduction in over-preparation and 20% cut in plate waste."),
            ("Projected Food Rescued", "1,870+ kg of edible food rescued annually per facility."),
            ("Financial Cost Saved", "₹1,12,000+ in raw ingredient cost saved per facility per year."),
            ("Environmental Abatement", "~4.67 Tons of CO₂e emissions prevented and waste percentage dropped from 15.2% to 9.8%.")
        ])
    ]
    for i, (title, col, items) in enumerate(s11_cards):
        add_card(s11, l3[i], Inches(1.95), Inches(3.7), Inches(5.1), col)
        tb = s11.shapes.add_textbox(l3[i] + Inches(0.2), Inches(2.15), Inches(3.3), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.size = Pt(13.5)
        r.font.bold = True
        r.font.color.rgb = CLR_TEXT_MAIN
        for h, b in items:
            p2 = tf.add_paragraph()
            p2.space_before = Pt(8)
            r2 = p2.add_run()
            r2.text = f"• {h}: "
            r2.font.bold = True
            r2.font.size = Pt(10)
            r2.font.color.rgb = col
            r3 = p2.add_run()
            r3.text = b
            r3.font.size = Pt(9.5)
            r3.font.color.rgb = CLR_TEXT_MUTED

    # =========================================================================
    # SLIDE 12: 11. ADVANTAGES AND APPLICATIONS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_light_bg(s12)
    add_light_header(s12, "Section 11", "11. Advantages and Applications", "Practical operational benefits and cross-industry deployment opportunities.")

    add_card(s12, Inches(0.8), Inches(1.95), Inches(5.6), Inches(5.1), CLR_TERRACOTTA)
    tb = s12.shapes.add_textbox(Inches(1.1), Inches(2.15), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "🌟 Key System Advantages"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = CLR_TERRACOTTA

    adv_items = [
        ("Action-Oriented Architecture", "Unlike generic BI dashboards, translates statistical anomalies directly into concrete kitchen protocols."),
        ("Proactive Forecasting vs Passive History", "ARIMA and EWMA predict consumption 14 days ahead, preventing over-preparation before it occurs."),
        ("Significant Financial ROI", "Achieves 15–25% waste reduction, recovering ₹1.5–₹2 Lakhs per facility annually with zero hardware capital cost."),
        ("Carbon & ESG Governance", "Tracks and quantifies greenhouse gas abatement (CO₂e) and meals rescued for sustainability audits."),
        ("Zero 'Undefined' Visual Elegance", "Robust Plotly formatting, clean card boxes, and culinary bistro styling ensure high user adoption.")
    ]
    for k, v in adv_items:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {k}: "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = CLR_TERRACOTTA
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = CLR_TEXT_MUTED

    add_card(s12, Inches(6.9), Inches(1.95), Inches(5.6), Inches(5.1), CLR_SAFFRON)
    tb = s12.shapes.add_textbox(Inches(7.2), Inches(2.15), Inches(5.0), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "🏢 Practical Real-World Applications"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = CLR_SAFFRON

    app_items = [
        ("University & College Hostel Messes", "Calibrating student headcount against leave registers and academic schedules to stop weekend food dumps."),
        ("Corporate & IT Park Cafeterias", "Adjusting meal prep dynamically to hybrid work patterns (e.g. low attendance on Mondays & Fridays)."),
        ("Hospital & Healthcare Dietary Units", "Managing strict nutritional portions and perishable ingredient lifecycles to avoid spoilage."),
        ("Commercial Event Catering & Banquets", "Modeling historical guest turnout ratios to right-size bulk prep for weddings and conventions."),
        ("Municipal & NGO Food Redistribution", "Connecting surplus food predictions with local food rescue organizations before expiration.")
    ]
    for k, v in app_items:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {k}: "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = CLR_SAFFRON
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = CLR_TEXT_MUTED

    # =========================================================================
    # SLIDE 13: 12. CONCLUSION & FUTURE SCOPE
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    bg13 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg13.fill.solid()
    bg13.fill.fore_color.rgb = CLR_DARK_BG
    bg13.line.fill.background()

    ribbon = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    ribbon.fill.solid()
    ribbon.fill.fore_color.rgb = CLR_SAFFRON
    ribbon.line.fill.background()

    tag_box = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(3.8), Inches(0.32))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = RGBColor(44, 32, 24)
    tag_box.line.color.rgb = CLR_SAFFRON
    p = tag_box.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "SECTION 12"
    r.font.size = Pt(9)
    r.font.bold = True
    r.font.color.rgb = CLR_SAFFRON

    title_box = s13.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "12. Conclusion & Future Scope"
    r.font.size = Pt(21)
    r.font.bold = True
    r.font.color.rgb = CLR_TEXT_LIGHT

    # Left Dark Card: Conclusion
    c_conc = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(4.7))
    c_conc.fill.solid()
    c_conc.fill.fore_color.rgb = RGBColor(27, 21, 17)
    c_conc.line.color.rgb = RGBColor(61, 45, 34)
    c_conc.line.width = Pt(1.5)

    tb = s13.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(5.0), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "🎯 Project Conclusion"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = CLR_SAFFRON

    conc_bullets = [
        ("Bridging Data to Operations", "Successfully created an end-to-end DAV platform that converts static meal records into active kitchen interventions."),
        ("Validated Hypothesis", "Proved that over-preparation (48%) and volatile staples (Rice/Bread: 41.7%) represent the primary levers for institutional waste reduction."),
        ("Proven Analytical Soundness", "Combined linear regression (r=0.689, R²=0.474) with ARIMA(1,1,1) forward projections and interactive 'What-If' simulation."),
        ("Real-World Impact", "Delivers an actionable pathway to achieve 15–25% waste reduction and save over ₹1.5 Lakhs annually per facility.")
    ]
    for k, v in conc_bullets:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {k}: "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = CLR_SAFFRON
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = CLR_TEXT_LIGHT_MUTED

    # Right Dark Card: Future Scope
    c_fut = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(4.7))
    c_fut.fill.solid()
    c_fut.fill.fore_color.rgb = RGBColor(27, 21, 17)
    c_fut.line.color.rgb = RGBColor(61, 45, 34)
    c_fut.line.width = Pt(1.5)

    tb = s13.shapes.add_textbox(Inches(7.2), Inches(1.7), Inches(5.0), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "🚀 Future Scope & Technological Roadmap"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = CLR_AMBER

    fut_bullets = [
        ("IoT Smart Weighing Bins", "Deploying load-cell digital smart bins at plate drop-off stations to log real-time plate waste automatically."),
        ("Computer Vision Tray Scanners", "Utilizing YOLO/ResNet deep learning models on conveyor cameras to automatically classify and weigh uneaten food categories."),
        ("Biometric Turnstile API Sync", "Connecting campus gate access and student RFID turnstiles directly to kitchen requisitions 2 hours before meal prep."),
        ("Automated NGO Redistribution Dispatch", "Integrating automated alerts with local food rescue charities when surplus exceeds 15 kg of wholesome food.")
    ]
    for k, v in fut_bullets:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {k}: "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = CLR_AMBER
        r2 = p.add_run()
        r2.text = v
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = CLR_TEXT_LIGHT_MUTED

    # Bottom Thank You / Q&A
    qa_bar = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.35), Inches(11.7), Inches(0.7))
    qa_bar.fill.solid()
    qa_bar.fill.fore_color.rgb = RGBColor(44, 32, 24)
    qa_bar.line.color.rgb = CLR_SAFFRON
    p = qa_bar.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Thank You! Questions & Discussion  |  Food Waste Analytics and Management System (DAV Project)"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = CLR_TEXT_LIGHT

    prs.save(output_path)
    print(f"Full 13-slide academic presentation created at: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "Food_Waste_Analytics_Presentation.pptx"
    build_presentation(out)
