// Fetches data for all the trades featuring this User by Username
// PS: don't forget the name of the parasm is the [thing] in the file name :)

export async function get({params}) {
    const URL = 'http://localhost:5000/blockchain/@'
    const res = await fetch(URL + params.username)
    const blockchain = await res.json()

    return {
        status: 200,
        body: blockchain
    }
}