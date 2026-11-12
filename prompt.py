import openai
from config import api_key

client = openai.OpenAI(api_key=api_key)

class Prompt:
    def generate_prompt(self, extracted_data ,bmr , daily_calories , activity_level,disease):
        query_1 = f'''{extracted_data}. 
        
        Give 100 words strictly!! summary  of the CBC report of the patient based on the given data in lay man manner .'''

        query_5 = f'''{extracted_data}.

        Give 50 words strictly!! preventive measures for the patients based on their CBC report given above, BMR : {bmr} and Disease: {disease} , short and crisp  .'''

                    
        query_2 = f'''{extracted_data}.
        
        Give  100 words strictly!! What type of anemia is it based on the given data and differential count statistics'''

        query_3 = f'''{extracted_data} .
        
        Can you prescribe concise dietary recommendations for an given Indian patient , based on their Complete Blood Count results which is the above data ,BMR:{bmr},their daily calories{daily_calories} and chronic disease:{disease}? in the following structure
        1. Breakfast: [Indian cuisine food recommendations, nutrient value tags]
        2. Lunch: [Indian cuisine food recommendations, nutrient value tags]
        3. Dinner: [Indian cuisine food recommendations, nutrient value tags]
        '''

        query_4 = f'''{extracted_data}.
        
        Give me a list of 10 physical activities for this person based on their BMR :{bmr} , Activity level :{activity_level} . only name'''
                    
        summary = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": query_1}
            ]).choices[0].message.content

        stats = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": query_2}
            ]).choices[0].message.content

        diet = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": query_3}
            ]).choices[0].message.content

        recommendation = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": query_4}
            ]).choices[0].message.content
        prevention= client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": query_5}
            ]).choices[0].message.content

        return summary, stats, diet, recommendation , prevention


if __name__=='__main__':
    extracted_data = '''
    Lab No : 86200
    Name : Miss Archana Rajeshwar Age : 20 Yrs Sex : Female
    ( Labelled Sample Received )
    Ref By : HEALTH TREE The Family Clinic
    Dr. Ameya Phansalkar
    COMPLETE BLOOD COUNT
    Test Result Normal Range Units
    HEMOGLOBIN 12.3 12.00 - 15.60 gm/dl
    RED BLOOD CELL 3.90 3.8 - 5.8 mill/cmm
    TOTAL WBC COUNT 10,300 4000 - 11000 /cmm
    Haematocrit 33.5 Low 35 - 47 %
    Mean Corpuscular Volume 85.9 76 - 96 fl
    Mean Corpuscular hemoglobin 31.5 27 - 32 pg
    Mean Corpuscular HGB Conc. 36.7 High 30 -36 gm/dl
    RDW - CV 15.0 11.5 - 16.5
    DIFFERENTIAL COUNT
    Neutrophils 54 40 - 75 %
    Lymphocytes 41 20 - 45 %
    Eosinophils 04 1 - 6 %
    Monocytes 01 2 - 10 %
    Basophils 00 0 - 1 %
    3
    PLATELET COUNT 395 150 - 450 x10 /cmm
    RBC Morphology Normochromic Normocytic
    WBC Morphology Normal
    Blood cell count done on MEDONIC Cell Counter
    '''
    bmr = 1286

    daily_calories = 1459

    activity_level = 1.55
    disease = "None"
    text = [Prompt().generate_prompt(extracted_data,bmr , daily_calories , activity_level,disease)]
    print(text)