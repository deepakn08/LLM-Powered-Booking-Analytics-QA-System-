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
   - Creating Reports using **Fast-API** Interface. 

3. **Question Answering from the CSV data** ✍️  
   - Question Answering based on insights of the question
   - Generating the user query into **SQL-Query**.
   - Using this query to fetch data from **SQL-Database**.
   - Uses **Groq API** to generate concise, structured summaries.  
   - Generating the UI using **Fast-API**.  
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
### Results

![Screenshot 2025-03-24 022211](https://github.com/user-attachments/assets/fce19dfd-db17-43e3-8d48-f3537402b724)
![Screenshot 2025-03-24 022159](https://github.com/user-attachments/assets/4ae41e68-c11a-4154-a6d3-68c6f165a851)
![Screenshot 2025-03-24 022412](https://github.com/user-attachments/assets/286dd473-fef3-4704-b344-b7d89ce0f00e)
![Screenshot 2025-03-24 022419](https://github.com/user-attachments/assets/96d8fa70-7fc2-4e0d-8d95-1d7c059bf882)
![Screenshot 2025-03-24 022441](https://github.com/user-attachments/assets/37435485-0f98-4b3a-bac7-341f5dd80a21)
![Screenshot 2025-03-24 022450](https://github.com/user-attachments/assets/23e9fdf4-e1b8-4f1b-b51f-31285d42d849)
