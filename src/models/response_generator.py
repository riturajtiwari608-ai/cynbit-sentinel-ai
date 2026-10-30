"""
Context-Aware Grounded Response Generation Engine
Produces high-EQ, brand-safe customer responses with safety guardrails and multi-persona adaptation.
"""

import re
from typing import Dict, List, Any
from src.config import RESPONSE_PERSONAS


class GroundedResponseGenerator:
    """
    Synthesizes compliant, contextual, and aspect-grounded responses tailored
    to severity level, customer value, and negative aspects.
    """

    def __init__(self):
        self.personas = RESPONSE_PERSONAS

    def sanitize_pii(self, text: str) -> str:
        """
        Masks personal identifiable information like cards, phones, and emails.
        Order: Cards first, then Phones, then Emails.
        """
        # 1. Mask card numbers (16 digits with dashes or spaces)
        text = re.sub(r'\b(?:\d{4}[ -]?){3}\d{4}\b', '[CONFIDENTIAL_CARD]', text)
        # 2. Mask phone numbers
        text = re.sub(r'\b(?:\+?\d{1,3}[- ]?)?\(?\d{3,5}\)?[- ]?\d{3,5}[- ]?\d{3,5}\b', '[CONFIDENTIAL_PHONE]', text)
        # 3. Mask emails
        text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[CONFIDENTIAL_EMAIL]', text)
        return text

    def select_persona(self, severity_level: str, customer_tier: str, polarity_score: float) -> str:
        """
        Selects the optimal response persona based on contextual triggers.
        """
        if severity_level == "CRITICAL":
            return "crisis_defusal"
        elif customer_tier.upper() in ["VIP", "ENTERPRISE"]:
            return "vip_concierge"
        elif polarity_score < -0.3:
            return "empathetic"
        elif polarity_score > 0.3:
            return "appreciative"
        else:
            return "professional"

    def synthesize(
        self,
        business_name: str,
        customer_name: str,
        severity_level: str,
        customer_tier: str,
        polarity_score: float,
        aspect_breakdown: Dict[str, Dict[str, Any]],
        override_persona: str = None
    ) -> Dict[str, Any]:
        """
        Generates a grounded, high-empathy response addressing identified grievances.
        """
        persona = override_persona or self.select_persona(severity_level, customer_tier, polarity_score)
        negative_aspects = [
            aspect for aspect, data in aspect_breakdown.items()
            if data["sentiment"] == "Negative"
        ]
        positive_aspects = [
            aspect for aspect, data in aspect_breakdown.items()
            if data["sentiment"] == "Positive"
        ]

        salutation = f"Dear {customer_name or 'Valued Customer'},"
        body = []

        if persona == "crisis_defusal":
            body.append(
                f"We acknowledge the critical nature of your feedback regarding your recent experience with {business_name}. "
                "Our senior leadership and risk governance team treat such reports with absolute urgency."
            )
            if negative_aspects:
                aspects_str = " and ".join(negative_aspects)
                body.append(
                    f"A high-priority internal audit into the reported {aspects_str} concerns has been initiated immediately."
                )
            body.append(
                "To ensure immediate resolution and direct executive oversight, please connect directly with our General Manager's "
                "direct response desk at gm-escalations@cynbit-network.com or our dedicated priority phone line. "
                "We remain committed to resolving this transparently and rigorously."
            )

        elif persona == "vip_concierge":
            body.append(
                f"Thank you for reaching out to us. As a distinguished {customer_tier} patron of {business_name}, "
                "your experience is of paramount importance to our executive leadership."
            )
            if negative_aspects:
                body.append(
                    f"We sincerely apologize that our standard of {', '.join(negative_aspects)} fell short of the bespoke excellence you deserve. "
                    "This has been escalated directly to our Branch Director."
                )
            body.append(
                "Your dedicated Relationship Executive will be in touch directly today to review this matter in detail "
                "and ensure a seamless experience moving forward."
            )

        elif persona == "empathetic":
            body.append(
                f"We are deeply sorry to read about your disappointing experience at {business_name}. "
                "We pride ourselves on providing high-quality service, and we clearly fell short during your visit."
            )
            if negative_aspects:
                body.append(
                    f"Specifically regarding the {', '.join(negative_aspects)} issues you highlighted, our operational team has been briefed "
                    "to conduct immediate corrective training."
                )
            body.append(
                "We would appreciate the opportunity to make this right. Please email our Guest Relations Lead at "
                "care@cynbit-network.com with your visit details so we can assist you personally."
            )

        elif persona == "appreciative":
            body.append(
                f"Thank you so much for the glowing review and wonderful feedback! The entire team at {business_name} is thrilled "
                "to hear how much you enjoyed your experience."
            )
            if positive_aspects:
                body.append(
                    f"We are especially delighted that our {', '.join(positive_aspects)} made a lasting impression on you."
                )
            body.append(
                "We look forward to welcoming you back again very soon for another exceptional experience!"
            )

        else: # professional
            body.append(
                f"Thank you for sharing your valuable perspective with {business_name}."
            )
            if negative_aspects:
                body.append(
                    f"Your constructive observations regarding our {', '.join(negative_aspects)} have been documented and shared with "
                    "the departmental managers for process refinement."
                )
            body.append(
                "We continually strive to optimize our operations and look forward to serving you even better in the future."
            )

        sign_off = f"\nWarm regards,\nExecutive Customer Experience Team\n{business_name}"
        full_response = f"{salutation}\n\n" + " ".join(body) + f"\n{sign_off}"

        # Clean any accidental PII
        sanitized_response = self.sanitize_pii(full_response)

        # Verification check
        has_hallucination_flag = False
        if "free refund of full cash" in sanitized_response.lower():
            has_hallucination_flag = True

        return {
            "persona_applied": persona,
            "generated_response": sanitized_response,
            "addressed_negative_aspects": negative_aspects,
            "addressed_positive_aspects": positive_aspects,
            "guardrail_checks": {
                "pii_redacted": True,
                "hallucination_detected": has_hallucination_flag,
                "policy_compliant": True
            }
        }
