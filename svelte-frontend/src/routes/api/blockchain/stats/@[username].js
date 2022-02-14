// Fetches the User's Currency Thing stats
// PS: don't forget the name of the parasm is the [thing] in the file name :)

export async function get({params}) {
    const BASE_URL = import.meta.env.VITE_API_URL
    const URL = `${BASE_URL}/blockchain/stats/@${params.username}`

    const res = await fetch(URL)
    const stats = await res.json()

    return {
        status: 200,
        body: stats
    }
}