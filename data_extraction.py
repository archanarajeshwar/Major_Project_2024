import re
import pdfplumber
from dataclasses import dataclass

@dataclass
class ExtractPDFData:
    def extract_value(self, text, keyword):
        pattern = re.compile(r'{}[\s:]+(.+?)(?:\n|$)'.format(keyword), re.IGNORECASE)
        match = re.search(pattern, text)
        if match:
            return int(match.group(1).strip().split()[0])
        return None


    def extract_information(self, pdf_file_path):
        extracted_data = []
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                page_text= page.extract_text()
                extracted_data.append(page_text)
        print("Information Extracted")
        return extracted_data


    def identify_anemia_type(self, mcv_value):
        if mcv_value is None:
            return "Data not available"
        mcv_value = float(mcv_value)
        if mcv_value < 80:
            return "Microcytic Anemia"
        elif 80 <= mcv_value <= 100:
            return "Normocytic Anemia"
        else:
            return "Macrocytic Anemia"
        

if __name__=="__main__":
    filepath = r"extract_data\uploads\report.pdf"
    file = open(filepath, 'rb')
    
    extract_data = ExtractPDFData()
    extracted_information = extract_data.extract_information(file)
    print(extracted_information)
    
    count_names = ['Neutrophils', 'Lymphocytes', 'Eosinophils', 'Monocytes', 'Basophils']
    values = [extract_data.extract_value(extracted_information[0], value) for value in count_names]
    print(values)