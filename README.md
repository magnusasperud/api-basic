# Databricks Data Retrieval API

This project is a Flask API that allows users to interact with data stored in Databricks. It provides endpoints for deleting employees and retrieving data from Databricks based on the provided schema and table.

## Installation

Install the required packages by running:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python run.py
```

## API Endpoints

- `DELETE /employee/<int:emp_id>`: Deletes an employee with the given ID.
- `GET /get_data`: Retrieves data from Databricks. Requires `schema` and `table` parameters. Optional `limit` and `skip` parameters for pagination.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.