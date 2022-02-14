// # Basically a proxy for the backend Flask API
export async function get({params, url}) {
    const descending = url.searchParams.get('descending')
    console.log(descending)


    const BASE_URL = import.meta.env.VITE_API_URL
    const URL = `${BASE_URL}/blockchain?descending=True`
    const res = await fetch(URL)
    const data = await res.json()

    return {
        status: 200,
        body: data
    }
}