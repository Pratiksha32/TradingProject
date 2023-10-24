import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Candle
from .forms import UploadCSVForm  # Assuming you have created a form for the upload
from datetime import datetime
def upload_csv(request):
    

    download_link = None  # Initialize the download link variable

    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data['csv_file']
            timeframe = form.cleaned_data['timeframe']

            # Process the uploaded CSV file


            # Read the CSV file using pandas
            try:
                df = pd.read_csv(uploaded_file)
                pf= df["time"]
                print(pf)
                 # Check if the CSV file has the expected columns (id, open, high, low, close, date)
                expected_columns = ['BANKNIFTY','date',	'time',	'open',	'high',	'low',	'close',	'volume']
                if not all(col in df.columns for col in expected_columns):
                    return HttpResponse('CSV file does not have the expected columns')

         # Create a list of Candle objects from the DataFrame
                
                candles = []
                
                for index, row in df.iterrows():  # Use 'index' and 'row' within the loop
                    date = datetime.fromisoformat(row['date'])
                    # Combine 'date' and 'time' to create a datetime object
                    date_str = f"{row['date']} {row['time']}"
                    try:
                        date = datetime.strptime(date_str, "%Y%m%d %H:%M")
                    except ValueError:
                        # Handle invalid date format
                        date = None  # You can set a default date or skip the row

                    # Create the Candle object
                    candle = Candle(
                        open=row['open'],
                        high=row['high'],
                        low=row['low'],
                        close=row['close'],
                        date=date  # Use the parsed datetime object
                    )
                    candles.append(candle)
            # Save the Candle objects in the database
                Candle.objects.bulk_create(candles)

            # You can add your CSV processing logic here
            # For example, saving the data to the database or converting to the desired timeframe

            # After processing, set the download link to the generated JSON file
                download_link = '/download_json/'  # Adjust the URL to your application

            # Redirect to a success page or render an appropriate template
                return HttpResponseRedirect('/success/')
            except pd.errors.EmptyDataError:
                return HttpResponse('CSV file is empty')
            except pd.errors.ParserError:
                return HttpResponse('Error reading the CSV file')
    

    else:
        form = UploadCSVForm()  # Create a new form instance if the request method is GET

    # Render the upload_csv template with the download link
    return render(request, 'MainApp/upload_csv.html', {'form': form, 'download_link': download_link})
