//  # Returns a dict-like object of all thousandth Currency Thing milestones and their respective transaction ID
export async function get({params}) {
    const URL = 'http://localhost:5000/blockchain/milestones'
    const res = await fetch(URL)
    const data = await res.json()

    return {
        status: 200,
        body: data
    }
}