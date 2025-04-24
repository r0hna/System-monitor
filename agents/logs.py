import win32evtlog

def read_event_logs(log_type, server='localhost'):
    # Connect to the event log
    handle = win32evtlog.OpenEventLog(server, log_type)
    
    # Read the event log
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = win32evtlog.GetNumberOfEventLogRecords(handle)
    
    events = []
    while True:
        events_chunk = win32evtlog.ReadEventLog(handle, flags, 0)
        if not events_chunk:
            break
        for event in events_chunk:
            event_dict = {
                'EventID': event.EventID,
                'TimeGenerated': event.TimeGenerated,
                'SourceName': event.SourceName,
                'EventType': event.EventType,
                'EventCategory': event.EventCategory,
                'EventData': event.StringInserts
            }
            events.append(event_dict)
    
    win32evtlog.CloseEventLog(handle)
    return events


# # Example usage
# server = 'localhost'
# log_type = 'System'
# logs = read_event_logs(server, log_type)
# for log in logs:
#     print(log)
