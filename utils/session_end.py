from typing import Dict
from utils.scheduler import FunctionScheduler

scheduler = FunctionScheduler()

def end_session(session_id: str, sessions: Dict) -> str:
    ''' End a session '''
    try:
        del sessions[session_id]
    except Exception as e:
        raise KeyError("Session not found.") from e

def schedule_session_end(session_id: str, interval: int):
    """ Schedule a conversation to end in [interval] seconds.
    """
    scheduler.schedule_function(
        interval=interval,
        function=end_session,
        session_id=session_id
    )