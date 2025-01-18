from presidio_analyzer import Pattern, PatternRecognizer
from typing import Optional, List, Tuple

class EnhancedPhoneRecognizer(PatternRecognizer):
    def __init__(self, supported_language: str):
        # Wspólne wzorce dla obu języków
        patterns = [
            Pattern(
                "BASIC_PHONE",
                r'\b\d{7,12}\b',
                0.6
            ),
            Pattern(
                "SPACED_PHONE",
                r'\b\d{3}[\s-]?\d{3}[\s-]?\d{3}\b',
                0.7
            ),
            Pattern(
                "PHONE_WITH_PREFIX",
                r'\b(\+?\d{2})?[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3}\b',
                0.8
            )
        ]
        
        # Dodatkowe wzorce specyficzne dla języka
        if supported_language == "pl":
            patterns.extend([
                Pattern(
                    "PL_MOBILE",
                    r'\b(?:45|50|51|53|57|60|66|69|72|73|78|79|88)\d{7}\b',
                    0.9
                ),
                Pattern(
                    "PL_LANDLINE",
                    r'\b(?:12|13|14|15|16|17|18|22|23|24|25|29|32|33|34|41|42|43|44|46|47|48|52|54|55|56|58|59|61|62|63|65|67|68|71|74|75|76|77|81|82|83|84|85|86|87|89|91|92|93|94|95)\d{7}\b',
                    0.9
                )
            ])
        elif supported_language == "en":
            patterns.extend([
                Pattern(
                    "US_PHONE",
                    r'\b(?:\+1|1)?[\s-]?\(?([0-9]{3})\)?[\s-]?([0-9]{3})[\s-]?([0-9]{4})\b',
                    0.9
                ),
                Pattern(
                    "UK_PHONE",
                    r'\b(?:\+44|44)?[\s-]?\(?([0-9]{4})\)?[\s-]?([0-9]{6})\b',
                    0.9
                )
            ])

        super().__init__(
            supported_entity="PHONE_NUMBER",
            patterns=patterns,
            supported_language=supported_language,
            name=f"Enhanced Phone Recognizer ({supported_language.upper()})"
        )

    def validate_result(self, pattern_text: str) -> Optional[bool]:
        clean_number = ''.join(filter(str.isdigit, pattern_text))
        
        if len(clean_number) < 7 or len(clean_number) > 15:
            return False
            
        if self.supported_language == "pl":
            if len(clean_number) == 9:
                valid_prefixes = {'45','50','51','53','57','60','66','69','72','73','78','79','88',
                                '12','13','14','15','16','17','18','22','23','24','25','29','32',
                                '33','34','41','42','43','44','46','47','48','52','54','55','56',
                                '58','59','61','62','63','65','67','68','71','74','75','76','77',
                                '81','82','83','84','85','86','87','89','91','92','93','94','95'}
                return clean_number[:2] in valid_prefixes
                
        return True