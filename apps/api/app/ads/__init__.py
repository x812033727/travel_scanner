"""Display advertising on article pages: the one public answer to "is it on, and with which IDs".

Nothing here reads a session, a trip, or a member identity. The endpoint is anonymous
because article readers are anonymous, and it reports "off" unless every identifier is
present and valid, so a half-filled back-office card never reaches a reader.
"""
