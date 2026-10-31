def generate_bfi_interpretation(domain_name, level):
    level_lower = level.lower().capitalize()  # Normalize to 'High', 'Moderate', 'Low'
    
    extraversion_map = {
        'High': 'sociable, energetic, and comfortable engaging with others',
        'Moderate': 'moderately interactive depending on the situation',
        'Low': 'reserved, reflective, and selective in social interactions'
    }
    
    agreeableness_map = {
        'High': 'a strong tendency toward cooperation, empathy, and consideration for others',
        'Moderate': 'balanced interpersonal functioning',
        'Low': 'a more independent, critical, or competitive interpersonal style'
    }
    
    conscientiousness_map = {
        'High': 'good self-discipline, organization, responsibility, and goal-directed behaviour',
        'Moderate': 'average levels of planning and responsibility',
        'Low': 'difficulties with organization, consistency, time management, or task completion'
    }
    
    neuroticism_map = {
        'High': 'increased emotional sensitivity, worry, self-doubt, or vulnerability to stress',
        'Moderate': 'occasional emotional fluctuations',
        'Low': 'good emotional stability and resilience'
    }
    
    openness_map = {
        'High': 'curiosity, creativity, flexibility, and willingness to explore new ideas',
        'Moderate': 'balanced openness to new experiences',
        'Low': 'preference for familiarity, structure, and conventional approaches'
    }
    
    if "extraversion" in domain_name.lower():
        desc = extraversion_map.get(level_lower, extraversion_map['Moderate'])
        return (f"The student's score on Extraversion falls within the {level_lower.lower()} range. "
                f"This suggests that the student is {desc}. "
                f"This trait may influence classroom participation, peer engagement, leadership tendencies, "
                f"and comfort in collaborative settings.")
                
    elif "agreeableness" in domain_name.lower():
        desc = agreeableness_map.get(level_lower, agreeableness_map['Moderate'])
        return (f"The student's score on Agreeableness falls within the {level_lower.lower()} range. "
                f"This indicates {desc}. "
                f"This domain may influence relationship-building, conflict resolution, and teamwork.")
                
    elif "conscientiousness" in domain_name.lower():
        desc = conscientiousness_map.get(level_lower, conscientiousness_map['Moderate'])
        return (f"The student's score on Conscientiousness falls within the {level_lower.lower()} range. "
                f"This suggests {desc}. "
                f"This domain is particularly relevant to academic performance and personal accountability.")
                
    elif "neuroticism" in domain_name.lower():
        desc = neuroticism_map.get(level_lower, neuroticism_map['Moderate'])
        return (f"The student's score on Neuroticism falls within the {level_lower.lower()} range. "
                f"This reflects {desc}. "
                f"Elevated scores may indicate a tendency to experience distress more intensely during challenging situations.")
                
    elif "openness" in domain_name.lower():
        desc = openness_map.get(level_lower, openness_map['Moderate'])
        return (f"The student's score on Openness to Experience falls within the {level_lower.lower()} range. "
                f"This indicates {desc}.")
                
    return ""

def generate_dass_interpretation(domain_name, severity):
    sev_lower = severity.lower()
    
    if "depression" in domain_name.lower():
        return (f"The student's score falls within the {sev_lower} range for Depression. "
                f"This reflects the extent to which the student may be experiencing symptoms such as low mood, "
                f"reduced interest in activities, diminished motivation, hopelessness, self-criticism, "
                f"or difficulty experiencing positive emotions. Higher scores may indicate greater emotional distress "
                f"and reduced psychological well-being.")
                
    elif "anxiety" in domain_name.lower():
        return (f"The student's score falls within the {sev_lower} range for Anxiety. "
                f"This reflects the presence of symptoms such as excessive worry, nervousness, "
                f"physiological tension, fearfulness, panic-like experiences, or heightened emotional arousal. "
                f"Elevated anxiety may affect concentration, confidence, decision-making, and academic functioning.")
                
    elif "stress" in domain_name.lower():
        return (f"The student's score falls within the {sev_lower} range for Stress. "
                f"This indicates the degree to which the student experiences tension, irritability, "
                f"emotional pressure, impatience, or difficulty relaxing. Higher levels of stress may impact "
                f"emotional regulation, academic performance, and interpersonal relationships.")
                
    return ""

def generate_dass_overall(severities_dict):
    # Normalize keys and values
    sevs = {k.lower(): v.lower() for k, v in severities_dict.items()}
    
    dep = sevs.get("depression", "normal")
    anx = sevs.get("anxiety", "normal")
    str_ = sevs.get("stress", "normal")
    
    # Check worst severity
    all_sevs = [dep, anx, str_]
    
    if any(s in ["severe", "extremely severe"] for s in all_sevs):
        level = "significant"
    elif any(s == "moderate" for s in all_sevs):
        level = "moderate"
    elif any(s == "mild" for s in all_sevs):
        level = "mild"
    else:
        level = "minimal"
        
    return (f"The DASS-21 profile suggests that the student is experiencing {level} emotional distress. "
            f"These findings should be understood in relation to current life circumstances, academic demands, "
            f"social relationships, and other psychosocial factors.")

