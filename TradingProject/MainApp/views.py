from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
import csv
import os
from .models import Candle
from django.conf import settings




def upload_csv(request):
    if request.method == 'POST':
        
        uploaded_file = request.FILES['csv_file']
        
        if not uploaded_file.name.endswith('.csv'):
            return HttpResponse('File is not a CSV')

        
        
        timeframe = request.POST.get('timeframe')
        
        
        candles = []

        
        try:
            reader = csv.reader(uploaded_file.read().decode('utf-8').splitlines())
            header = next(reader)  
            
            for row in reader:
               
                id, open, high, low, close, date = map(float, row)
                candle = Candle(id=id, open=open, high=high, low=low, close=close, date=date)
                candles.append(candle)
        except csv.Error:
            return HttpResponse('Error reading the CSV file')

        
        Candle.objects.bulk_create(candles)

        
        json_data = json.dumps([candle.__dict__ for candle in candles], indent=4)

        
        json_file_path = os.path.join(settings.MEDIA_ROOT, 'processed_data.json')

       
        with open(json_file_path, 'w') as json_file:
            json_file.write(json_data)

       
        download_link = f"{settings.MEDIA_URL}processed_data.json" 

    

       
        return HttpResponseRedirect('/success/')  # Redirect to a success page

   
    return render(request,{'download_link': download_link}, 'upload_csv.html')

def download_json(request):
    
    data = {
        "example_key": "example_value",
        "another_key": "another_value"
    }

    
    json_data = json.dumps(data, indent=4) 
    
    response = HttpResponse(json_data, content_type='application/json')
    
    response['Content-Disposition'] = 'attachment; filename="processed_data.json"'

    return response



# @asynchronous
# async def async_view(request):
#     # Asynchronous code here
#     data = await database_sync_to_async(fetch_data)()
#     return HttpResponse(json.dumps(data), content_type='application/json')


