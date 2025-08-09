import google.generativeai as genai

API_KEY = "AIzaSyCnwh66Ba-kHUm2ySC3L_ui10sIczmzHug"

try:
    genai.configure(api_key=API_KEY)
    models = genai.list_models()
    print("📦 Available Gemini Models:")
    for model in models:
        print(f"🧠 {model.name} | Generatable: {'generateContent' in model.supported_generation_methods}")
except Exception as e:
    print("❌ Error:", e)