def generate_eq_sq_interpretation(eq_level, sq_level):
    eq_lvl = eq_level.lower().capitalize()
    sq_lvl = sq_level.lower().capitalize()
    
    eq_p = (f"The student's EQ score falls within the {eq_lvl.lower()} range. "
            f"This reflects their ability to recognize, understand, express, and regulate emotions effectively. "
            f"Higher scores suggest emotional maturity, resilience, adaptive coping, and the ability to manage stress constructively. "
            f"Lower scores may indicate difficulties with emotional awareness, emotional regulation, impulse control, "
            f"or coping with challenging situations.")
            
    sq_p = (f"The student's SQ score falls within the {sq_lvl.lower()} range. "
            f"This reflects the student's ability to communicate effectively, establish and maintain relationships, "
            f"adapt to social situations, and function within groups. Higher scores indicate strong interpersonal "
            f"competence and social adaptability, whereas lower scores may suggest difficulties with social confidence, "
            f"communication, or peer interactions.")
            
    if eq_lvl == "Low" and sq_lvl == "Low":
        status = "requiring support"
    elif eq_lvl == "High" and sq_lvl == "High":
        status = "well developed"
    else:
        status = "adequately developed"
        
    overall_p = (f"The student's emotional and social functioning appears to be {status}. "
                 f"These competencies influence resilience, peer relationships, conflict management, "
                 f"and adjustment within academic and social environments.")
                 
    return eq_p, sq_p, overall_p

def generate_home_adjustment_interpretation(level):
    lvl_cap = level.lower().capitalize()
    
    if "healthy" in level.lower():
        text = "A healthy score suggests that the student perceives the family environment as supportive, emotionally secure, and conducive to well-being."
        display_level = "healthy adjustment"
    elif "mild" in level.lower():
        text = "Mild concerns may indicate occasional family conflicts, communication difficulties, perceived criticism, or feelings of misunderstanding."
        display_level = "mild concerns"
    else:
        text = "Significant difficulties may reflect considerable dissatisfaction with family relationships, emotional insecurity, conflict, lack of support, or stress arising from the home environment."
        display_level = "significant difficulties"
        
    return (f"The student's Home Adjustment score indicates {display_level}. "
            f"{text} "
            f"The student's perception of family relationships is an important contextual factor, "
            f"as family experiences often influence emotional well-being, self-esteem, coping abilities, and overall adjustment.")

def generate_integrated_summary(all_scores):
    # all_scores is a dict containing bfi (levels), dass (levels), eq_sq (eq_level, sq_level), home (level)
    strengths = []
    concerns = []
    
    bfi_lvls = all_scores.get('bfi', {}).get('levels', {})
    dass_lvls = all_scores.get('dass', {}).get('levels', {})
    eq_lvl = all_scores.get('eq_sq', {}).get('eq_level', 'Moderate')
    sq_lvl = all_scores.get('eq_sq', {}).get('sq_level', 'Moderate')
    home_lvl = all_scores.get('home', {}).get('level', 'Healthy Adjustment')
    
    # Check Strengths
    if bfi_lvls.get('Conscientiousness', 'Moderate').lower() == 'high':
        strengths.append("high Conscientiousness")
    if eq_lvl.lower() == 'high':
        strengths.append("high EQ")
    if sq_lvl.lower() == 'high':
        strengths.append("high SQ")
    if bfi_lvls.get('Neuroticism', 'Moderate').lower() == 'low':
        strengths.append("low Neuroticism")
    if 'healthy' in home_lvl.lower():
        strengths.append("healthy Home Adjustment")
    if bfi_lvls.get('Agreeableness', 'Moderate').lower() == 'high':
        strengths.append("high Agreeableness")
        
    # Check Concerns
    if bfi_lvls.get('Neuroticism', 'Moderate').lower() == 'high':
        concerns.append("high Neuroticism")
    if bfi_lvls.get('Conscientiousness', 'Moderate').lower() == 'low':
        concerns.append("low Conscientiousness")
        
    # DASS concerns
    dass_concerns = []
    for k, v in dass_lvls.items():
        if v.lower() in ["severe", "extremely severe"]:
            dass_concerns.append(f"{v.lower()} {k} scores")
    if dass_concerns:
        concerns.extend(dass_concerns)
        
    if eq_lvl.lower() == 'low' or sq_lvl.lower() == 'low':
        concerns.append("low EQ/SQ")
    if 'significant' in home_lvl.lower():
        concerns.append("home adjustment difficulties")
        
    strengths_str = ", ".join(strengths) if strengths else "standard developmental assets"
    concerns_str = ", ".join(concerns) if concerns else "no acute concern areas"
    
    return (f"The assessment findings suggest that the student demonstrates {strengths_str}. "
            f"Areas requiring attention include {concerns_str}. "
            f"Overall, the profile indicates that the student's current functioning is influenced by a combination "
            f"of personality characteristics, emotional well-being, social competencies, and perceived family environment.")
