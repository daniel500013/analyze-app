from flask import Flask, request, jsonify
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngineProvider
from phone_recognizer import EnhancedPhoneRecognizer
from iban_recognizer import PolishIbanRecognizer
from presidio_analyzer.predefined_recognizers import (
    CreditCardRecognizer,
    EmailRecognizer,
    IbanRecognizer,
    IpRecognizer,
    NhsRecognizer,
    PhoneRecognizer,
    SpacyRecognizer,
    UsBankRecognizer,
    UsLicenseRecognizer,
    UsPassportRecognizer,
    UsItinRecognizer,
    UsSsnRecognizer,
    SgFinRecognizer,
    AuAbnRecognizer,
    AuAcnRecognizer,
    AuTfnRecognizer,
    CryptoRecognizer,
    UrlRecognizer
)

app = Flask(__name__)

# Ustawienia NLP
LANGUAGES_CONFIG_FILE = "languages-config.yml"

# Tworzenie NLP engine na podstawie pliku konfiguracyjnego
provider = NlpEngineProvider(conf_file=LANGUAGES_CONFIG_FILE)
nlp_engine_with_polish = provider.create_engine()

# Tworzenie rejestru recognizerów
registry = RecognizerRegistry(supported_languages=["en", "pl"])

    # Dodanie podstawowych recognizerów
recognizers = [
    EmailRecognizer(),           # Adresy email
    PhoneRecognizer(),           # Numery telefonów
    CreditCardRecognizer(),      # Numery kart kredytowych
    IbanRecognizer(),            # Numery IBAN
    IpRecognizer(),              # Adresy IP
    UrlRecognizer(),             # Adresy URL
    SpacyRecognizer(supported_entities=["PERSON", "ORG", "LOC"]),  # Tylko wybrane encje
    UsBankRecognizer(),          # Amerykańskie numery kont bankowych
    CryptoRecognizer(),          # Adresy kryptowalut
]

# Dodanie wbudowanych recognizerów
registry.add_recognizer(EnhancedPhoneRecognizer(supported_language="pl"))
registry.add_recognizer(EnhancedPhoneRecognizer(supported_language="en"))
registry.add_recognizer(PolishIbanRecognizer())

for recognizer in recognizers:
    registry.add_recognizer(recognizer)

# Tworzenie silnika analizy
analyzer = AnalyzerEngine(
    registry=registry,
    supported_languages=["en", "pl"],
    nlp_engine=nlp_engine_with_polish
)

@app.route('/analyze', methods=['POST'])
def analyze_text():
    try:
        data = request.json
        text = data.get('text')
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Wykonywanie analizy
        results = analyzer.analyze(
            text=text, 
            language="en",
            entities=[
                "PERSON",
                "PHONE_NUMBER",
                "EMAIL_ADDRESS",
                "CREDIT_CARD",
                "IBAN",
                "PL_BANK_ACCOUNT",
                "LOCATION",
                "ORGANIZATION",
                "IP_ADDRESS",
                "URL",
                "CRYPTO"
            ]
        )

        # Przetwarzanie wyników
        detected_entities = []
        for result in results:
            detected_entities.append({
                "type": result.entity_type,
                "start": result.start,
                "end": result.end,
                "score": result.score,
                "value": text[result.start:result.end]
            })

        return jsonify({"detected_entities": detected_entities}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
