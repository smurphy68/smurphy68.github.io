import geocoder
def get_location():
    try:
        # Get your current location using the 'ipinfo' provider
        location = geocoder.ip('me')
        # Print the location details
        print(f"Your Location Details:")
        print(f"City: {location.city}")
        print(f"Country: {location.country}")
        print(f"Latitude: {location.latlng[0]}")
        print(f"Longitude: {location.latlng[1]}")
        return location
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_location()