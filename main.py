import requests
from datetime import datetime
import smtplib
from time import sleep

MY_LAT = 39.469065
MY_LONG = -0.368241

my_email = "Your Email"
password = "Password"


def iss_close():
    """Compares the ISS position with my position and return True if it is at +-5 from my position"""
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    if (MY_LONG - 5) < longitude < (MY_LONG + 5) and (MY_LAT - 5) < latitude < (MY_LAT + 5):
        return True
    else:
        return False


def is_night():
    """Check if it's nighttime"""
    # Parameters to upload to the API
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    # API request
    response2 = requests.get(url=f"https://api.sunrise-sunset.org/json", params=parameters)
    response2.raise_for_status()

    # Getting the sunrise and the sunset time
    sunrise = response2.json()["results"]["sunrise"]
    sunset = response2.json()["results"]["sunset"]

    # Formatting the sunrise and the sunset time as lists
    sunrise_hour = int(sunrise.split("T")[1].split(":")[0])
    sunset_hour = int(sunset.split("T")[1].split(":")[0])

    # Getting and formatting the time now
    time_now = datetime.now()
    time_now_hour = time_now.hour

    if 24 > time_now_hour > sunset_hour or 1 < time_now_hour < sunrise_hour:
        return True
    else:
        return False


def main():
    if is_night():
        if iss_close():
            print("Sending EMAIL")
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs="DESTINATION ADDRESS",
                    msg="Subject: ISS in the SKY\n\n"
                        f"The ISS is ABOVE you, look up to the sky"
                )
            print("EMAIL SENT")
        else:
            print("ISS not close")
    else:
        print("Not the time yet")


is_on = True

while is_on:
    sleep(600)
    main()

