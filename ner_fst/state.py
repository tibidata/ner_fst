"""
Module: State
-------------------------------------
Defines the `State` class, which represents a single state in a finite state transducer.
The `State` class supports transitions defined by regular expressions and provides 
methods to add transitions and determine the next state based on input text.
"""

import re
from typing import List, Tuple, Optional


class State:
    """
    Represents a state in a finite state transducer.

    Each state can have multiple transitions defined by regular expressions.
    The state keeps track of its name, whether it is a final state, and the transitions
    leading to other states.
    """

    def __init__(self, name: str, is_final: bool = False) -> None:
        """
        Initializes a state with a name, a flag indicating if it is a final state,
        and an empty list of transitions.

        Args:
            name (str): The name of the state.
            is_final (bool): Whether the state is a final state. Defaults to False.
        """
        self.name: str = name
        self.is_final: bool = is_final
        self.transitions: List[Tuple[str, "State", Optional[str]]] = []

    def add_transition(
        self, regex: str, next_state: "State", output: Optional[str] = None
    ) -> None:
        """
        Adds a transition from this state to another state.

        Args:
            regex (str): The regular expression to match the input triggering this transition.
            next_state (State): The state to transition to if the regex matches.
            output (Optional[str]): Optional output label for this transition. Defaults to None.
        """
        self.transitions.append((regex, next_state, output))

    def get_next_state(
        self, input_text: str
    ) -> Tuple[Optional["State"], Optional[str]]:
        """
        Determines the next state based on the given input text.

        Args:
            input_text (str): The input text to evaluate against the transitions.

        Returns:
            Tuple[Optional[State], Optional[str]]: The next state if a matching transition is found,
                                                  and the associated output label (if any).
                                                  Returns (None, None) if no transition matches.
        """
        for regex, next_state, output in self.transitions:
            if re.fullmatch(regex, input_text):
                return next_state, output
        return None, None
