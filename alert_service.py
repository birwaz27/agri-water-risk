import os

class AlertService:
    """
    Multilingual SMS and Voice Alert Dispatcher for Farm Risk Warnings
    """
    def __init__(self):
        self.api_key = os.getenv("SMS_API_KEY", "demo_key")
        
        # Pre-configured templates in Kannada
        self.templates = {
            "High": "ಖಚಿತ ಎಚ್ಚರಿಕೆ: ನಿಮ್ಮ ಕೃಷಿ ಕೊಳದಲ್ಲಿ ನೀರಿನ ಅಪಾಯದ ಮಟ್ಟ ಹೆಚ್ಚಾಗಿದೆ. ತಕ್ಷಣ ಗಾಳಿ ಯಂತ್ರವನ್ನು ಚಾಲನೆ ಮಾಡಿ.",
            "Medium": "ಎಚ್ಚರಿಕೆ: ನಿಮ್ಮ ಕೊಳದಲ್ಲಿ ನೀರಿನ ಗುಣಮಟ್ಟ ಬದಲಾಗುತ್ತಿದೆ. ಮುಂದಿನ 12 ಗಂಟೆಗಳಲ್ಲಿ ಪರಿಶೀಲಿಸಿ."
        }

    def format_kannada_alert(self, risk_level: str) -> str:
        """Returns localized alert text based on risk severity."""
        return self.templates.get(risk_level, "ನೀರಿನ ಸ್ಥಿತಿ ಸಾಮಾನ್ಯವಾಗಿದೆ.")

    def send_sms(self, phone_number: str, risk_level: str) -> dict:
        """Simulates sending SMS via Fast2SMS/Twilio API gateway."""
        message = self.format_kannada_alert(risk_level)
        
        return {
            "phone": phone_number,
            "message": message,
            "status": "sent",
            "gateway_response": "200 OK"
        }
