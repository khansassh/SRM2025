# from pymisp import PyMISP
# from config import Config

# misp = PyMISP(Config.MISP_URL, Config.MISP_KEY, False)

# def fetch_misp_threats():
#     """Fetch latest threat intelligence from MISP."""
#     try:
#         events = misp.search(controller="events", return_format="json")
#         return events
#     except Exception as e:
#         print(f"Error fetching MISP threats: {e}")
#         return []
