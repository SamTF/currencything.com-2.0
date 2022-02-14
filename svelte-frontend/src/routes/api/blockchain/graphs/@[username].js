// Fetches the User's graphs based on their stats
// PS: don't forget the name of the param is the [thing] in the file name :)

export async function get({params}) {
    const BASE_URL = import.meta.env.VITE_API_URL
    const URL = `${BASE_URL}/blockchain/stats/@${params.username}/graphs`

    const res = await fetch(URL)
    const stats = await res.json()

    return {
        status: 200,
        body: stats
    }
}