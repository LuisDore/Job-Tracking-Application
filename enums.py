from enum import Enum

class StatusEnum(str, Enum):
    APPLIED = "Applied"
    ONLINE_ASSESSMENT = "Online Assessment"
    INTERVIEWING = "Interviewing"
    OFFER = "Offer"
    REJECTED = "Rejected"