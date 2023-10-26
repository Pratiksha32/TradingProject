# MainApp/views.py
from django.shortcuts import render
from .forms import DataUploadForm
from .models import Candle
from django.http import JsonResponse, HttpResponse
import pandas as pd
import json
import asyncio

# Define the asynchronous function to convert candles to a given timeframe
# async def convert_candles_to_timeframe(candles, timeframe):
#     # Your conversion logic here
#     converted_candles = []  # Placeholder for converted candles

#     for candle in candles:
#         # Your conversion logic for the timeframe goes here
#         converted_candles.append(candle)  # Placeholder, modify as needed

#     return converted_candles

def convert_data(request):
    if request.method == 'POST':
        form = DataUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            timeframe = form.cleaned_data['timeframe']

            # Process the CSV file and convert data
            df = pd.read_csv(csv_file)
            # Perform data conversion based on the timeframe

            # Create and save the JSON file
            json_data = df.to_json(orient='records')
            with open('converted_data.json', 'w') as json_file:
                json_file.write(json_data)

                    #  # Process the CSV file and convert data asynchronously
                    # async def process_and_convert():
                    #     # Read the CSV file
                    #     df = pd.read_csv(csv_file)

                    #     # Convert data to candles (modify this part as per your CSV format)
                    #     candles = df.to_dict(orient='records')

                    #     # Perform data conversion asynchronously
                    #     converted_candles = await convert_candles_to_timeframe(candles, timeframe)

                    #     # Create and save the JSON file
                    #     with open('converted_data.json', 'w') as json_file:
                    #         json.dump(converted_candles, json_file)

                    # # Run the asyncio event loop
                    # asyncio.run(process_and_convert())



            response = HttpResponse(open('converted_data.json', 'rb').read())
            response['Content-Type'] = 'application/json'
            response['Content-Disposition'] = 'attachment; filename="converted_data.json"'

            return response
    else:
        form = DataUploadForm()

    return render(request, 'MainApp/upload.html', {'form': form})



