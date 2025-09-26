import google.generativeai as genai   #Gemini API client for calling the generative model.
import streamlit as st                #Framework for building web apps.
from fpdf import FPDF                # Library to generate PDF files
from io import BytesIO                #Used to store PDF in memory for downloading without saving to disk.


##   Sets your Gemini API key. This connects your app to the Google Generative AI service.
genai.configure(api_key="your api key")

## Loads the Gemini 1.5 Flash model, optimized for fast and lightweight content generation.
model = genai.GenerativeModel("models/gemini-1.5-flash")


## SEO Extraction Function  for responding in given text or blog and news and tweets 
def extract_seo_insights(text):
    prompt = f"""
    Analyze the following content and extract:
    1. keyword suggestions,
    2. readability score, 
    3.and optimization opportunities
    

    Content:
    \"\"\"
    {text}
    \"\"\"
    """
    response = model.generate_content(prompt)
    return response.text
 # 1. Top keywords (single words or short phrases)
    # 2. Long-tail keyword suggestions
    # 3. SEO insights like readability, internal linking opportunities, and meta description ideas.


def text_to_pdf_bytes(text):    #This function takes text and converts it to a PDF (in memory).
    pdf = FPDF()                # Initializes a PDF page.
    pdf.add_page()
    
    # Settings Enables auto page break to prevent overflow.
    pdf.set_auto_page_break(auto=True, margin=15) 
    title_font_size = 16
    para_font_size = 12
    line_height = 7

    lines = text.strip().split('\n')

    for line in lines:
        clean_line = line.strip()
        
        if not clean_line:
            pdf.ln(line_height)  # Add space between paragraphs
            continue

        # Treat lines starting with "#" as headings Paragraph and Header Parsing
        if clean_line.startswith("# "):
            pdf.set_font("Arial", "B", size=title_font_size)
            pdf.multi_cell(0, 10, clean_line[2:])
            pdf.ln(2)
        elif clean_line.startswith("## "):
            pdf.set_font("Arial", "B", size=title_font_size - 2)
            pdf.multi_cell(0, 8, clean_line[3:])
            pdf.ln(1)
        else:
            pdf.set_font("Arial", "", size=para_font_size)
            pdf.multi_cell(0, line_height, clean_line)

    # Output as bytes Generates the PDF in-memory using 'latin-1' encoding
    
    try:
        pdf_output = pdf.output(dest='S').encode('latin-1')
    except UnicodeEncodeError:
        # Remove unsupported characters
        safe_text = text.encode('latin-1', 'ignore').decode('latin-1')
        return text_to_pdf_bytes(safe_text)

    return BytesIO(pdf_output)
## for front-end part 

st.set_page_config(page_title="SEO Keyword Analyzer", layout="centered")
# web_app  Sets the Streamlit page title
st.title("🔍 SEO Keyword Analyzer")
#Adds a user-friendly heading and instruction
st.markdown("Paste your **blog** or **news article**, and this tool will extract relevant SEO keywords using Gemini AI.")

# for takeing input  button from the user
content = st.text_area("✍️ Paste your article below:", height=300, placeholder="Enter your blog or news article content here...")

#  extract the SEO keyword from text when user clicks the extract button
if st.button("🚀 Extract SEO Keywords"):

# adding a condition for exp handling 
    if content.strip() == "":
        st.warning("Please paste some text to analyze.")
    else:
        with st.spinner("Analyzing..."):
            try:
                ## calling the funtion for extract the seo keywords

                keywords = extract_seo_insights(content)
                
                # Displays a success message and shows the extracted keyword insights

                st.success("✅ Keywords extracted successfully!")
                st.markdown("### 📌 SEO Keywords:")
                st.write(keywords)
                for kw in keywords.split(","):
                    st.markdown(f"- {kw.strip()}")
             
           

                #Creates a download button for the user to download the result
                 #  Converts keywords to PDF using text_to_pdf_bytes
                st.download_button(
                    label="⬇️ Download PDF",
                    data=text_to_pdf_bytes(keywords),
                    file_name="seo_keywords.pdf",
                    mime="application/pdf"
                     )
            #Shows error message if anything goes wrong during extraction
            except Exception as e:
             st.error(f"❌ Error: {str(e)}")
