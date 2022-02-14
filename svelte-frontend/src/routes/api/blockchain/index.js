// # Basically a proxy for the backend Flask API
export async function get({params}) {
    const URL = 'http://localhost:5000/blockchain?descending=True'
    const res = await fetch(URL)
    const data = await res.json()

    return {
        status: 200,
        body: data
    }
}