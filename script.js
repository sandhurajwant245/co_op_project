// script.js
function explore() {
    window.location.href = 'search.html';
}

// script.js
export const getCurrentLocation = () => {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    const { latitude, longitude } = position.coords;
                    resolve({ lat: latitude, lng: longitude });
                },
                error => {
                    reject(error.message);
                }
            );
        } else {
            reject('Geolocation is not supported by this browser.');
        }
    });
};

// Function to fetch places data
export const getPlacesData = async (type, sw, ne) => {
    try {
        const { data } = await axios.get(`https://travel-advisor.p.rapidapi.com/${type}/list-in-boundary`, {
            params: {
                bl_latitude: sw.lat,
                bl_longitude: sw.lng,
                tr_longitude: ne.lng,
                tr_latitude: ne.lat,
            },
            headers: {
                'x-rapidapi-key': "1fa9ff4126d95b8db54f3897a208e91c",
                'x-rapidapi-host': 'travel-advisor.p.rapidapi.com',
            },
        });

        return data;
    } catch (error) {
        console.error("Error fetching places data:", error);
        throw error;
    }
};

// Function to fetch weather data
export const getWeatherData = async (lat, lng) => {
    try {
        if (lat && lng) {
            const { data } = await axios.get('https://community-open-weather-map.p.rapidapi.com/find', {
                params: { lat, lon: lng },
                headers: {
                    'x-rapidapi-key': "1fa9ff4126d95b8db54f3897a208e91c",
                    'x-rapidapi-host': 'community-open-weather-map.p.rapidapi.com',
                },
            });
            return data;
        }
    } catch (error) {
        console.error("Error fetching weather data:", error);
        throw error;
    }
};
