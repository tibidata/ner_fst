"""
Module: Finite State Transducer (FST)
-------------------------------------
This module implements a Finite State Transducer (FST) for Named Entity Recognition (NER) 
and similar text processing tasks. The FST is configured using an external configuration 
class and processes input text to extract labeled entities based on defined states and transitions.
"""

from typing import List, Tuple
from .config import TransducerConfig
from .state import State


class FiniteStateTransducer:
    """
    A Finite State Transducer (FST) for processing input text and extracting structured information
    based on predefined states and transitions.

    Attributes:
        states (dict): A mapping of state names to State objects.
        current_state (State): The current active state of the FST during processing.
        config (dict): Configuration data for states, transitions, and the initial state.
    """

    def __init__(self, config: TransducerConfig) -> None:
        """
        Initializes the Finite State Transducer by setting up states, transitions,
        and the initial state based on the configuration.
        """
        self.states: dict[str, State] = {}
        self.current_state: State | None = None

        # Load configuration and setup states and transitions
        self.config = config.config
        self.__setup_states()
        self.__setup_transitions()
        self.__set_initial_state(self.config["initial_state"])

    def __call__(self, process: str = "NER", **kwargs) -> List[Tuple[str, str]]:
        """
        Allows the FST to be called directly for processing input text.

        Args:
            process (str): The type of processing to perform. Defaults to "NER".
            kwargs: Additional arguments, such as `input_text` for processing.

        Returns:
            List[Tuple[str, str]]: A list of extracted entities and their labels.
        """
        if process == "NER":
            return self.__process(input_text=kwargs.get("input_text"))
        raise ValueError(f"Unsupported process type: {process}")

    def __str__(self) -> str:
        """
        Returns a string representation of the FST configuration.

        Returns:
            str: The configuration of the Finite State Transducer as a string.
        """
        return f"{self.config}"

    def __setup_states(self) -> None:
        """
        Sets up the states of the FST based on the configuration.
        """
        for state_name, is_final in self.config["states"]:
            self.__add_state(state_name, is_final)

    def __setup_transitions(self) -> None:
        """
        Sets up the transitions between states based on the configuration.
        """
        for from_state, regex, to_state, *output in self.config["transitions"]:
            self.__add_transition(
                from_state, regex, to_state, output[0] if output else None
            )

    def __add_state(self, name: str, is_final: bool = False) -> None:
        """
        Adds a state to the FST.

        Args:
            name (str): The name of the state.
            is_final (bool): Whether the state is a final state. Defaults to False.
        """
        self.states[name] = State(name, is_final)

    def __set_initial_state(self, name: str) -> None:
        """
        Sets the initial state of the FST.

        Args:
            name (str): The name of the initial state.
        """
        self.current_state = self.states[name]

    def __add_transition(
        self, from_state: str, regex: str, to_state: str, output: str | None = None
    ) -> None:
        """
        Adds a transition between two states with a regex-based condition.

        Args:
            from_state (str): The name of the starting state.
            regex (str): The regex condition for the transition.
            to_state (str): The name of the destination state.
            output (str | None): Optional output label for the transition.
        """
        self.states[from_state].add_transition(regex, self.states[to_state], output)

    def __process(self, input_text: str) -> List[Tuple[str, str]]:
        """
        Processes the input text using the FST and extracts labeled entities.

        Args:
            input_text (str): The input text to process.

        Returns:
            List[Tuple[str, str]]: A list of tuples where each tuple contains a detected
            entity and its corresponding label.
        """
        results: List[Tuple[str, str]] = []
        tokens = input_text.split()

        tokens = [token.strip(".") for token in tokens]

        buffer: List[str] = []
        category: str | None = None

        for token in tokens:
            next_state, output = self.current_state.get_next_state(token)
            if next_state:
                # Transition to the next state
                self.current_state = next_state
                buffer.append(token)
                if output:
                    category = output
            else:
                # Flush buffer when no valid transition is found
                if buffer and category:
                    results.append((" ".join(buffer), category))
                # Reset to initial state
                self.current_state = self.states["q0"]
                buffer, category = [], None
                # Reattempt processing for the current token
                next_state, output = self.current_state.get_next_state(token)
                if next_state:
                    self.current_state = next_state
                    buffer.append(token)
                    if output:
                        category = output

        # Handle any remaining buffer after processing
        if buffer and category:
            results.append((" ".join(buffer), category))

        return results
