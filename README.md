# AI_SOC2_Assessor
ChatGPT wrapper that analyzes SOC2 security controls, mapping security controls into an Excel matrix
# 📊 SOC 2 Report Control Analysis with ChatGPT

This Python project automates the review of **SOC 2 audit reports** by extracting text from a PDF, splitting it into manageable chunks, and using **OpenAI’s GPT-4o model** to verify whether specific security controls are implemented. The results are saved to an Excel file for easy reporting and review.

---

## 📦 Features

- 📖 Extracts text from a SOC 2 report PDF using `pdfplumber`.
- ✂️ Splits the text into chunks for manageable analysis by the ChatGPT API.
- 🧑‍💻 Uses OpenAI’s `gpt-4o` model to analyze each chunk for predefined security controls.
- 📄 Outputs the results into a structured Excel file using `pandas`.
- 🔒 Supports environment-based API key management using `python-dotenv`.

---

## 🛠️ Dependencies

Install the required libraries via:

```bash
pip install openai pandas pdfplumber python-dotenv
