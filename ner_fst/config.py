"""
Module: Transducer Configuration
---------------------------------
This module defines the `TransducerConfig` class, which provides the configuration 
for a Finite State Transducer (FST). The configuration includes states, the initial 
state, and transitions with associated regex patterns and optional outputs.
"""

from typing import List, Tuple, Optional


class TransducerConfig:
    """
    Manages the configuration for a Finite State Transducer (FST), including states, transitions,
    and the initial state. Allows for dynamic modification of states and transitions.
    """

    def __init__(self) -> None:
        """
        Initializes the TransducerConfig with predefined states, an initial state,
        and transitions. These definitions are used to control the behavior of the FST.
        """
        self.config = {
            "states": [
                ("q0", False),  # Initial state
                ("q1_person", False),  # Intermediate state for person names
                ("q_date", True),  # Final state for dates
                ("q2_person", True),  # Final state for person names
                ("q_email", True),  # Final state for emails
                ("q_phone", True),  # Final state for phone numbers
                ("q_url", True),  # Final state for URLs
                ("q_number", False),  # Intermediate state for numbers
                ("q_currency", True),  # Final state for currency values
                ("q_postalcode", False),  # Intermediate state for postal codes
                ("q_city", False),  # Intermediate state for cities
                ("q_street", False),  # Intermediate state for street names
                ("q_street_type", False),  # Intermediate state for street types
                ("q_address", True),  # Final state for complete addresses
            ],
            "initial_state": "q0",  # Define the initial state
            "transitions": [
                # Recognize phone numbers
                (
                    "q0",
                    r"(06|\+36)\d{2}[\s\-]?\d{3}[\s\-]?\d{4}",
                    "q_phone",
                    "PHONE_NUMBER",
                ),
                # Recognize numbers
                ("q0", r"\d+", "q_number"),
                # Recognize currency following a number
                (
                    "q_number",
                    r"\s?(forint|HUF|EUR|USD|dollars|euros|yen|pounds|GBP)",
                    "q_currency",
                    "PRICE",
                ),
                # Recognize postal codes
                ("q0", r"\d{4},?", "q_postalcode", "POSTALCODE"),
                # Recognize city names after postal codes
                (
                    "q_postalcode",
                    r"[A-Z][a-z]+(?: [A-Za-z]+)*,?",
                    "q_city",
                    "CITY",
                ),
                # Recognize street names after city names
                ("q_city", r"[A-Za-z\s]+", "q_street", "ADDRESS"),
                # Recognize street types after street names
                (
                    "q_street",
                    r"(utca|tér|út|körút)",
                    "q_street_type",
                    "ADDRESS",
                ),
                # Recognize house numbers after street types
                ("q_street_type", r"\d+", "q_address", "ADDRESS"),
                # Recognize person first names
                ("q0", r"[A-Z][a-z]+", "q1_person"),
                # Recognize optional middle names
                ("q1_person", r"[A-Z][a-z]+", "q1_person", "PERSON"),
                # Recognize last names
                ("q1_person", r"[A-Z][a-z]+", "q2_person", "PERSON"),
                # Recognize email addresses
                (
                    "q0",
                    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                    "q_email",
                    "EMAIL",
                ),
                # Recognize dates in MM/DD/YYYY format
                (
                    "q0",
                    r"(\d{4}[.\-]?\d{2}[.\-]?\d{2}|\d{2}[.\-]?\d{2}[.\-]?\d{4}|\d{2}/\d{2}/\d{4})",
                    "q_date",
                    "DATE",
                ),
                # Recognize URLs
                (
                    "q0",
                    r"https?://[A-Za-z0-9.-]+(?:/[A-Za-z0-9&%_./-]*)?",
                    "q_url",
                    "URL",
                ),
            ],
        }

    def get_initial_state(self) -> str:
        """
        Returns the initial state of the transducer.

        Returns:
            str: The name of the initial state.
        """
        return self.config["initial_state"]

    def add_state(self, state_name: str, is_final: bool = False) -> None:
        """
        Adds a new state to the configuration.

        Args:
            state_name (str): The name of the new state.
            is_final (bool): Whether the state is a final state. Default is False.
        """
        self.config["states"].append((state_name, is_final))

    def add_transition(
        self, from_state: str, regex: str, to_state: str, output: Optional[str] = None
    ) -> None:
        """
        Adds a new transition to the configuration.

        Args:
            from_state (str): The starting state for the transition.
            regex (str): The regular expression that triggers the transition.
            to_state (str): The target state for the transition.
            output (Optional[str]): The output label for the transition. Default is None.
        """
        transition = (from_state, regex, to_state) + ((output,) if output else ())
        self.config["transitions"].append(transition)

    def get_states(self) -> List[Tuple[str, bool]]:
        """
        Retrieves the list of states in the configuration.

        Returns:
            List[Tuple[str, bool]]: A list of states, each represented
              as a tuple (state_name, is_final).
        """
        return self.config["states"]

    def get_transitions(self) -> List[Tuple[str, str, str, Optional[str]]]:
        """
        Retrieves the list of transitions in the configuration.

        Returns:
            List[Tuple[str, str, str, Optional[str]]]: A list of transitions,
              each represented as a tuple
            (from_state, regex, to_state, optional_output).
        """
        return self.config["transitions"]
