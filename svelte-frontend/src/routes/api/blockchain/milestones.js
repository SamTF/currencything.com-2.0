//  # Returns a dict-like object of all thousandth Currency Thing milestones and their respective transaction ID
export async function get({params}) {
    const BASE_URL = import.meta.env.VITE_API_URL
    const URL = `${BASE_URL}/blockchain/milestones`

    const res = await fetch(URL)
    const data = await res.json()

    return {
        status: 200,
        body: data
    }
}