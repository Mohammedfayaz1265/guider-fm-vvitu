import json
import os
import re
import google.generativeai as genai

# Determine path for vercel vs local
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, 'college_data.json')

# Load college data
try:
    with open(json_path, 'r') as f:
        college_data = json.load(f)
except Exception:
    college_data = {}

# Configure Gemini if API key is provided
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    # create the model
    model = genai.GenerativeModel('gemini-1.5-flash')

def get_fallback_response(user_message):
    msg = user_message.lower()
    
    # Keyword matching fallback
    if any(word in msg for word in ["fee", "cost", "price", "pay"]):
        return f"**Fees Structure** 💰\n- CSE/ECE/AI branches: ₹{college_data.get('programs', {}).get('BTech', {}).get('CSE', '2,00,000')}\n- EEE/ME/CE: ₹1,00,000\n- BBA/MBA: ₹1,50,000\n\nIs there anything else I can help you with? 😊"
    
    if any(word in msg for word in ["hostel", "accommodation", "room"]):
        return f"**Hostel Facilities** 🏠\n{college_data.get('hostel_fee', '₹1,00,000 - ₹1,50,000 per year (AC, includes food)')}. Boys & Girls separate.\n\nIs there anything else I can help you with? 😊"
        
    if any(word in msg for word in ["time", "timing", "hours"]):
        return "**College Timings** ⏰\n- College: 8:00 AM - 3:50 PM\n- Library: 8:00 AM - 4:00 PM\n- Canteen: 8:00 AM - 4:30 PM\n- Days: Mon-Sat\n\nIs there anything else I can help you with? 😊"
        
    if any(word in msg for word in ["package", "placement", "jobs", "salary"]):
        placements = college_data.get('placements', {})
        return f"**Placements** 💼\n- Average Package: {placements.get('average_package', '6.5 LPA')}\n- Highest Package: {placements.get('highest_package', '44 LPA')}\n- Placement Rate: {placements.get('placement_rate', '85%')}\n- Placed in 2025: {placements.get('placed_2025', '500+')}\n\nIs there anything else I can help you with? 😊"

    if any(word in msg for word in ["contact", "phone", "call", "number"]):
        return f"**Contact Us** 📞\nPhones: {', '.join(college_data.get('phones', []))}\nWebsite: {college_data.get('website', 'www.vvitu.ac.in')}\n\nIs there anything else I can help you with? 😊"
        
    if any(word in msg for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! 👋 I'm FM Guider, your AI companion for VVITU. You can ask me about fees, timings, placements, hostels, and more! How can I assist you today? 😊"

    if any(word in msg for word in ["thank", "thanks"]):
        return "You're very welcome! If you have any more questions about VVITU, feel free to ask. 😊"
        
    if any(word in msg for word in ["bye", "goodbye"]):
        return "Goodbye! Have a great day ahead! 👋"

    # Default fallback
    phone = college_data.get('phones', ['83410 98336'])[0] if college_data.get('phones') else '83410 98336'
    return f"**Hmm, I'm not entirely sure about that.** 🤔\nI can help you with:\n- ⏰ Timings\n- 🏠 Hostel\n- 💰 Fees\n- 🏫 Departments\n- 💼 Placements\n- 📞 Contact\n\nFor more details, please reach out to: {phone}\n\nIs there anything else I can help you with? 😊"

def generate_chatbot_response(user_message):
    try:
        if api_key:
            prompt = f"""You are FM Guider, a helpful AI assistant for VVITU (Vasireddy Venkatadri International Technological University) built by Fayaz & Masthan. 
Be conversational, helpful, and act like ChatGPT to enthusiastically answer general questions. If the user asks about the college, use the following info:
{json.dumps(college_data)}
If they ask something unrelated to the college, still answer them nicely like a general AI. 
Use emojis and friendly markdown. End with 'Is there anything else I can help you with? 😊'.

User Question: {user_message}"""
            response = model.generate_content(prompt)
            return response.text
        else:
            return "⚠️ **ERROR: API Key is missing!** You have not added `GEMINI_API_KEY` to your Vercel Environment Variables, or you forgot to Redeploy after adding it."
    except Exception as e:
        print("AI Error:", e)
        return f"⚠️ **AI Error:** {str(e)}"
