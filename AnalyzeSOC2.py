import openai
import pandas as pd
import pdfplumber
from dotenv import load_dotenv
import os 

# Create a .env file, set the variable "OPENAI_API_KEY" to your key
# Load API key using a .env file. 
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") 

# Read PDF SOC2 report and convert into chunks 
def extract_chunks_from_pdf(pdf_path, chunk_size=3000):
    text = ""
    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                if len(text) >= chunk_size:
                    chunks.append(text)
                    text = ""
    if text:
        chunks.append(text)
    return chunks

# Note, the 'prompt' variable uses comments for large blocks of code. (Triple Quoted String Literals)
# Analyze controls using ChatGPT

def analyze_controls(chunks, control_checks):
    results = []
    for control in control_checks:
        found = False
        reasoning = ""
        for chunk in chunks:
            prompt = f"""
            You are an auditor assistant.
            Given the following SOC 2 report texts, confirm if the control '{control}' is implemented.
            Respond with 'Yes' or 'No', a brief reasoning and a reference to the control section.

            SOC 2 Report Chunk:
            {chunk}

            Control: {control}
            """
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            answer = response.choices[0].message.content.strip()

            if "Yes" in answer:
                found = True
                reasoning = answer
                break  # Stop checking further chunks for this control

        final_answer = reasoning if found else "No - not found in the reviewed sections."
        results.append({"Control": control, "Confirmation": final_answer})
    return results

# Write results to Excel
def save_results_to_excel(results, output_path):
    df = pd.DataFrame(results)
    df.to_excel(output_path, index = False)

if __name__ == "__main__":
    pdf_path = #YOUR_SOC2_REPORT.PDF
    output_path = "soc2_control_results.xlsx"
    controls_to_check = [

        "Multi-factor authentication, MFA, or two-factor authentication is implemented",
        "Security awareness training is completed on an annual basis",
        "Penetration testing is conducted by an independent party on an annual basis",
        "Information Security Policies are reviewed and approved on an annual basis by leadership",
        "Changes to infrastructure or software are tested and approved prior to implementation",
        "Vulnerabilities are identified, tracked and remediated", 
        "Third parties or vendors are reviewed for security on annual basis", 
        "User access is requested and approved prior to granting access",
        "Firewalls are implemented", 
        "Encryption in transit is in place", 
        "Encryption at rest is implemented on endpoint devices such as laptops, databases or backups"

    ]

    chunks = extract_chunks_from_pdf(pdf_path)
    results = analyze_controls(chunks, controls_to_check)
    save_results_to_excel(results, output_path)

    print("SOC 2 analysis complete. Results saved to Excel")