import getCookie from './GetCookie.jsx'
import { CONFIG } from '../config.js'

const authFetch = (route, options = {}) => {
    const requestOptions = {
        // Merge options
        credentials: 'include',
        ...options,
        // Merge headers
        headers: {
            'X-CSRF-TOKEN': getCookie('csrf_access_token'),
            ...options.headers,
        },
    };

    return fetch(CONFIG.API_BASE_URL + route, requestOptions)
        .then(response => {
            const data = response.json();

            // check for error response
            if (!response.ok) {
                // get error message from body or default to response status
                const error = (data && data.message) || response.status;
                return Promise.reject(error);
            }

            return data;
        })
        .catch(error => {
            console.error('There was an error!', error);
        });
}

export default authFetch;