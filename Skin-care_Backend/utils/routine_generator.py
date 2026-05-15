"""
Skincare routine generation logic
"""

def generate_skincare_routine(skin_type, concerns, lifestyle):
    """
    Generate personalized skincare routine
    
    Args:
        skin_type: str - 'Oily', 'Dry', or 'Normal'
        concerns: list - User's skin concerns
        lifestyle: dict - Sleep, water, stress, etc.
    
    Returns:
        dict - Complete personalized routine
    """
    
    # Base routines by skin type
    base_routines = {
        'Oily': {
            'morning': [
                {
                    'step': 'Cleanser',
                    'commercial': 'Gel-based foaming cleanser (CeraVe, La Roche-Posay)',
                    'natural': ' Honey + tea tree oil cleanser',
                    'home_remedy': 'Mix 1 tbsp honey + 2 drops tea tree oil',
                    'why': 'Remove excess oil without stripping'
                },
                {
                    'step': 'Toner',
                    'commercial': 'Salicylic acid toner (Paula\'s Choice)',
                    'natural': ' Witch hazel or green tea toner',
                    'home_remedy': 'Brew strong green tea, cool, apply with cotton pad',
                    'why': 'Control oil and minimize pores'
                },
                {
                    'step': 'Serum',
                    'commercial': 'Niacinamide 10% (The Ordinary)',
                    'natural': ' Aloe vera gel',
                    'home_remedy': 'Fresh aloe vera leaf gel (refrigerate)',
                    'why': 'Reduce oil and brighten'
                },
                {
                    'step': 'Moisturizer',
                    'commercial': 'Oil-free gel moisturizer (Neutrogena Hydro Boost)',
                    'natural': ' Lightweight jojoba oil (2-3 drops)',
                    'home_remedy': 'Aloe vera gel + 1 drop jojoba oil',
                    'why': 'Hydrate without adding oil'
                },
                {
                    'step': 'Sunscreen',
                    'commercial': 'Matte finish SPF 50 (La Roche-Posay Anthelios)',
                    'natural': ' Zinc oxide mineral sunscreen',
                    'home_remedy': 'Research DIY zinc oxide recipes',
                    'why': 'Essential UV protection'
                }
            ],
            'evening': [
                {
                    'step': 'Cleanser',
                    'commercial': 'Gel cleanser',
                    'natural': ' Honey + yogurt cleanser',
                    'home_remedy': '1 tbsp honey + 1 tbsp yogurt, massage and rinse',
                    'why': 'Deep clean pores'
                },
                {
                    'step': 'Treatment',
                    'commercial': 'BHA 2% (Paula\'s Choice)',
                    'natural': ' Tea tree oil (diluted 1:10)',
                    'home_remedy': 'Mix 1 drop tea tree + 10 drops jojoba oil',
                    'why': 'Prevent acne and unclog pores'
                },
                {
                    'step': 'Moisturizer',
                    'commercial': 'Light night cream',
                    'natural': ' Rosehip oil (2-3 drops)',
                    'home_remedy': 'Aloe vera gel + rosehip oil',
                    'why': 'Overnight hydration'
                }
            ],
            'weekly_treatments': [
                ' Clay mask 1-2x/week',
                ' DIY: Bentonite clay + apple cider vinegar',
                ' Green tea ice cubes (morning)',
                ' Lemon + honey spot treatment'
            ],
            'avoid': ['Heavy oils', 'Thick creams', 'Over-washing'],
            'diet_tips': ['Reduce dairy', 'Limit sugar', 'Drink green tea', 'Zinc-rich foods']
        },
        'Dry': {
            'morning': [
                {
                    'step': 'Cleanser',
                    'commercial': 'Cream cleanser (CeraVe Hydrating)',
                    'natural': ' Milk + honey cleanser',
                    'home_remedy': '2 tbsp milk + 1 tsp honey, massage gently',
                    'why': 'Cleanse without stripping'
                },
                {
                    'step': 'Toner',
                    'commercial': 'Hydrating toner with hyaluronic acid',
                    'natural': ' Rose water',
                    'home_remedy': 'Pure rose water or rose petals steeped in water',
                    'why': 'Add moisture layer'
                },
                {
                    'step': 'Serum',
                    'commercial': 'Hyaluronic acid serum (The Ordinary)',
                    'natural': ' Aloe vera gel',
                    'home_remedy': 'Fresh aloe vera + 1 drop vitamin E oil',
                    'why': 'Deep hydration'
                },
                {
                    'step': 'Face Oil',
                    'commercial': 'Facial oil blend',
                    'natural': ' Argan or rosehip oil (3-5 drops)',
                    'home_remedy': 'Mix 50% argan + 50% rosehip oil',
                    'why': 'Lock in moisture'
                },
                {
                    'step': 'Moisturizer',
                    'commercial': 'Rich cream (CeraVe Moisturizing Cream)',
                    'natural': ' Shea butter + coconut oil blend',
                    'home_remedy': 'Melt equal parts shea butter + coconut oil',
                    'why': 'Seal in hydration'
                },
                {
                    'step': 'Sunscreen',
                    'commercial': 'Hydrating SPF 50',
                    'natural': ' Zinc-based mineral sunscreen with oils',
                    'home_remedy': 'DIY mineral sunscreen (research recipes)',
                    'why': 'Protect while moisturizing'
                }
            ],
            'evening': [
                {
                    'step': 'Oil Cleanser',
                    'commercial': 'Cleansing balm (Banila Co)',
                    'natural': ' Coconut oil cleanser',
                    'home_remedy': 'Massage coconut oil, remove with warm cloth',
                    'why': 'Gentle makeup removal'
                },
                {
                    'step': 'Cream Cleanser',
                    'commercial': 'Hydrating cleanser',
                    'natural': ' Milk cleanser',
                    'home_remedy': 'Whole milk or cream, massage and rinse',
                    'why': 'Second cleanse without drying'
                },
                {
                    'step': 'Treatment',
                    'commercial': 'Ceramide serum',
                    'natural': ' Avocado oil',
                    'home_remedy': 'Pure avocado oil, 3-5 drops',
                    'why': 'Repair skin barrier'
                },
                {
                    'step': 'Night Cream',
                    'commercial': 'Rich overnight mask (Laneige)',
                    'natural': ' Shea butter + vitamin E',
                    'home_remedy': 'Melt shea butter, add vitamin E capsule',
                    'why': 'Intensive overnight repair'
                }
            ],
            'weekly_treatments': [
                ' Avocado + honey mask (2x/week)',
                ' Milk + turmeric mask',
                ' Banana + yogurt mask',
                ' Olive oil overnight treatment'
            ],
            'avoid': ['Hot water', 'Foaming cleansers', 'Alcohol-based products'],
            'diet_tips': ['Omega-3 fatty acids', 'Drink 8+ glasses water', 'Healthy fats', 'Vitamin E']
        },
        'Normal': {
            'morning': [
                {
                    'step': 'Cleanser',
                    'commercial': 'Gentle cleanser (Cetaphil)',
                    'natural': ' Honey cleanser',
                    'home_remedy': 'Raw honey, massage on damp face',
                    'why': 'Maintain natural balance'
                },
                {
                    'step': 'Toner',
                    'commercial': 'Balancing toner',
                    'natural': ' Rose water',
                    'home_remedy': 'Pure rose water or DIY rose petal water',
                    'why': 'Refresh and prep skin'
                },
                {
                    'step': 'Serum',
                    'commercial': 'Vitamin C serum (Timeless)',
                    'natural': ' Rosehip seed oil',
                    'home_remedy': 'Pure cold-pressed rosehip oil, 3 drops',
                    'why': 'Brightening and antioxidants'
                },
                {
                    'step': 'Moisturizer',
                    'commercial': 'Lightweight lotion (Neutrogena)',
                    'natural': ' Aloe vera + jojoba oil',
                    'home_remedy': 'Mix 1 tbsp aloe + 3 drops jojoba',
                    'why': 'Balanced hydration'
                },
                {
                    'step': 'Sunscreen',
                    'commercial': 'Broad spectrum SPF 50',
                    'natural': ' Mineral SPF (zinc oxide)',
                    'home_remedy': 'Research DIY zinc oxide recipes',
                    'why': 'Daily UV protection'
                }
            ],
            'evening': [
                {
                    'step': 'Cleanser',
                    'commercial': 'Gentle cleanser',
                    'natural': ' Honey + milk',
                    'home_remedy': '1 tsp honey + 1 tbsp milk',
                    'why': 'Remove impurities'
                },
                {
                    'step': 'Treatment',
                    'commercial': 'Retinol 0.5% (2-3x/week)',
                    'natural': ' Bakuchiol serum',
                    'home_remedy': 'Rosehip oil (natural vitamin A)',
                    'why': 'Anti-aging prevention'
                },
                {
                    'step': 'Moisturizer',
                    'commercial': 'Night cream',
                    'natural': ' Rosehip oil + vitamin E',
                    'home_remedy': 'Mix 1 tsp rosehip + 1 vitamin E capsule',
                    'why': 'Overnight repair'
                }
            ],
            'weekly_treatments': [
                ' Honey + turmeric mask (1x/week)',
                ' Green tea rinse',
                ' Cucumber + aloe mask',
                ' Lemon + honey (with SPF!)'
            ],
            'avoid': ['Over-treatment', 'Too many actives', 'Harsh scrubs'],
            'diet_tips': ['Balanced diet', 'Antioxidants', 'Stay hydrated', 'Vitamins C & E']
        }
    }
    
    # Get base routine
    routine = base_routines.get(skin_type, base_routines['Normal']).copy()
    
    # Customize based on concerns
    if 'Acne' in concerns or 'Breakouts' in concerns:
        routine['morning'].insert(3, {
            'step': 'Spot Treatment',
            'commercial': 'Benzoyl peroxide 2.5%',
            'natural': ' Tea tree oil (diluted)',
            'home_remedy': 'Honey + cinnamon paste on spots',
            'why': 'Target active breakouts'
        })
        routine['weekly_treatments'].append(' Tea tree oil spot treatment')
    
    if 'Dark Circles' in concerns or 'Eye Bags' in concerns:
        routine['morning'].insert(4, {
            'step': 'Eye Treatment',
            'commercial': 'Caffeine eye cream (The Ordinary)',
            'natural': ' Cold cucumber slices',
            'home_remedy': 'Place cold cucumber slices for 10 min',
            'why': 'Reduce puffiness and dark circles'
        })
        routine['weekly_treatments'].append(' Cucumber slices daily')
    
    if 'Pigmentation' in concerns or 'Dark Spots' in concerns:
        routine['morning'][2] = {
            'step': 'Brightening Serum',
            'commercial': 'Vitamin C 20% (The Ordinary)',
            'natural': ' Lemon juice + honey',
            'home_remedy': 'Mix 1 tsp lemon + 1 tbsp honey (USE SPF!)',
            'why': 'Fade dark spots'
        }
        routine['weekly_treatments'].append(' Turmeric + milk mask')
    
    if 'Wrinkles' in concerns or 'Fine Lines' in concerns:
        routine['evening'].insert(2, {
            'step': 'Anti-Aging',
            'commercial': 'Retinol 0.5-1%',
            'natural': ' Rosehip oil',
            'home_remedy': 'Rosehip oil massage nightly',
            'why': 'Stimulate collagen, reduce wrinkles'
        })
        routine['weekly_treatments'].append(' Rosehip oil facial massage')
    
    if 'Redness' in concerns or 'Sensitivity' in concerns:
        routine['morning'].insert(3, {
            'step': 'Calming Treatment',
            'commercial': 'Centella asiatica + niacinamide',
            'natural': ' Aloe vera + chamomile',
            'home_remedy': 'Fresh aloe vera + cooled chamomile tea',
            'why': 'Reduce inflammation'
        })
        routine['avoid'].extend(['Fragrances', 'Essential oils', 'Hot water'])
    
    # Add lifestyle tips
    lifestyle_tips = []
    
    if lifestyle.get('sleep') in ['Less than 5 hours', '5-6 hours']:
        lifestyle_tips.append({
            'issue': ' Low Sleep',
            'impact': 'Dark circles, dull skin, slower healing',
            'recommendation': 'Aim for 7-8 hours. Use silk pillowcase.',
            'natural_remedy': ' Cold cucumber before bed +  chamomile tea'
        })
    
    if lifestyle.get('water_intake') in ['Less than 3 glasses', '3-5 glasses']:
        lifestyle_tips.append({
            'issue': ' Low Hydration',
            'impact': 'Dryness, dullness, fine lines',
            'recommendation': 'Drink 8+ glasses daily.',
            'natural_remedy': ' Infuse water with lemon/cucumber'
        })
    
    if lifestyle.get('stress_level') in ['Very high', 'Moderate']:
        lifestyle_tips.append({
            'issue': ' High Stress',
            'impact': 'Breakouts, inflammation, premature aging',
            'recommendation': 'Meditation, exercise, adequate rest',
            'natural_remedy': ' Lavender oil aromatherapy,  green tea'
        })
    
    if lifestyle.get('sun_exposure') in ['High', 'Moderate']:
        lifestyle_tips.append({
            'issue': ' Sun Exposure',
            'impact': 'Accelerated aging, pigmentation',
            'recommendation': 'SPF 50 DAILY. Reapply every 2 hours.',
            'natural_remedy': ' Eat tomatoes (lycopene), wear UPF clothing'
        })
    
    routine['lifestyle_tips'] = lifestyle_tips
    
    # Add wellness tips
    routine['wellness_tips'] = [
        ' Facial massage (3 min daily): Boost circulation',
        ' Face yoga (5 min daily): Tone muscles',
        ' Silk pillowcase: Reduce friction',
        ' Final rinse with cold water: Tighten pores'
    ]
    
    return routine