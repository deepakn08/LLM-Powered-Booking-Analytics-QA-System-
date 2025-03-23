# LLM-Powered-Booking-Analytics-QA-System-

## Overview  
Developed a system that processes hotel booking data, extracts insights, and enables Question Answering from the data. The system should provide analytics as mentioned in below sections and answer user queries about the data.

---

## Features  

   ✅ Generating the analytics reports on the basis of the question asked.
   
   ✅ Giving the insights from the data on the basis of the CSV file. 
   
   ✅ Implemented the fast-api at the end.
   
---
## Working 
1. **Generating the Analytics Report** 📰
   - Ploting the distribution of the insights from the data like Revenue Trend, Geographical Distribution, Lead Time Distribution.
   - Creating Plot using **Fast-API**. 

3. **Question Answering from the CSV data** ✍️  
   - Question Answering based on insights of the question
   - Generating the user query into **SQL-Query**.
   - Using this query to fetch data from **SQL-Database**.
   - Uses **Groq API** to generate concise, structured summaries.  
   - Performing Question Answering using **Fast-API**.  
---

## Run Locally  
### Clone the project  
```bash
git clone https://github.com/deepakn08/LLM-Powered-Booking-Analytics-QA-System-
```  

### Go to the project directory  
```bash
cd LLM-Powered-Booking-Analytics-QA-System-
```  

### Install dependencies  
```bash
pip install -r requirements.txt
```  

### Set up environment variables  
Create a `.env` file and add necessary API keys and configurations (e.g., **Groq API key**).  

### Start the analytics api
```bash
final_analytics.py
```
### Start the rag api
```bash
final_rag.py
``` 
This will start the **API for question answering on Hotel Booking Data** that will fetch, summarize and plot of the analytics report.

---
