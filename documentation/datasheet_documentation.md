# Summary

Initially we identified several categories of datasheets, including **Stainless Steel, Nickel** **Alloy**, **Special Purpose Grade**s, **Low Alloy and Mild Steel**, and **Technical Brochures** total 163 datasheets.we incorporated a Safety Datasheet category without further subcategories. To organize this information effectively, we manually created a Google Sheet that captured essential fields such as **chunk\_no, chunk\_title, text\_content, html\_content** and **datasheet\_id** for all categories.

Furthermore, we created a separate **datasheet\_index** Google Sheet that listed all datasheet names alongside their corresponding IDs. These IDs were then utilized to populate the **`datasheet_id`** field in the original datasheet data, ensuring seamless integration with the **`chunk_no`** and **`chunk_title`** fields. After populating the sheets with the relevant data, we exported them as CSV files. Each category was organized into separate CSV files for clarity, which were then converted into pickle files for more efficient storage and retrieval in our application.

Once the pickle files were created, we proceeded to upload the data to Azure AI Search. This involved extracting relevant information from the pickle files, generating embeddings for the text content using OpenAI's API, and inserting the structured data into the Azure Search index. This step allowed the datasheets to be easily searchable and accessible through Azure's AI-powered search functionalities, ensuring efficient data retrieval and enabling more advanced search capabilities within the application.

# Data Extraction 

## **Data Extraction Process**

To effectively manage and organize the datasheets, we began with a manual extraction process. This involved identifying and categorizing datasheets into specific groups. The categories we established included:

* **Stainless Steel**  
* **Nickel Alloy**  
* **Special Purpose Grades**  
* **Low Alloy and Mild Steel**  
* **Technical Brochures**  
* **Safety Datasheets**

Each of these categories was carefully reviewed, and relevant information was collected and structured into essential fields within the Google Sheets.

**Google Sheets Organization**

To streamline the management of datasheets, we created two Google Sheets:

1. **Main Datasheet Google Sheet**: This sheet included fields such as:  
   * `chunk_no`  
   * `chunk_title`  
   * `text_content`  
   * `html_content`  
   * `datasheet_id`  
2. **Datasheet Index Google Sheet**: This sheet provided a comprehensive mapping of all datasheet names and their corresponding IDs.

These IDs were used to populate the `datasheet_id` field in the main datasheet, ensuring seamless integration with the chunk data.

## **Export and Conversion to Pickle Files**

Once the Google Sheets were populated with the relevant data, we exported the sheets as **CSV files**. To ensure clarity and ease of use, each category (e.g., Stainless Steel, Nickel Alloy, etc.) was organized into its own CSV file. The following code demonstrates how we converted these CSV files into **pickle files** for efficient storage and quick retrieval within the application:

