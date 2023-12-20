import requests
import psycopg2
import json

def get_toxicity_result(api_key, text):

    api_url = "https://api.moderatehatespeech.com/api/v1/moderate/"
    headers = {
        "Content-Type": "application/json",
    }

    text_data = [str(item) for item in text]

    # Join the string representations with a separator (e.g., newline)
    result_text = ' '.join(text_data)
    result_text=result_text.replace('"', "'")
    payload = {
        "token": api_key,
        "text": result_text
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        return result

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print(response.content)  # Print the response content for debugging
        return None

def connect_to_database():
    # Replace with your PostgreSQL connection details
    connection = psycopg2.connect(
        host="localhost",
        database="reddit_data",
        user="kkamara1",
        password="12345"
    )


    return connection

def get_comments_from_database(connection):
    query = "SELECT four_chan.p_comment FROM four_chan where class='' OR class IS NULL;"

    with connection.cursor() as cursor:
        cursor.execute(query)
        comments = cursor.fetchall()

    return comments
# 
def update_toxicity_results_in_database(connection, comment, response, toxic_class, confidence):
    query = "UPDATE four_chan SET response = %s, class = %s, confidence = %s WHERE four_chan.p_comment = %s"
    confidence=float(confidence)
    with connection.cursor() as cursor:
        cursor.execute(query, (response, toxic_class, confidence, comment))
        connection.commit()
    print("row updated")




# Replace "YOUR_API_KEY" with your actual API key
api_key = "ff9d0c959510d06eeeba4ba5072a6054"

# Connect to PostgreSQL database
database_connection = connect_to_database()


# Get comments from the "reddit_data" table
comments = get_comments_from_database(database_connection)


# Iterate through comments and get toxicity result for each
for comment in comments:
    toxicity_result = get_toxicity_result(api_key, comment)
    if toxicity_result is not None:
        # print("+++++++++++++++++++++++++++++++++++++")
        # print("printing comments insidee for loop")
        # print(comment)
        # print("+++++++++++++++++++++++++++++++++++++++++")
        response = toxicity_result["response"]
        toxic_class = toxicity_result["class"]
        confidence = toxicity_result["confidence"]
        # Update the database with toxicity results
        update_toxicity_results_in_database(database_connection, comment, response, toxic_class, confidence)
        # print(f"Toxicity Result for Comment")
        # print("------------------------")
        # print(toxicity_result["response"])
        # print(toxicity_result["class"])
        # print(toxicity_result["confidence"])
        # print("--------------------")
    else:
        print(f"Toxicity measurement failed for Comments")
        print("--------------------")


# Close the database connection
database_connection.close()
