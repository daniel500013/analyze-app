from presidio_analyzer import Pattern, PatternRecognizer

class PolishIbanRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(
                "POLISH_IBAN_WITH_PREFIX",
                r'\bPL\d{26}\b',  # Format z prefiksem PL
                0.9
            ),
            Pattern(
                "POLISH_IBAN_SPACED",
                r'\b\d{2}(?:\s?\d{4}){6}\b',  # Format ze spacjami
                0.85
            ),
            Pattern(
                "POLISH_ACCOUNT",
                r'\b\d{26}\b',  # Format bez spacji
                0.85
            )
        ]
        
        super().__init__(
            supported_entity="PL_BANK_ACCOUNT",
            patterns=patterns,
            supported_language="pl",
            name="Polish IBAN Recognizer"
        )
        
    def validate_result(self, pattern_text: str) -> bool:
        # Usuń wszystkie spacje z numeru
        clean_number = ''.join(pattern_text.split())
        
        # Usuń prefiks PL jeśli istnieje
        if clean_number.startswith('PL'):
            clean_number = clean_number[2:]
            
        # Sprawdź czy zostało dokładnie 26 cyfr
        if len(clean_number) != 26:
            return False
            
        # Można dodać dodatkową walidację, np. sprawdzenie pierwszych cyfr dla konkretnych banków
        return True