| import osimport pickleimport pandas as pdfrom django.core.management.base import BaseCommandclass Command(BaseCommand):    help \= "Convert CSV files to pickle files"    def add\_arguments(self, parser):        parser.add\_argument(            "csv\_dir\_path", type=str, help="Directory containing CSV files"        )        parser.add\_argument(            "pickle\_base\_path",            type=str,            help="Base directory to store pickle files",        )    def handle(self, \*args, \*\*options):        csv\_dir\_path \= options\["csv\_dir\_path"\]        pickle\_base\_path \= options\["pickle\_base\_path"\]        if not os.path.exists(pickle\_base\_path):            self.stdout.write(                f"Creating base pickle directory: {pickle\_base\_path}"            )            os.makedirs(pickle\_base\_path)        else:            self.stdout.write(                f"Base pickle directory already exists: {pickle\_base\_path}"            )        self.convert\_csvs\_to\_pickle(csv\_dir\_path, pickle\_base\_path)    def convert\_csvs\_to\_pickle(self, dir\_path, pkl\_base\_path):        """        Read the contents from CSV files and save them as pickle files.        Datastructure format:        \[            {                "root\_dict": {                    "level\_1": "category\_name",                    "level\_2": "subcategory\_name",                    ...                },                "datasheet\_name": "name\_of\_the\_datasheet",                "file\_name": "name\_of\_the\_file\_without\_extension",                "chunks": \[                    {                        "chunk\_no": "chunk\_number",                        "chunk\_title": "chunk\_title",                        "text\_content":                        "html\_content":                    }                \]            }        \]        Args:            dir\_path (str): Directory containing CSV files.            pkl\_base\_path (str): Base directory to store pickle files.        """        csv\_files \= \[\]        for root, \_, files in os.walk(dir\_path):            for file in files:                if not file.lower().endswith(".csv"):                    self.stdout.write(f"Skipping non-CSV file: {file}")                    continue                self.stdout.write(f"Processing CSV file: {file}")                csv\_dict \= {}                csv\_file\_path \= os.path.join(root, file)                root\_list \= root.split(os.path.sep)\[2:\]                root\_dict \= {                    f"level\_{idx}": item                    for idx, item in enumerate(root\_list, 1)                }                self.stdout.write(f"Root dict: {root\_dict}")                try:                    df \= pd.read\_csv(csv\_file\_path)                except Exception as e:                    self.stdout.write(                        self.style.ERROR(                            f"Error reading CSV file {csv\_file\_path}: {e}"                        )                    )                    continue                self.stdout.write(f"Dataframe columns: {df.columns}")                if (                    "datasheet\_name" not in df.columns                    or "chunk\_no" not in df.columns                ):                    self.stdout.write(                        self.style.ERROR(                            f"Missing expected columns in {csv\_file\_path}"                        )                    )                    continue                csv\_dict\["datasheet\_name"\] \= df\["datasheet\_name"\].iloc\[0\]                csv\_dict\["file\_name"\] \= file.replace(".csv", "")                csv\_dict\["datasheet\_id"\] \= int(df\["datasheet\_id"\].iloc\[0\])                csv\_dict\["chunks"\] \= \[\]                for \_, row in df.iterrows():                    csv\_dict\["chunks"\].append(                        {                            "chunk\_no": row\["chunk\_no"\],                            "chunk\_title": row\["chunk\_title"\],                            "text\_content": f"Datasheet name: {row\['datasheet\_name'\]}\\n{row\['text\_content'\]}",                            "html\_content": (                                f"Datasheet name: {row\['datasheet\_name'\]}\\n{row\['html\_content'\]}"                                if not pd.isna(row\["html\_content"\])                                else None                            ),                        }                    )                csv\_dict\["root\_list"\] \= root\_list                csv\_dict\["root\_dict"\] \= root\_dict                csv\_files.append(csv\_dict)        pickle\_file\_path \= os.path.join(            pkl\_base\_path, "low\_alloy\_mild\_steel.pkl"        )        self.stdout.write(f"Saving pickle file to: {pickle\_file\_path}")        try:            with open(pickle\_file\_path, "wb") as f:                pickle.dump(csv\_files, f)        except Exception as e:            self.stdout.write(                self.style.ERROR(f"Error saving pickle file: {e}")            )        else:            self.stdout.write(                self.style.SUCCESS(                    f"All contents from CSV files are extracted and saved into pickle file at {pickle\_file\_path}........"                )            ) |
| :---- |

##  **Inspecting Pickle File Contents**

## Once the CSV files have been successfully converted into pickle files, it is essential to verify the structure and content of these pickle files. Below is an example of how to load and print the contents of a pickle file in a readable format:

import pickle  
import json  
from pprint import pprint  
import pandas as pd  
file1 \= open('./datasheet\_files/stainless\_steel.pkl', 'rb')  
stainless\_steel\_data \= pickle.load(file1)  
for data in stainless\_steel\_data:  
  print(data)

