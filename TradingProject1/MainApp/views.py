from django.shortcuts import render

import pandas as pd
import json
import os
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from .models import Candle
from .forms import UploadCSVForm
from datetime import datetime  # Import datetime module


def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['csv_file']
            timeframe = form.cleaned_data['timeframe']

            # Read the CSV file using pandas
            df = pd.read_csv(uploaded_file)

            # Check if the CSV file has the expected columns
            expected_columns = ['open', 'high', 'low', 'close', 'date']
            if not all(col in df.columns for col in expected_columns):
                return HttpResponse('CSV file does not have the expected columns')

            # Create a list of Candle objects
            candles = []
            for _, row in df.iterrows():
                open_price = row['open']
                high_price = row['high']
                low_price = row['low']
                close_price = row['close']
                date_str = str(row['date'])  # Ensure date_str is a string
                date = datetime.strptime(date_str, "%Y%m%d %H:%M")
                date = date.replace(hour=0, minute=0)

                candle = Candle(open=open_price, high=high_price, low=low_price, close=close_price, date=date)
                candles.append(candle)

            # Save the Candle objects in the database
            Candle.objects.bulk_create(candles)

            # Convert the data to JSON
            json_data = json.dumps([candle.__dict__ for candle in candles], default=str, indent=4)

            # Define the path to save the JSON file
            json_file_path = os.path.join(settings.MEDIA_ROOT, 'processed_data.json')

            # Save the JSON data to a file on the server
            with open(json_file_path, 'w') as json_file:
                json_file.write(json_data)

            # Provide a link to download the JSON file
            download_link = json_file_path

            # Return a response with the download link
            return render(request, 'MainApp/success.html', {'download_link': download_link})

    else:
        form = UploadCSVForm()

    return render(request, 'MainApp/upload_csv.html', {'form': form})
