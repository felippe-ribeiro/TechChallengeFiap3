import re

# Classe pra validar a seguranca do que o bot responde
class MedicalGuardrails:
    
    @staticmethod
    def check_prescription(response: str) -> str:
        # Se falar de remedio ou receita, bota o aviso de seguranca obrigatorio
        prescription_keywords = [
            "prescrevo", "tome", "ingira", "receito", "medicamento", 
            "antibiótico", "comprimido", "dose", "mg"
        ]
        
        found = any(word in response.lower() for word in prescription_keywords)
        
        if found:
            disclaimer = "\n\n[AVISO]: Isso é apenas uma orientação com base nos protocolos. Qualquer receita ou remédio precisa ser avaliado por um médico de verdade antes."
            if disclaimer not in response:
                return response + disclaimer
        
        return response

    @staticmethod
    def anonymize_data(text: str) -> str:
        # Tira dados pessoais como CPF pra ficar em conformidade
        text = re.sub(r'\d{3}\.\d{3}\.\d{3}-\d{2}', '[CPF ANONIMIZADO]', text)
        return text
