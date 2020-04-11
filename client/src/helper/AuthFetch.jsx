import { getCookie } from './Cookie.jsx'
import { CONFIG } from '../config.js'

const authFetch = async (route, options = {}) => {
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

    try {
        const response = await fetch(CONFIG.API_BASE_URL + route, requestOptions);
        const data = response.json();
        // check for error response
        if (!response.ok) {
            // get error message from body or default to response status
            const error = (data && data.message) || response.status;
            // pass it such that it can be handled by catch below
            return Promise.reject(error);
        }
        return data;
    }
    catch (error_1) {
        console.error('There was an error!', error_1);
        return error_1;
    }
}

export default authFetch;