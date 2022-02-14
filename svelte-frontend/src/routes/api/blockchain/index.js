// # Basically a proxy for the backend Flask API
export async function get({params, url}) {
    // Gettinh Flask API URL from the .env file
    const BASE_URL = import.meta.env.VITE_API_URL
    let URL = `${BASE_URL}/blockchain`

    // adding descending option to the URL request if that parameter is present
    const descending = url.searchParams.get('descending')
    if (descending) URL += '?descending=True'

    const res = await fetch(URL)
    const data = await res.json()

    return {
        status: 200,
        body: data
    }
}