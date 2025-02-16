import openai
import csv
import os

def get_redevelopment_options(api_key, location):
    client = openai.OpenAI(api_key=api_key)  # Initialize the OpenAI client
    
    prompt = (
        "Persona:\n"
        "You are an expert in urban planning and redevelopment with a focus on brownfield sites. "
        "Only speak in lists of recommendations. Do not give details.\n\n"
        "Rules:\n"
        "• When a user inputs a location, find zoning laws, usage policies, and other regulations relevant to that location.\n"
        "• Provide an organized, comprehensive list of redevelopment possibilities.\n"
        "• Avoid technical legal jargon but remain precise and informative.\n"
        "• Maintain objectivity and advise that users consult legal experts for final decisions.\n\n"
        "Task/Goal:\n"
        "Analyze the provided brownfield site's location and, based on general zoning laws and usage policies, "
        "generate a tailored list of legal redevelopment possibilities. The tool’s objective is to inform users of "
        "potential redevelopment options that comply with zoning regulations, guiding them toward possible actionable paths "
        "and further professional review."
    )
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI specialized in urban planning and zoning laws."},
            {"role": "user", "content": f"Location: {location}\n\n{prompt}"}
        ]
    )
    
    redevelopment_options = response.choices[0].message.content.strip().split("\n")
    return redevelopment_options

def save_to_csv(location, options, output_filename="redevelopment_options.csv"):
    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Location", "Redevelopment Option"])
        for option in options:
            writer.writerow([location, option])
    print(f"Data saved to {output_filename}")

def main():
    api_key = os.getenv("OPENAI_API_KEY")  # Store API key as an environment variable
    if not api_key:
        api_key = input("Enter your OpenAI API key: ")
    
    location = input("Enter the brownfield location address: ")
    redevelopment_options = get_redevelopment_options(api_key, location)
    save_to_csv(location, redevelopment_options)
    print("Redevelopment options have been successfully generated and saved.")
    print(redevelopment_options)
    print(location)

if __name__ == "__main__":
    main()
