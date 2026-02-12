from googleapiclient.discovery import build
import datetime

class GoogleCalendarClient:
    def __init__(self, credentials):
        self.service = build('calendar', 'v3', credentials=credentials)

    def fetchEvents(self, max_results=50):
        # Fetch from now onwards
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        try:
            events_result = self.service.events().list(
                calendarId='primary', timeMin=now,
                maxResults=max_results, singleEvents=True,
                orderBy='startTime').execute()
            return events_result.get('items', [])
        except Exception as e:
            print(f"Error fetching events: {e}")
            raise e

    def addEvents(self, events):
        results = []
        for event in events:
            # Clean up fields that might cause 400 errors if passed blindly
            body = {
                'summary': event.get('summary'),
                'description': event.get('description', ''),
                'start': event.get('start'),
                'end': event.get('end'),
                'reminders': event.get('reminders', {'useDefault': True})
            }
            if 'colorId' in event:
                body['colorId'] = event['colorId']
            if 'location' in event:
                body['location'] = event['location']
            if 'recurrence' in event:
                body['recurrence'] = event['recurrence']
                
            try:
                res = self.service.events().insert(calendarId='primary', body=body).execute()
                results.append(res)
            except Exception as e:
                print(f"Error adding event {event.get('summary')}: {e}")
                # Don't raise, try to continue adding others
        return results

    def updateEvents(self, events):
        # Placeholder for update logic if needed
        pass

    def deleteEvents(self, event_ids):
        count = 0
        for event_id in event_ids:
            try:
                self.service.events().delete(calendarId='primary', eventId=event_id).execute()
                count += 1
            except Exception as e:
                print(f"Error deleting event {event_id}: {e}")
        return count
