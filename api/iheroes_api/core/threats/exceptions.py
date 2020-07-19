class HistoryInvalidEntries(ValueError):
    code = "list.entry_not_found"
    msg_template = "history does not contain lastest danger level and location"
