import re

class TextProcessor:
    def processor(self, recommendation):
        breakfast = recommendation.split('1. ')[1].split('2. ')[0]
        lunch = recommendation.split('2. ')[1].split('3. ')[0]
        dinner = recommendation.split('3. ')[1]
        
        return (
            breakfast,
            lunch,
            dinner,
            )
    def extract_activities(self, s):
        # Split the string by periods
        activities = s.split(". ")
        physical_activities = []
        for activity in activities:
            # Check if the part after the split contains any alphabetic characters
            if any(char.isalpha() for char in activity):
                # If yes, strip out the numbers and periods and add it to the list of physical activities
                physical_activities.append(''.join(filter(str.isalpha, activity.strip())))
        return physical_activities


if __name__=='__main__':
    paragraph = """SUMMARY OF THE REPORT WITH PERCENTAGE:\n- Hemoglobin: 12.3 gm/dl (within normal range)\n- Red Blood Cell Count: 3.90 mill/cmm (within normal range)\n- Total WBC Count: 10,300 /cmm (slightly elevated)\n- Haematocrit: 33.5% (below normal range)\n- Mean Corpuscular Volume: 85.9 fl (within normal range)\n- Mean Corpuscular Hemoglobin: 31.5 pg (within normal range)\n- Mean Corpuscular HGB Concentration: 36.7 gm/dl (slightly high)\n- RDW - CV: 15.0 (within normal range)\n- Neutrophils: 54%\n- Lymphocytes: 41%\n- Eosinophils: 4%\n- Monocytes: 1%\n- Basophils: 0%\n- Platelet Count: 395 x10^3 /cmm (within normal range)\n\n2. TYPE OF ANEMIA:\nBased on the results, this person has a mild iron deficiency anemia. This is indicated by the low hemoglobin and haematocrit levels, as well as the slightly high Mean Corpuscular HGB Concentration.\n\n3. DIETARY RECOMMENDATIONS (Indian Food Cuisine):\n- Breakfast: \n   - Spinach and paneer paratha with a side of curd\n- Lunch:\n   - Rajma curry with jeera rice and a side of salad\n- Dinner:\n   - Palak paneer with roti and a side of mixed vegetable raita\n\n4. DAILY ACTIVITY RECOMMENDATION:\nIt is recommended for this person to engage in daily physical activity such as walking, jogging, or yoga to improve blood circulation and overall health. Additionally, incorporating strength training exercises can help increase muscle strength and energy levels."""
    text_split = [TextProcessor().processor(paragraph)]
    print(text_split)