**Example Output:**  
```json{  
    'datasheet\_name': 'MIDALLOY MASTERCOR™ E312T1-1/4 AP Flux-Cored Wire',  
    'file\_name': 'MASTERCOR\_sup\_™\_\_sup\_ 312T1-1\_4AP Data Sheet \- Sheet1',  
    'datasheet\_id': 11,  
    'chunks': \[  
        {  
            'chunk\_no': 1,  
            'chunk\_title': 'CLASSIFICATION',  
            'text\_content': 'Datasheet name: MIDALLOY MASTERCOR™ E312T1-1/4 AP Flux-Cored Wire\\n• AWS 5.22 Class E312T1-1 and E312T1-4 and ASME SFA 5.22 Class E312T1-1 and E312T1-4\\r\\nThis product can be run with 100% CO2 or 75% Argon 25% / CO2 (UNS W31331)',  
            'html\_content': None,  
            'datasheet\_id': '11'  
        },  
        {  
            'chunk\_no': 2,  
            'chunk\_title': 'DESCRIPTION',  
            'text\_content': 'Datasheet name: MIDALLOY MASTERCOR™ E312T1-1/4 AP Flux-Cored Wire\\n• MIDALLOY Mastercorä E312T1-1/4 AP is an all-position flux-cored wire used to weld all types of stainless steel,\\r\\nlow-alloy steel and high strength steel.\\r\\n• MIDALLOY Mastercorä E312T1-1/4 AP has excellent slag removal and runs with a spatter free globular transfer.',  
            'html\_content': None,  
            'datasheet\_id': '11'  
}\]}
```

# Uploading Data to Azure AI Search

Once the CSV files have been converted into pickle files and their contents have been inspected, the next step is to upload this data to Azure AI Search. This process involves extracting relevant information from the pickle files, generating embeddings for the text content, and then inserting the structured data into the Azure Search index.

Below is an example code snippet that demonstrates how to upload data from the `aluminum_welding.pkl` file into Azure AI Search:

| import picklefrom azure.search.documents import SearchClientimport openai\_client\_utilsfrom midalloy\_project import settings \# Load the pickle file containing the aluminum welding datasheetswith open('./datasheet\_files/aluminum\_welding.pkl', 'rb') as file1:    aluminum\_welding \= pickle.load(file1)\# Prepare a list to hold structured data for Azure Searchaluminum\_welding\_list \= \[\]for item in aluminum\_welding:    for chunk in item\["chunks"\]:        aluminum\_welding\_list.append(            {                "id": f"{item\['datasheet\_id'\]}-{chunk\['chunk\_no'\]}",                "datasheet\_id": str(item\['datasheet\_id'\]),                "datasheet\_name": item\["datasheet\_name"\],                "reference\_link": item.get("reference\_link", ""),                 "chunk\_no": str(chunk\["chunk\_no"\]),                "chunk\_title": chunk\["chunk\_title"\],                "text\_content": f'{chunk\["chunk\_title"\]}\\n{chunk\["text\_content"\]}',                "html\_content": f'{chunk\["chunk\_title"\]}\\n{chunk\["html\_content"\]}' if chunk\["html\_content"\] else "",            }        )\# Generate embeddings for the text content using OpenAI's APIinput\_texts \= \[x\['text\_content'\] for x in aluminum\_welding\_list\]embeddings\_node \= openai\_client\_utils.OpenAIEmbeddings(api\_key=settings.OPEN\_AI\_API\_KEY, input\_data=input\_texts)result, embeddings, log\_object \= embeddings\_node.get\_embeddings()\# Associate the embeddings with each item in the listfor idx, item in enumerate(aluminum\_welding\_list):    item\["text\_content\_embeddings"\] \= embeddings\[idx\].embedding\# Initialize the Azure Search clientsearch\_client \= SearchClient(endpoint=settings.AZURE\_SEARCH\_SERVICE\_ENDPOINT,                              index\_name="midalloy\_datasheets",                              credential=settings.AI\_SEARCH\_CREDENTIAL)\# Optionally, print the number of documents in the indexdocument\_count \= search\_client.get\_document\_count()print(f"Current document count in the index: {document\_count}")\# Upload the documents to the Azure Search indexresult \= search\_client.upload\_documents(documents=aluminum\_welding\_list)print(f"Uploaded {len(aluminum\_welding\_list)} documents to Azure AI Search.") |
| :---- |

### **Explanation:**

1. **Loading the Pickle File**: The code starts by loading the contents of `aluminum_welding.pkl` into a Python object.  
2. **Data Preparation**: Each chunk of data is organized into a dictionary, which is then appended to a list for easy management.  
3. **Embedding Generation**: The text content of the chunks is processed through the OpenAI API to create embeddings, which are included in the final data structure.  
4. **Azure Search Client Initialization**: The Azure Search client is set up using the service endpoint and credentials from your project settings.  
5. **Document Upload**: Finally, the prepared documents are uploaded to Azure AI Search using `search_client.upload_documents`.

