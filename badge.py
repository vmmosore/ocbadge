from collections import defaultdict
import base64

def make_card(data):
    try: logo = open("data/logo.svg", 'r').read()
    except: raise ValueError("data/logo.svg not found")
    
    data["logo"] = base64.b64encode(logo.encode()).decode()
    try: return open("data/template.svg", 'r').read().format_map(defaultdict(lambda: "N/A", data))
    except Exception as e:
        raise ValueError("data/template.svg not found, or invalid: " + str(e))
