from flask import Flask, jsonify, request
import psycopg2
import yaml
import os

app = Flask(__name__)

# Database connection details
db_config = {
    'user': os.getenv("POSTGRES_USER", "postgres"),
    'password': os.getenv("POSTGRES_PASSWORD", "password"),
    'host': os.getenv("POSTGRES_HOST", "postgres-service"),
    'database': os.getenv("POSTGRES_DB", "mydb"),
    'port': os.getenv("POSTGRES_PORT", 5432)
}

# Load config mappings
def load_mappings():
    config_file = os.path.join(os.path.dirname(__file__), "config/mappings.yaml")
    with open(config_file, "r") as f:
        return yaml.safe_load(f).get("mappings", [])

mappings = load_mappings()

@app.route("/<string:endpoint>", methods=["GET"])
def handle_request(endpoint):
    try:
        # Find mapping for requested endpoint
        mapping = next((m for m in mappings if m["api_endpoint"].lstrip("/") == endpoint), None)
        if not mapping:
            return jsonify({"error": "Endpoint not found in mappings"}), 404

        query = mapping["query"]
        columns_map = mapping["columns"]

        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        # Transform DB rows -> JSON
        results = []
        for row in rows:
            row_dict = {}
            for db_col, value in zip(colnames, row):
                api_field = columns_map.get(db_col)
                if api_field:
                    row_dict[api_field] = value
            results.append(row_dict)

        cur.close()
        conn.close()
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
