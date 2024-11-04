
# Politician and Organization Relationship Analyzer

## Overview

The **Politician and Organization Relationship Analyzer** is a Python-based project that utilizes Natural Language Processing (NLP) and graph theory to analyze and visualize relationships between politicians and various organizations. The tool scrapes data from online sources, extracts entities from the collected text, identifies direct and indirect relationships, and visualizes these connections in a clear and informative manner.

## Features

- **Data Scraping**: Includes a `scrape_data` script that gathers relevant articles and text data from specified online sources for analysis.
- **Entity Extraction**: Utilizes spaCy for Named Entity Recognition (NER) to identify politicians, organizations, locations, nationalities, monetary values, and dates from the scraped text.
- **Relationship Mapping**: Constructs a graph representation of the relationships, including direct collaborations and campaign finance ties.
- **Graph Analysis**: Identifies the largest connected component of the graph to focus on the most significant relationships.
- **High-Quality Visualizations**: Produces clear and high-definition graphs using Matplotlib and NetworkX, with customizable node colors and sizes to distinguish between different entity types.

## Requirements

To run this project, ensure you have the following Python packages installed:

- `matplotlib`
- `networkx`
- `spacy`

You can install the necessary libraries using pip:

```bash
pip install matplotlib networkx spacy
```

Additionally, download the spaCy English language model:

```bash
python -m spacy download en_core_web_sm
```

## Usage

1. **Data Scraping**: Run the `scrape_data.py` script to gather articles from the specified online sources. Ensure to configure the script according to the sources you wish to scrape.
2. **Data Analysis**: Execute the main analysis script to process the scraped data, extract entities, and generate the relationship graph.
3. **View the Graph**: The resulting graph will be displayed and saved as a high-resolution PNG file.

## Example Output

The project generates visualizations that clearly display the relationships among politicians and organizations, highlighting the largest connected component to enhance readability and comprehension.

## Contributing

Contributions to enhance the functionality of the Politician and Organization Relationship Analyzer are welcome! Please fork the repository and submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License.
