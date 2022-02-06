// Fetches the User's Currency Thing stats
// PS: don't forget the name of the parasm is the [thing] in the file name :)

export async function get({params}) {
    const URL = 'http://localhost:5000/blockchain/stats/@'
    const res = await fetch(URL + params.username)
    const stats = await res.json()

    return {
        status: 200,
        body: stats
    }
}