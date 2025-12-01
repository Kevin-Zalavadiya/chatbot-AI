import google.generativeai as genai
import re

class HealthChatbot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def extract_symptoms(self, text):
        prompt = f"""
        Extract symptoms from this message: "{text}"
        Return only a Python list of symptoms in lowercase.
        Example: ["fever", "headache"]
        
        Rules:
        - Extract ALL symptoms mentioned
        - Convert variations: "head hurting" → "headache", "feverish" → "fever", "body pain" → "body ache"
        - If only 1 symptom found, still return it
        - If no clear symptoms, return ["fever", "headache"] (default symptoms)
        - Always return a list, never return empty
        """
        response = self.model.generate_content(prompt)
        try:
            symptoms = eval(response.text.strip())
            if not symptoms or symptoms == []:
                return ["fever", "headache"]  # Default symptoms for testing
            return symptoms
        except:
            return ["fever", "headache"]  # Default symptoms
    
    def detect_treatment_type(self, message):
        message = message.lower()
        if "ayurved" in message:
            return "ayurveda"
        elif "homeopath" in message:
            return "homeopathy" 
        elif "home remedy" in message or "home remedies" in message:
            return "home remedy"
        else:
            return "all"
    
    def get_treatment(self, symptoms, treatment_type):
        symptoms_str = ", ".join(symptoms)
        
        if treatment_type == "ayurveda":
            prompt = f"""
            Provide ONLY Ayurvedic treatment for: {symptoms_str}
            
            Format your response cleanly with HTML:
            <p><strong>Ayurvedic Medicine:</strong> [medicine name]</p>
            <p><strong>Dosage:</strong> [how to take]</p>
            <p><strong>Precautions:</strong> [what to avoid]</p>
            <p><strong>Home Tips:</strong> [additional advice]</p>
            
            Keep response focused only on Ayurvedic treatments.
            Include medical disclaimer at the end.
            Use simple formatting without excessive asterisks or markdown.
            """
        
        elif treatment_type == "homeopathy":
            prompt = f"""
            Provide ONLY Homeopathic treatment for: {symptoms_str}
            
            Format your response cleanly with HTML:
            <p><strong>Homeopathic Medicine:</strong> [medicine name]</p>
            <p><strong>Dosage:</strong> [how to take]</p>
            <p><strong>Precautions:</strong> [what to avoid]</p>
            <p><strong>Home Tips:</strong> [additional advice]</p>
            
            Keep response focused only on Homeopathic treatments.
            Include medical disclaimer at the end.
            Use simple formatting without excessive asterisks or markdown.
            """
        
        elif treatment_type == "home remedy":
            prompt = f"""
            Provide ONLY Home Remedies for: {symptoms_str}
            
            Format your response cleanly with HTML:
            <p><strong>Home Remedy:</strong> [remedy name]</p>
            <p><strong>How to Use:</strong> [instructions]</p>
            <p><strong>Precautions:</strong> [warnings]</p>
            <p><strong>Benefits:</strong> [why it helps]</p>
            
            Keep response focused only on natural home remedies.
            Include medical disclaimer at the end.
            Use simple formatting without excessive asterisks or markdown.
            """
        
        else:  # all types
            prompt = f"""
            Provide treatments for: {symptoms_str}
            Include all three types: Ayurvedic, Homeopathy, and Home Remedies.
            
            Format your response cleanly with HTML:
            <p><strong>Ayurvedic:</strong> [medicine] - [dosage]</p>
            <p><strong>Homeopathy:</strong> [medicine] - [dosage]</p>
            <p><strong>Home Remedy:</strong> [remedy] - [how to use]</p>
            
            Keep each treatment type separate and clear.
            Include medical disclaimer at the end.
            Use simple formatting without excessive asterisks or markdown.
            """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def chat(self, user_message):
        symptoms = self.extract_symptoms(user_message)
        treatment_type = self.detect_treatment_type(user_message)
        
        # Always proceed with treatment, no more "describe symptoms" message
        return self.get_treatment(symptoms, treatment_type)

def main():
    print("🏥 Ayurvedic Health Chatbot")
    print("=" * 60)
    print("💬 Supported treatment types:")
    print("   • Ayurvedic")
    print("   • Homeopathy") 
    print("   • Home Remedies")
    print("📝 Example queries:")
    print("   • 'I have fever and headache'")
    print("   • 'ayurvedic treatment for cold'")
    print("   • 'home remedies for stomach pain'")
    print("   • 'homeopathy for anxiety'")
    print("🚪 Type 'quit', 'exit', or 'bye' to leave")
    print("=" * 60)
    
    # Initialize chatbot with your API key
    bot = HealthChatbot("AIzaSyCLcDWRmx4F-aHMuXqj0Ot8VGkYEateK8w")
    
    print("\n🤖 How can I help you today?")
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n👋 Take care! Stay healthy! 🌿")
                break
            
            if not user_input:
                print("🤖 Please tell me about your symptoms...")
                continue
            
            print("\n🤖 Bot: ", end="")
            response = bot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Stay healthy! 🌿")
            break
        except Exception as e:
            print(f"\n❌ Sorry, I encountered an error: {e}")
            print("🤖 Please try again or rephrase your question.")

if __name__ == "__main__":
    main()
