from requests import get
import os


custom_user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0'
}



def get_meme():
    x = get("https://www.reddit.com/r/Animemes/new/.json" , headers=custom_user_agent).json()
    y = x["data"]['children'][0]['data']['url']
    return y

url = f"https://api.telegram.org/bot{os.environ["BOT"]}/sendPhoto?chat_id=-1001720367079&photo={get_meme()}"
get(url)
