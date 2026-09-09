import gradio as gr
from google import genai
from google.genai import types

# १. तुमची सुरक्षित API Key इथे टाका
NEW_GEMINI_API_KEY = "insert api key here"

# २. गुगल जेनएआय क्लायंट सुरू करा
client = genai.Client(api_key=NEW_GEMINI_API_KEY)

system_instruction = """
तुम्ही एक हुशार, अनुभवी आणि मदत करणारे 'कृषी सहाय्यक' (AI Farming Expert) आहात.
तुमचे काम शेतकऱ्यांना पिकांचे नियोजन, खत व्यवस्थापन, कीड नियंत्रण आणि
आधुनिक शेती तंत्रज्ञानाबद्दल सोप्या मराठी भाषेत अचूक माहिती देणे आहे.
जर शेतकऱ्याने फोटो पाठवला असेल, तर पिकाचा रोग ओळखून मराठीत योग्य उपाय सांगा.
"""

# ३. साधे इनपुट-आउटपुट फंक्शन (कोणताही हिस्टरी एरर येणार नाही)
def ask_krishi_sahayak(marathi_question, upload_image):
    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction
        )

        contents = []

        # १. प्रश्न जोडणे
        if marathi_question:
            contents.append(marathi_question)

        # २. फोटो जोडणे
        if upload_image is not None:
            # फाईल पाथ मिळवून बाइट्स रीड करणे
            file_path = upload_image.name if hasattr(upload_image, 'name') else upload_image
            with open(file_path, "rb") as f:
                image_bytes = f.read()
            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg"
                )
            )

        if not contents:
            return "कृपया तुमचा प्रश्न लिहा किंवा पिकाचा फोटो अपलोड करा."

        # मॉडेलकडून थेट उत्तर मिळवणे
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=config
        )

        return response.text

    except Exception as e:
        return f"तांत्रिक अडचण आली आहे: {str(e)}"

# ४. स्टँडर्ड इंटरफेस डिझाईन (कधीही न अडकणारे)
demo = gr.Interface(
    fn=ask_krishi_sahayak,
    inputs=[
        gr.Textbox(label="तुमचा प्रश्न इथे मराठीत लिहा", placeholder="उदा. कांदा लागवड कशी करावी? किंवा खाली फोटो अपलोड करा..."),
        gr.Image(label="पिकाचा/रोगाचा फोटो अपलोड करा (ऐच्छिक)", type="filepath")
    ],
    outputs=gr.Textbox(label="कृषी सहाय्यकाचा सल्ला (मराठीत)", lines=10),
    title="🌾 कृषी सहाय्यक सल्ला केंद्र",
    description="शेतकरी बंधूंनो, तुमचा प्रश्न लिहा किंवा पिकाच्या समस्येचा फोटो अपलोड करा आणि 'Submit' वर क्लिक करा.",
    theme=gr.themes.Soft()
)

# ५. लाईव्ह करा
demo.launch(share=True)

