# Finite State Transducer (FST) for Named Entity Recognition (NER)

## Overview

This package implements a Finite State Transducer (FST) for Named Entity Recognition (NER). The `FiniteStateTransducer` class uses states and transitions based on regular expressions to process text and extract named entities like dates, phone numbers, email addresses, person names, and more.

FSTs are widely used in natural language processing (NLP) and other fields for tasks like tokenization, information extraction, and pattern matching. This package offers an easy-to-use framework for defining states, transitions, and processing text based on these configurations.

## Theory: What is a Finite State Transducer?

A **Finite State Transducer (FST)** is a type of finite state machine that produces output for each input symbol as it transitions between states. It consists of:
- **States**: Represent different situations or conditions in a system.
- **Transitions**: Define the rules for moving between states based on input data.
- **Input Alphabet**: The set of symbols that can trigger transitions.
- **Output Alphabet**: The set of symbols that are generated during transitions.

In this package, FST is used to recognize entities in text based on regular expressions, producing output labels for recognized entities (like "PERSON", "EMAIL", "DATE", etc.).

## Features

- Add states and transitions dynamically.
- Define regular expressions for each state transition.
- Support for recognizing multiple entity types (e.g., names, dates, phone numbers, etc.).
- Easily configurable via a configuration file (`config`).
- Output recognized tokens and categories (e.g., "PERSON", "EMAIL").

## Installation

To install this package, clone it from the repository:

```bash
git clone https://github.com/tibidata/fst-ner.git
```

## How It Works

1.	States: Each state represents a stage in the process of recognizing an entity. For example, q1_person is the state for recognizing a person’s first name, and q_date is the state for recognizing dates.
	
2.	Transitions: The transitions define rules to move between states based on input text. Each transition is triggered by a regular expression that matches part of the input text.

3.	Processing Text: The FST processes the input text token by token. For each token, it checks the current state and applies any transitions that match the token. If a transition matches, the state changes, and if there’s an output label, it is assigned to the token.

4.	Final Output: The FST produces a list of tuples, where each tuple consists of a recognized entity and its category (e.g., “PERSON”, “EMAIL”).

## Usage

```python
from ner_fst import FiniteStateTransducer, TransducerConfig

# Instantiate config class with default states
fst_config = TransducerConfig()

# Instantiate fst class with the config
fst = FiniteStateTransducer(config=fst_config)

# Example input
input_text = "Some example input text"

# Extract the entities
output = fst(process="NER", input_text=input_text)
```

## Default categories
### Extractable Entities with Category Codes and Examples

| **Entity**           | **Category Code** | **Example**                                |
|----------------------|-------------------|--------------------------------------------|
| **Person Name**       | `PERSON`          | `Kovács János`, `Nagy László`              |
| **Postal Code**       | `POSTALCODE`      | `1234`                                     |
| **City**              | `CITY`            | `Budapest`                                 |
| **Street Name**       | `ADDRESS`         | `Fő utca 56, 2. emelet`                    |
| **Street Type**       | `ADDRESS`         | `utca`, `tér`, `körút`                    |
| **Address**           | `ADDRESS`         | `Fő utca 56, 2. emelet`                    |
| **Currency**          | `PRICE`           | `3000 HUF`, `USD`, `EUR`                   |
| **Email**             | `EMAIL`           | `kovacs.janos@example.com`                 |
| **Date**              | `DATE`            | `2024.12.10`, `12/10/2024`                 |
| **Phone Number**      | `PHONE_NUMBER`    | `+36 30 123 4567`, `06 20 345 6789`        |
| **URL**               | `URL`             | `https://example.com`, `http://domain.org` |
| **Number**            | `NUMBER`          | `1000`, `42`, `500`                        |


## Adding new states and transitions

In addition to the default categories new categories can be added as in the following example:


```python
# Instantiate config class with default states
fst_config = TransducerConfig()

# Add a new state to the config
fst.add_state('q_new_state')

# Add a new transition to the config q0 is the initial state
fst.add_transition('q0', r'regex to find the category', 'q_new_state', 'NEWCATEGORY')
```

## Contributing

If you want to contribute to this package, feel free to fork the repository, create a branch, and submit a pull request.

## License

This package is licensed under the MIT License.